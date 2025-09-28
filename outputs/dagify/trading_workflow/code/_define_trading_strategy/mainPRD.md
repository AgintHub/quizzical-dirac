# _define_trading_strategy - Complete PRD Documentation

## Overview
PRDs for nodes in the '_define_trading_strategy' module.

## Table of Contents

- [validate_and_structure_data](#validate_and_structure_data)

- [compute_descriptive_statistics](#compute_descriptive_statistics)

- [generate_technical_indicators](#generate_technical_indicators)

- [analyze_indicator_predictive_power](#analyze_indicator_predictive_power)

- [formulate_entry_rules](#formulate_entry_rules)

- [design_exit_rules](#design_exit_rules)

- [create_position_sizing_rule](#create_position_sizing_rule)

- [create_risk_management_rule](#create_risk_management_rule)

- [filter_tradeable_assets](#filter_tradeable_assets)

- [generate_strategy_name](#generate_strategy_name)



---

## validate_and_structure_data

### Description
Transforms raw string inputs of assets, timestamps, price values, and timeframes into a validated, structured pandas DataFrame and returns it as a CSV string.

### Implementation Plan

#### 1. Parse and validate the input strings to ensure all lists are of equal length and timestamps are ISO 8601 compliant.

| Category | Details |
| --- | --- |
| **Reason** | Input consistency is critical for reliable downstream analytics. |
| **Impact** | Prevents misaligned data rows and reduces runtime errors in later stages. |
| **Complexity** | LOW |
| **Method** | Use Python's `split(',')` to create lists, `dateutil.parser.isoparse` for timestamp validation, and simple length checks. |

#### 2. Construct a pandas DataFrame from the validated lists, sort by timestamp, and serialize it to CSV for easy consumption by subsequent nodes.

| Category | Details |
| --- | --- |
| **Reason** | A structured tabular format is required for statistical analysis and indicator generation. |
| **Impact** | Provides a uniform data contract that all downstream nodes can rely on. |
| **Complexity** | LOW |
| **Method** | Instantiate `pd.DataFrame` with columns `asset`, `timestamp`, `price`, `timeframe`, sort via `df.sort_values('timestamp')`, then convert to CSV with `df.to_csv(index=False)`. |

#### 3. Implement robust error handling and logging to capture parsing or validation failures and provide clear diagnostic messages.

| Category | Details |
| --- | --- |
| **Reason** | Facilitates debugging and ensures that failures are traceable in production. |
| **Impact** | Improves system reliability and developer productivity. |
| **Complexity** | MEDIUM |
| **Method** | Wrap parsing logic in `try/except` blocks, use Python's `logging` module to record errors, and raise custom exceptions with informative messages. |


---

## compute_descriptive_statistics

### Description
Computes descriptive statistics grouped by asset and timeframe from a provided data frame string.

### Implementation Plan

#### 1. Parse the `dataframe` string to a pandas DataFrame, supporting CSV and pickle formats.

| Category | Details |
| --- | --- |
| **Reason** | The input may be a file path or serialized DataFrame; robust parsing ensures correct data ingestion. |
| **Impact** | Provides a consistent DataFrame for downstream statistical computations. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv` if the string ends with `.csv`, otherwise `pandas.read_pickle`; include error handling for unsupported formats. |

#### 2. Group the DataFrame by `asset` and `timeframe` and compute descriptive statistics using `groupby().describe()`.

| Category | Details |
| --- | --- |
| **Reason** | Statistics are required per asset/timeframe for strategy development. |
| **Impact** | Generates a structured summary that can be serialized to JSON and consumed by other nodes. |
| **Complexity** | LOW |
| **Method** | Apply `df.groupby(['asset', 'timeframe']).describe()` and reshape the MultiIndex result into a dictionary mapping. |

#### 3. Serialize the statistics dictionary to a JSON string, ensuring non-serializable types (e.g., numpy types) are converted to native Python types.

| Category | Details |
| --- | --- |
| **Reason** | The shim interface expects a string output; JSON serialization guarantees portability. |
| **Impact** | Output can be easily deserialized by downstream components without data loss. |
| **Complexity** | MEDIUM |
| **Method** | Use `json.dumps` with a custom encoder that casts numpy scalars to Python primitives; wrap the result in a try/except block to handle serialization errors. |


---

## generate_technical_indicators

### Description
Generates a comprehensive set of technical indicators for the provided market data across specified timeframes.

### Implementation Plan

#### 1. Validate and parse input JSON strings into a pandas DataFrame and a list of timeframes.

| Category | Details |
| --- | --- |
| **Reason** | Ensures correct data types and structure before computation. |
| **Impact** | Prevents downstream errors and guarantees accurate indicator calculations. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` to parse the input strings, convert the dataframe via `pandas.read_json`, and validate that required columns (e.g., timestamp, price) and timeframe formats are present. |

#### 2. Compute technical indicators for each specified timeframe using a vectorized approach with pandas‑ta.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality to generate the enriched indicator dataset. |
| **Impact** | Produces the comprehensive dataframe needed for strategy formulation. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over each timeframe, resample the dataframe to the timeframe, apply a predefined set of indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.) via pandas‑ta, and concatenate the results into a single DataFrame. |

#### 3. Serialize the resulting dataframe to a JSON string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | Provides a consistent data format for downstream nodes. |
| **Impact** | Ensures interoperability and easy consumption of indicator data. |
| **Complexity** | LOW |
| **Method** | Use `dataframe.to_json(orient='split')` and embed the string in the output JSON structure. |


---

## analyze_indicator_predictive_power

### Description
Analyzes the predictive power of a set of technical indicators by correlating them with statistical metadata and identifying the most informative indicators for generating trading signals.

### Implementation Plan

#### 1. Calculate the correlation matrix between all technical indicators and the target price returns to identify linear relationships.

| Category | Details |
| --- | --- |
| **Reason** | Linear correlations provide an initial filter for indicators that have direct influence on price movements. |
| **Impact** | Creates a ranking that helps downstream nodes prioritize indicators for rule generation. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas DataFrame correlation functions to compute Pearson coefficients and sort by absolute value. |

#### 2. Train a lightweight machine‑learning model (e.g., RandomForestRegressor) on lagged returns to quantify non‑linear predictive importance of each indicator.

| Category | Details |
| --- | --- |
| **Reason** | Captures complex interactions that simple correlations miss, giving a more accurate importance score. |
| **Impact** | Produces a feature importance list that can be directly used to craft entry/exit rules. |
| **Complexity** | HIGH |
| **Method** | Prepare a training set with future return labels, fit the model using scikit‑learn, extract feature_importances_ and normalize for reporting. |

#### 3. Aggregate correlation and ML importance results into a formatted string summary highlighting the top‑performing indicators.

| Category | Details |
| --- | --- |
| **Reason** | Provides a human‑readable, machine‑processable output that downstream nodes can consume. |
| **Impact** | Ensures consistency and clarity in strategy definition, facilitating automation and debugging. |
| **Complexity** | LOW |
| **Method** | Merge ranked lists, format as JSON or plain text, and return as the 'output' field. |


---

## formulate_entry_rules

### Description
Generate a concise entry rule string for a trading strategy based on the predictive power analysis of technical indicators.

### Implementation Plan

#### 1. Validate and parse the input strings into structured data using JSON and Pandas CSV parsers.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the function can work with the raw string representations provided by upstream nodes. |
| **Impact** | Prevents runtime errors and guarantees that subsequent steps operate on reliable data structures. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` for `signal_results` and `pd.read_csv` with `StringIO` for `indicators_df`. |

#### 2. Select top-performing indicators based on predictive power thresholds and rank them for rule construction.

| Category | Details |
| --- | --- |
| **Reason** | Focuses the entry rule on the most informative signals, improving strategy effectiveness. |
| **Impact** | Results in a more robust and potentially higher‑yielding entry condition. |
| **Complexity** | MEDIUM |
| **Method** | Filter the parsed JSON for metrics > 0.20, then sort by metric descending and store the indicator list. |

#### 3. Assemble the entry rule string by combining selected indicator thresholds using logical operators.

| Category | Details |
| --- | --- |
| **Reason** | Creates the final human‑readable rule that can be interpreted by the trading engine. |
| **Impact** | Provides a reusable rule that can be directly applied within a strategy configuration. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over the ranked indicators, retrieve corresponding columns from the DataFrame, compute simple threshold conditions (e.g., mean or median), and concatenate them into a single string with `AND`/`OR` clauses. |


---

## design_exit_rules

### Description
Generates a textual exit rule specification from indicator data and statistical metadata.

### Implementation Plan

#### 1. Parse the indicator DataFrame and compute threshold‑based exit conditions such as moving‑average crossovers and volatility triggers.

| Category | Details |
| --- | --- |
| **Reason** | Data‑driven exit logic ensures that positions close when technical signals indicate adverse market conditions. |
| **Impact** | Provides robust, evidence‑based exit rules that reduce risk of holding losing positions. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas to read the CSV/JSON, calculate indicators (e.g., SMA, ATR), and translate conditions into a rule string format. |

#### 2. Integrate time‑based exit clauses (e.g., daily close, position age limit) to enforce systematic position duration.

| Category | Details |
| --- | --- |
| **Reason** | Time constraints prevent over‑exposure and align strategy with predefined holding periods. |
| **Impact** | Reduces holding risk and ensures consistent trade lifecycles across assets. |
| **Complexity** | LOW |
| **Method** | Append a simple time condition to the rule string (e.g., `if position_age > 1 day then exit`). |

#### 3. Validate the generated rule string against a predefined DSL or JSON schema to guarantee syntactic correctness before downstream usage.

| Category | Details |
| --- | --- |
| **Reason** | Prevents runtime errors when the strategy engine parses the exit rules. |
| **Impact** | Increases reliability of strategy deployment and speeds up debugging. |
| **Complexity** | MEDIUM |
| **Method** | Implement a lightweight parser or use `jsonschema` to check that the rule string conforms to expected structure. |


---

## create_position_sizing_rule

### Description
Generates a position sizing rule string for a trading strategy based on a specified risk tolerance and chosen sizing method.

### Implementation Plan

#### 1. Validate input parameters: ensure risk_tolerance can be parsed to a float between 0 and 1 and that method is one of the supported strategies.

| Category | Details |
| --- | --- |
| **Reason** | Prevents invalid or nonsensical inputs from propagating through the strategy. |
| **Impact** | Guarantees downstream nodes receive reliable, well‑typed sizing rules, reducing runtime errors. |
| **Complexity** | LOW |
| **Method** | Use Python type hints and runtime checks (e.g., try/except for float conversion, membership test against a predefined set of methods). |

#### 2. Implement the fixed‑fractional sizing logic: compute the allocation as `allocation = risk_tolerance * portfolio_value` and format it into a human‑readable rule string.

| Category | Details |
| --- | --- |
| **Reason** | Fixed‑fractional is the most common method and forms the core use case. |
| **Impact** | Provides traders with a clear, reproducible rule that ties position size directly to risk tolerance. |
| **Complexity** | MEDIUM |
| **Method** | Define a helper function that takes risk_tolerance float and portfolio_value placeholder, then returns a formatted string such as `'Allocate {risk_tolerance*100}% of equity per trade'`. Use f‑strings for readability. |

#### 3. Extend support for additional methods (e.g., fixed_capital, volatility_adjusted) by mapping method identifiers to rule templates and incorporating optional parameters.

| Category | Details |
| --- | --- |
| **Reason** | Allows future growth and customization without altering the core interface. |
| **Impact** | Enables flexible strategy design and easier integration with other nodes that may require different sizing conventions. |
| **Complexity** | HIGH |
| **Method** | Create a dispatch dictionary that maps method names to lambda functions or template strings, and allow the function to accept an optional `parameters` JSON that can be passed into the template rendering. Validate these parameters with Pydantic models. |


---

## create_risk_management_rule

### Description
Creates a risk management rule string based on maximum drawdown, maximum number of assets, and maximum daily loss.

### Implementation Plan

#### 1. Validate and convert input parameters to numeric types and ensure they fall within acceptable ranges.

| Category | Details |
| --- | --- |
| **Reason** | Input validation prevents downstream errors and ensures the rule is logically sound. |
| **Impact** | Produces a reliable risk rule and avoids runtime failures during strategy definition. |
| **Complexity** | LOW |
| **Method** | Parse each string to float or int, then check bounds (e.g., drawdown > 0 and < 1). |

#### 2. Format the risk management rule using a standardized template that includes all parameters.

| Category | Details |
| --- | --- |
| **Reason** | Consistent formatting enables downstream components to parse and apply the rule easily. |
| **Impact** | Ensures interoperability with other nodes and improves maintainability. |
| **Complexity** | LOW |
| **Method** | Use Python f-strings or str.format to inject validated values into a predefined string pattern. |

#### 3. Return the constructed rule string as the shim output.

| Category | Details |
| --- | --- |
| **Reason** | Provides the final artifact for the strategy definition node. |
| **Impact** | Completes the shim's responsibility and allows the calling node to use the rule. |
| **Complexity** | LOW |
| **Method** | Simply return the formatted string from the function. |


---

## filter_tradeable_assets

### Description
Filters a list of asset tickers based on their data quality score, trading volume, and a minimum quality threshold to produce a list of tradeable assets.

### Implementation Plan

#### 1. Parse and validate input strings into structured formats, ensuring that asset tickers, quality scores, and DataFrame rows are correctly aligned.

| Category | Details |
| --- | --- |
| **Reason** | Proper alignment and type correctness are essential to avoid mismatches and runtime errors during filtering. |
| **Impact** | Guarantees that subsequent filtering logic operates on accurate data, preventing incorrect asset inclusion or exclusion. |
| **Complexity** | LOW |
| **Method** | Use Python's csv and pandas libraries to split the assets string, convert quality scores to floats, and load the dataframe string via `pd.read_csv(StringIO(df_str))`. |

#### 2. Apply the minimum quality threshold and volume criteria to identify tradeable assets.

| Category | Details |
| --- | --- |
| **Reason** | The core business rule is to exclude assets that do not meet the required data quality or trading volume. |
| **Impact** | Produces a reliable subset of assets that meet risk and liquidity standards, directly influencing downstream strategy creation. |
| **Complexity** | MEDIUM |
| **Method** | Filter the DataFrame rows where `data_quality_score >= min_quality_threshold` and `volume > MIN_VOLUME`; then intersect the resulting asset list with the original assets list. |

#### 3. Return the filtered asset list as a comma‑separated string.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output format is needed for downstream nodes that expect a string of asset symbols. |
| **Impact** | Ensures compatibility with the rest of the pipeline without additional parsing steps. |
| **Complexity** | LOW |
| **Method** | Convert the filtered pandas Series to a list and join with commas, e.g., `','.join(filtered_assets.tolist())`. |


---

## generate_strategy_name

### Description
Creates a concise, descriptive trading strategy name based on provided entry rules and timeframes.

### Implementation Plan

#### 1. Extract key phrases from the entry rules and assemble them into a base name, ensuring uniqueness by appending a short hash if duplicates occur.

| Category | Details |
| --- | --- |
| **Reason** | A meaningful base name improves strategy identification and reduces ambiguity when multiple strategies share similar rules. |
| **Impact** | Facilitates quick understanding and retrieval of strategy characteristics in downstream processes. |
| **Complexity** | LOW |
| **Method** | Use NLP token extraction (e.g., regex or spaCy) to find nouns/adjectives, concatenate them, and generate a UUID hash if needed. |

#### 2. Normalize and aggregate the timeframes string (e.g., '1h,4h,1d') into a concise suffix and attach it to the base name.

| Category | Details |
| --- | --- |
| **Reason** | Including timeframes in the name conveys the strategy’s temporal coverage and differentiates multi-timeframe approaches. |
| **Impact** | Provides immediate context to users and other system components without requiring deeper inspection. |
| **Complexity** | MEDIUM |
| **Method** | Parse the comma‑separated list, map standard abbreviations (1h → 1H), sort alphabetically, and join with hyphens. |

#### 3. Sanitize the resulting name by removing illegal characters, trimming whitespace, and enforcing a maximum length (e.g., 64 characters).

| Category | Details |
| --- | --- |
| **Reason** | Ensures compatibility with file systems, database keys, and external integrations that may impose naming constraints. |
| **Impact** | Prevents runtime errors and storage issues in downstream components. |
| **Complexity** | LOW |
| **Method** | Apply a regex pattern to filter out non‑alphanumeric characters, collapse multiple spaces, and truncate to the allowed length. |
