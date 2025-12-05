# calculate_realized_volatility PRD

## Description
Computes a rolling realized volatility series from a price DataFrame using a specified window length.


## Implementation Plan

### 1. Parse the incoming `price_df` string into a pandas DataFrame with a Date column and a Close price column.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives data as a serialized string; it must be converted to a structured format before calculations. |
| **Impact** | Enables downstream numeric operations and ensures date ordering for accurate rolling calculations. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_json` or `pd.read_csv` based on a simple format flag; raise a clear error if required columns are missing. |

### 2. Calculate daily log returns and then compute the rolling standard deviation over the specified `window`, annualizing the result to obtain realized volatility.

| Category | Details |
| --- | --- |
| **Reason** | Realized volatility is defined as the annualized standard deviation of log returns over a moving window. |
| **Impact** | Provides the core metric required by downstream nodes for volatility forecasting and risk analysis. |
| **Complexity** | MEDIUM |
| **Method** | Convert `window` to int, use `np.log` for returns, `df['log_ret'].rolling(window).std()` for rolling std, multiply by sqrt(252) to annualize. |

### 3. Serialize the resulting DataFrame (Date and Realized Volatility columns) back to a string matching the expected output format.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect the output as a string; consistent serialization ensures interoperability. |
| **Impact** | Allows seamless hand‑off to nodes like `fetch_volatility_data` without additional transformation steps. |
| **Complexity** | LOW |
| **Method** | Use `df.to_json(orient="records")` or `df.to_csv(index=False)` based on a configurable output flag; include error handling for serialization failures. |
