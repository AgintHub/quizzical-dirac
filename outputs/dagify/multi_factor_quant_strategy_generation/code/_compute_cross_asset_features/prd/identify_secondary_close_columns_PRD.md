# identify_secondary_close_columns PRD

## Description
Identifies all secondary asset close‑price column names from a DataFrame column list, excluding the primary asset close column.


## Implementation Plan

### 1. Parse the `columns` input into a concrete Python list and normalise each element (strip whitespace, handle optional JSON list format).

| Category | Details |
| --- | --- |
| **Reason** | The shim receives column information as a string; converting it to a list enables reliable programmatic processing. |
| **Impact** | Ensures that subsequent filtering operates on a clean, deterministic collection of column names, preventing mis‑identification due to formatting quirks. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` when the string starts with '['; otherwise split on commas and apply `.strip()` to each token. |

### 2. Filter the parsed list to retain only names that end with the suffix `_Close` and are not equal to `primary_col`.

| Category | Details |
| --- | --- |
| **Reason** | Secondary assets are defined by their close‑price columns; the primary column must be excluded to avoid self‑correlation and duplicate spread calculations. |
| **Impact** | Produces the exact set of secondary close columns required for cross‑asset correlation and spread feature generation. |
| **Complexity** | LOW |
| **Method** | List comprehension: `[col for col in column_list if col.endswith('_Close') and col != primary_col]`. |

### 3. Return the filtered list in the original order to preserve the natural ordering of assets as they appear in the source DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes (e.g., asset‑pair building) rely on positional consistency between secondary columns and generated feature arrays. |
| **Impact** | Guarantees alignment between `secondary_close_cols`, `asset_pairs`, and flattened feature vectors, eliminating ordering bugs. |
| **Complexity** | LOW |
| **Method** | Simply return the list produced by the comprehension without re‑sorting; optionally validate that the list is non‑empty and raise a clear error if no secondary columns are found. |
