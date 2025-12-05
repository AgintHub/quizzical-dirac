# _assemble_feature_matrix - Complete PRD Documentation

## Overview
PRDs for nodes in the '_assemble_feature_matrix' module.

## Table of Contents

- [load_price_action_csv](#load_price_action_csv)

- [load_cross_asset_csv](#load_cross_asset_csv)

- [load_regime_csv](#load_regime_csv)

- [load_volatility_csv](#load_volatility_csv)

- [standardize_date_index](#standardize_date_index)

- [inner_join_on_date](#inner_join_on_date)

- [resolve_duplicate_columns](#resolve_duplicate_columns)

- [compute_next_day_return_target](#compute_next_day_return_target)

- [sort_and_reset_index](#sort_and_reset_index)

- [validate_feature_matrix](#validate_feature_matrix)

- [serialize_to_csv_string](#serialize_to_csv_string)

- [log_feature_matrix_summary](#log_feature_matrix_summary)



---

## load_price_action_csv

### Description
Loads a CSV‑formatted string of price‑action data and returns a structured representation for further processing.

### Implementation Plan

#### 1. Validate the CSV payload and ensure required columns (Date and at least one feature column) are present.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes assume a well‑formed table; missing columns would cause runtime errors. |
| **Impact** | Prevents propagation of malformed data and provides early, clear error messages. |
| **Complexity** | LOW |
| **Method** | Use Python's `csv` module or `pandas.read_csv` with `StringIO`; check `df.columns` for required names and raise a descriptive exception if validation fails. |

#### 2. Parse the CSV string into a DataFrame‑like structure and serialize it to a string for the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The rest of the pipeline expects a consumable table; serializing to JSON keeps the shim language‑agnostic. |
| **Impact** | Enables seamless integration with subsequent nodes that will deserialize the string back into a DataFrame. |
| **Complexity** | MEDIUM |
| **Method** | Load with `pandas.read_csv(StringIO(csv_data), parse_dates=['Date'])`, then `df.to_json(orient='records')` (or `df.to_csv` if a CSV string is preferred) and assign the result to `output`. |

#### 3. Implement robust error handling for malformed rows, non‑parseable dates, and empty inputs.

| Category | Details |
| --- | --- |
| **Reason** | Real‑world CSV feeds can contain irregularities; graceful handling avoids crashes. |
| **Impact** | Improves system resilience and provides actionable logs for operators. |
| **Complexity** | MEDIUM |
| **Method** | Wrap parsing logic in try/except blocks, catch `pd.errors.ParserError` and `ValueError` for date parsing, and return a standardized error message or raise a custom `ShimLoadError` that downstream nodes can recognize. |


---

## load_cross_asset_csv

### Description
Converts raw cross‑asset feature inputs into a CSV string aligned by date for downstream merging.

### Implementation Plan

#### 1. Parse the incoming string parameters into native Python structures (lists) and validate lengths and ordering.

| Category | Details |
| --- | --- |
| **Reason** | Input values are passed as serialized strings; they must be deserialized and checked for consistency before any transformation. |
| **Impact** | Prevents mis‑aligned rows, runtime errors, and ensures data integrity for downstream CSV generation. |
| **Complexity** | MEDIUM |
| **Method** | Use `json.loads` (or `ast.literal_eval`) to deserialize each parameter; verify that `len(dates) * len(asset_pairs) == len(correlations) == len(price_spreads)` and raise descriptive exceptions on mismatch. |

#### 2. Construct a pandas DataFrame where each row represents a date and each asset‑pair contributes two columns: one for correlation and one for price spread.

| Category | Details |
| --- | --- |
| **Reason** | A tabular representation simplifies column naming, alignment, and CSV serialization while preserving the required ordering (date → asset‑pair). |
| **Impact** | Produces a well‑structured CSV that can be directly merged with other feature tables using standard date‑index joins. |
| **Complexity** | LOW |
| **Method** | Iterate over `asset_pairs`, create column names like `{pair}_corr` and `{pair}_spread`, reshape the flat lists into matrices with `numpy.reshape`, and assemble the DataFrame via `pd.DataFrame` with the `dates` column as the index. |

#### 3. Serialize the DataFrame to a CSV string, ensuring the Date column is first and that no index column is added.

| Category | Details |
| --- | --- |
| **Reason** | The downstream `load_cross_asset_csv` shim expects a pure CSV payload without extra index artifacts. |
| **Impact** | Enables seamless ingestion by `assemble_feature_matrix` and other pipeline nodes, preserving column order and data types. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` to obtain the CSV text; return it as the `output` field along with the original serialized inputs for traceability. |


---

## load_regime_csv

### Description
Converts the supplied regime feature arrays into a CSV string with a Date column and corresponding regime and PMI flag columns for later merging.

### Implementation Plan

#### 1. Parse the three string inputs into Python lists, validate length consistency and date format (ISO‑8601).

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the downstream DataFrame construction receives well‑formed, aligned data and prevents mis‑alignment errors. |
| **Impact** | Prevents runtime crashes during CSV serialization and guarantees correct row count for merging. |
| **Complexity** | LOW |
| **Method** | Split each input on commas, strip whitespace, use datetime.strptime with '%Y-%m-%d' to validate dates, and raise a ValueError if any list lengths differ. |

#### 2. Create a pandas DataFrame with columns ['Date', 'regime_label', 'pmi_flag'] and populate it with the parsed lists.

| Category | Details |
| --- | --- |
| **Reason** | A DataFrame provides a convenient, tabular representation that can be easily converted to CSV and aligns with the matrix‑assembly pipeline. |
| **Impact** | Facilitates seamless integration with the `standardize_date_index` and `inner_join_on_date` utilities used later in the workflow. |
| **Complexity** | MEDIUM |
| **Method** | Import pandas, construct df = pd.DataFrame({ 'Date': dates_list, 'regime_label': regime_list, 'pmi_flag': pmi_list }), cast 'pmi_flag' to boolean, and set dtype consistency. |

#### 3. Serialize the DataFrame to a CSV‑formatted string without an index and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect a raw CSV string that they can ingest via `load_regime_csv` again; preserving column order is critical. |
| **Impact** | Provides the exact payload format required by `assemble_feature_matrix`, enabling correct inner‑join alignment. |
| **Complexity** | LOW |
| **Method** | Use df.to_csv(index=False) to generate the string, assign it to the `output` key, and ensure the function returns a dict matching the defined output_structure. |


---

## load_volatility_csv

### Description
Loads volatility feature CSV data into a DataFrame, validates its schema, and returns the serialized CSV along with the raw input strings.

### Implementation Plan

#### 1. Parse the three input CSV strings into a single pandas DataFrame with columns Date, garch_forecast, and implied_vol_delta_5d.

| Category | Details |
| --- | --- |
| **Reason** | The downstream assemble_feature_matrix node expects a unified DataFrame to join on the Date index. |
| **Impact** | Provides a consistent, tabular representation of volatility features, enabling reliable merging with other feature tables. |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` to feed each string into `pd.read_csv`, concatenate them horizontally, and rename columns to a standard schema. |

#### 2. Validate and coerce the Date column to datetime objects (ISO‑8601) and set it as the DataFrame index.

| Category | Details |
| --- | --- |
| **Reason** | Accurate date parsing is essential for correct inner‑join alignment across all feature tables. |
| **Impact** | Prevents mismatched or duplicate date entries, ensuring chronological integrity of the final feature matrix. |
| **Complexity** | MEDIUM |
| **Method** | Apply `pd.to_datetime(df['Date'], errors='raise', utc=True)` and `df.set_index('Date', inplace=True)`; raise a clear exception on parsing failures. |

#### 3. Serialize the validated DataFrame back to a CSV string for the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The assemble_feature_matrix node consumes CSV‑formatted strings; returning the processed CSV guarantees downstream compatibility. |
| **Impact** | Delivers clean, ready‑to‑join data while preserving the original raw inputs for traceability. |
| **Complexity** | LOW |
| **Method** | Use `df.to_csv(index=False)` wrapped in a `StringIO` buffer to capture the string. |


---

## standardize_date_index

### Description
Converts the Date column of a CSV‑encoded DataFrame to a normalized datetime index and returns the updated CSV string.

### Implementation Plan

#### 1. Parse the CSV string into a pandas DataFrame, locate the Date column (case‑insensitive), convert it to UTC ISO‑8601 datetime objects, set it as the index, and sort the frame in ascending order.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes rely on a consistent, timezone‑aware datetime index to correctly join feature tables. |
| **Impact** | Ensures all feature tables share a common, correctly ordered Date index, preventing join mismatches and time‑zone bugs. |
| **Complexity** | MEDIUM |
| **Method** | Use `io.StringIO` with `pd.read_csv`, identify the Date column via `df.columns.str.lower()`, apply `pd.to_datetime(..., utc=True)`, assign `df.set_index('Date')`, and call `df.sort_index()`. |

#### 2. Validate the resulting Date index for uniqueness and the absence of missing values, raising a clear exception if violations are detected.

| Category | Details |
| --- | --- |
| **Reason** | Duplicate or null dates would corrupt inner joins and downstream feature alignment. |
| **Impact** | Prevents silent data corruption and provides immediate feedback for data quality issues. |
| **Complexity** | LOW |
| **Method** | After indexing, check `df.index.is_unique` and `df.index.isna().any()`; if false, raise `ValueError` with an informative message. |

#### 3. Serialize the cleaned DataFrame back to a CSV string, ensuring the Date column appears as the first column and all other feature columns retain their original order and values.

| Category | Details |
| --- | --- |
| **Reason** | Subsequent processing steps expect the Date column first and unchanged feature columns. |
| **Impact** | Maintains feature integrity while delivering a standardized CSV format for downstream consumption. |
| **Complexity** | LOW |
| **Method** | Reset the index to make Date a column with `df.reset_index()`, reorder columns if necessary, and use `df.to_csv(index=False)` with a `StringIO` buffer to capture the CSV string. |


---

## inner_join_on_date

### Description
Merges the price, cross‑asset, regime, and volatility feature tables by performing an inner join on their standardized Date index and returns the combined table as a CSV string.

### Implementation Plan

#### 1. Parse each input CSV string into a pandas DataFrame, coerce the Date column to datetime, and set it as the index.

| Category | Details |
| --- | --- |
| **Reason** | Uniform datetime handling is required for a reliable join across all feature tables. |
| **Impact** | Ensures all tables share a common, correctly typed Date index, preventing join mismatches and downstream errors. |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` with `pd.read_csv`, apply `pd.to_datetime` on the Date column, and call `set_index('Date')` on each DataFrame. |

#### 2. Rename columns in each DataFrame with a source‑specific prefix (e.g., price_, cross_, regime_, vol_) to avoid name collisions, then perform an inner join on the Date index across the four DataFrames.

| Category | Details |
| --- | --- |
| **Reason** | Feature columns from different sources may share names (e.g., "close"), which would be overwritten without disambiguation. |
| **Impact** | Produces a single, conflict‑free feature matrix that downstream nodes can consume without ambiguity. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `df.columns` to prepend the appropriate prefix, then use `functools.reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'), dfs)`; finally serialize with `df.to_csv(StringIO, index=False)`. |

#### 3. Validate that the merged DataFrame contains at least one row and that the Date index is monotonic increasing; raise a descriptive `ValueError` if the validation fails.

| Category | Details |
| --- | --- |
| **Reason** | An empty or unsorted result indicates mismatched date ranges and would break model training. |
| **Impact** | Provides early, clear feedback to developers or pipelines, preventing silent downstream failures. |
| **Complexity** | LOW |
| **Method** | Check `merged_df.empty` and `merged_df.index.is_monotonic_increasing`; if conditions are not met, raise `ValueError` with details of the offending inputs. |


---

## resolve_duplicate_columns

### Description
Renames any duplicate column names in a merged DataFrame by prefixing them with supplied source identifiers to ensure column uniqueness.

### Implementation Plan

#### 1. Detect duplicate column names in the provided DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Merging multiple feature tables often yields columns with identical names, which breaks downstream operations like model training. |
| **Impact** | Prevents runtime errors and ensures each feature is uniquely identifiable. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.Index.duplicated() on df.columns to locate duplicated names; generate a boolean mask of duplicates. |

#### 2. Assign deterministic prefixes to each duplicated column based on the ordered list of source_prefixes.

| Category | Details |
| --- | --- |
| **Reason** | The caller supplies a known ordering of feature sources (e.g., ['price_', 'cross_', 'regime_', 'vol_']); applying these prefixes resolves ambiguity while preserving provenance. |
| **Impact** | Creates a clear naming convention that downstream nodes can rely on for feature selection and interpretability. |
| **Complexity** | MEDIUM |
| **Method** | Split source_prefixes string on commas, iterate over duplicated columns, and prepend the matching prefix (cycling if more duplicates than prefixes) to the original column name. |

#### 3. Return the DataFrame with updated column names, preserving original data and index order.

| Category | Details |
| --- | --- |
| **Reason** | Only the column labels need alteration; the data and chronological index must remain unchanged for correct model alignment. |
| **Impact** | Delivers a clean, ready‑to‑use feature matrix without side‑effects, enabling seamless continuation of the pipeline. |
| **Complexity** | LOW |
| **Method** | Create a copy of the original DataFrame, assign the new column list via df.columns = new_names, then serialize the DataFrame back to a CSV/JSON string for the output field. |


---

## compute_next_day_return_target

### Description
Computes a next‑day simple return target column for the provided DataFrame and returns the updated CSV string.

### Implementation Plan

#### 1. Parse the input CSV string into a pandas DataFrame and ensure the Date column is sorted chronologically.

| Category | Details |
| --- | --- |
| **Reason** | Accurate calculations depend on correct ordering and proper data types for numeric operations. |
| **Impact** | Guarantees that subsequent calculations operate on a clean, correctly indexed DataFrame. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(df))`, convert the Date column to datetime with `pd.to_datetime`, and sort by Date. |

#### 2. Create the `Target` column by shifting the specified close price column one row forward and applying the simple return formula.

| Category | Details |
| --- | --- |
| **Reason** | The core business requirement is to provide the next‑day return as the model's target variable. |
| **Impact** | Adds a predictive target that aligns with feature rows, enabling supervised learning downstream. |
| **Complexity** | MEDIUM |
| **Method** | Compute `df['Target'] = df[close_column].shift(-1) / df[close_column] - 1`, then drop the last row where `Target` is NaN. |

#### 3. Serialize the enriched DataFrame back to a CSV string while preserving the original column order and including the new `Target` column.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect CSV‑formatted text, not a DataFrame object. |
| **Impact** | Provides a seamless interface for the rest of the pipeline, maintaining compatibility with existing loaders. |
| **Complexity** | LOW |
| **Method** | Use `df.to_csv(index=False)` with an in‑memory `StringIO` buffer and return the buffer's contents as `output`. |


---

## sort_and_reset_index

### Description
Sorts the provided DataFrame by its Date column in chronological order and resets the index to a default integer range, returning the transformed data as a CSV‑formatted string.

### Implementation Plan

#### 1. Parse the input CSV string into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Subsequent operations require a structured, in‑memory representation of the data. |
| **Impact** | Enables reliable column‑wise manipulation and ensures downstream logic works on a proper DataFrame object. |
| **Complexity** | LOW |
| **Method** | Use Python's `io.StringIO` together with `pd.read_csv(df)` to read the `df` string into a DataFrame. |

#### 2. Convert the Date column to datetime, sort the DataFrame chronologically, and reset the index.

| Category | Details |
| --- | --- |
| **Reason** | Time‑series features must be aligned in proper temporal order and have a clean integer index for further joins and modeling. |
| **Impact** | Guarantees that all later nodes (e.g., joins, target calculation) operate on correctly ordered data, preventing mis‑alignment bugs. |
| **Complexity** | MEDIUM |
| **Method** | Apply `pd.to_datetime(df['Date'])`, then `df.sort_values('Date', inplace=True)`, and finally `df.reset_index(drop=True, inplace=True)`. |

#### 3. Serialize the sorted DataFrame back to a CSV‑formatted string for output.

| Category | Details |
| --- | --- |
| **Reason** | The node contract specifies a string output, matching the format expected by downstream nodes. |
| **Impact** | Provides a compact, portable representation that can be passed through the pipeline without losing data fidelity. |
| **Complexity** | LOW |
| **Method** | Use `df.to_csv(index=False)` and return the resulting string as the `output` field. |


---

## validate_feature_matrix

### Description
Validates that the assembled feature matrix DataFrame contains the required columns, has no duplicate or missing values, and is properly indexed before serialization.

### Implementation Plan

#### 1. Check presence of all required columns, including Date and Target.

| Category | Details |
| --- | --- |
| **Reason** | The downstream model expects these columns to exist for training and inference. |
| **Impact** | Prevents runtime errors due to missing features and ensures consistent schema. |
| **Complexity** | LOW |
| **Method** | Parse the CSV string into a pandas DataFrame, compare df.columns with the expected list, and raise an exception if any are absent. |

#### 2. Detect and reject duplicate column names.

| Category | Details |
| --- | --- |
| **Reason** | Duplicate columns can cause ambiguous references and corrupt feature alignment. |
| **Impact** | Ensures each feature is uniquely identifiable, maintaining data integrity. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.DataFrame.columns.duplicated() to identify duplicates and raise a validation error. |

#### 3. Validate that there are no missing (NaN) values and that the Date column is monotonic increasing.

| Category | Details |
| --- | --- |
| **Reason** | Missing values can degrade model performance, and unsorted dates break temporal alignment. |
| **Impact** | Guarantees clean input for model training and reliable time-series ordering. |
| **Complexity** | MEDIUM |
| **Method** | Check df.isnull().any().any() for any NaNs; verify df['Date'] is datetime and df['Date'].is_monotonic_increasing. |


---

## serialize_to_csv_string

### Description
Converts a pandas DataFrame into a CSV‑formatted string for downstream consumption.

### Implementation Plan

#### 1. Serialize the DataFrame using pandas `to_csv` into an in‑memory string buffer.

| Category | Details |
| --- | --- |
| **Reason** | The downstream `assemble_feature_matrix` node expects a CSV string to embed in its output model. |
| **Impact** | Provides a correctly formatted CSV representation that can be written to disk, transmitted over APIs, or parsed by other components. |
| **Complexity** | MEDIUM |
| **Method** | Create a `io.StringIO` buffer, call `df.to_csv(buf, index=False, date_format='%Y-%m-%d', na_rep='', quoting=csv.QUOTE_MINIMAL)`, then retrieve `buf.getvalue()`. |

#### 2. Enforce deterministic column ordering and unified line endings.

| Category | Details |
| --- | --- |
| **Reason** | Inconsistent column order or platform‑specific newline characters cause downstream parsing mismatches and flaky tests. |
| **Impact** | Ensures that every invocation yields identical CSV output given the same DataFrame, improving reproducibility. |
| **Complexity** | LOW |
| **Method** | Do not alter the original column order; explicitly set `line_terminator='\n'` in `to_csv` and avoid including the index unless required. |

#### 3. Validate the generated CSV string before returning.

| Category | Details |
| --- | --- |
| **Reason** | Early detection of serialization issues (e.g., missing mandatory columns like `Date`) prevents obscure errors later in the pipeline. |
| **Impact** | Raises a clear exception if the CSV is empty or lacks required structure, allowing the pipeline to fail fast and be easier to debug. |
| **Complexity** | MEDIUM |
| **Method** | After serialization, read the string back with `pd.read_csv(io.StringIO(csv_str))`, assert that the DataFrame is non‑empty and that `'Date'` is among its columns; raise `ValueError` otherwise. |


---

## log_feature_matrix_summary

### Description
Logs a summary of the assembled feature matrix for observability and debugging purposes.

### Implementation Plan

#### 1. Extract basic shape information (row count, column count) from the DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Stakeholders need to verify that the merged matrix has the expected dimensions before downstream modeling. |
| **Impact** | Provides immediate visibility into data volume, helping detect unexpected truncation or duplication early. |
| **Complexity** | LOW |
| **Method** | Use `df.shape` to obtain rows and columns; format into a short string and include in the log message. |

#### 2. Compute missing‑value statistics for each column.

| Category | Details |
| --- | --- |
| **Reason** | Missing data can cause model failures; summarizing it aids quick diagnostics. |
| **Impact** | Enables rapid identification of columns that may require imputation or exclusion, improving data quality monitoring. |
| **Complexity** | MEDIUM |
| **Method** | Apply `df.isnull().sum()` to get per‑column missing counts; optionally calculate the percentage and append to the log. |

#### 3. Generate descriptive statistics (mean, std, min, max) for all numeric columns.

| Category | Details |
| --- | --- |
| **Reason** | Understanding the distribution of features helps spot outliers or scaling issues before training. |
| **Impact** | Offers a snapshot of feature health, supporting early detection of data drift or anomalies. |
| **Complexity** | MEDIUM |
| **Method** | Call `df.describe(include=[np.number])`, convert the result to a compact string (e.g., via `to_string()`), and include it in the logged output. |
