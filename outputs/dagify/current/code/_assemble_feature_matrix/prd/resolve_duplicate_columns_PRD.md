# resolve_duplicate_columns PRD

## Description
Renames any duplicate column names in a merged DataFrame by prefixing them with supplied source identifiers to ensure column uniqueness.


## Implementation Plan

### 1. Detect duplicate column names in the provided DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Merging multiple feature tables often yields columns with identical names, which breaks downstream operations like model training. |
| **Impact** | Prevents runtime errors and ensures each feature is uniquely identifiable. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.Index.duplicated() on df.columns to locate duplicated names; generate a boolean mask of duplicates. |

### 2. Assign deterministic prefixes to each duplicated column based on the ordered list of source_prefixes.

| Category | Details |
| --- | --- |
| **Reason** | The caller supplies a known ordering of feature sources (e.g., ['price_', 'cross_', 'regime_', 'vol_']); applying these prefixes resolves ambiguity while preserving provenance. |
| **Impact** | Creates a clear naming convention that downstream nodes can rely on for feature selection and interpretability. |
| **Complexity** | MEDIUM |
| **Method** | Split source_prefixes string on commas, iterate over duplicated columns, and prepend the matching prefix (cycling if more duplicates than prefixes) to the original column name. |

### 3. Return the DataFrame with updated column names, preserving original data and index order.

| Category | Details |
| --- | --- |
| **Reason** | Only the column labels need alteration; the data and chronological index must remain unchanged for correct model alignment. |
| **Impact** | Delivers a clean, ready‑to‑use feature matrix without side‑effects, enabling seamless continuation of the pipeline. |
| **Complexity** | LOW |
| **Method** | Create a copy of the original DataFrame, assign the new column list via df.columns = new_names, then serialize the DataFrame back to a CSV/JSON string for the output field. |
