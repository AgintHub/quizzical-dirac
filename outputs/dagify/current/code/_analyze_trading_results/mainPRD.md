# _analyze_trading_results - Complete PRD Documentation

## Overview
PRDs for nodes in the '_analyze_trading_results' module.

## Table of Contents

- [deserialize_monitoring_snapshot](#deserialize_monitoring_snapshot)

- [compute_total_trades](#compute_total_trades)

- [calculate_win_rate](#calculate_win_rate)

- [calculate_average_return_per_trade](#calculate_average_return_per_trade)

- [calculate_max_drawdown](#calculate_max_drawdown)

- [calculate_sharpe_ratio](#calculate_sharpe_ratio)

- [generate_improvement_suggestions](#generate_improvement_suggestions)

- [map_suggestions_to_actions](#map_suggestions_to_actions)

- [assess_statistical_significance](#assess_statistical_significance)

- [validate_output_schema](#validate_output_schema)



---

## deserialize_monitoring_snapshot

### Description
Deserializes a JSON string representing a monitoring snapshot into a Python dictionary for further processing.

### Implementation Plan

#### 1. Safely parse the input JSON string into a dictionary, catching and logging any parsing errors.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the shim can handle malformed inputs without crashing the workflow. |
| **Impact** | Provides reliable data ingestion for downstream analysis nodes. |
| **Complexity** | LOW |
| **Method** | Use Python's json.loads inside a try-except block; log exceptions and return an empty dict if parsing fails. |

#### 2. Validate the parsed dictionary against the expected schema (required fields and types) to guarantee data integrity.

| Category | Details |
| --- | --- |
| **Reason** | Prevents downstream nodes from failing due to missing or incorrectly typed data. |
| **Impact** | Improves robustness and debuggability of the trading analysis pipeline. |
| **Complexity** | MEDIUM |
| **Method** | Define a Pydantic model or JSON Schema matching the expected snapshot structure and run validation on the parsed dict. |

#### 3. Return the validated dictionary as a JSON string to preserve the output type expected by the workflow.

| Category | Details |
| --- | --- |
| **Reason** | Maintains consistency with the node's defined output type (STR). |
| **Impact** | Ensures seamless integration with subsequent nodes that consume this output. |
| **Complexity** | LOW |
| **Method** | Serialize the validated dict with json.dumps before assigning it to the output field. |


---

## compute_total_trades

### Description
Computes the total number of trades for a monitoring period, using an optional snapshot total or falling back to the sum of winning and losing trades.

### Implementation Plan

#### 1. Parse the snapshot_total string into an integer and validate its positivity; if parsing fails or the value is non‑positive, compute total_trades by adding winning_trades and losing_trades.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the function can work with both pre‑computed snapshot data and raw win/loss counts. |
| **Impact** | Provides a reliable total_trades count regardless of input format, preventing downstream division-by-zero or negative trade count errors. |
| **Complexity** | LOW |
| **Method** | Use Python's int() conversion with exception handling; apply a simple >0 check; fall back to summation of provided counts. |

#### 2. Return the computed total_trades as a primitive INT and preserve the original snapshot_total string in the output for traceability.

| Category | Details |
| --- | --- |
| **Reason** | Maintains consistency with the defined output schema and enables debugging by keeping the raw input. |
| **Impact** | Allows downstream nodes to verify that the shim used the correct source for total trade calculation. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary with keys 'output' and 'snapshot_total', then return it. |

#### 3. Add unit tests covering scenarios where snapshot_total is valid, missing, invalid, or zero, and where winning_trades or losing_trades are zero.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees robustness and catches regressions during future implementation. |
| **Impact** | Increases confidence in the shim's correctness and aids continuous integration pipelines. |
| **Complexity** | MEDIUM |
| **Method** | Create pytest functions that call compute_total_trades with various inputs and assert expected outputs. |


---

## calculate_win_rate

### Description
Calculates the win rate as the ratio of winning trades to total trades, returning a float between 0 and 1.

### Implementation Plan

#### 1. Validate and convert input strings to integers, ensuring numeric values.

| Category | Details |
| --- | --- |
| **Reason** | Inputs are strings and must be parsed to perform numeric calculations. |
| **Impact** | Prevents type errors during computation and allows graceful handling of malformed inputs. |
| **Complexity** | LOW |
| **Method** | Use `int()` conversion inside a try/except block; on failure, log an error and return a default win rate of 0.0. |

#### 2. Guard against division by zero by checking if total_trades > 0 before computing the win rate.

| Category | Details |
| --- | --- |
| **Reason** | Avoids runtime errors and undefined behavior. |
| **Impact** | Ensures the function returns a sensible result (0.0) when no trades were executed. |
| **Complexity** | LOW |
| **Method** | If total_trades == 0, set output to 0.0; otherwise compute `winning_trades / total_trades`. |

#### 3. Return the computed win rate as a float and format the output according to the defined schema.

| Category | Details |
| --- | --- |
| **Reason** | The node contract specifies a float output. |
| **Impact** | Guarantees compatibility with downstream nodes that expect a float win rate. |
| **Complexity** | LOW |
| **Method** | Return the value directly, ensuring it matches the `FLOAT` type in the schema. |


---

## calculate_average_return_per_trade

### Description
Calculates the average return per trade by processing snapshot data and total trade count.

### Implementation Plan

#### 1. Validate that snapshot_data contains a numeric list of trade returns and that total_trades is a positive integer.

| Category | Details |
| --- | --- |
| **Reason** | Prevent division-by-zero errors and ensure data integrity. |
| **Impact** | Improves reliability of the shim and reduces runtime errors. |
| **Complexity** | LOW |
| **Method** | Use isinstance checks and simple length validations before proceeding with calculations. |

#### 2. Compute the average return per trade by summing the returns in snapshot_data and dividing by total_trades; if snapshot_average is provided, use it instead.

| Category | Details |
| --- | --- |
| **Reason** | Provides the core metric needed for performance analysis. |
| **Impact** | Yields the accurate average return per trade for downstream nodes. |
| **Complexity** | LOW |
| **Method** | Implement with Python's sum() function and a straightforward division, with a conditional branch for the snapshot_average fallback. |

#### 3. Gracefully handle edge cases where snapshot_data is empty or total_trades is zero by returning 0.0 and logging a warning.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the function does not crash on anomalous inputs. |
| **Impact** | Maintains system stability and provides clear diagnostics. |
| **Complexity** | MEDIUM |
| **Method** | Include a try-except block or pre-checks that return 0.0 and emit a warning via the logging module. |


---

## calculate_max_drawdown

### Description
Computes the maximum percentage drop from peak to trough of an equity curve.

### Implementation Plan

#### 1. Parse `equity_curve` into a numeric list, handling both CSV and JSON formats.

| Category | Details |
| --- | --- |
| **Reason** | The function must interpret the input regardless of its textual representation. |
| **Impact** | Ensures robustness to different data serialization methods used by upstream nodes. |
| **Complexity** | LOW |
| **Method** | Use Python's `json.loads` for JSON arrays; if that fails, split the string by commas, strip whitespace, and convert each element to `float`. |

#### 2. Compute the running maximum of the equity curve and calculate drawdowns as `(peak - current) / peak` for each point, then return the maximum drawdown value.

| Category | Details |
| --- | --- |
| **Reason** | This is the core mathematical operation needed to assess risk. |
| **Impact** | Provides an accurate, industry‑standard measure of portfolio risk over the period. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over the numeric list while maintaining a `max_so_far` variable; at each step compute `drawdown = (max_so_far - value) / max_so_far`; keep track of the largest drawdown. |

#### 3. Validate that the computed drawdown is a non‑negative float and optionally compare it against the provided `snapshot_drawdown`, returning the larger of the two if the snapshot value is supplied.

| Category | Details |
| --- | --- |
| **Reason** | Allows the function to serve as both a validator and a fallback when an existing drawdown is present. |
| **Impact** | Guarantees consistency between historical and computed metrics, preventing downstream logic errors. |
| **Complexity** | LOW |
| **Method** | Convert `snapshot_drawdown` to float if non‑empty; use `max(computed_drawdown, snapshot_drawdown)`; raise a ValueError if any result is not a float or is negative. |


---

## calculate_sharpe_ratio

### Description
Computes the Sharpe ratio for a trading strategy using the provided snapshot and returns data.

### Implementation Plan

#### 1. Validate and parse input strings into JSON objects, ensuring required fields exist.

| Category | Details |
| --- | --- |
| **Reason** | Input validation prevents malformed data from propagating to the calculation stage. |
| **Impact** | Improves reliability and reduces runtime errors during Sharpe ratio computation. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` within a try/except block; check for expected keys such as 'returns' and 'risk_free_rate' and raise informative errors if missing. |

#### 2. Compute the mean return and standard deviation of the return series, subtract the risk‑free rate, and divide to obtain the Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | This is the core statistical calculation required for the metric. |
| **Impact** | Provides the quantitative performance measure used in subsequent analysis nodes. |
| **Complexity** | MEDIUM |
| **Method** | Leverage NumPy or Pandas to calculate `np.mean(returns)` and `np.std(returns, ddof=1)`, then compute `(mean - risk_free_rate) / std`. |

#### 3. Handle edge cases such as zero volatility, missing or NaN values, and return NaN or a descriptive error if calculation is invalid.

| Category | Details |
| --- | --- |
| **Reason** | Robustness against edge cases ensures the node does not silently produce incorrect results. |
| **Impact** | Maintains system integrity and provides clear feedback to downstream components. |
| **Complexity** | LOW |
| **Method** | Check if standard deviation equals zero or if any required field is None; if so, return `float('nan')` or raise a ValueError with a message indicating the specific issue. |


---

## generate_improvement_suggestions

### Description
Generate a concise set of improvement suggestions based on win rate, maximum drawdown, and Sharpe ratio.

### Implementation Plan

#### 1. Define performance thresholds for win rate, max drawdown, and Sharpe ratio to classify strategy health.

| Category | Details |
| --- | --- |
| **Reason** | Thresholds provide a decision framework for generating relevant suggestions. |
| **Impact** | Ensures the suggestions are tailored to actual performance gaps. |
| **Complexity** | LOW |
| **Method** | Implement simple conditional checks against hardcoded threshold values. |

#### 2. Map each performance category to a set of templated improvement suggestions using a lookup dictionary.

| Category | Details |
| --- | --- |
| **Reason** | Allows systematic translation of categories into actionable recommendations. |
| **Impact** | Produces consistent, high‑quality suggestions without manual drafting. |
| **Complexity** | MEDIUM |
| **Method** | Create a dictionary where keys are category identifiers and values are formatted strings; lookup based on evaluated thresholds. |

#### 3. Format the final suggestion list as a single comma‑separated string and return it alongside the input parameters.

| Category | Details |
| --- | --- |
| **Reason** | Matches the expected output structure and simplifies downstream parsing. |
| **Impact** | Provides a uniform API response for consuming nodes. |
| **Complexity** | LOW |
| **Method** | Use string.join on the list of suggestions and return the resulting string. |


---

## map_suggestions_to_actions

### Description
Transforms a comma‑separated string of improvement suggestions into a string of concrete, implementable action items.

### Implementation Plan

#### 1. Validate the suggestions input to ensure it is non‑empty and contains at least one suggestion.

| Category | Details |
| --- | --- |
| **Reason** | Prevents downstream errors and unnecessary API calls when input is malformed. |
| **Impact** | Improves reliability and reduces latency by catching obvious issues early. |
| **Complexity** | LOW |
| **Method** | Use simple string checks (e.g., strip() and split()) and raise a descriptive exception if validation fails. |

#### 2. Invoke a language‑model API to translate each suggestion into a concrete action item.

| Category | Details |
| --- | --- |
| **Reason** | The conversion from abstract suggestions to actionable steps requires natural language understanding beyond simple rule‑based logic. |
| **Impact** | Provides accurate, context‑aware action items that align with domain knowledge, enabling automated execution. |
| **Complexity** | MEDIUM |
| **Method** | Call OpenAI’s text‑generation endpoint with a prompt that includes the suggestions and asks for bullet‑pointed actions. Parse the model’s output into the required string format. |

#### 3. Format the final output as a single string with each action on its own line prefixed by a dash.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output structure simplifies downstream parsing by other components. |
| **Impact** | Ensures compatibility with downstream nodes that consume the action items string. |
| **Complexity** | LOW |
| **Method** | Join the list of actions with newline characters and prepend each with "- ". |


---

## assess_statistical_significance

### Description
Determines if the current trading win rate is statistically significant relative to historical performance.

### Implementation Plan

#### 1. Parse and validate the `historical_data` JSON to extract a list of historical win rates, ensuring numeric consistency and handling missing or malformed entries.

| Category | Details |
| --- | --- |
| **Reason** | Accurate statistical analysis requires clean, numerical historical data. |
| **Impact** | Prevents runtime errors and ensures reliable significance testing. |
| **Complexity** | LOW |
| **Method** | Use Python's `json` module to parse and `pydantic` or type hints to enforce numeric types; replace or remove non-numeric entries. |

#### 2. Perform a one‑sample t‑test comparing the observed win rate to the historical mean using a pre‑defined alpha level (e.g., 0.05).

| Category | Details |
| --- | --- |
| **Reason** | The t‑test is a standard approach to assess whether a single observation deviates significantly from a population mean. |
| **Impact** | Provides a statistically valid boolean output reflecting significant change. |
| **Complexity** | MEDIUM |
| **Method** | Leverage `scipy.stats.ttest_1samp`; compute t-statistic and p-value, return `true` if p < alpha. |

#### 3. Handle edge cases such as insufficient historical data (less than 2 observations) by defaulting to `false` and logging a warning.

| Category | Details |
| --- | --- |
| **Reason** | Statistical tests require a minimum sample size; otherwise the result is unreliable. |
| **Impact** | Ensures the function behaves predictably under low‑data scenarios and informs users of data limitations. |
| **Complexity** | LOW |
| **Method** | Check historical list length before testing; if < 2, set `output = False` and emit a warning via Python's `warnings` module. |


---

## validate_output_schema

### Description
Validates that the provided output data string conforms to the expected schema for the node and raises an error if validation fails.

### Implementation Plan

#### 1. Parse the `output_data` JSON string into a Python dictionary before validation.

| Category | Details |
| --- | --- |
| **Reason** | Pydantic requires a dict to perform schema validation. |
| **Impact** | Ensures the input is in the correct format for downstream validation steps. |
| **Complexity** | LOW |
| **Method** | Use `json.loads(output_data)` to convert the string into a dict, handling `JSONDecodeError` to provide clear feedback. |

#### 2. Validate the parsed dictionary against the appropriate Pydantic model for the node.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees that the output conforms to the expected types, field names, and constraints defined by the schema. |
| **Impact** | Prevents propagation of malformed data downstream, improving reliability and maintainability. |
| **Complexity** | LOW |
| **Method** | Instantiate the node's Pydantic model (e.g., `AnalyzeTradingResultsOutput`) with the parsed dict and catch `pydantic.ValidationError` to surface validation errors. |

#### 3. Return a clear success message or raise a custom validation error with detailed context.

| Category | Details |
| --- | --- |
| **Reason** | Provides developers with actionable information when validation fails. |
| **Impact** | Facilitates debugging and ensures consistent error handling across the system. |
| **Complexity** | LOW |
| **Method** | If validation succeeds, return `"Validation successful"`; otherwise raise a custom `ValueError` containing the validation error details. |
