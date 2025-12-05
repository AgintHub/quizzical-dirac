# extract_regime_labels_list PRD

## Description
Extracts the ordered list of regime labels from a CSV‑encoded DataFrame string.


## Implementation Plan

### 1. Parse the input CSV string into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives raw CSV text; converting it to a structured DataFrame enables column‑wise operations. |
| **Impact** | Provides a reliable in‑memory representation for subsequent extraction steps and validates CSV integrity. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(dataframe))` within a try/except block to catch parsing errors and raise a clear exception if the CSV is malformed. |

### 2. Validate that the `regime_label` column exists and extract its values in row order.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring the required column prevents downstream key errors and guarantees the output aligns with dates generated earlier. |
| **Impact** | Returns a deterministic List[str] that downstream nodes (e.g., `ComputeRegimeFeaturesOutput`) can rely on for correct mapping to dates. |
| **Complexity** | LOW |
| **Method** | Check `'regime_label' in df.columns`; if missing, raise a `ValueError`. Then obtain `df['regime_label'].astype(str).tolist()` to produce the output list. |
