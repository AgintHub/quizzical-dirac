# _fetch_volatility_data - Complete PRD Documentation

## Overview
PRDs for nodes in the '_fetch_volatility_data' module.

## Table of Contents

- [parse_implied_vol_source](#parse_implied_vol_source)

- [fetch_primary_asset_prices](#fetch_primary_asset_prices)

- [calculate_realized_volatility](#calculate_realized_volatility)

- [fetch_implied_volatility_data](#fetch_implied_volatility_data)

- [merge_volatility_data](#merge_volatility_data)

- [validate_volatility_data](#validate_volatility_data)

- [extract_dates_list](#extract_dates_list)

- [extract_realized_vol_list](#extract_realized_vol_list)

- [extract_implied_vol_list](#extract_implied_vol_list)

- [log_volatility_data_summary](#log_volatility_data_summary)



---

## parse_implied_vol_source

### Description
Extracts the implied volatility provider identifier from a plain‑text list of data‑source descriptions.

### Implementation Plan

#### 1. Implement robust string parsing to split `data_sources` into individual lines and extract the provider name from the line that mentions implied volatility.

| Category | Details |
| --- | --- |
| **Reason** | The input is a free‑form text block; reliable extraction requires deterministic line handling and pattern matching. |
| **Impact** | Accurately identifies the correct provider, enabling downstream calls to fetch implied volatility data. |
| **Complexity** | MEDIUM |
| **Method** | Use Python's `str.splitlines()` to obtain lines, then apply a regular expression such as `r"Implied\s*Volatility\s*[:\-]?\s*(.+?)(?:,|$)"` (case‑insensitive) to capture the provider name; trim whitespace before returning. |

#### 2. Add fallback heuristics to handle variations in wording (e.g., "IV Index", "Implied Vol", or provider name appearing before the dataset type).

| Category | Details |
| --- | --- |
| **Reason** | Data source descriptions may not follow a strict template, and missing the provider would break the pipeline. |
| **Impact** | Improves resilience against inconsistencies in source listings, reducing false negatives. |
| **Complexity** | LOW |
| **Method** | If the primary regex fails, iterate through lines and check for keywords like "implied vol", "iv index", then split the line on ':' or '-' and take the segment that is not the dataset type as the provider. |

#### 3. Validate the extracted provider against a whitelist of known implied volatility providers and return an empty string if validation fails.

| Category | Details |
| --- | --- |
| **Reason** | Prevent propagation of misspelled or unsupported provider names to downstream fetch functions. |
| **Impact** | Ensures only supported providers are used, avoiding runtime errors in `fetch_implied_volatility_data`. |
| **Complexity** | LOW |
| **Method** | Maintain a set such as `{"CBOE", "Bloomberg", "Refinitiv"}`; after extraction, check `provider.strip()` against the set (case‑insensitive). If not found, log a warning and return `""`. |


---

## fetch_primary_asset_prices

### Description
This shim retrieves historical price data for the primary asset based on the provided data source information.

### Implementation Plan

#### 1. Implement data source parsing logic to identify the provider and dataset for primary asset prices.

| Category | Details |
| --- | --- |
| **Reason** | The function needs to know which provider (e.g., Bloomberg, Refinitiv) and dataset to query for price data. |
| **Impact** | Enables the function to dynamically fetch data from the correct source, ensuring compatibility with various data providers. |
| **Complexity** | MEDIUM |
| **Method** | Utilize regular expressions or string parsing techniques to extract the provider name and dataset identifier from the data_sources string.  Create a mapping between these identifiers and the appropriate data retrieval functions. |

#### 2. Develop a data retrieval mechanism to fetch historical price data from the identified provider.

| Category | Details |
| --- | --- |
| **Reason** | The historical price data is essential for calculating realized volatility. |
| **Impact** | Provides the raw data required for downstream calculations, directly influencing the accuracy of the volatility metrics. |
| **Complexity** | HIGH |
| **Method** | Implement API calls or database queries to fetch the price data, ensuring proper authentication and error handling. Consider using a library like `yfinance` or `pandas-datareader` if the data source is publicly available. If a proprietary API is needed, write custom client code. |

#### 3. Structure the fetched price data into a Pandas DataFrame with 'Date' and 'Price' columns.

| Category | Details |
| --- | --- |
| **Reason** | The 'calculate_realized_volatility' function expects the price data in this format. |
| **Impact** | Ensures compatibility with the rest of the volatility calculation pipeline. |
| **Complexity** | LOW |
| **Method** | Transform the raw data (e.g., from a list of lists or a dictionary) into a Pandas DataFrame, ensuring the 'Date' column is in a standard date format (YYYY-MM-DD) and the 'Price' column contains numeric values. |


---

## calculate_realized_volatility

### Description
Computes a rolling realized volatility series from a price DataFrame using a specified window length.

### Implementation Plan

#### 1. Parse the incoming `price_df` string into a pandas DataFrame with a Date column and a Close price column.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives data as a serialized string; it must be converted to a structured format before calculations. |
| **Impact** | Enables downstream numeric operations and ensures date ordering for accurate rolling calculations. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_json` or `pd.read_csv` based on a simple format flag; raise a clear error if required columns are missing. |

#### 2. Calculate daily log returns and then compute the rolling standard deviation over the specified `window`, annualizing the result to obtain realized volatility.

| Category | Details |
| --- | --- |
| **Reason** | Realized volatility is defined as the annualized standard deviation of log returns over a moving window. |
| **Impact** | Provides the core metric required by downstream nodes for volatility forecasting and risk analysis. |
| **Complexity** | MEDIUM |
| **Method** | Convert `window` to int, use `np.log` for returns, `df['log_ret'].rolling(window).std()` for rolling std, multiply by sqrt(252) to annualize. |

#### 3. Serialize the resulting DataFrame (Date and Realized Volatility columns) back to a string matching the expected output format.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect the output as a string; consistent serialization ensures interoperability. |
| **Impact** | Allows seamless hand‑off to nodes like `fetch_volatility_data` without additional transformation steps. |
| **Complexity** | LOW |
| **Method** | Use `df.to_json(orient="records")` or `df.to_csv(index=False)` based on a configurable output flag; include error handling for serialization failures. |


---

## fetch_implied_volatility_data

### Description
Fetches implied volatility index series from a specified provider source for the requested date range.

### Implementation Plan

#### 1. Validate and normalize input parameters (provider_source and start_date).

| Category | Details |
| --- | --- |
| **Reason** | Ensures that downstream API calls receive correctly formatted strings and prevents runtime errors due to malformed dates or unknown providers. |
| **Impact** | Reduces failure rates and improves reliability of the data retrieval step. |
| **Complexity** | LOW |
| **Method** | Use regex or date‑parsing libraries (e.g., datetime.strptime) to enforce YYYY‑MM‑DD format and whitelist known provider identifiers. |

#### 2. Implement a connector that authenticates (if needed) and queries the provider's API for implied volatility data.

| Category | Details |
| --- | --- |
| **Reason** | The core functionality of the shim is to obtain the raw volatility series from an external source. |
| **Impact** | Provides the necessary data for downstream volatility calculations and forecasting models. |
| **Complexity** | MEDIUM |
| **Method** | Create a thin wrapper using requests (or an SDK supplied by the provider) that builds the request URL with provider_source, start_date, and an inferred end_date (e.g., today), handles API keys via environment variables, and retries on transient HTTP errors. |

#### 3. Transform the retrieved time‑series into a deterministic string format and handle missing or out‑of‑order records.

| Category | Details |
| --- | --- |
| **Reason** | Consumers of this shim expect a stable, parse‑able output; inconsistencies would break downstream merging logic. |
| **Impact** | Ensures downstream nodes receive clean, chronologically ordered data, improving overall pipeline stability. |
| **Complexity** | MEDIUM |
| **Method** | Load the response into a pandas DataFrame, sort by date, forward‑fill any gaps, then serialize to JSON with a fixed schema (e.g., [{"date":"YYYY-MM-DD","implied_vol":float}, ...]). |


---

## merge_volatility_data

### Description
Merges realized and implied volatility DataFrames on their date column, handling missing values and returning a unified representation.

### Implementation Plan

#### 1. Parse the input JSON strings into pandas DataFrames and perform an inner join on the 'Date' column.

| Category | Details |
| --- | --- |
| **Reason** | The core purpose of the shim is to combine realized and implied volatility series for identical dates. |
| **Impact** | Produces a single DataFrame where each row contains both realized and implied volatility values, enabling downstream forecasting steps. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` to deserialize, `pd.DataFrame.from_records`, then `pd.merge(df_realized, df_implied, on='Date', how='inner')`. |

#### 2. Validate the merged DataFrame for missing values, correct data types, and chronological ordering, then serialize back to a JSON string.

| Category | Details |
| --- | --- |
| **Reason** | Ensures data integrity and a predictable output format for consumers of the node. |
| **Impact** | Downstream nodes receive clean, type‑consistent data and can rely on chronological continuity for time‑series modeling. |
| **Complexity** | MEDIUM |
| **Method** | Check `df.isnull().any()`, enforce `float` dtype for volatility columns, sort by `Date`, fill or drop any residual gaps, and finally use `df.to_json(orient='records')`. |


---

## validate_volatility_data

### Description
Validates and cleans a merged volatility DataFrame, ensuring no missing dates or NaNs before returning it.

### Implementation Plan

#### 1. Parse the input JSON string into a pandas DataFrame and verify that the 'Date' column contains a continuous daily range without gaps.

| Category | Details |
| --- | --- |
| **Reason** | Missing dates can break time‑series models and lead to inaccurate volatility forecasts. |
| **Impact** | Ensures temporal continuity, allowing downstream forecasting nodes to assume a regular time index. |
| **Complexity** | MEDIUM |
| **Method** | Use `pd.read_json` to load the DataFrame, generate a complete date range with `pd.date_range`, and compare it to the existing dates; raise an error or fill gaps as needed. |

#### 2. Check all numeric columns ('realized_vol', 'implied_vol') for NaN or non‑numeric values, and either interpolate missing data or drop affected rows.

| Category | Details |
| --- | --- |
| **Reason** | NaNs or invalid entries corrupt statistical calculations such as rolling volatility. |
| **Impact** | Produces a clean dataset that downstream nodes can safely use for calculations without additional error handling. |
| **Complexity** | MEDIUM |
| **Method** | Apply `df[['realized_vol','implied_vol']].apply(pd.to_numeric, errors='coerce')`, then use `df.interpolate(method='linear')` followed by `df.dropna()`; finally sort by date. |

#### 3. Serialize the validated DataFrame back to a JSON string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The surrounding pipeline expects string‑based payloads for node communication. |
| **Impact** | Maintains consistency with the system’s data‑exchange contract, allowing seamless integration with subsequent nodes. |
| **Complexity** | LOW |
| **Method** | Use `df.to_json(orient='records', date_format='iso')` and assign the result to the `output` key. |


---

## extract_dates_list

### Description
Extracts a list of date strings (YYYY-MM-DD) from a validated volatility DataFrame.

### Implementation Plan

#### 1. Deserialize the input string back into a pandas DataFrame and verify the presence and datatype of the 'Date' column.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string; it must be converted back to a usable structure before extracting dates. |
| **Impact** | Ensures that downstream extraction works on a correctly structured DataFrame, preventing runtime errors. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` or `pickle.loads` based on the serialization format, then check `if 'Date' not in df.columns` and `pd.api.types.is_datetime64_any_dtype(df['Date'])`. |

#### 2. Normalize the 'Date' column to pandas datetime objects and convert each entry to an ISO‑8601 string (YYYY‑MM‑DD).

| Category | Details |
| --- | --- |
| **Reason** | Dates may be stored as datetime objects, strings, or other formats; standardizing ensures consistent output. |
| **Impact** | Produces a clean, uniformly formatted list of dates suitable for downstream models and API contracts. |
| **Complexity** | MEDIUM |
| **Method** | Apply `pd.to_datetime(df['Date'], errors='coerce')`, drop NaT values, then use `.dt.strftime('%Y-%m-%d').tolist()` to generate the list. |

#### 3. Return the list of date strings while preserving the original chronological order and handling any missing/invalid entries gracefully.

| Category | Details |
| --- | --- |
| **Reason** | Order matters for time‑series alignment and missing dates should not break the contract. |
| **Impact** | Provides reliable, ordered output that downstream nodes can safely consume without additional cleaning. |
| **Complexity** | LOW |
| **Method** | After conversion, filter out any `None` or empty strings, retain the order of the DataFrame index, and assign the result to the `output` field. |


---

## extract_realized_vol_list

### Description
Extracts a list of realized volatility floats from a validated DataFrame provided as a string.

### Implementation Plan

#### 1. Parse the input string into a pandas DataFrame, supporting common serialization formats such as CSV and JSON.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives the DataFrame as a string; it must be materialized into a structured object for column operations. |
| **Impact** | Enables downstream column extraction and ensures the shim works with the data format produced by previous nodes. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv with StringIO for CSV strings and pandas.read_json for JSON strings, detecting format via simple heuristics or a file‑type flag. |

#### 2. Validate that the DataFrame contains a column named (or synonymous with) 'realized_vol' and that all entries are numeric.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring the expected column exists and contains clean numeric data prevents runtime errors and guarantees correct output. |
| **Impact** | Provides robust error handling and clear messages if the source data is malformed, improving pipeline reliability. |
| **Complexity** | MEDIUM |
| **Method** | Check DataFrame.columns for exact or case‑insensitive matches (e.g., 'RealizedVol', 'realized_vol'); coerce column to float using pandas.to_numeric with errors='raise'; raise a custom ValidationError if checks fail. |

#### 3. Extract the validated realized volatility column and convert it to a plain Python list of floats.

| Category | Details |
| --- | --- |
| **Reason** | The node's contract requires a List[float] output, not a pandas Series. |
| **Impact** | Delivers the final output in the expected format for downstream Pydantic models and API consumers. |
| **Complexity** | LOW |
| **Method** | Use df[realized_vol_column].tolist() after confirming the column; ensure the list contains native float types (e.g., via map(float)). |


---

## extract_implied_vol_list

### Description
Extracts the implied volatility column from a validated DataFrame and returns it as a list of floats.

### Implementation Plan

#### 1. Validate that the DataFrame contains an 'implied_vol' column of numeric type.

| Category | Details |
| --- | --- |
| **Reason** | Ensures downstream calculations receive correct data and prevents runtime type errors. |
| **Impact** | Provides early failure detection and clearer error messages, improving reliability of the volatility pipeline. |
| **Complexity** | LOW |
| **Method** | Use pandas `if 'implied_vol' not in df.columns` check and `pd.api.types.is_numeric_dtype(df['implied_vol'])` to verify presence and type. |

#### 2. Convert the 'implied_vol' column to a plain Python list of floats.

| Category | Details |
| --- | --- |
| **Reason** | The downstream Pydantic model expects a native Python list, not a pandas Series. |
| **Impact** | Ensures compatibility with the `FetchVolatilityDataOutput` model and downstream serialization. |
| **Complexity** | LOW |
| **Method** | Apply `df['implied_vol'].astype(float).tolist()` after validation. |

#### 3. Implement robust error handling that raises a descriptive `ValueError` if validation fails.

| Category | Details |
| --- | --- |
| **Reason** | Facilitates debugging and maintains data integrity across the workflow. |
| **Impact** | Consumers of the shim receive clear feedback, reducing silent failures and simplifying troubleshooting. |
| **Complexity** | MEDIUM |
| **Method** | Wrap validation and conversion in a try/except block; raise `ValueError` with message indicating missing column or non‑numeric data. |


---

## log_volatility_data_summary

### Description
Logs a concise summary of the volatility dataset including the date range, data source, and number of records.

### Implementation Plan

#### 1. Validate and normalise all inputs (dates, source, row_count) as strings before logging.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim receives consistent, type‑safe data regardless of upstream representations. |
| **Impact** | Prevents runtime type errors and guarantees that the log message is correctly formatted. |
| **Complexity** | LOW |
| **Method** | Use isinstance checks; if an input is a list (e.g., dates), join it into a comma‑separated string; raise a clear ValueError for unsupported types. |

#### 2. Create a human‑readable summary string that includes the earliest and latest dates, the data source, and the total row count.

| Category | Details |
| --- | --- |
| **Reason** | Provides auditors and developers with a quick snapshot of the volatility dataset without inspecting raw data. |
| **Impact** | Improves traceability and speeds up debugging when data pipelines fail or produce unexpected results. |
| **Complexity** | MEDIUM |
| **Method** | Parse the dates string (or list) to extract min/max dates; format the summary with an f‑string like `"Volatility data from {start} to {end} sourced from {source} – {row_count} rows"`. |

#### 3. Emit the summary via the standard logging framework at INFO level and return it in the prescribed output structure.

| Category | Details |
| --- | --- |
| **Reason** | Integrates the shim with existing observability tooling while also supplying downstream nodes with the logged message if needed. |
| **Impact** | Ensures the summary appears in logs, can be captured by monitoring systems, and satisfies the node contract by returning the output fields. |
| **Complexity** | LOW |
| **Method** | Import Python's `logging` module, configure a logger (or use the global logger), call `logger.info(summary)`, and set the `output` field to the same summary string before returning. |
