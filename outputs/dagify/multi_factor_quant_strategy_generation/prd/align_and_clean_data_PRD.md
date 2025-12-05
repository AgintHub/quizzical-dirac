# align_and_clean_data PRD

## Description
Synchronize all fetched datasets to a common calendar, handle missing values, and store a clean master dataset.


## Implementation Plan

### 1. Load each parent node's output into a Pandas DataFrame with Date parsed as `datetime64[ns]` and set as the index.

| Category | Details |
| --- | --- |
| **Reason** | Uniform datetime indexing guarantees a deterministic merge order and simplifies calendar alignment. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.DataFrame` constructors from the primitive lists; e.g., for fetch_price_data build columns Date, Open, High, Low, Close, Volume. Apply `pd.to_datetime(df['Date'])` and `df.set_index('Date', inplace=True)` for all five DataFrames. |

### 2. Validate that all five DataFrames share the same timezone (UTC) and that there are no duplicate Date entries within any table.

| Category | Details |
| --- | --- |
| **Reason** | Duplicate dates or timezone mismatches cause ambiguous merges and hidden NaNs. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `df.index.duplicated().any()` and raise an exception if true; enforce `df.index = df.index.tz_localize('UTC')` when tz‑naive. |

### 3. Perform an outer join on the Date index across all five DataFrames using `pd.merge(..., how='outer')` sequentially or `pd.concat(..., axis=1, join='outer')`.

| Category | Details |
| --- | --- |
| **Reason** | Outer join preserves the full universe of dates from any source, creating the superset calendar required for downstream feature engineering. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Start with `master_df = price_df`; iterate over `[cross_asset_df, regime_df, volatility_df]` and execute `master_df = master_df.join(other_df, how='outer')`. Preserve original column names to avoid collisions. |

### 4. Create a boolean flag `missing_before_fill = master_df.isna().any().any()` to record whether any NaNs exist prior to imputation.

| Category | Details |
| --- | --- |
| **Reason** | The output field `missing_values_filled` must reflect whether forward‑fill actually occurred. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Store the result; after forward‑fill, compute `missing_after_fill = master_df.isna().any().any()` and set `missing_values_filled = missing_before_fill and not missing_after_fill`. |

### 5. Apply forward‑fill (`ffill`) on the merged DataFrame, then backward‑fill (`bfill`) as a safety net for leading NaNs.

| Category | Details |
| --- | --- |
| **Reason** | Forward‑fill respects causality (using the most recent known value), while a trailing `bfill` ensures the first rows are not dropped unnecessarily. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Execute `master_df.ffill(inplace=True); master_df.bfill(inplace=True)`. |

### 6. Drop any remaining rows that still contain NaN values after imputation using `master_df.dropna(inplace=True)`.

| Category | Details |
| --- | --- |
| **Reason** | Downstream models cannot handle missing entries; dropping ensures a clean dataset. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Call `master_df.dropna(inplace=True)` and verify `master_df.empty` is false; otherwise raise an alert. |

### 7. Capture `row_count = master_df.shape[0]` and `column_names = list(master_df.columns)` for output metadata.

| Category | Details |
| --- | --- |
| **Reason** | These fields are required by the downstream schema and useful for sanity‑checking the cleaning step. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Assign variables directly after the final drop operation. |

### 8. Convert the cleaned DataFrame to a CSV‑formatted string without the index (`index=False`) and store as `cleaned_data_csv`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream nodes expect CSV text; omitting the index avoids an extra unnamed column. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use `cleaned_data_csv = master_df.reset_index().to_csv(index=False, line_terminator='\n')`. |

### 9. Assemble the final output dictionary matching the declared `output_structure` and return it to the workflow engine.

| Category | Details |
| --- | --- |
| **Reason** | Consistent typing and field naming allow downstream nodes to consume the result without conversion errors. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return `{ 'cleaned_data_csv': cleaned_data_csv, 'row_count': int(row_count), 'column_names': column_names, 'missing_values_filled': bool(missing_values_filled) }`. |
