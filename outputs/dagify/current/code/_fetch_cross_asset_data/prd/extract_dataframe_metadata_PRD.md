# extract_dataframe_metadata PRD

## Description
Extracts key metadata (start date, end date, and row count) from a given DataFrame and returns it as a JSON‑encoded string.


## Implementation Plan

### 1. Parse the incoming string into an actual pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string representation, so it must be materialized before analysis. |
| **Impact** | Enables subsequent operations to work with genuine DataFrame methods, ensuring correct metadata extraction. |
| **Complexity** | LOW |
| **Method** | Use `ast.literal_eval` or `json.loads` combined with `pd.DataFrame.from_records` depending on the serialization format; include error handling for malformed inputs. |

### 2. Compute start_date, end_date, and row_count from the DataFrame's index and shape.

| Category | Details |
| --- | --- |
| **Reason** | These three pieces of information constitute the essential metadata required by downstream nodes. |
| **Impact** | Provides accurate temporal boundaries and size metrics for the fetched cross‑asset price series. |
| **Complexity** | MEDIUM |
| **Method** | If the index is datetime‑like, call `df.index.min()` and `df.index.max()`, convert to ISO‑8601 strings with `strftime('%Y-%m-%d')`; obtain `row_count` via `len(df)`; handle non‑datetime indexes by falling back to the first/last row values. |

### 3. Serialize the metadata dictionary to a JSON string and return it.

| Category | Details |
| --- | --- |
| **Reason** | The node contract expects a string output that downstream code can parse without importing pandas. |
| **Impact** | Ensures a language‑agnostic, lightweight representation that can be stored or transmitted easily. |
| **Complexity** | LOW |
| **Method** | Create `metadata = {'start_date': start_date, 'end_date': end_date, 'row_count': row_count}` and return `json.dumps(metadata)`. Include validation to guarantee all fields are present. |
