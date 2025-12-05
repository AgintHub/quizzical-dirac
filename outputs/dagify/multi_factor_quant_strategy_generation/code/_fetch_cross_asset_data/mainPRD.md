# _fetch_cross_asset_data - Complete PRD Documentation

## Overview
PRDs for nodes in the '_fetch_cross_asset_data' module.

## Table of Contents

- [extract_cross_asset_tickers](#extract_cross_asset_tickers)

- [get_primary_asset_date_range](#get_primary_asset_date_range)

- [download_close_prices](#download_close_prices)

- [create_unified_dataframe](#create_unified_dataframe)

- [slice_dataframe_by_dates](#slice_dataframe_by_dates)

- [dataframe_to_csv](#dataframe_to_csv)

- [extract_column_names](#extract_column_names)

- [extract_dataframe_metadata](#extract_dataframe_metadata)

- [persist_csv_data](#persist_csv_data)



---

## extract_cross_asset_tickers

### Description
Extracts a list of cross‑asset ticker symbols from a plain‑text description of data sources.

### Implementation Plan

#### 1. Tokenize each line of the `data_sources` string and identify ticker symbols using regular‑expression patterns.

| Category | Details |
| --- | --- |
| **Reason** | Data‑source descriptions are free‑form text; a reliable pattern match is needed to reliably pull out tickers. |
| **Impact** | Ensures that the downstream `fetch_cross_asset_data` node receives accurate ticker identifiers, preventing download failures. |
| **Complexity** | MEDIUM |
| **Method** | Compile a regex such as `(?i)\b([A-Z]{1,5})(?:\.[A-Z]{1,2})?\b` to capture common ticker formats, iterate over lines, and collect matches while ignoring duplicates. |

#### 2. Normalize and validate extracted tickers against a known asset‑type whitelist (e.g., equities, ETFs, futures).

| Category | Details |
| --- | --- |
| **Reason** | Raw text may contain non‑ticker words or malformed symbols that would cause downstream API errors. |
| **Impact** | Filters out invalid entries, reducing unnecessary network calls and improving overall data quality. |
| **Complexity** | LOW |
| **Method** | Maintain a set of allowed prefix/suffix patterns (e.g., no spaces, optional suffix like .X), and discard any match that fails these rules; optionally cross‑check against a cached symbol lookup service. |

#### 3. Return the unique list of tickers in the order they appear, preserving deterministic output for caching.

| Category | Details |
| --- | --- |
| **Reason** | Downstream processes may rely on consistent ordering for reproducibility and caching mechanisms. |
| **Impact** | Provides stable input to downstream nodes, enabling cache hits and easier debugging. |
| **Complexity** | LOW |
| **Method** | Use an OrderedDict or a simple list with a membership set to track insertion order while eliminating duplicates before returning. |


---

## get_primary_asset_date_range

### Description
Returns a dictionary with the ISO‑8601 start_date and end_date of the primary asset based on its metadata, or empty values if unavailable.

### Implementation Plan

#### 1. Read primary‑asset metadata from the configured source (e.g., a database, API, or configuration file).

| Category | Details |
| --- | --- |
| **Reason** | The date range must reflect the actual coverage of the primary asset's historical data. |
| **Impact** | Ensures downstream nodes (like fetch_cross_asset_data) request data only for dates that exist for the primary asset, preventing empty or misaligned time series. |
| **Complexity** | MEDIUM |
| **Method** | Implement a lightweight accessor that queries the metadata store (SQL SELECT, REST GET, or file read) and extracts the 'start_date' and 'end_date' fields, parsing them into ISO‑8601 format. |

#### 2. Validate and normalize the extracted dates, defaulting to empty strings when metadata is missing or malformed.

| Category | Details |
| --- | --- |
| **Reason** | Robustness: downstream logic expects string values and will skip slicing if dates are falsy. |
| **Impact** | Prevents runtime errors in date parsing and allows the workflow to continue gracefully when the primary asset lacks date information. |
| **Complexity** | LOW |
| **Method** | Use Python's datetime.strptime with a try/except block; on failure set date variables to "" and log a warning. |

#### 3. Serialize the result as a JSON string matching the declared output type.

| Category | Details |
| --- | --- |
| **Reason** | The node contract specifies a PrimitiveType.STR output, so callers must be able to deserialize the dict. |
| **Impact** | Provides a consistent, language‑agnostic payload for any downstream node or external system. |
| **Complexity** | LOW |
| **Method** | Return json.dumps({"start_date": start_date, "end_date": end_date}) from the shim function. |


---

## download_close_prices

### Description
Downloads the historical daily closing price series for a given ticker between two ISO‑8601 dates and returns the data as a CSV‑formatted string.

### Implementation Plan

#### 1. Validate inputs (ticker symbol format, ISO‑8601 dates, logical ordering) and normalize them to a standard representation.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that downstream API calls receive well‑formed parameters and prevents obscure runtime errors. |
| **Impact** | Reduces failure rates, provides clear error messages to callers, and guarantees consistent date handling across data providers. |
| **Complexity** | LOW |
| **Method** | Use regex for ticker validation, Python's `datetime` module for date parsing, and raise `ValueError` with descriptive messages on failure. |

#### 2. Fetch closing price data from a reliable market data provider (e.g., yfinance, Alpha Vantage, or Bloomberg SDK) handling authentication, rate limits, and missing data gracefully.

| Category | Details |
| --- | --- |
| **Reason** | The core functionality of the shim is to retrieve accurate historical price data; handling provider quirks is essential for reliability. |
| **Impact** | Provides a robust, production‑ready data retrieval layer that can be swapped for different vendors without affecting downstream nodes. |
| **Complexity** | MEDIUM |
| **Method** | Encapsulate provider logic in a strategy pattern, implement exponential back‑off for rate‑limit retries, and fill missing dates with `NaN` using pandas. |

#### 3. Transform the retrieved pandas Series/DataFrame into a CSV‑formatted string and embed it in the `output` field; include error handling for empty results.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect a CSV string; consistent formatting avoids parsing errors later in the workflow. |
| **Impact** | Ensures downstream compatibility and makes the shim’s output directly consumable by `fetch_cross_asset_data` and other nodes. |
| **Complexity** | LOW |
| **Method** | Use `DataFrame.to_csv(index=True, date_format='%Y-%m-%d')` to generate the string, strip trailing newlines, and raise a custom exception if the DataFrame is empty. |


---

## create_unified_dataframe

### Description
Creates a single pandas DataFrame by outer‑joining multiple price‑series provided as a dictionary and returns the result as a CSV‑formatted string.

### Implementation Plan

#### 1. Parse the incoming `series_dict` JSON string into a Python dict of pandas Series objects.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives data as a string to stay type‑agnostic for the workflow engine; it must be deserialized before any dataframe operations. |
| **Impact** | Ensures that downstream dataframe logic operates on proper pandas objects, preventing runtime type errors. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` to convert the string to a dict, then iterate over items creating a `pd.Series` for each ticker, setting the date column as the index. |

#### 2. Perform an outer join across all Series to produce a unified DataFrame aligned on the full date range.

| Category | Details |
| --- | --- |
| **Reason** | Cross‑asset correlation analysis requires a common timeline; missing dates for any asset must be represented as NaN. |
| **Impact** | Produces a complete, date‑aligned dataset that downstream nodes can slice or analyze without additional alignment steps. |
| **Complexity** | MEDIUM |
| **Method** | Create a list of individual Series DataFrames, then use `pd.concat(series_df_list, axis=1, join='outer')`, rename columns to tickers, and optionally sort the index. |

#### 3. Serialize the resulting DataFrame to a CSV‑formatted string.

| Category | Details |
| --- | --- |
| **Reason** | The workflow expects the unified data in a portable, text‑based format for storage or further processing. |
| **Impact** | Provides a compact representation that can be easily persisted, transmitted, or converted back to a DataFrame later. |
| **Complexity** | LOW |
| **Method** | Call `df.reset_index().to_csv(index=False)` and capture the resulting string to return as `output`. |


---

## slice_dataframe_by_dates

### Description
Slices a DataFrame to retain only rows with dates between start_date and end_date (inclusive).

### Implementation Plan

#### 1. Validate that start_date and end_date conform to ISO‑8601 (YYYY‑MM‑DD) format.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that date comparisons are reliable and prevents parsing errors later in the pipeline. |
| **Impact** | Early detection of malformed dates reduces downstream failures and makes debugging easier. |
| **Complexity** | LOW |
| **Method** | Use Python's datetime.strptime with the pattern "%Y-%m-%d"; raise a descriptive ValueError if parsing fails. |

#### 2. Deserialize the incoming df string into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string representation; converting it back to a DataFrame is required for slicing operations. |
| **Impact** | Provides a concrete DataFrame object that can be manipulated with pandas APIs, enabling accurate date filtering. |
| **Complexity** | MEDIUM |
| **Method** | Detect the format (CSV, JSON, or pickled base64) and use the appropriate pandas loader (pd.read_csv, pd.read_json, or pd.read_pickle after base64 decode). If format detection fails, fallback to a clear exception. |

#### 3. Apply a boolean mask to keep rows where the Date column is between start_date and end_date, then serialize the result back to a string.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality of the shim – returning only the requested date range for downstream consumption. |
| **Impact** | Produces a filtered DataFrame that matches the primary asset’s timeline, ensuring downstream nodes receive consistent temporal data. |
| **Complexity** | LOW |
| **Method** | Convert the Date column to datetime (pd.to_datetime), then filter with df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]. Finally, serialize with df.to_csv(index=False) (or to_json if original format was JSON) and assign to the output field. |


---

## dataframe_to_csv

### Description
Converts a DataFrame (provided as a string) into a CSV‑formatted string.

### Implementation Plan

#### 1. Parse the incoming string into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string representation; it must be materialized before conversion. |
| **Impact** | Enables downstream logic to work with a proper DataFrame object, preventing runtime errors during CSV conversion. |
| **Complexity** | MEDIUM |
| **Method** | Attempt JSON deserialization first; if that fails, fall back to ast.literal_eval for Python literal formats, finally try csv.read_csv on a StringIO buffer. |

#### 2. Serialize the DataFrame to CSV using pandas' to_csv method.

| Category | Details |
| --- | --- |
| **Reason** | Pandas provides a reliable, configurable CSV serialization that handles edge cases like commas in data and NaN values. |
| **Impact** | Produces a standards‑compliant CSV string that can be stored, transmitted, or consumed by other nodes. |
| **Complexity** | LOW |
| **Method** | Call df.to_csv(index=False, line_terminator='\n', encoding='utf-8') and capture the result from a StringIO buffer. |

#### 3. Validate and clean the resulting CSV string before returning.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the output does not contain unexpected carriage returns, BOM characters, or trailing newlines that could break downstream parsers. |
| **Impact** | Improves robustness of the workflow and guarantees consistent output format across environments. |
| **Complexity** | LOW |
| **Method** | Strip any leading/trailing whitespace, replace Windows line endings ("\r\n") with UNIX style ("\n"), and optionally verify that at least one header row exists. |


---

## extract_column_names

### Description
Extracts the list of column names from a CSV‑formatted DataFrame string.

### Implementation Plan

#### 1. Parse the CSV string into an in‑memory table structure (e.g., pandas DataFrame) without loading full data into memory when possible.

| Category | Details |
| --- | --- |
| **Reason** | A reliable parser is required to correctly interpret delimiters, quoting, and line breaks before column extraction. |
| **Impact** | Ensures accurate column name retrieval even for complex CSV payloads and prevents downstream errors. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv(io.StringIO(df), nrows=0)` to load only the header row, or fall back to Python's `csv` module if pandas is unavailable. |

#### 2. Extract the ordered list of column headers from the parsed table.

| Category | Details |
| --- | --- |
| **Reason** | The core purpose of the shim is to provide downstream nodes with the exact column identifiers for further processing. |
| **Impact** | Provides a deterministic, order‑preserving list that downstream nodes (e.g., asset name extraction) can rely on. |
| **Complexity** | LOW |
| **Method** | Retrieve `dataframe.columns.tolist()` when using pandas, or read the first row from the CSV reader and return it as a list of strings. |

#### 3. Return the column list as a JSON‑serializable `LIST_STR` field while preserving the original `df` input for traceability.

| Category | Details |
| --- | --- |
| **Reason** | The node contract expects both the original input and the extracted output for auditing and debugging. |
| **Impact** | Facilitates transparent data lineage and enables easy inspection of inputs/outputs in workflow logs. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary `{ "output": column_list, "df": df }` and let the surrounding framework handle JSON serialization. |


---

## extract_dataframe_metadata

### Description
Extracts key metadata (start date, end date, and row count) from a given DataFrame and returns it as a JSON‑encoded string.

### Implementation Plan

#### 1. Parse the incoming string into an actual pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string representation, so it must be materialized before analysis. |
| **Impact** | Enables subsequent operations to work with genuine DataFrame methods, ensuring correct metadata extraction. |
| **Complexity** | LOW |
| **Method** | Use `ast.literal_eval` or `json.loads` combined with `pd.DataFrame.from_records` depending on the serialization format; include error handling for malformed inputs. |

#### 2. Compute start_date, end_date, and row_count from the DataFrame's index and shape.

| Category | Details |
| --- | --- |
| **Reason** | These three pieces of information constitute the essential metadata required by downstream nodes. |
| **Impact** | Provides accurate temporal boundaries and size metrics for the fetched cross‑asset price series. |
| **Complexity** | MEDIUM |
| **Method** | If the index is datetime‑like, call `df.index.min()` and `df.index.max()`, convert to ISO‑8601 strings with `strftime('%Y-%m-%d')`; obtain `row_count` via `len(df)`; handle non‑datetime indexes by falling back to the first/last row values. |

#### 3. Serialize the metadata dictionary to a JSON string and return it.

| Category | Details |
| --- | --- |
| **Reason** | The node contract expects a string output that downstream code can parse without importing pandas. |
| **Impact** | Ensures a language‑agnostic, lightweight representation that can be stored or transmitted easily. |
| **Complexity** | LOW |
| **Method** | Create `metadata = {'start_date': start_date, 'end_date': end_date, 'row_count': row_count}` and return `json.dumps(metadata)`. Include validation to guarantee all fields are present. |


---

## persist_csv_data

### Description
Persists the provided CSV‑formatted string to a temporary location tied to the current workflow context and returns the file path.

### Implementation Plan

#### 1. Derive a deterministic temporary directory from the `workflow_context` string.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that files are scoped to the specific workflow execution and avoid collisions across runs. |
| **Impact** | Files are organized per workflow, simplifying cleanup and traceability. |
| **Complexity** | MEDIUM |
| **Method** | Parse `workflow_context` as JSON (or a simple key‑value string), extract a unique identifier (e.g., run_id), and join it with the system's temp directory using `os.path.join`. |

#### 2. Write the `csv_data` string to a uniquely‑named file within the derived directory.

| Category | Details |
| --- | --- |
| **Reason** | A unique filename prevents overwriting existing data and supports parallel executions. |
| **Impact** | Reliable persistence of CSV payloads without race conditions. |
| **Complexity** | LOW |
| **Method** | Generate a UUID‑based filename with a `.csv` extension, open the file in text mode with UTF‑8 encoding, and write the string atomically using a context manager. |

#### 3. Return the full file path and handle I/O errors gracefully.

| Category | Details |
| --- | --- |
| **Reason** | Consumers need the location for downstream processing, and robust error handling prevents silent failures. |
| **Impact** | Provides a clear contract (path string) and ensures the workflow fails fast with informative messages if persistence fails. |
| **Complexity** | MEDIUM |
| **Method** | Wrap the write operation in a try/except block, catching `OSError` and re‑raising a custom `PersistCSVError` with details; on success, return the absolute path as the `output` field. |
