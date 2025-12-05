# compute_price_action_features PRD

## Description
Generate technical features from the primary asset price series (e.g., returns, momentum, volatility).


## Implementation Plan

### 1. Load the `cleaned_data_csv` string output from the parent node `align_and_clean_data` into a pandas DataFrame using `pd.read_csv(io.StringIO(...), parse_dates=['Date'])`.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the downstream calculations operate on a structured, date‑indexed table that contains the fully cleaned OHLCV columns required for technical indicator computation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `io` and `pandas`; wrap the CSV string in `StringIO`; specify `Date` as the index or a column; verify that columns `Open`, `High`, `Low`, `Close` exist; raise a descriptive error if any are missing. |

### 2. Validate that the DataFrame is sorted chronologically ascending; if not, sort by `Date` and re‑index to guarantee proper rolling calculations.

| Category | Details |
| --- | --- |
| **Reason** | Rolling windows (moving averages, RSI, etc.) depend on correct temporal order; unsorted data would produce misleading features. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `df['Date'].is_monotonic_increasing`; if false, execute `df = df.sort_values('Date').reset_index(drop=True)`. |

### 3. Compute daily log returns: `log_return = np.log(df['Close'] / df['Close'].shift(1))` and store as a new Series named `log_return`.

| Category | Details |
| --- | --- |
| **Reason** | Log returns are the foundation for many momentum and risk metrics; using `np.log` provides additive properties over time. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `numpy as np`; handle the first row NaN by leaving it as `np.nan` (it will be removed later). |

### 4. Calculate 10‑day and 30‑day simple moving averages on the `Close` price: `ma_10 = df['Close'].rolling(window=10, min_periods=10).mean()` and `ma_30 = df['Close'].rolling(window=30, min_periods=30).mean()`.

| Category | Details |
| --- | --- |
| **Reason** | Moving averages capture short‑ and medium‑term trend information; using `min_periods` equal to the window prevents premature values. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use pandas `rolling`; assign results to columns `ma_10` and `ma_30`. |

### 5. Implement the Relative Strength Index (RSI) with a 14‑day look‑back: calculate upward and downward price changes, compute exponential weighted averages, then apply the RSI formula `100 - (100 / (1 + RS))`.

| Category | Details |
| --- | --- |
| **Reason** | RSI is a widely‑used momentum oscillator; the 14‑day period is standard and provides a balanced signal. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
delta = df['Close'].diff()
up = delta.clip(lower=0)
down = -delta.clip(upper=0)
roll_up = up.ewm(span=14, adjust=False).mean()
roll_down = down.ewm(span=14, adjust=False).mean()
RS = roll_up / roll_down
rsi = 100 - (100 / (1 + RS))
``` Assign to column `rsi`. |

### 6. Compute MACD (Moving Average Convergence Divergence) using standard parameters (fast EMA 12, slow EMA 26, signal EMA 9): `macd_line = EMA_fast - EMA_slow`; `macd_signal = macd_line.ewm(span=9, adjust=False).mean(); macd = macd_line - macd_signal`.

| Category | Details |
| --- | --- |
| **Reason** | MACD captures trend‑following momentum; the standard parameter set is a de‑facto industry baseline. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
ema_fast = df['Close'].ewm(span=12, adjust=False).mean()
ema_slow = df['Close'].ewm(span=26, adjust=False).mean()
macd_line = ema_fast - ema_slow
macd_signal = macd_line.ewm(span=9, adjust=False).mean()
macd = macd_line - macd_signal
``` Store in column `macd`. |

### 7. Calculate the Average True Range (ATR) over a 14‑day window: first compute True Range (TR) as the max of three values (high‑low, |high‑prev_close|, |low‑prev_close|), then apply a rolling mean.

| Category | Details |
| --- | --- |
| **Reason** | ATR quantifies recent volatility, essential for risk‑adjusted sizing and stop‑loss logic. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
high_low = df['High'] - df['Low']
high_prev_close = (df['High'] - df['Close'].shift(1)).abs()
low_prev_close = (df['Low'] - df['Close'].shift(1)).abs()
tr = pd.concat([high_low, high_prev_close, low_prev_close], axis=1).max(axis=1)
atr = tr.rolling(window=14, min_periods=14).mean()
``` Assign to column `atr`. |

### 8. Assemble all computed feature Series (`log_return`, `ma_10`, `ma_30`, `rsi`, `macd`, `atr`) into a single DataFrame alongside the original `Date` column; drop any rows that contain NaN in any feature column to ensure a fully populated matrix.

| Category | Details |
| --- | --- |
| **Reason** | Down‑stream models cannot handle missing values; removing incomplete rows preserves alignment with the target variable and other feature tables. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create `features_df = pd.DataFrame({ 'Date': df['Date'], 'log_return': log_return, 'ma_10': ma_10, 'ma_30': ma_30, 'rsi': rsi, 'macd': macd, 'atr': atr })`; then `features_df = features_df.dropna().reset_index(drop=True)`. |

### 9. Generate `feature_names` as a Python list ordered exactly as they appear in the CSV (excluding `Date`): `['log_return', 'ma_10', 'ma_30', 'rsi', 'macd', 'atr']`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream node `assemble_feature_matrix` expects an explicit ordering to correctly align columns during merges. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Hard‑code the list or derive via `features_df.columns.tolist()[1:]`. |

### 10. Export `features_df` to CSV string without index: `csv_data = features_df.to_csv(index=False)`; compute `row_count = len(features_df)`.

| Category | Details |
| --- | --- |
| **Reason** | The node's output contract requires a CSV‑formatted string and the exact row count for validation in later steps. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use pandas `to_csv`; store result in variable `csv_data`; calculate `row_count = features_df.shape[0]`. |

### 11. Wrap the entire computation in a try/except block that captures any unexpected errors (e.g., missing columns, division by zero) and raises a custom `ValueError` with a clear message indicating which step failed.

| Category | Details |
| --- | --- |
| **Reason** | Robust error handling simplifies debugging of the DAG and prevents silent failures that would propagate downstream. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | ```python
try:
    # all steps above
except Exception as e:
    raise ValueError(f'compute_price_action_features failed at step X: {e}')
``` |
