# extract_column_names PRD

## Description
Extracts the list of column names from a CSV‑formatted DataFrame string.


## Implementation Plan

### 1. Parse the CSV string into an in‑memory table structure (e.g., pandas DataFrame) without loading full data into memory when possible.

| Category | Details |
| --- | --- |
| **Reason** | A reliable parser is required to correctly interpret delimiters, quoting, and line breaks before column extraction. |
| **Impact** | Ensures accurate column name retrieval even for complex CSV payloads and prevents downstream errors. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv(io.StringIO(df), nrows=0)` to load only the header row, or fall back to Python's `csv` module if pandas is unavailable. |

### 2. Extract the ordered list of column headers from the parsed table.

| Category | Details |
| --- | --- |
| **Reason** | The core purpose of the shim is to provide downstream nodes with the exact column identifiers for further processing. |
| **Impact** | Provides a deterministic, order‑preserving list that downstream nodes (e.g., asset name extraction) can rely on. |
| **Complexity** | LOW |
| **Method** | Retrieve `dataframe.columns.tolist()` when using pandas, or read the first row from the CSV reader and return it as a list of strings. |

### 3. Return the column list as a JSON‑serializable `LIST_STR` field while preserving the original `df` input for traceability.

| Category | Details |
| --- | --- |
| **Reason** | The node contract expects both the original input and the extracted output for auditing and debugging. |
| **Impact** | Facilitates transparent data lineage and enables easy inspection of inputs/outputs in workflow logs. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary `{ "output": column_list, "df": df }` and let the surrounding framework handle JSON serialization. |
