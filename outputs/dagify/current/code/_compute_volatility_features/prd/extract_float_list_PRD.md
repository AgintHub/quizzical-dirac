# extract_float_list PRD

## Description
Extracts a list of float values from a string‑identified series for downstream volatility calculations.


## Implementation Plan

### 1. Validate that the `series` string corresponds to an existing numeric column in the aligned DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Pre‑empt runtime errors caused by misspelled or missing column names. |
| **Impact** | Ensures the shim fails fast with a clear error, preventing downstream propagation of invalid data. |
| **Complexity** | LOW |
| **Method** | Check column existence using `if series not in df.columns: raise ValueError`; optionally expose a whitelist of allowed series. |

### 2. Convert the selected column to a flat Python list of floats, handling NaN values appropriately.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect a clean `List[float]` without pandas‑specific types or missing values. |
| **Impact** | Provides consistent numeric input for GARCH forecast extraction and implied‑vol delta calculations. |
| **Complexity** | MEDIUM |
| **Method** | Use `df[series].astype(float).fillna(method='ffill').tolist()` or similar, with configurable NaN handling (drop, fill, or error). |

### 3. Return the extracted list together with the original series identifier in a deterministic order.

| Category | Details |
| --- | --- |
| **Reason** | The calling node aligns multiple series by index; preserving order guarantees correct pairing of forecasts and deltas. |
| **Impact** | Maintains data integrity across the pipeline, avoiding misaligned outputs. |
| **Complexity** | LOW |
| **Method** | Wrap the list in the response model, ensuring the order matches `df.index` after any alignment steps. |
