# _collect_historical_market_data - Complete PRD Documentation

## Overview
PRDs for nodes in the '_collect_historical_market_data' module.

## Table of Contents

- [parse_market_data_request](#parse_market_data_request)

- [select_optimal_data_source](#select_optimal_data_source)

- [fetch_raw_market_data](#fetch_raw_market_data)

- [clean_and_validate_market_data](#clean_and_validate_market_data)

- [calculate_data_quality_score](#calculate_data_quality_score)

- [format_market_data_output](#format_market_data_output)



---

## parse_market_data_request

### Description
Parses a general market data request string and keyword arguments to extract asset tickers and requested timeframes for historical data collection.

### Implementation Plan

#### 1. Implement robust parsing of the input string using regular expressions to isolate asset tickers (e.g., comma‑separated symbols) and timeframes (e.g., '1d', '1w', '1m').

| Category | Details |
| --- | --- |
| **Reason** | Accurate extraction is critical for downstream data retrieval. |
| **Impact** | Ensures that the correct assets and timeframes are requested, preventing missing or incorrect data. |
| **Complexity** | MEDIUM |
| **Method** | Use Python's `re` module to capture named groups for assets and timeframes, with fallbacks for default values. |

#### 2. Validate extracted assets against a whitelist of supported tickers and normalize timeframes into a standardized list (e.g., mapping '1d' to 'daily', '1w' to 'weekly').

| Category | Details |
| --- | --- |
| **Reason** | Prevent invalid or unsupported requests from propagating through the system. |
| **Impact** | Improves reliability and reduces runtime errors during data fetching. |
| **Complexity** | LOW |
| **Method** | Load a configuration file or database of valid tickers and use a dictionary to map timeframe shorthand to canonical forms. |

#### 3. Return the parsed results as a JSON string so that downstream nodes can easily deserialize the data into native Python structures.

| Category | Details |
| --- | --- |
| **Reason** | Maintains consistency with the expected input format of other nodes. |
| **Impact** | Simplifies integration and reduces parsing overhead for consuming functions. |
| **Complexity** | LOW |
| **Method** | Serialize the result dictionary with `json.dumps` before returning it in the `output` field. |


---

## select_optimal_data_source

### Description
Selects the best data source for the provided asset tickers based on coverage, latency, cost, and data quality.

### Implementation Plan

#### 1. Create a source metadata repository that stores coverage, latency, cost, and quality metrics for each data provider.

| Category | Details |
| --- | --- |
| **Reason** | Having up‑to‑date metrics is essential for accurate source ranking. |
| **Impact** | Enables dynamic source selection and reduces reliance on hard‑coded preferences. |
| **Complexity** | MEDIUM |
| **Method** | Implement a JSON or YAML config file that can be updated via an admin UI or scheduled job, and load it into memory at startup. |

#### 2. Implement a scoring function that weights each metric and calculates a composite score for each source.

| Category | Details |
| --- | --- |
| **Reason** | A consistent scoring algorithm allows objective comparison across providers. |
| **Impact** | Guarantees that the chosen source maximizes the desired trade‑offs (e.g., high coverage with acceptable latency). |
| **Complexity** | MEDIUM |
| **Method** | Define weights (e.g., coverage=0.4, latency=0.2, cost=0.2, quality=0.2) and compute `score = w1*coverage + w2*latency + w3*cost + w4*quality`. Normalize metrics to 0‑1 range. |

#### 3. Return the source with the highest score and expose the function as a shim for downstream nodes.

| Category | Details |
| --- | --- |
| **Reason** | The shim must be a thin wrapper that can be called by higher‑level logic without exposing internal details. |
| **Impact** | Provides a single point of truth for data source selection, simplifying maintenance. |
| **Complexity** | LOW |
| **Method** | Sort the sources by score, pick the top, and return its name; handle ties with a deterministic rule. |


---

## fetch_raw_market_data

### Description
Fetch raw market data for specified assets, timeframes, and source, returning the raw data dictionary as a JSON string.

### Implementation Plan

#### 1. Validate the format of `assets`, `timeframes`, and `source` to ensure they are non‑empty strings and follow expected patterns.

| Category | Details |
| --- | --- |
| **Reason** | Prevent malformed requests and downstream failures. |
| **Impact** | Improves data integrity and user feedback before network calls. |
| **Complexity** | LOW |
| **Method** | Use simple regular expressions or string splitting checks; raise informative errors if validation fails. |

#### 2. Construct and execute an HTTP request to the selected data source API, handling query parameters for multiple assets and timeframes and supporting pagination or chunking as required by the source.

| Category | Details |
| --- | --- |
| **Reason** | Actual data retrieval is the core of the shim. |
| **Impact** | Enables integration with external market data providers and ensures scalability for large asset lists. |
| **Complexity** | MEDIUM |
| **Method** | Leverage the `requests` library to build query strings, set appropriate headers, manage authentication, and iterate over paginated responses. |

#### 3. Normalize the API response into a unified dictionary format and serialize it to a JSON string for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output structure simplifies downstream processing. |
| **Impact** | Guarantees that all consuming nodes receive data in the expected schema regardless of source differences. |
| **Complexity** | LOW |
| **Method** | Parse the JSON payload, map source‑specific field names to standard keys (`timestamps`, `price_values`, etc.), and use `json.dumps` to produce the final string. |


---

## clean_and_validate_market_data

### Description
Cleans and validates raw historical market data, ensuring schema compliance, data integrity, and quality flags.

### Implementation Plan

#### 1. Parse the raw_data string into a Python dict and validate against a Pydantic schema to guarantee required fields and correct types.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the data structure is correct before any processing, preventing downstream errors. |
| **Impact** | Provides early error detection and a standardized data shape for subsequent steps. |
| **Complexity** | MEDIUM |
| **Method** | Use json.loads to convert the string to a dict, then instantiate a Pydantic model (e.g., RawMarketData) to perform validation; catch ValidationError to return informative errors. |

#### 2. Perform data integrity checks: verify timestamps are unique and sorted, confirm that asset lists match between assets and price_values, detect and flag missing or NaN values, and identify outliers via z‑score thresholds.

| Category | Details |
| --- | --- |
| **Reason** | Maintains data quality by ensuring logical consistency and spotting anomalous records that could skew analyses. |
| **Impact** | Sets a reliable basis for clean data, reduces risk of model bias, and enables accurate quality scoring. |
| **Complexity** | MEDIUM |
| **Method** | Load data into a pandas DataFrame, use .duplicated(), .isna(), and scipy.stats.zscore for outlier detection; flag issues and set an 'is_clean' boolean accordingly. |

#### 3. Clean the dataset by imputing missing values with forward/backward fill, removing detected outliers, normalizing timestamps to ISO 8601, and returning a cleaned dict with an 'is_clean' flag.

| Category | Details |
| --- | --- |
| **Reason** | Provides a usable, high‑quality dataset ready for downstream analysis or storage. |
| **Impact** | Improves model performance and ensures consistency across datasets from different sources. |
| **Complexity** | LOW |
| **Method** | Apply pandas .ffill()/ .bfill() for imputation, drop rows flagged as outliers, use dateutil.parser to convert timestamps, and serialize the cleaned DataFrame back to a dict before returning. |


---

## calculate_data_quality_score

### Description
Computes a numeric score between 0 and 1 representing the overall quality of cleaned market data based on completeness, consistency, and validity metrics.

### Implementation Plan

#### 1. Validate the JSON input against an expected schema to ensure required fields and types are present.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees that subsequent computations are based on well‑formed data, preventing runtime errors. |
| **Impact** | Reduces failures in downstream analysis modules and improves overall system reliability. |
| **Complexity** | LOW |
| **Method** | Use the jsonschema library to validate the input against a predefined schema describing fields such as assets, timestamps, price_values, and is_clean. |

#### 2. Implement a multi‑metric calculation that aggregates missing‑value ratio, timestamp consistency, price volatility bounds, and duplicate record detection to derive a single score.

| Category | Details |
| --- | --- |
| **Reason** | Captures the key dimensions of data quality necessary for market analysis and trading strategy performance. |
| **Impact** | Provides a single actionable metric that can be used for data quality monitoring, automated alerts, and quality‑based filtering of assets. |
| **Complexity** | HIGH |
| **Method** | Parse the JSON into pandas DataFrame, compute each metric, normalize them to [0,1], weight them appropriately, and sum to produce the final score. |

#### 3. Return the score with clear error handling and logging for debugging.

| Category | Details |
| --- | --- |
| **Reason** | Ensures transparency and traceability of quality assessments and simplifies maintenance. |
| **Impact** | Facilitates troubleshooting and improves developer confidence when integrating the shim into larger pipelines. |
| **Complexity** | MEDIUM |
| **Method** | Wrap the scoring logic in a try/except block, log any exceptions with context, and return NaN or a sentinel value if validation fails. |


---

## format_market_data_output

### Description
Formats cleaned market data into a standardized dictionary for downstream consumption.

### Implementation Plan

#### 1. Parse the input JSON string and validate that it contains the required keys assets, timeframes, timestamps, and price_values.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim receives all necessary data before processing. |
| **Impact** | Prevents downstream failures caused by missing or malformed fields. |
| **Complexity** | LOW |
| **Method** | Use json.loads with try/except and validate with a pydantic model or jsonschema. |

#### 2. Transform the raw lists into the standardized output structure, converting timestamps to ISO 8601 format and ensuring price_values are floats.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees consistent data types for downstream analytics and reporting. |
| **Impact** | Improves data integrity and interoperability with other components. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over the lists, cast to the appropriate types, format timestamps with datetime.isoformat, assemble the output dictionary, then serialize with json.dumps. |

#### 3. Compute record_count and propagate the is_clean flag from the input, then serialize the final dictionary to JSON.

| Category | Details |
| --- | --- |
| **Reason** | Provides quick metrics for quality assessment without extra processing. |
| **Impact** | Enables higher-level nodes to quickly gauge dataset size and cleanliness. |
| **Complexity** | LOW |
| **Method** | Use len() on the timestamps list for record_count, read the is_clean flag, update the dict, and return json.dumps of the dict. |
