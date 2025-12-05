# load_cross_asset_csv PRD

## Description
Converts raw cross‑asset feature inputs into a CSV string aligned by date for downstream merging.


## Implementation Plan

### 1. Parse the incoming string parameters into native Python structures (lists) and validate lengths and ordering.

| Category | Details |
| --- | --- |
| **Reason** | Input values are passed as serialized strings; they must be deserialized and checked for consistency before any transformation. |
| **Impact** | Prevents mis‑aligned rows, runtime errors, and ensures data integrity for downstream CSV generation. |
| **Complexity** | MEDIUM |
| **Method** | Use `json.loads` (or `ast.literal_eval`) to deserialize each parameter; verify that `len(dates) * len(asset_pairs) == len(correlations) == len(price_spreads)` and raise descriptive exceptions on mismatch. |

### 2. Construct a pandas DataFrame where each row represents a date and each asset‑pair contributes two columns: one for correlation and one for price spread.

| Category | Details |
| --- | --- |
| **Reason** | A tabular representation simplifies column naming, alignment, and CSV serialization while preserving the required ordering (date → asset‑pair). |
| **Impact** | Produces a well‑structured CSV that can be directly merged with other feature tables using standard date‑index joins. |
| **Complexity** | LOW |
| **Method** | Iterate over `asset_pairs`, create column names like `{pair}_corr` and `{pair}_spread`, reshape the flat lists into matrices with `numpy.reshape`, and assemble the DataFrame via `pd.DataFrame` with the `dates` column as the index. |

### 3. Serialize the DataFrame to a CSV string, ensuring the Date column is first and that no index column is added.

| Category | Details |
| --- | --- |
| **Reason** | The downstream `load_cross_asset_csv` shim expects a pure CSV payload without extra index artifacts. |
| **Impact** | Enables seamless ingestion by `assemble_feature_matrix` and other pipeline nodes, preserving column order and data types. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` to obtain the CSV text; return it as the `output` field along with the original serialized inputs for traceability. |
