# compute_log_returns PRD

## Description
Computes daily logarithmic returns for a specified price column in a CSV‑encoded DataFrame and returns the augmented DataFrame as a CSV string.


## Implementation Plan

### 1. Validate that the input CSV can be parsed into a DataFrame and that the specified price column exists.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim operates on correct and complete data, preventing runtime errors in later steps. |
| **Impact** | Prevents crashes due to missing columns or malformed CSV, providing early feedback to the caller. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv` on the input string, then check `price_column` in `df.columns`; raise a clear `ValueError` if validation fails. |

### 2. Calculate the logarithmic return for each row using the price column.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality required by downstream volatility modeling (e.g., GARCH). |
| **Impact** | Adds a `LogReturn` column that accurately represents daily returns, enabling correct statistical calculations later in the pipeline. |
| **Complexity** | MEDIUM |
| **Method** | Create a Series `prices = df[price_column].astype(float)`, compute `log_returns = np.log(prices / prices.shift(1))`, assign to `df['LogReturn']`; handle division‑by‑zero and initial NaN by optionally filling with 0 or leaving as NaN. |

### 3. Serialize the augmented DataFrame back to a CSV string and populate the output fields.

| Category | Details |
| --- | --- |
| **Reason** | Provides the next node with data in the expected format (CSV string) while also echoing the original inputs for traceability. |
| **Impact** | Ensures seamless integration with downstream nodes that expect CSV inputs, maintaining the data flow continuity. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` to obtain the CSV string, assign it to the `output` field, and return a dictionary containing `output`, `dataframe`, and `price_column`. |
