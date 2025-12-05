# extract_dates_list PRD

## Description
Extracts a list of date strings (YYYY-MM-DD) from a validated volatility DataFrame.


## Implementation Plan

### 1. Deserialize the input string back into a pandas DataFrame and verify the presence and datatype of the 'Date' column.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string; it must be converted back to a usable structure before extracting dates. |
| **Impact** | Ensures that downstream extraction works on a correctly structured DataFrame, preventing runtime errors. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` or `pickle.loads` based on the serialization format, then check `if 'Date' not in df.columns` and `pd.api.types.is_datetime64_any_dtype(df['Date'])`. |

### 2. Normalize the 'Date' column to pandas datetime objects and convert each entry to an ISO‑8601 string (YYYY‑MM‑DD).

| Category | Details |
| --- | --- |
| **Reason** | Dates may be stored as datetime objects, strings, or other formats; standardizing ensures consistent output. |
| **Impact** | Produces a clean, uniformly formatted list of dates suitable for downstream models and API contracts. |
| **Complexity** | MEDIUM |
| **Method** | Apply `pd.to_datetime(df['Date'], errors='coerce')`, drop NaT values, then use `.dt.strftime('%Y-%m-%d').tolist()` to generate the list. |

### 3. Return the list of date strings while preserving the original chronological order and handling any missing/invalid entries gracefully.

| Category | Details |
| --- | --- |
| **Reason** | Order matters for time‑series alignment and missing dates should not break the contract. |
| **Impact** | Provides reliable, ordered output that downstream nodes can safely consume without additional cleaning. |
| **Complexity** | LOW |
| **Method** | After conversion, filter out any `None` or empty strings, retain the order of the DataFrame index, and assign the result to the `output` field. |
