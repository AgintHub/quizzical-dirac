# extract_realized_vol_list PRD

## Description
Extracts a list of realized volatility floats from a validated DataFrame provided as a string.


## Implementation Plan

### 1. Parse the input string into a pandas DataFrame, supporting common serialization formats such as CSV and JSON.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string; it must be materialized into a structured object for column operations. |
| **Impact** | Enables downstream column extraction and ensures the shim works with the data format produced by previous nodes. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv with StringIO for CSV strings and pandas.read_json for JSON strings, detecting format via simple heuristics or a file‑type flag. |

### 2. Validate that the DataFrame contains a column named (or synonymous with) 'realized_vol' and that all entries are numeric.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring the expected column exists and contains clean numeric data prevents runtime errors and guarantees correct output. |
| **Impact** | Provides robust error handling and clear messages if the source data is malformed, improving pipeline reliability. |
| **Complexity** | MEDIUM |
| **Method** | Check DataFrame.columns for exact or case‑insensitive matches (e.g., 'RealizedVol', 'realized_vol'); coerce column to float using pandas.to_numeric with errors='raise'; raise a custom ValidationError if checks fail. |

### 3. Extract the validated realized volatility column and convert it to a plain Python list of floats.

| Category | Details |
| --- | --- |
| **Reason** | The node's contract requires a List[float] output, not a pandas Series. |
| **Impact** | Delivers the final output in the expected format for downstream Pydantic models and API consumers. |
| **Complexity** | LOW |
| **Method** | Use df[realized_vol_column].tolist() after confirming the column; ensure the list contains native float types (e.g., via map(float)). |
