# assemble_feature_matrix PRD

## Description
Combine all individual feature tables into a single matrix aligned with the target variable.


## Implementation Plan

### 1. Load the CSV payloads from each parent node (price_action, cross_asset, regime, volatility) into in‑memory data frames using a robust CSV parser that respects ISO‑8601 dates and quoted fields.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that all feature tables are correctly interpreted before any join operation; parsing errors are caught early. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.read_csv with `parse_dates=['Date']`, `dayfirst=False`, `dtype` inference disabled; wrap in try/except to capture malformed rows. |

### 2. Standardize the Date column across all data frames to midnight UTC and set it as the index to guarantee exact alignment during the merge.

| Category | Details |
| --- | --- |
| **Reason** | Date inconsistencies (timezones, format variations) would cause mismatched joins and missing rows. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Apply `df['Date'] = pd.to_datetime(df['Date']).dt.normalize()` and then `df.set_index('Date', inplace=True)`. |

### 3. Perform an inner join on the Date index across the four feature data frames to keep only dates present in every source, thereby guaranteeing a complete feature row for each observation.

| Category | Details |
| --- | --- |
| **Reason** | Target computation requires a complete set of predictors; dropping dates with missing features avoids NaNs later in modeling. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `merged = price_df.join([cross_df, regime_df, vol_df], how='inner')`. |

### 4. Detect and resolve any duplicate column names that may arise from overlapping feature names (e.g., both price and volatility tables containing a column called `date`).

| Category | Details |
| --- | --- |
| **Reason** | Duplicate columns cause CSV export failures and ambiguous feature references in downstream models. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | After merging, inspect `merged.columns`. For any duplicates, rename using a prefix based on source table (e.g., `price_`, `vol_`). Implement a helper `unique_rename(columns, source_prefix)`. |

### 5. Compute the target variable – next‑day simple return – using the cleaned primary asset closing price series that resides in the price_action feature table (column `close`).

| Category | Details |
| --- | --- |
| **Reason** | The model learns to predict this target; it must be aligned with the feature row date (i.e., return from t to t+1 assigned to row at date t). |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a series `next_day_return = price_df['close'].shift(-1) / price_df['close'] - 1`. Append as a new column `Target` to the merged data frame. Drop the final row where Target is NaN. |

### 6. Re‑index the final merged data frame to ensure chronological order (oldest to newest) and reset the index to a regular `Date` column for CSV export.

| Category | Details |
| --- | --- |
| **Reason** | Ordered dates simplify downstream time‑series splits and improve readability of the CSV output. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Execute `merged.sort_index(inplace=True); merged.reset_index(inplace=True)`. |

### 7. Validate the final matrix: ensure no missing values, confirm that the column count equals sum of unique feature columns plus `Date` and `Target`, and verify that row count matches the expected number of trading days (original dates minus one for target lag).

| Category | Details |
| --- | --- |
| **Reason** | A sanity check prevents propagation of corrupted data into model training and backtesting stages. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Run assertions: `assert merged.isnull().sum().sum() == 0`, `assert 'Target' in merged.columns`, `assert len(merged) == expected_rows`. |

### 8. Serialize the validated data frame to a CSV‑formatted string with UTF‑8 encoding, ensuring the header line includes `Date` followed by all feature names and finally `Target`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream nodes expect a plain string CSV; consistent encoding avoids hidden character issues. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `feature_matrix_csv = merged.to_csv(index=False, line_terminator='\n')` and store as a Python string. |

### 9. Return the CSV string as the node output `feature_matrix_csv` and log a concise summary (row count, column count, date range) for observability.

| Category | Details |
| --- | --- |
| **Reason** | Provides transparency for pipeline monitoring and aids debugging if downstream nodes fail. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Construct a log message: `logger.info(f'Feature matrix generated: {len(merged)} rows, {len(merged.columns)} columns, dates {merged["Date"].min()}–{merged["Date"].max()}')` then assign to output. |
