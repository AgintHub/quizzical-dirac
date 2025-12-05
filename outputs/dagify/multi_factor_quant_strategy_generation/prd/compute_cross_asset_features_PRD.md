# compute_cross_asset_features PRD

## Description
Create correlation and spread features between the primary asset and each cross‑asset.


## Implementation Plan

### 1. Load the `cleaned_data_csv` string from the parent node `align_and_clean_data`, parse it into a pandas DataFrame with `Date` parsed as datetime, and set `Date` as the index.

| Category | Details |
| --- | --- |
| **Reason** | Ensures a structured, time‑aligned dataset that can be directly used for rolling calculations and guarantees correct handling of missing dates. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(cleaned_data_csv), parse_dates=['Date'])`; then `df.set_index('Date', inplace=True)`. |

### 2. Identify the primary asset columns: locate the column ending with `_Close` (or a column named `Primary_Close`). Store its name as `primary_close_col`. All other columns that end with `_Close` and are not the primary are treated as secondary asset price columns.

| Category | Details |
| --- | --- |
| **Reason** | Clear naming conventions avoid ambiguous column selection and make the feature generation robust to future additions of assets. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Iterate over `df.columns`; `primary_close_col = [c for c in df.columns if c.lower().endswith('_close') and 'primary' in c.lower()][0]`; `secondary_close_cols = [c for c in df.columns if c.lower().endswith('_close') and c != primary_close_col]`. |

### 3. Compute daily log returns for the primary asset and each secondary asset: `log_return = np.log(price).diff()` and store them in a new DataFrame `returns_df` with the same column naming scheme (`<ticker>_ret`).

| Category | Details |
| --- | --- |
| **Reason** | Log returns are additive and preferred for correlation calculations; they also match the definition used in downstream model training. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | For each close column: `returns_df[col.replace('_Close', '_Ret')] = np.log(df[col]).diff()`; drop the first NaN row after diff. |

### 4. For each secondary asset, compute a rolling 20‑day Pearson correlation between the primary log return series and the secondary log return series using `Series.rolling(window=20).corr()`; store results in a DataFrame `corr_df` with column names `corr_<SecondaryTicker>`.

| Category | Details |
| --- | --- |
| **Reason** | Rolling correlation captures the dynamic relationship between assets, which is a key predictive signal for the strategy. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Loop over `secondary_close_cols`; for each: `sec_ret = returns_df[sec_col.replace('_Close', '_Ret')]`; `corr_series = returns_df[primary_ret_col].rolling(20).corr(sec_ret)`; assign to `corr_df['corr_' + ticker]`. |

### 5. Compute the daily price spread for each secondary asset as `primary_close - secondary_close`; store in a DataFrame `spread_df` with column names `spread_<SecondaryTicker>`.

| Category | Details |
| --- | --- |
| **Reason** | The spread directly measures relative valuation and is a complementary feature to correlation. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | For each secondary column: `spread_df['spread_' + ticker] = df[primary_close_col] - df[sec_col]`. |

### 6. Combine `corr_df` and `spread_df` into a single feature DataFrame `features_df` aligned on the same index (Date). Drop any rows that still contain NaNs (the first 19 rows will have NaNs for correlation).

| Category | Details |
| --- | --- |
| **Reason** | A single DataFrame simplifies extraction of output arrays and guarantees that each date has a complete set of features. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `features_df = pd.concat([corr_df, spread_df], axis=1); features_df.dropna(inplace=True)`. |

### 7. Construct the `date` list by converting the index of `features_df` to ISO‑8601 strings: `date = features_df.index.strftime('%Y-%m-%d').tolist()`.

| Category | Details |
| --- | --- |
| **Reason** | Matches the required output type `List[str]` and provides a human‑readable date format for downstream nodes. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use pandas `strftime` as shown. |

### 8. Build the `asset_pairs` list: for each secondary ticker, create a string `Primary-<Ticker>`; the order must be the same as the order used when generating correlation and spread columns.

| Category | Details |
| --- | --- |
| **Reason** | Provides a clear mapping from the flattened correlation/spread values back to the underlying asset pair. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Extract ticker from column names (e.g., `col.split('_')[0]`), then `asset_pairs = ['Primary-' + t for t in secondary_tickers]`. |

### 9. Flatten the correlation values: iterate over `features_df` rows (by date) and for each row concatenate the correlation columns in `asset_pairs` order into a single list; repeat for all dates to obtain `correlations` list.

| Category | Details |
| --- | --- |
| **Reason** | The output schema expects a one‑dimensional list where the temporal dimension is implicit via ordering. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```
correlations = []
for _, row in features_df.iterrows():
    for pair in asset_pairs:
        corr_col = 'corr_' + pair.split('-')[1]
        correlations.append(row[corr_col])
```
 |

### 10. Flatten the price spread values using the same loop order as correlations, pulling from `spread_<Ticker>` columns into the `price_spreads` list.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the two flattened lists stay perfectly aligned (date‑major, then asset‑pair order). |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Similar to correlation flattening, replace `corr_` with `spread_` in column lookup. |

### 11. Validate the lengths: `len(date) * len(asset_pairs)` must equal `len(correlations)` and `len(price_spreads)`; raise an exception if mismatched.

| Category | Details |
| --- | --- |
| **Reason** | Catches programming errors early, guaranteeing downstream nodes receive correctly shaped data. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Simple `assert` statements. |

### 12. Return a JSON‑serializable dictionary containing the four output fields (`date`, `asset_pairs`, `correlations`, `price_spreads`).

| Category | Details |
| --- | --- |
| **Reason** | Conforms to the declared output structure for the node and enables downstream Python code to consume the results directly. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `return {"date": date, "asset_pairs": asset_pairs, "correlations": correlations, "price_spreads": price_spreads}`. |
