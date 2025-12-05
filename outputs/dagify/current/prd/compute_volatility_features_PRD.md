# compute_volatility_features PRD

## Description
Generate forecasted volatility inputs using GARCH‑type calculations and implied‑vol trends.


## Implementation Plan

### 1. Parse the `cleaned_data_csv` string from the `align_and_clean_data` output into a Pandas DataFrame, ensuring the `Date` column is converted to `datetime64[ns]` and set as the index.

| Category | Details |
| --- | --- |
| **Reason** | A structured DataFrame is required for reliable column selection, lag calculations, and model fitting; parsing once avoids repeated I/O. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(cleaned_data_csv), parse_dates=['Date'])`; call `df.set_index('Date', inplace=True)`; verify that the index is monotonic and unique. |

### 2. Validate the presence of the primary asset's price columns (`Close` or equivalent) and the `ImpliedVol` column; raise a descriptive error if missing.

| Category | Details |
| --- | --- |
| **Reason** | The GARCH model needs returns derived from closing prices, and the implied‑vol delta calculation requires the implied volatility series; early validation prevents silent failures later in the pipeline. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `{'Close', 'ImpliedVol'}.issubset(df.columns)`; if not, construct an error message listing missing columns. |

### 3. Compute daily log returns of the primary asset: `log_return = np.log(df['Close'] / df['Close'].shift(1))`; drop the first NaN resulting from the shift.

| Category | Details |
| --- | --- |
| **Reason** | GARCH models are traditionally fit on return series rather than price levels; log returns ensure additive properties and stationarity assumptions. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a new Series `returns = np.log(df['Close']).diff()`; store it in `df['LogReturn']`. |

### 4. Fit a GARCH(1,1) model to the `LogReturn` series using the `arch` Python library (e.g., `arch.univariate.ConstantMean` with `arch_model(returns, vol='Garch', p=1, q=1)`). Optimize parameters via maximum likelihood.

| Category | Details |
| --- | --- |
| **Reason** | The `arch` package provides a battle‑tested implementation of GARCH models with automatic handling of convergence, parameter constraints, and diagnostics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```python
from arch import arch_model
am = arch_model(df['LogReturn'].dropna(), vol='Garch', p=1, q=1, mean='Zero')
res = am.fit(disp='off')
``` |

### 5. Generate one‑step‑ahead conditional volatility forecasts for each date in the cleaned data after the model fitting horizon. Use `res.forecast(horizon=1, start=df.index[0])` to obtain the forecasted variance, then take the square‑root to get volatility.

| Category | Details |
| --- | --- |
| **Reason** | A one‑step‑ahead forecast aligns with the downstream model’s need for a forward‑looking volatility input; using the built‑in forecast method guarantees consistency with the fitted parameters. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```python
forecast = res.forecast(start=df.index[0], horizon=1)
vol_forecast = np.sqrt(forecast.variance.iloc[:, 0])
``` |

### 6. Calculate the 5‑day implied‑volatility delta: for each date `t`, compute `ImpVolDelta[t] = df['ImpliedVol'].loc[t] - df['ImpliedVol'].shift(5).loc[t]`. Align the resulting Series with the GARCH forecast Series, dropping dates where the 5‑day lag is unavailable.

| Category | Details |
| --- | --- |
| **Reason** | The 5‑day delta captures recent implied‑vol momentum, a valuable predictive signal; aligning both series ensures a one‑to‑one correspondence in the final output. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | ```python
imp_vol_delta = df['ImpliedVol'] - df['ImpliedVol'].shift(5)
# Align with vol_forecast index
aligned = pd.concat([vol_forecast, imp_vol_delta], axis=1).dropna()
aligned.columns = ['GARCHForecast', 'ImpliedVolDelta']
``` |

### 7. Extract the final output lists: `dates = aligned.index.strftime('%Y-%m-%d').tolist()`, `garch_forecasts = aligned['GARCHForecast'].astype(float).tolist()`, `implied_vol_delta_5d = aligned['ImpliedVolDelta'].astype(float).tolist()`. Return them in the node’s defined output structure.

| Category | Details |
| --- | --- |
| **Reason** | Converting to plain Python lists matches the typed output contract and facilitates downstream serialization (e.g., JSON or CSV). |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Assign the three lists to the respective output fields; ensure no NaNs remain; optionally log the length of each list for debugging. |

### 8. Add robust error handling and logging: capture exceptions during CSV parsing, GARCH fitting, and delta calculation; log the error context (e.g., date range, number of observations) and re‑raise a custom `VolatilityFeatureError` with a clear message.

| Category | Details |
| --- | --- |
| **Reason** | The volatility step is mathematically intensive; failures (non‑convergence, insufficient data) must be surfaced early to prevent downstream cascade failures. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Wrap each major block in `try/except`; use Python’s `logging` module to record `INFO` on successful completion and `ERROR` on failure; define a lightweight exception class for clarity. |
