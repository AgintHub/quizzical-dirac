# compute_rolling_correlations PRD

## Description
Computes rolling Pearson correlation values over a configurable window between a primary return series and each secondary return series.


## Implementation Plan

### 1. Validate that `returns_df` is a JSON‑serialised DataFrame string containing numeric return columns and that `primary_col` exists within it.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim receives well‑formed data and prevents runtime errors during correlation calculations. |
| **Impact** | Early detection of malformed inputs reduces crashes and produces clearer error messages for upstream nodes. |
| **Complexity** | LOW |
| **Method** | Parse the string with `json.loads` (or `pd.read_json`), check for the primary column in `df.columns`, and raise a descriptive `ValueError` if checks fail. |

### 2. Compute rolling Pearson correlations using pandas `rolling(window).corr()` for each secondary return column against the primary column.

| Category | Details |
| --- | --- |
| **Reason** | Provides the core financial feature needed for cross‑asset analysis with a configurable look‑back period. |
| **Impact** | Generates a time‑series DataFrame of correlation values that downstream nodes will flatten and expose as model outputs. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over all columns except the primary, call `df[primary_col].rolling(window).corr(df[col])`, collect results in a new DataFrame, and forward‑fill or drop NaNs as appropriate. |

### 3. Serialize the resulting correlation DataFrame into a JSON‑compatible string and assign it to the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The rest of the pipeline expects string‑based payloads; converting to JSON maintains consistency with other node interfaces. |
| **Impact** | Downstream nodes can easily deserialize the string back into a DataFrame for further processing without additional conversion steps. |
| **Complexity** | LOW |
| **Method** | Use `df.to_json(orient='split')` (or similar) to produce a compact representation, then return it as the `output` value. |
