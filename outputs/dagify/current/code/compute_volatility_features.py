from ._compute_volatility_features.parse_csv_to_dataframe import parse_csv_to_dataframe
from ._compute_volatility_features.validate_required_columns import validate_required_columns
from ._compute_volatility_features.compute_log_returns import compute_log_returns
from ._compute_volatility_features.fit_garch_model import fit_garch_model
from ._compute_volatility_features.generate_garch_forecasts import generate_garch_forecasts
from ._compute_volatility_features.calculate_implied_vol_delta import calculate_implied_vol_delta
from ._compute_volatility_features.align_volatility_series import align_volatility_series
from ._compute_volatility_features.extract_date_strings import extract_date_strings
from ._compute_volatility_features.extract_float_list import extract_float_list
from ._compute_volatility_features.log_volatility_success import log_volatility_success
from ._compute_volatility_features.handle_volatility_feature_error import handle_volatility_feature_error

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Parse the `cleaned_data_csv` string from the `align_and_clean_data` output
#   into a Pandas DataFrame, ensuring the `Date` column is converted to
#   `datetime64[ns]` and set as the index.
#   Reason: A structured DataFrame is required for reliable column selection, lag
#           calculations, and model fitting; parsing once avoids repeated
#           I/O.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `pd.read_csv(io.StringIO(cleaned_data_csv), parse_dates=['Date'])`;
#           call `df.set_index('Date', inplace=True)`; verify that the
#           index is monotonic and unique.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the presence of the primary asset's price columns (`Close` or
#   equivalent) and the `ImpliedVol` column; raise a descriptive error if
#   missing.
#   Reason: The GARCH model needs returns derived from closing prices, and the
#           implied‑vol delta calculation requires the implied volatility
#           series; early validation prevents silent failures later in the
#           pipeline.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Check `{'Close', 'ImpliedVol'}.issubset(df.columns)`; if not, construct an
#           error message listing missing columns.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Compute daily log returns of the primary asset: `log_return =
#   np.log(df['Close'] / df['Close'].shift(1))`; drop the first NaN resulting
#   from the shift.
#   Reason: GARCH models are traditionally fit on return series rather than price
#           levels; log returns ensure additive properties and stationarity
#           assumptions.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Create a new Series `returns = np.log(df['Close']).diff()`; store it in
#           `df['LogReturn']`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Fit a GARCH(1,1) model to the `LogReturn` series using the `arch` Python
#   library (e.g., `arch.univariate.ConstantMean` with `arch_model(returns,
#   vol='Garch', p=1, q=1)`). Optimize parameters via maximum likelihood.
#   Reason: The `arch` package provides a battle‑tested implementation of GARCH models
#           with automatic handling of convergence, parameter constraints,
#           and diagnostics.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: ```python from arch import arch_model am =
#           arch_model(df['LogReturn'].dropna(), vol='Garch', p=1, q=1,
#           mean='Zero') res = am.fit(disp='off') ```
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Generate one‑step‑ahead conditional volatility forecasts for each date in the
#   cleaned data after the model fitting horizon. Use
#   `res.forecast(horizon=1, start=df.index[0])` to obtain the forecasted
#   variance, then take the square‑root to get volatility.
#   Reason: A one‑step‑ahead forecast aligns with the downstream model’s need for a
#           forward‑looking volatility input; using the built‑in forecast
#           method guarantees consistency with the fitted parameters.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: ```python forecast = res.forecast(start=df.index[0], horizon=1)
#           vol_forecast = np.sqrt(forecast.variance.iloc[:, 0]) ```
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Calculate the 5‑day implied‑volatility delta: for each date `t`, compute
#   `ImpVolDelta[t] = df['ImpliedVol'].loc[t] -
#   df['ImpliedVol'].shift(5).loc[t]`. Align the resulting Series with the
#   GARCH forecast Series, dropping dates where the 5‑day lag is unavailable.
#   Reason: The 5‑day delta captures recent implied‑vol momentum, a valuable predictive
#           signal; aligning both series ensures a one‑to‑one
#           correspondence in the final output.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: ```python imp_vol_delta = df['ImpliedVol'] - df['ImpliedVol'].shift(5) #
#           Align with vol_forecast index aligned =
#           pd.concat([vol_forecast, imp_vol_delta], axis=1).dropna()
#           aligned.columns = ['GARCHForecast', 'ImpliedVolDelta'] ```
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Extract the final output lists: `dates =
#   aligned.index.strftime('%Y-%m-%d').tolist()`, `garch_forecasts =
#   aligned['GARCHForecast'].astype(float).tolist()`, `implied_vol_delta_5d =
#   aligned['ImpliedVolDelta'].astype(float).tolist()`. Return them in the
#   node’s defined output structure.
#   Reason: Converting to plain Python lists matches the typed output contract and
#           facilitates downstream serialization (e.g., JSON or CSV).
#   Impact: HIGH
#   Complexity: LOW
#   Method: Assign the three lists to the respective output fields; ensure no NaNs
#           remain; optionally log the length of each list for debugging.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Add robust error handling and logging: capture exceptions during CSV parsing,
#   GARCH fitting, and delta calculation; log the error context (e.g., date
#   range, number of observations) and re‑raise a custom
#   `VolatilityFeatureError` with a clear message.
#   Reason: The volatility step is mathematically intensive; failures (non‑convergence,
#           insufficient data) must be surfaced early to prevent downstream
#           cascade failures.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Wrap each major block in `try/except`; use Python’s `logging` module to
#           record `INFO` on successful completion and `ERROR` on failure;
#           define a lightweight exception class for clarity.
# -- END PRD --



