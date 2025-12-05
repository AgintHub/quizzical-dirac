# _compute_cross_asset_features - Complete PRD Documentation

## Overview
PRDs for nodes in the '_compute_cross_asset_features' module.

## Table of Contents

- [load_and_parse_csv_with_datetime_index](#load_and_parse_csv_with_datetime_index)

- [identify_primary_close_column](#identify_primary_close_column)

- [identify_secondary_close_columns](#identify_secondary_close_columns)

- [compute_log_returns](#compute_log_returns)

- [compute_rolling_correlations](#compute_rolling_correlations)

- [compute_price_spreads](#compute_price_spreads)

- [combine_and_clean_features](#combine_and_clean_features)

- [extract_dates_as_iso_strings](#extract_dates_as_iso_strings)

- [build_asset_pairs_list](#build_asset_pairs_list)

- [flatten_correlations](#flatten_correlations)

- [flatten_price_spreads](#flatten_price_spreads)

- [validate_output_lengths](#validate_output_lengths)



---

## load_and_parse_csv_with_datetime_index

### Description
Parses a CSV‑formatted string into a pandas DataFrame and sets a timezone‑aware, sorted datetime index for downstream financial calculations.

### Implementation Plan

#### 1. Read the CSV string into a pandas DataFrame using `pd.read_csv` with `StringIO`, automatically detecting the delimiter.

| Category | Details |
| --- | --- |
| **Reason** | The raw CSV is provided as a plain string; converting it to a DataFrame is required for all subsequent numeric operations. |
| **Impact** | Creates a structured tabular representation that downstream nodes can reliably index and manipulate. |
| **Complexity** | MEDIUM |
| **Method** | Wrap `csv_data` in `io.StringIO`, call `csv.Sniffer().sniff` to infer delimiter, then execute `pd.read_csv(io_obj, delimiter=detected, parse_dates=True)`. |

#### 2. Identify the column containing dates, convert it to a timezone‑aware `datetime64[ns, UTC]` type, set it as the DataFrame index, and ensure the index is sorted.

| Category | Details |
| --- | --- |
| **Reason** | All downstream calculations assume a clean, monotonic datetime index for rolling windows and time‑based merges. |
| **Impact** | Guarantees chronological consistency, prevents alignment bugs, and enables efficient time‑series operations. |
| **Complexity** | LOW |
| **Method** | Search for columns named 'date', 'Date', or the first column if ambiguous; use `pd.to_datetime(..., utc=True)`, assign `df.set_index(date_col, inplace=True)`, and call `df.sort_index(inplace=True)`. |

#### 3. Validate the parsed DataFrame (non‑empty, required numeric columns present) and raise a descriptive `ValueError` for malformed input.

| Category | Details |
| --- | --- |
| **Reason** | Early error detection provides clear feedback to callers and avoids obscure downstream failures. |
| **Impact** | Improves robustness of the pipeline and simplifies debugging of data ingestion issues. |
| **Complexity** | HIGH |
| **Method** | Check `df.empty`, verify presence of at least one column ending with `_Close`, confirm the index dtype is `datetime64[ns, UTC]`; construct informative error messages and optionally suggest corrective actions. |


---

## identify_primary_close_column

### Description
Identifies and returns the column name that contains the primary asset's closing price from a comma‑separated list of DataFrame column names.

### Implementation Plan

#### 1. Parse the `columns` string into a list of clean column identifiers.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives column names as a single string; converting it to a list enables programmatic analysis. |
| **Impact** | Provides a reliable, order‑preserving collection of column names for downstream heuristics. |
| **Complexity** | LOW |
| **Method** | Split the string on commas, strip whitespace from each token, and store the result in a Python list. |

#### 2. Apply a deterministic heuristic to select the primary close column from the parsed list.

| Category | Details |
| --- | --- |
| **Reason** | Multiple close‑price columns may exist (primary and secondary assets); a consistent rule is needed to isolate the primary one. |
| **Impact** | Ensures downstream feature calculations (correlations, spreads) use the correct reference asset, preventing data leakage or misalignment. |
| **Complexity** | MEDIUM |
| **Method** | 1️⃣ Look for a column that matches the pattern `*Primary*_Close` (case‑insensitive). 2️⃣ If none, select the first column that ends with `_Close` or contains the word `Close`. 3️⃣ If still ambiguous, fallback to the first column in the list. Return the chosen column name. |


---

## identify_secondary_close_columns

### Description
Identifies all secondary asset close‑price column names from a DataFrame column list, excluding the primary asset close column.

### Implementation Plan

#### 1. Parse the `columns` input into a concrete Python list and normalise each element (strip whitespace, handle optional JSON list format).

| Category | Details |
| --- | --- |
| **Reason** | The shim receives column information as a string; converting it to a list enables reliable programmatic processing. |
| **Impact** | Ensures that subsequent filtering operates on a clean, deterministic collection of column names, preventing mis‑identification due to formatting quirks. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` when the string starts with '['; otherwise split on commas and apply `.strip()` to each token. |

#### 2. Filter the parsed list to retain only names that end with the suffix `_Close` and are not equal to `primary_col`.

| Category | Details |
| --- | --- |
| **Reason** | Secondary assets are defined by their close‑price columns; the primary column must be excluded to avoid self‑correlation and duplicate spread calculations. |
| **Impact** | Produces the exact set of secondary close columns required for cross‑asset correlation and spread feature generation. |
| **Complexity** | LOW |
| **Method** | List comprehension: `[col for col in column_list if col.endswith('_Close') and col != primary_col]`. |

#### 3. Return the filtered list in the original order to preserve the natural ordering of assets as they appear in the source DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes (e.g., asset‑pair building) rely on positional consistency between secondary columns and generated feature arrays. |
| **Impact** | Guarantees alignment between `secondary_close_cols`, `asset_pairs`, and flattened feature vectors, eliminating ordering bugs. |
| **Complexity** | LOW |
| **Method** | Simply return the list produced by the comprehension without re‑sorting; optionally validate that the list is non‑empty and raise a clear error if no secondary columns are found. |


---

## compute_log_returns

### Description
Computes daily log‑returns for the specified close‑price columns of a price DataFrame and returns the result as a CSV‑formatted string.

### Implementation Plan

#### 1. Parse the incoming CSV strings into pandas DataFrames and deserialize the close‑column list.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives all data as strings, so they must be converted to usable structures before any calculation. |
| **Impact** | Enables downstream numeric operations and ensures type safety for the rest of the pipeline. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv` with `io.StringIO` for the price DataFrame; use `json.loads` to convert the close_columns string into a Python list. |

#### 2. Validate that each requested close column exists and that the index is datetime‑compatible.

| Category | Details |
| --- | --- |
| **Reason** | Missing or mis‑named columns would cause silent failures or incorrect calculations. |
| **Impact** | Prevents runtime errors and provides clear feedback to upstream nodes if input data is malformed. |
| **Complexity** | MEDIUM |
| **Method** | Check `column in df.columns` for each name; attempt `pd.to_datetime(df.index)` and raise a descriptive `ValueError` if conversion fails. |

#### 3. Compute the log‑returns, handle NaNs, and serialize the result back to CSV.

| Category | Details |
| --- | --- |
| **Reason** | Log‑return calculation is the core functionality; NaNs must be managed to keep the output tidy for later aggregation. |
| **Impact** | Produces a clean, ready‑to‑use feature set for correlation and spread calculations downstream. |
| **Complexity** | MEDIUM |
| **Method** | For each column: `np.log(df[col] / df[col].shift(1))`; concatenate results, drop the first row (which will be NaN), optionally forward‑fill remaining NaNs; finally `result_df.to_csv(index=False)` and return the string. |


---

## compute_rolling_correlations

### Description
Computes rolling Pearson correlation values over a configurable window between a primary return series and each secondary return series.

### Implementation Plan

#### 1. Validate that `returns_df` is a JSON‑serialised DataFrame string containing numeric return columns and that `primary_col` exists within it.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim receives well‑formed data and prevents runtime errors during correlation calculations. |
| **Impact** | Early detection of malformed inputs reduces crashes and produces clearer error messages for upstream nodes. |
| **Complexity** | LOW |
| **Method** | Parse the string with `json.loads` (or `pd.read_json`), check for the primary column in `df.columns`, and raise a descriptive `ValueError` if checks fail. |

#### 2. Compute rolling Pearson correlations using pandas `rolling(window).corr()` for each secondary return column against the primary column.

| Category | Details |
| --- | --- |
| **Reason** | Provides the core financial feature needed for cross‑asset analysis with a configurable look‑back period. |
| **Impact** | Generates a time‑series DataFrame of correlation values that downstream nodes will flatten and expose as model outputs. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over all columns except the primary, call `df[primary_col].rolling(window).corr(df[col])`, collect results in a new DataFrame, and forward‑fill or drop NaNs as appropriate. |

#### 3. Serialize the resulting correlation DataFrame into a JSON‑compatible string and assign it to the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The rest of the pipeline expects string‑based payloads; converting to JSON maintains consistency with other node interfaces. |
| **Impact** | Downstream nodes can easily deserialize the string back into a DataFrame for further processing without additional conversion steps. |
| **Complexity** | LOW |
| **Method** | Use `df.to_json(orient='split')` (or similar) to produce a compact representation, then return it as the `output` value. |


---

## compute_price_spreads

### Description
Computes daily price spread series (PrimaryClose - SecondaryClose) for a set of secondary assets given a price DataFrame and column identifiers.

### Implementation Plan

#### 1. Parse the CSV‑encoded price_df string into a pandas DataFrame with a datetime index.

| Category | Details |
| --- | --- |
| **Reason** | All downstream calculations require a structured DataFrame, not raw CSV text. |
| **Impact** | Enables vectorised arithmetic for spread computation and ensures consistent date alignment. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(price_df), parse_dates=['Date'], index_col='Date')` and handle parsing errors with try/except. |

#### 2. Validate that primary_col exists in the DataFrame and that every entry in secondary_cols is present.

| Category | Details |
| --- | --- |
| **Reason** | Missing or miss‑spelled column names would raise runtime errors during subtraction. |
| **Impact** | Provides early, clear error messages and prevents silent data corruption. |
| **Complexity** | MEDIUM |
| **Method** | Check `primary_col in df.columns` and `set(secondary_cols).issubset(df.columns)`, raise a ValueError with a descriptive message if validation fails. |

#### 3. Compute a new DataFrame of price spreads by subtracting each secondary close column from the primary close column and return the result as a JSON‑serializable string.

| Category | Details |
| --- | --- |
| **Reason** | The core functionality of the shim is to deliver spread series for each asset pair in the order required by downstream nodes. |
| **Impact** | Produces the `price_spreads` feature used in correlation/feature pipelines, maintaining the same index (dates) as the input price data. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `secondary_cols`, calculate `df[primary_col] - df[sec]` for each, store in a dictionary keyed by secondary ticker, then `json.dumps` the dictionary (or convert to a CSV string) and assign to the `output` field. |


---

## combine_and_clean_features

### Description
Merges the rolling correlation DataFrame and price spread DataFrame, aligns their indices, fills or drops NaN values, and returns the cleaned combined features as a CSV‑formatted string.

### Implementation Plan

#### 1. Parse the input CSV strings into pandas DataFrames with a DateTime index.

| Category | Details |
| --- | --- |
| **Reason** | Subsequent operations require DataFrames to align on dates for accurate merging. |
| **Impact** | Enables correct temporal alignment and subsequent feature engineering steps. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv with StringIO, parse dates column, and set it as the index. |

#### 2. Align the two DataFrames on their index, perform an inner join, and handle missing values by forward‑filling then back‑filling.

| Category | Details |
| --- | --- |
| **Reason** | Correlation and spread series may have different start dates or NaNs; consistent rows are needed for modeling. |
| **Impact** | Produces a clean combined feature set without gaps, improving downstream model performance. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.DataFrame.join with 'inner' mode, then apply df.ffill().bfill() to fill remaining NaNs. |

#### 3. Serialize the cleaned combined DataFrame back to a CSV string for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | The pipeline expects string outputs to be passed between nodes without persisting to disk. |
| **Impact** | Provides a portable, text‑based representation compatible with the rest of the workflow. |
| **Complexity** | LOW |
| **Method** | Use DataFrame.to_csv with StringIO, ensuring ISO‑8601 date formatting. |


---

## extract_dates_as_iso_strings

### Description
Converts a pandas DatetimeIndex into a list of ISO‑8601 formatted date strings.

### Implementation Plan

#### 1. Parse the incoming `df_index` into a pandas DatetimeIndex if it is not already one.

| Category | Details |
| --- | --- |
| **Reason** | The shim may receive the index as a raw string representation, a list, or a pandas Index; normalising it ensures consistent processing. |
| **Impact** | Guarantees that downstream date extraction works reliably regardless of input format. |
| **Complexity** | MEDIUM |
| **Method** | Use `pd.to_datetime` with `errors='raise'` to coerce the input; handle cases where the input is already a DatetimeIndex by bypassing conversion. |

#### 2. Convert each timestamp in the normalized DatetimeIndex to an ISO‑8601 date string (YYYY‑MM‑DD).

| Category | Details |
| --- | --- |
| **Reason** | The downstream `ComputeCrossAssetFeaturesOutput` expects dates strictly in ISO format for sorting and serialization. |
| **Impact** | Produces a deterministic, standards‑compliant list of date strings that can be consumed by JSON‑based APIs or other services. |
| **Complexity** | LOW |
| **Method** | Iterate over the index (or use `.strftime('%Y-%m-%d')`) and collect results into a Python list. |

#### 3. Validate and sort the resulting list to ensure ascending chronological order and remove any `NaT` entries.

| Category | Details |
| --- | --- |
| **Reason** | Data pipelines assume dates are monotonic; missing or out‑of‑order dates can cause misalignment of features. |
| **Impact** | Prevents downstream alignment errors and guarantees that the `date` field matches the ordering of flattened feature arrays. |
| **Complexity** | LOW |
| **Method** | Filter out `pd.NaT` values, then apply `sorted()` on the list; optionally assert that the length matches the original index length minus any NaT rows. |


---

## build_asset_pairs_list

### Description
Generates a list of cross‑asset pair identifiers from a comma‑separated string of secondary close column names.

### Implementation Plan

#### 1. Parse the incoming comma‑separated string of secondary close column names into a clean Python list.

| Category | Details |
| --- | --- |
| **Reason** | The upstream node supplies secondary column names as a single string; converting it to a list is required for deterministic processing. |
| **Impact** | Ensures that each secondary asset is individually recognized, eliminating parsing errors downstream. |
| **Complexity** | LOW |
| **Method** | Use `str.split(',')` followed by `strip()` on each element to produce `List[str] secondary_cols`. |

#### 2. Strip the `_Close` suffix from each column name to obtain the raw ticker symbol.

| Category | Details |
| --- | --- |
| **Reason** | Column names follow the `<Ticker>_Close` convention; the ticker is the meaningful identifier for asset‑pair construction. |
| **Impact** | Produces clean ticker strings that can be safely concatenated with the primary asset identifier. |
| **Complexity** | LOW |
| **Method** | Iterate over `secondary_cols` and apply `col.replace('_Close', '')` (or regex) to generate `ticker` list. |

#### 3. Combine each ticker with the primary asset identifier to form pair strings in the format `Primary-SecondaryTicker`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream features expect asset pairs to be explicitly named; embedding the primary asset provides consistent ordering for correlation and spread flattening. |
| **Impact** | Creates the `output` list required by `ComputeCrossAssetFeaturesOutput.asset_pairs`, enabling correct feature alignment. |
| **Complexity** | MEDIUM |
| **Method** | Retrieve the primary ticker from a known source (e.g., a configuration file, environment variable, or a dedicated helper function `identify_primary_ticker()`), then build each pair with an f‑string: `f"{primary_ticker}-{ticker}"`. |


---

## flatten_correlations

### Description
Flattens the rolling correlation matrix into a single list ordered by date then asset pair.

### Implementation Plan

#### 1. Extract correlation columns for each asset pair from the features DataFrame in the same order as the asset_pairs list.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the flattened list aligns correctly with downstream expectations for date‑wise ordering. |
| **Impact** | Provides a deterministic sequence of correlation values for model ingestion and evaluation. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over asset_pairs, locate the corresponding correlation column (e.g., "Corr_Primary-Secondary"), and concatenate its series values respecting the chronological index. |

#### 2. Validate that the length of the flattened list equals number_of_dates * number_of_asset_pairs.

| Category | Details |
| --- | --- |
| **Reason** | Prevents mismatched dimensions that could cause runtime errors in downstream nodes. |
| **Impact** | Early detection of data integrity issues, leading to clearer error messages. |
| **Complexity** | LOW |
| **Method** | Compute expected_length = len(features_df.index) * len(asset_pairs) and raise a ValueError if len(output) != expected_length. |

#### 3. Handle missing or NaN correlation values by forward‑filling or imputing with a neutral placeholder (e.g., 0.0).

| Category | Details |
| --- | --- |
| **Reason** | Rolling correlation windows produce NaNs at the start; downstream models require numeric inputs. |
| **Impact** | Ensures the output list contains no missing values, maintaining model compatibility. |
| **Complexity** | MEDIUM |
| **Method** | Apply pandas .fillna(method='ffill').fillna(0.0) on the correlation columns before flattening. |


---

## flatten_price_spreads

### Description
Flattens daily price spread values from a features DataFrame into a single ordered list of floats.

### Implementation Plan

#### 1. Parse the `features_df` CSV string into a pandas DataFrame and verify that each identifier in `asset_pairs` maps to a corresponding spread column.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives data as a string; converting it to a DataFrame is required to perform column‑wise extraction and to catch mismatches early. |
| **Impact** | Ensures downstream processing works on a structured DataFrame and provides clear errors if expected columns are missing. |
| **Complexity** | MEDIUM |
| **Method** | Use `io.StringIO` with `pd.read_csv`, split `asset_pairs` on commas, and assert that for each pair a column named `<pair>_Spread` (or the naming convention used) exists in the DataFrame. |

#### 2. Iterate over the ordered `asset_pairs` list and, for each pair, collect the column values row‑by‑row, preserving the chronological order of the index.

| Category | Details |
| --- | --- |
| **Reason** | The required output ordering is first by date (oldest to newest) then by asset‑pair, matching the specification for the `price_spreads` field. |
| **Impact** | Produces a correctly ordered flat list that aligns with the flattened correlation list, enabling downstream models to pair spreads with their correlations. |
| **Complexity** | MEDIUM |
| **Method** | For each asset pair, retrieve the spread column (`df[col]`), convert to a NumPy array, and extend a master list; optionally use `df[[col1, col2, ...]].to_numpy().ravel('F')` for vectorized flattening. |

#### 3. Handle missing or NaN spread values by forward‑filling, backward‑filling, or substituting a sentinel (e.g., 0.0) before flattening.

| Category | Details |
| --- | --- |
| **Reason** | NaNs would break numeric downstream pipelines and could distort statistical calculations. |
| **Impact** | Produces a clean, numeric‑only list that can be safely consumed by downstream nodes without additional sanitisation. |
| **Complexity** | LOW |
| **Method** | Apply `df.fillna(method='ffill').fillna(method='bfill').fillna(0.0)` on the selected spread columns before extraction. |


---

## validate_output_lengths

### Description
Ensures that the lengths of the date, asset_pairs, correlations, and price_spreads arrays are consistent and match the expected dimensions before returning the output.

### Implementation Plan

#### 1. Check that the length of the `date` list equals the number of rows in the combined feature DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The date list must map one‑to‑one with each row of feature data to preserve temporal alignment. |
| **Impact** | Prevents misaligned timestamps from propagating downstream, ensuring downstream consumers can rely on correct date ordering. |
| **Complexity** | LOW |
| **Method** | Compare `len(date)` with `features_df.shape[0]`; raise a ValueError with a descriptive message if they differ. |

#### 2. Verify that the lengths of `correlations` and `price_spreads` each equal `len(date) * len(asset_pairs)`.

| Category | Details |
| --- | --- |
| **Reason** | Both correlation and spread arrays are flattened across dates and asset pairs; mismatched lengths indicate a flattening or calculation error. |
| **Impact** | Guarantees that each (date, asset_pair) combination has a corresponding correlation and spread value, preventing index errors in later processing. |
| **Complexity** | MEDIUM |
| **Method** | Compute `expected_len = len(date) * len(asset_pairs)` and assert `len(correlations) == expected_len` and `len(price_spreads) == expected_len`; raise detailed errors on failure. |

#### 3. Provide a single, unified validation interface that raises a clear, informative exception when any length check fails.

| Category | Details |
| --- | --- |
| **Reason** | A consistent error‑handling strategy simplifies debugging and makes the node’s contract explicit to callers. |
| **Impact** | Improves developer experience and pipeline reliability by surfacing mismatches early with actionable messages. |
| **Complexity** | LOW |
| **Method** | Wrap the checks in a helper function `validate_output_lengths(...)` that collects all mismatches and raises a `ValueError` summarizing all issues at once. |
