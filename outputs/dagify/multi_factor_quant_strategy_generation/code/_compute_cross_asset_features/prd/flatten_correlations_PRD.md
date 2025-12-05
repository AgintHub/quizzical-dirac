# flatten_correlations PRD

## Description
Flattens the rolling correlation matrix into a single list ordered by date then asset pair.


## Implementation Plan

### 1. Extract correlation columns for each asset pair from the features DataFrame in the same order as the asset_pairs list.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the flattened list aligns correctly with downstream expectations for date‑wise ordering. |
| **Impact** | Provides a deterministic sequence of correlation values for model ingestion and evaluation. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over asset_pairs, locate the corresponding correlation column (e.g., "Corr_Primary-Secondary"), and concatenate its series values respecting the chronological index. |

### 2. Validate that the length of the flattened list equals number_of_dates * number_of_asset_pairs.

| Category | Details |
| --- | --- |
| **Reason** | Prevents mismatched dimensions that could cause runtime errors in downstream nodes. |
| **Impact** | Early detection of data integrity issues, leading to clearer error messages. |
| **Complexity** | LOW |
| **Method** | Compute expected_length = len(features_df.index) * len(asset_pairs) and raise a ValueError if len(output) != expected_length. |

### 3. Handle missing or NaN correlation values by forward‑filling or imputing with a neutral placeholder (e.g., 0.0).

| Category | Details |
| --- | --- |
| **Reason** | Rolling correlation windows produce NaNs at the start; downstream models require numeric inputs. |
| **Impact** | Ensures the output list contains no missing values, maintaining model compatibility. |
| **Complexity** | MEDIUM |
| **Method** | Apply pandas .fillna(method='ffill').fillna(0.0) on the correlation columns before flattening. |