class AlignAndCleanDataOutput(BaseModel):
    """Pydantic model for align_and_clean_data node outputs."""
    cleaned_data_csv: str = Field(..., description="CSV\u2011formatted text of the cleaned master DataFrame after merging and imputation.")
    row_count: int = Field(..., description="Number of rows (dates) present in the cleaned DataFrame.")
    column_names: List[str] = Field(..., description="List of column names in the cleaned DataFrame, including the primary asset fields and all feature columns.")
    missing_values_filled: bool = Field(..., description="Indicates whether any missing values were forward\u2011filled during the cleaning process (true if any fill occurred, false if none were needed).")


class ComputeVolatilityFeaturesOutput(BaseModel):
    """Pydantic model for compute_volatility_features node outputs."""
    dates: List[str] = Field(..., description="List of dates (ISO format) for which the forecasts are generated.")
    garch_forecasts: List[float] = Field(..., description="One\u2011step\u2011ahead volatility forecast from the GARCH(1,1) model for each corresponding date.")
    implied_vol_delta_5d: List[float] = Field(..., description="5\u2011day change in implied volatility (ImpliedVol[t] - ImpliedVol[t-5]) for each date.")


def compute_volatility_features(align_and_clean_data_input: AlignAndCleanDataOutput, **kwargs) -> ComputeVolatilityFeaturesOutput:
    """Generate forecasted volatility inputs using GARCH‑type calculations and implied‑vol trends.

    Args:
        align_and_clean_data_input: Input from the 'align_and_clean_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ComputeVolatilityFeaturesOutput: Object containing outputs for this node.
    """
    try:
        # Parse cleaned CSV data into DataFrame with proper datetime index
        df = parse_csv_to_dataframe(csv_string=align_and_clean_data_input.cleaned_data_csv)
        
        # Validate presence of required columns
        validate_required_columns(dataframe=df, required_columns=['Close', 'ImpliedVol'])
        
        # Compute daily log returns
        df_with_returns = compute_log_returns(dataframe=df, price_column='Close')
        
        # Fit GARCH(1,1) model to log returns
        garch_model = fit_garch_model(returns_series=df_with_returns['LogReturn'])
        
        # Generate one-step-ahead volatility forecasts
        vol_forecasts = generate_garch_forecasts(fitted_model=garch_model, start_date=df_with_returns.index[0])
        
        # Calculate 5-day implied volatility delta
        imp_vol_delta = calculate_implied_vol_delta(implied_vol_series=df_with_returns['ImpliedVol'], lag_days=5)
        
        # Align forecast and delta series, dropping NaN values
        aligned_data = align_volatility_series(garch_forecasts=vol_forecasts, implied_vol_delta=imp_vol_delta)
        
        # Extract final output lists
        output_dates: List[str] = extract_date_strings(datetime_index=aligned_data.index)
        output_garch_forecasts: List[float] = extract_float_list(series=aligned_data['GARCHForecast'])
        output_implied_vol_delta: List[float] = extract_float_list(series=aligned_data['ImpliedVolDelta'])
        
        # Log successful completion
        log_volatility_success(num_dates=len(output_dates))
        
        return ComputeVolatilityFeaturesOutput(
            dates=output_dates,
            garch_forecasts=output_garch_forecasts,
            implied_vol_delta_5d=output_implied_vol_delta
        )
        
    except Exception as e:
        # Handle errors with detailed logging and custom exception
        handle_volatility_feature_error(error=e, context={'input_columns': align_and_clean_data_input.column_names, 'row_count': align_and_clean_data_input.row_count})