# _compute_volatility_features - Complete PRD Documentation

## Overview
PRDs for nodes in the '_compute_volatility_features' module.

## Table of Contents

- [parse_csv_to_dataframe](#parse_csv_to_dataframe)

- [validate_required_columns](#validate_required_columns)

- [compute_log_returns](#compute_log_returns)

- [fit_garch_model](#fit_garch_model)

- [generate_garch_forecasts](#generate_garch_forecasts)

- [calculate_implied_vol_delta](#calculate_implied_vol_delta)

- [align_volatility_series](#align_volatility_series)

- [extract_date_strings](#extract_date_strings)

- [extract_float_list](#extract_float_list)

- [log_volatility_success](#log_volatility_success)

- [handle_volatility_feature_error](#handle_volatility_feature_error)



---

## parse_csv_to_dataframe

### Description
Converts a CSV‑formatted string into a pandas DataFrame with a datetime index and appropriate column dtypes.

### Implementation Plan

#### 1. Parse the CSV string into a pandas DataFrame using `io.StringIO` and `pd.read_csv`.

| Category | Details |
| --- | --- |
| **Reason** | The raw data arrives as a plain text CSV; it must be transformed into a structured tabular format for all downstream analytics. |
| **Impact** | Provides a canonical DataFrame object that other nodes can safely consume without re‑implementing CSV parsing logic. |
| **Complexity** | LOW |
| **Method** | Import `io` and `pandas`; wrap the input string with `io.StringIO`; call `pd.read_csv(StringIO(csv_string))` with default parameters. |

#### 2. Detect and parse the datetime column, setting it as the DataFrame index.

| Category | Details |
| --- | --- |
| **Reason** | Time‑series calculations (log returns, GARCH forecasts, etc.) require a proper datetime index. |
| **Impact** | Ensures chronological ordering and enables date‑based slicing, which is critical for accurate volatility modeling. |
| **Complexity** | MEDIUM |
| **Method** | Inspect the first few columns for date‑like patterns (e.g., using `pd.to_datetime` with `errors='coerce'`); once identified, re‑read CSV with `parse_dates=[col]` and `index_col=col`; fallback to the first column if detection fails. |

#### 3. Coerce numeric columns to appropriate dtypes and validate required fields (`Close`, `ImpliedVol`).

| Category | Details |
| --- | --- |
| **Reason** | Downstream functions assume numeric types; any non‑numeric entries would cause runtime errors. |
| **Impact** | Prevents crashes in later nodes and provides early, clear feedback if the CSV lacks essential data. |
| **Complexity** | MEDIUM |
| **Method** | After loading, apply `pd.to_numeric(..., errors='coerce')` on all non‑datetime columns; use `df.dropna(subset=required_columns, inplace=True)`; if required columns are missing, raise a custom `CSVParseError` with a descriptive message. |


---

## validate_required_columns

### Description
Ensures that a DataFrame string contains all columns required for downstream volatility calculations.

### Implementation Plan

#### 1. Parse the CSV string into a pandas DataFrame and check that each column listed in `required_columns` exists.

| Category | Details |
| --- | --- |
| **Reason** | Subsequent nodes assume these columns are present; missing columns would cause runtime failures. |
| **Impact** | Prevents downstream errors by failing fast with a clear validation message. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(StringIO(dataframe))` to create the DataFrame, split `required_columns` on commas, and verify membership with `set(required_columns).issubset(df.columns)`. Raise a `ValueError` with a detailed message if any are missing. |

#### 2. Return a standardized success string when validation passes.

| Category | Details |
| --- | --- |
| **Reason** | Provides a consistent output contract for the calling node. |
| **Impact** | Allows downstream logic to proceed without additional checks, simplifying the pipeline. |
| **Complexity** | LOW |
| **Method** | If validation succeeds, set `output = "validation_success"` and return it alongside the original inputs in the prescribed JSON structure. |


---

## compute_log_returns

### Description
Computes daily logarithmic returns for a specified price column in a CSV‑encoded DataFrame and returns the augmented DataFrame as a CSV string.

### Implementation Plan

#### 1. Validate that the input CSV can be parsed into a DataFrame and that the specified price column exists.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim operates on correct and complete data, preventing runtime errors in later steps. |
| **Impact** | Prevents crashes due to missing columns or malformed CSV, providing early feedback to the caller. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv` on the input string, then check `price_column` in `df.columns`; raise a clear `ValueError` if validation fails. |

#### 2. Calculate the logarithmic return for each row using the price column.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality required by downstream volatility modeling (e.g., GARCH). |
| **Impact** | Adds a `LogReturn` column that accurately represents daily returns, enabling correct statistical calculations later in the pipeline. |
| **Complexity** | MEDIUM |
| **Method** | Create a Series `prices = df[price_column].astype(float)`, compute `log_returns = np.log(prices / prices.shift(1))`, assign to `df['LogReturn']`; handle division‑by‑zero and initial NaN by optionally filling with 0 or leaving as NaN. |

#### 3. Serialize the augmented DataFrame back to a CSV string and populate the output fields.

| Category | Details |
| --- | --- |
| **Reason** | Provides the next node with data in the expected format (CSV string) while also echoing the original inputs for traceability. |
| **Impact** | Ensures seamless integration with downstream nodes that expect CSV inputs, maintaining the data flow continuity. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` to obtain the CSV string, assign it to the `output` field, and return a dictionary containing `output`, `dataframe`, and `price_column`. |


---

## fit_garch_model

### Description
Fits a GARCH(1,1) model to a series of log returns and returns a serialized representation of the fitted model.

### Implementation Plan

#### 1. Validate and parse the returns_series input into a numeric pandas Series.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim receives clean, numeric data and fails early with informative errors if the format is wrong. |
| **Impact** | Prevents downstream model‑fitting crashes and guarantees consistent input shape for the GARCH algorithm. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv on the string, coerce to float, drop NaNs, and raise ValueError with a clear message if parsing fails. |

#### 2. Fit a GARCH(1,1) model to the parsed returns using the `arch` library.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality of the shim – producing a statistical model that can later generate volatility forecasts. |
| **Impact** | Provides a reliable fitted model object that downstream nodes can use for one‑step‑ahead volatility predictions. |
| **Complexity** | MEDIUM |
| **Method** | Import `arch.univariate.ArchModel`, instantiate with mean='Zero', vol='GARCH', p=1, q=1, fit with `disp='off'`, and capture convergence warnings; fallback to default parameters if fitting fails. |

#### 3. Serialize the fitted model to a base64‑encoded string for the output field.

| Category | Details |
| --- | --- |
| **Reason** | The node's output schema requires a string, so the binary model must be safely encoded for transport between nodes. |
| **Impact** | Allows the model to be stored, logged, or passed to subsequent nodes without loss of fidelity. |
| **Complexity** | MEDIUM |
| **Method** | Use `pickle.dumps` on the fitted model, then `base64.b64encode`, and decode to UTF‑8; include a corresponding deserialization snippet in documentation. |


---

## generate_garch_forecasts

### Description
Generates one‑step‑ahead volatility forecasts from a serialized fitted GARCH(1,1) model starting at a specified date.

### Implementation Plan

#### 1. Deserialize the `fitted_model` string into a usable GARCH model object.

| Category | Details |
| --- | --- |
| **Reason** | The model is passed between nodes as a string to avoid cross‑process object sharing. |
| **Impact** | Enables downstream forecasting logic to operate on an actual statistical model. |
| **Complexity** | MEDIUM |
| **Method** | Use base64‑decoded pickle (or joblib) to reconstruct the model, then verify its type and required methods. |

#### 2. Generate one‑step‑ahead volatility forecasts beginning at `start_date` for the required horizon.

| Category | Details |
| --- | --- |
| **Reason** | The core business need is to produce forward volatility estimates for each trading day after the start date. |
| **Impact** | Provides the primary numeric output consumed by subsequent volatility‑feature calculations. |
| **Complexity** | MEDIUM |
| **Method** | Call the model's `forecast` method (e.g., `model.forecast(horizon=n)`) and map the resulting array to a pandas DatetimeIndex starting from `start_date`. |

#### 3. Serialize the forecast series back to a string for the node output.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect a plain‑text representation to remain language‑agnostic. |
| **Impact** | Ensures seamless data flow through the pipeline without requiring binary objects. |
| **Complexity** | LOW |
| **Method** | Convert the forecast numpy array to a Python list of floats and use `json.dumps` (or CSV‑style string) to produce the `output` field. |


---

## calculate_implied_vol_delta

### Description
This shim calculates the change in implied volatility over a specified number of lag days.

### Implementation Plan

#### 1. Implement the implied volatility delta calculation.

| Category | Details |
| --- | --- |
| **Reason** | To calculate the change in implied volatility which is feature used in the volatility forecast. |
| **Impact** | Provides a key input feature to the volatility forecasting model, influencing forecast accuracy. |
| **Complexity** | MEDIUM |
| **Method** | Use a sliding window approach or vectorized operations on the Pandas Series to calculate the difference between the current ImpliedVol and the ImpliedVol 'lag_days' periods prior. |

#### 2. Handle missing values within the ImpliedVol series.

| Category | Details |
| --- | --- |
| **Reason** | To ensure that missing data points do not crash the function or return incorrect results. |
| **Impact** | Prevents errors and ensures data integrity in the volatility delta calculation. |
| **Complexity** | LOW |
| **Method** | Implement a check for NaN values in the input series and handle them using forward fill, backward fill, or interpolation before calculation, depending on acceptable data loss. |

#### 3. Ensure type consistency and input validation.

| Category | Details |
| --- | --- |
| **Reason** | To prevent type errors from string encoded numbers, the inputs to this function MUST be validated. |
| **Impact** | Reduces errors and ensures that the function behaves predictably based on valid inputs. |
| **Complexity** | LOW |
| **Method** | Add type checking where the string based inputs are coerced to numerical datatypes before use in the calculation. The lag_days parameter must be validated to be an integer. |


---

## align_volatility_series

### Description
Aligns the GARCH volatility forecasts with the 5‑day implied‑volatility delta series on a common date index, discarding any mismatched or missing entries.

### Implementation Plan

#### 1. Perform an inner join of the two input series on their datetime index to produce a DataFrame with matching dates only.

| Category | Details |
| --- | --- |
| **Reason** | The downstream volatility feature calculations require that each forecast has a corresponding implied‑volatility delta; misaligned dates would corrupt the model input. |
| **Impact** | Ensures a clean, one‑to‑one mapping between GARCH forecasts and implied‑volatility deltas, preventing NaNs and index mismatches in later steps. |
| **Complexity** | MEDIUM |
| **Method** | Convert both string inputs to pandas Series (or DataFrames) with a DateTimeIndex, then use `pd.concat([garch_series, delta_series], axis=1, join='inner')` followed by `dropna()` to eliminate any residual missing values. |

#### 2. Validate input formats and lengths before alignment, raising explicit errors for non‑numeric data or mismatched types.

| Category | Details |
| --- | --- |
| **Reason** | Early validation guards against silent failures caused by malformed inputs, making debugging faster and more reliable. |
| **Impact** | Provides clear feedback to upstream nodes or users, reducing runtime exceptions later in the pipeline. |
| **Complexity** | LOW |
| **Method** | Check that both inputs are parsable into numeric pandas Series, confirm they contain a DateTimeIndex, and compare lengths; if checks fail, raise a `ValueError` with a descriptive message. |

#### 3. Serialize the aligned DataFrame and each individual series back to strings for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | The node contract specifies string outputs; downstream nodes expect CSV or JSON strings they can readily parse. |
| **Impact** | Delivers data in the exact format required by the `ComputeVolatilityFeaturesOutput` builder, enabling seamless integration. |
| **Complexity** | MEDIUM |
| **Method** | After alignment, use `aligned_df.to_csv()` (including the index) for the combined output, and `aligned_df['GARCHForecast'].to_json()` / `to_csv()` and `aligned_df['ImpliedVolDelta'].to_json()` / `to_csv()` for the individual series, assigning the results to the respective output fields. |


---

## extract_date_strings

### Description
Extracts a list of ISO‑format date strings from a pandas DatetimeIndex supplied as a string representation.

### Implementation Plan

#### 1. Validate and safely parse the `datetime_index` string into a pandas DatetimeIndex object.

| Category | Details |
| --- | --- |
| **Reason** | The input may be malformed, empty, or not represent a DatetimeIndex, which would cause runtime errors downstream. |
| **Impact** | Prevents crashes and provides clear error messages, improving robustness of the pipeline. |
| **Complexity** | MEDIUM |
| **Method** | Use `ast.literal_eval` or `pd.read_json` to deserialize the string, then wrap with `pd.DatetimeIndex`; catch `ValueError` and raise a custom exception with context. |

#### 2. Convert each timestamp in the parsed DatetimeIndex to an ISO‑8601 string.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect dates in a standardized string format for consistency across datasets. |
| **Impact** | Ensures uniform date representation, enabling correct alignment of time‑series data. |
| **Complexity** | LOW |
| **Method** | Call `datetime_index.strftime('%Y-%m-%d')` (or `%Y-%m-%dT%H:%M:%S%z` if time components are needed) and collect the results into a Python list. |

#### 3. Return the list of date strings as the `output` field while preserving the original `datetime_index` input for logging/debugging.

| Category | Details |
| --- | --- |
| **Reason** | The shim’s contract requires both the derived list and the raw input to be part of the output structure. |
| **Impact** | Facilitates downstream tracing and debugging without needing to recompute the parsing step. |
| **Complexity** | LOW |
| **Method** | Construct and return a dictionary `{ "output": date_list, "datetime_index": original_string }` that conforms to the defined output schema. |


---

## extract_float_list

### Description
Extracts a list of float values from a string‑identified series for downstream volatility calculations.

### Implementation Plan

#### 1. Validate that the `series` string corresponds to an existing numeric column in the aligned DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Pre‑empt runtime errors caused by misspelled or missing column names. |
| **Impact** | Ensures the shim fails fast with a clear error, preventing downstream propagation of invalid data. |
| **Complexity** | LOW |
| **Method** | Check column existence using `if series not in df.columns: raise ValueError`; optionally expose a whitelist of allowed series. |

#### 2. Convert the selected column to a flat Python list of floats, handling NaN values appropriately.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect a clean `List[float]` without pandas‑specific types or missing values. |
| **Impact** | Provides consistent numeric input for GARCH forecast extraction and implied‑vol delta calculations. |
| **Complexity** | MEDIUM |
| **Method** | Use `df[series].astype(float).fillna(method='ffill').tolist()` or similar, with configurable NaN handling (drop, fill, or error). |

#### 3. Return the extracted list together with the original series identifier in a deterministic order.

| Category | Details |
| --- | --- |
| **Reason** | The calling node aligns multiple series by index; preserving order guarantees correct pairing of forecasts and deltas. |
| **Impact** | Maintains data integrity across the pipeline, avoiding misaligned outputs. |
| **Complexity** | LOW |
| **Method** | Wrap the list in the response model, ensuring the order matches `df.index` after any alignment steps. |


---

## log_volatility_success

### Description
Logs a message indicating successful volatility feature generation and reports the number of processed dates.

### Implementation Plan

#### 1. Emit a structured log entry containing the node name, a success flag, and the numeric count of dates.

| Category | Details |
| --- | --- |
| **Reason** | Downstream monitoring and audit trails need a deterministic record that the volatility computation completed without error. |
| **Impact** | Enables automated health‑checks, alerting, and traceability in the pipeline execution logs. |
| **Complexity** | LOW |
| **Method** | Use Python's built‑in logging module (e.g., logging.info) with a JSON‑serializable dict; format the count as an integer and then cast to string for the returned field. |

#### 2. Validate and coerce the input `num_dates` to a string while preserving numeric semantics.

| Category | Details |
| --- | --- |
| **Reason** | The surrounding workflow expects a string type for consistency with other shim outputs, but the caller supplies an integer. |
| **Impact** | Prevents type‑mismatch errors in downstream nodes that deserialize shim outputs. |
| **Complexity** | LOW |
| **Method** | Apply `str(num_dates)` conversion; raise a ValueError with a clear message if the input is not an integer. |

#### 3. Make the shim side‑effect‑free aside from logging, returning only the formatted strings.

| Category | Details |
| --- | --- |
| **Reason** | Shims should not alter external state beyond observable logs to keep the data pipeline deterministic and testable. |
| **Impact** | Facilitates unit testing and ensures that repeated executions produce identical outputs given the same input. |
| **Complexity** | MEDIUM |
| **Method** | Encapsulate logging in a helper function; mock this helper in tests to verify that the log call is made without emitting real log records during test runs. |


---

## handle_volatility_feature_error

### Description
Handles errors that occur while computing volatility features by logging detailed context information and raising a custom exception.

### Implementation Plan

#### 1. Log the received error and execution context using the standard logging framework.

| Category | Details |
| --- | --- |
| **Reason** | Visibility into failures is essential for debugging and operational monitoring. |
| **Impact** | Provides a searchable audit trail that accelerates root‑cause analysis and reduces mean‑time‑to‑resolution. |
| **Complexity** | LOW |
| **Method** | Import Python's `logging` module, configure a logger for the node, and emit a structured log message that includes `str(error)` and a JSON‑serialized version of `context`. |

#### 2. Raise a dedicated `VolatilityFeatureError` exception that encapsulates the original error and context.

| Category | Details |
| --- | --- |
| **Reason** | A domain‑specific exception enables upstream nodes to differentiate volatility‑feature failures from generic errors. |
| **Impact** | Allows downstream workflows to catch and handle this specific failure mode, preserving pipeline stability. |
| **Complexity** | MEDIUM |
| **Method** | Define a subclass of `Exception` named `VolatilityFeatureError` with attributes `original_error` and `context`; instantiate it with the captured values and raise it after logging. |

#### 3. Serialize the `context` dictionary to a JSON string before placing it in the output structure.

| Category | Details |
| --- | --- |
| **Reason** | The shim's output schema expects string values, but callers may need the full context for further processing. |
| **Impact** | Ensures downstream nodes receive a portable, parsable representation of the context without type mismatches. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps(context)` to convert the dict to a string and assign it to the `context` output field; similarly convert the error object to `str(error)` for the `error` field. |
