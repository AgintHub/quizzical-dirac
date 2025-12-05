# inner_join_on_date PRD

## Description
Merges the price, cross‑asset, regime, and volatility feature tables by performing an inner join on their standardized Date index and returns the combined table as a CSV string.


## Implementation Plan

### 1. Parse each input CSV string into a pandas DataFrame, coerce the Date column to datetime, and set it as the index.

| Category | Details |
| --- | --- |
| **Reason** | Uniform datetime handling is required for a reliable join across all feature tables. |
| **Impact** | Ensures all tables share a common, correctly typed Date index, preventing join mismatches and downstream errors. |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` with `pd.read_csv`, apply `pd.to_datetime` on the Date column, and call `set_index('Date')` on each DataFrame. |

### 2. Rename columns in each DataFrame with a source‑specific prefix (e.g., price_, cross_, regime_, vol_) to avoid name collisions, then perform an inner join on the Date index across the four DataFrames.

| Category | Details |
| --- | --- |
| **Reason** | Feature columns from different sources may share names (e.g., "close"), which would be overwritten without disambiguation. |
| **Impact** | Produces a single, conflict‑free feature matrix that downstream nodes can consume without ambiguity. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `df.columns` to prepend the appropriate prefix, then use `functools.reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'), dfs)`; finally serialize with `df.to_csv(StringIO, index=False)`. |

### 3. Validate that the merged DataFrame contains at least one row and that the Date index is monotonic increasing; raise a descriptive `ValueError` if the validation fails.

| Category | Details |
| --- | --- |
| **Reason** | An empty or unsorted result indicates mismatched date ranges and would break model training. |
| **Impact** | Provides early, clear feedback to developers or pipelines, preventing silent downstream failures. |
| **Complexity** | LOW |
| **Method** | Check `merged_df.empty` and `merged_df.index.is_monotonic_increasing`; if conditions are not met, raise `ValueError` with details of the offending inputs. |
