# _monitor_trading_performance - Complete PRD Documentation

## Overview
PRDs for nodes in the '_monitor_trading_performance' module.

## Table of Contents

- [initialize_monitoring_state](#initialize_monitoring_state)

- [load_performance_thresholds](#load_performance_thresholds)

- [filter_successful_trades](#filter_successful_trades)

- [update_position_map](#update_position_map)

- [calculate_trade_pnl](#calculate_trade_pnl)

- [update_equity_curve](#update_equity_curve)

- [calculate_performance_metrics](#calculate_performance_metrics)

- [evaluate_performance_stability](#evaluate_performance_stability)

- [generate_recommended_adjustments](#generate_recommended_adjustments)

- [check_alert_conditions](#check_alert_conditions)

- [get_current_iso_timestamp](#get_current_iso_timestamp)



---

## initialize_monitoring_state

### Description
Initializes in-memory monitoring state for tracking positions, closed trades, and equity curve.

### Implementation Plan

#### 1. Create an empty monitoring state dictionary with keys `position_map`, `closed_trades`, and `equity_curve`.

| Category | Details |
| --- | --- |
| **Reason** | Provides the foundational data structures required by downstream monitoring functions. |
| **Impact** | Ensures that the monitoring pipeline has a consistent initial state and prevents key‑errors during trade processing. |
| **Complexity** | LOW |
| **Method** | Return `{"position_map": {}, "closed_trades": [], "equity_curve": []}`. |

#### 2. Optionally load an existing state from disk or a cache if available to support persistence across restarts.

| Category | Details |
| --- | --- |
| **Reason** | Allows the monitoring system to resume from the last known state without loss of historical data. |
| **Impact** | Improves reliability and continuity in long‑running trading systems. |
| **Complexity** | MEDIUM |
| **Method** | Check for a serialized state file (e.g., JSON) before initializing; if present, deserialize and validate the structure. |

#### 3. Validate that the state dictionary contains all required keys and that each value is of the expected type.

| Category | Details |
| --- | --- |
| **Reason** | Prevents subtle bugs caused by corrupted or malformed state structures. |
| **Impact** | Increases robustness and aids debugging by failing fast if the state is malformed. |
| **Complexity** | LOW |
| **Method** | Use assertions or type checks (e.g., `assert isinstance(state['position_map'], dict)`) before returning the state. |


---

## load_performance_thresholds

### Description
Loads and returns the performance threshold configuration as a JSON string.

### Implementation Plan

#### 1. Read thresholds from a configuration file located in a predefined directory.

| Category | Details |
| --- | --- |
| **Reason** | The node requires access to the thresholds that guide performance evaluation. |
| **Impact** | Provides the core data needed for monitoring logic to function. |
| **Complexity** | LOW |
| **Method** | Use the built-in `open()` function with a path defined by an environment variable or default path, then read the entire file contents. |

#### 2. Validate the loaded JSON against a predefined schema.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the thresholds are complete and correctly typed before being used by downstream logic. |
| **Impact** | Prevents runtime errors caused by malformed configurations and aids debugging. |
| **Complexity** | MEDIUM |
| **Method** | Load the JSON into a dictionary and validate it using Pydantic models or jsonschema, raising a descriptive error if validation fails. |

#### 3. Cache the thresholds in memory to avoid repeated disk I/O.

| Category | Details |
| --- | --- |
| **Reason** | The function may be invoked frequently; caching improves performance. |
| **Impact** | Reduces latency for subsequent calls and lowers system load. |
| **Complexity** | LOW |
| **Method** | Apply `functools.lru_cache` to the loader function or store the result in a module-level variable that is refreshed only when the file changes. |


---

## filter_successful_trades

### Description
Filters successful trades from a batch of executed trades and returns them as a JSON string.

### Implementation Plan

#### 1. Validate that all input JSON arrays are non-empty and of equal length before processing.

| Category | Details |
| --- | --- |
| **Reason** | Ensures data consistency and prevents misalignment of trade attributes. |
| **Impact** | Prevents runtime errors and incorrect trade mapping. |
| **Complexity** | LOW |
| **Method** | Parse each JSON string into a Python list using `json.loads()` and compare their lengths; raise `ValueError` if mismatched. |

#### 2. Iterate through the arrays using a single index loop or list comprehension to filter trades where the corresponding status is `true`.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality to isolate successful trades. |
| **Impact** | Produces a list of dictionaries with trade details that are ready for downstream consumption. |
| **Complexity** | LOW |
| **Method** | Use a list comprehension that zips all arrays and selects elements with `status == True`. |

#### 3. Serialize the filtered list of trade dictionaries back into a JSON string for the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The output contract expects a string representation. |
| **Impact** | Provides a standard, machine‑readable format that can be parsed by subsequent nodes. |
| **Complexity** | LOW |
| **Method** | Apply `json.dumps()` to the filtered list and return it as the `output` value. |


---

## update_position_map

### Description
Updates the position map with a new trade, detects closures, and returns details about the update.

### Implementation Plan

#### 1. Validate and normalize input arguments, converting price and quantity to float and ensuring side is either 'buy' or 'sell'.

| Category | Details |
| --- | --- |
| **Reason** | Correct data types are essential for arithmetic and comparison operations during position updates. |
| **Impact** | Prevents runtime errors and ensures accurate position tracking. |
| **Complexity** | LOW |
| **Method** | Use Python's `float()` for conversion and a simple set check for side; raise `ValueError` on failure. |

#### 2. Implement position update logic: add quantity for 'buy', subtract for 'sell'; detect when the cumulative quantity for an instrument reaches zero to flag a closed position.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality of maintaining an accurate ledger of open positions. |
| **Impact** | Provides the basis for calculating P&L and updating equity curves downstream. |
| **Complexity** | MEDIUM |
| **Method** | Maintain `position_map` as a dict of `{instrument: {'side': str, 'quantity': float, 'entry_price': float}}`; update or close entries accordingly and return a structured result. |

#### 3. Return a comprehensive result dictionary with flags indicating closure, the entry price, original side, and closed quantity for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | Standardizes the output format so other nodes can reliably parse the update outcome. |
| **Impact** | Enables consistent downstream processing and simplifies debugging. |
| **Complexity** | LOW |
| **Method** | Build a `dict` with the required keys and serialize it as a JSON-compatible string if necessary. |


---

## calculate_trade_pnl

### Description
Calculates the profit or loss for a trade based on entry and exit prices, quantity, side, instrument, and timestamp.

### Implementation Plan

#### 1. Validate and convert all string inputs to appropriate numeric types before computation.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that calculations are performed on numeric values and prevents runtime errors due to invalid data types. |
| **Impact** | Improves reliability and robustness of the shim, making it safe to handle real-world input variations. |
| **Complexity** | MEDIUM |
| **Method** | Use Python's Decimal or float conversion with try/except blocks; normalize string formats and handle currency symbols or commas. |

#### 2. Implement the core P&L formula accounting for trade side: for 'buy' compute (exit_price - entry_price) * quantity, for 'sell' compute (entry_price - exit_price) * quantity.

| Category | Details |
| --- | --- |
| **Reason** | Accurate profit/loss calculation is the primary function of the node and must reflect standard trading conventions. |
| **Impact** | Provides correct financial metrics that downstream performance monitoring relies on. |
| **Complexity** | LOW |
| **Method** | Apply conditional logic based on the 'side' parameter, perform arithmetic, and store the result as a Decimal or float. |

#### 3. Return a JSON object containing all input fields and the computed output, and include error handling to return meaningful messages on invalid data.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output format is required for integration with the monitoring pipeline, and graceful error handling prevents cascading failures. |
| **Impact** | Ensures downstream nodes can parse results reliably and capture failure cases for debugging or alerts. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary with keys matching output_structure, serialize to JSON string, and catch exceptions to log and return an error string in the 'output' field. |


---

## update_equity_curve

### Description
Updates the equity curve data structure by incorporating the return fraction of a closed trade.

### Implementation Plan

#### 1. Validate input types and convert string representations of return_fraction and equity_curve into numeric data structures.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the shim operates on correctly typed data, preventing runtime errors. |
| **Impact** | Guarantees data integrity and consistency for subsequent calculations. |
| **Complexity** | LOW |
| **Method** | Use Python's json.loads to parse the equity_curve and float() to convert return_fraction. |

#### 2. Calculate the cumulative equity value by applying the return_fraction to the last equity point and append the new value to the equity_curve list.

| Category | Details |
| --- | --- |
| **Reason** | Accurately reflects the portfolio's value after the trade. |
| **Impact** | Provides an up‑to‑date equity trajectory for performance monitoring. |
| **Complexity** | LOW |
| **Method** | Retrieve the last element of the equity_curve list, compute new_equity = last_equity * (1 + return_fraction), and append new_equity. |

#### 3. Serialize the updated equity_curve back to a JSON string and return it along with a success status message.

| Category | Details |
| --- | --- |
| **Reason** | Maintains the expected string interface for downstream nodes. |
| **Impact** | Ensures compatibility with other components that consume the equity_curve as a string. |
| **Complexity** | LOW |
| **Method** | Use json.dumps to convert the equity_curve list to a string and return it together with a simple "success" message. |


---

## calculate_performance_metrics

### Description
Computes key trading performance statistics from closed trade data and an equity curve.

### Implementation Plan

#### 1. Deserialize the `closed_trades` and `equity_curve` JSON strings into Python objects while validating schema consistency.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that downstream computations receive correctly structured data and helps catch malformed inputs early. |
| **Impact** | Prevents runtime errors during metric calculations and guarantees that all required fields are present. |
| **Complexity** | LOW |
| **Method** | Use `json.loads()` with try/except blocks and optionally leverage Pydantic models or schema validation to enforce field types. |

#### 2. Iterate over the list of closed trades to compute trade‑level statistics (total, wins, losses, win rate, average return) and aggregate equity changes to calculate max drawdown and the Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | These metrics are the core outputs required by downstream performance monitoring nodes. |
| **Impact** | Provides a concise performance snapshot that informs risk management and strategy adjustments. |
| **Complexity** | MEDIUM |
| **Method** | Use plain Python loops or NumPy/Pandas for vectorized calculations; compute cumulative equity to derive drawdowns and use risk‑free rate = 0 to calculate Sharpe ratio. |

#### 3. Serialize the computed metrics dictionary into a JSON string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | Matches the shim’s expected output type and allows callers to parse the results easily. |
| **Impact** | Ensures compatibility with downstream nodes that expect a string payload. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps()` on the metrics dictionary and return the string. |


---

## evaluate_performance_stability

### Description
Evaluates whether trading performance metrics fall within acceptable thresholds and returns a stability status.

### Implementation Plan

#### 1. Validate and parse the incoming JSON strings for metrics and thresholds, ensuring required keys are present and values are numeric.

| Category | Details |
| --- | --- |
| **Reason** | Prevents runtime errors and ensures the function operates on well-formed data. |
| **Impact** | Guarantees robustness and easier debugging of input data issues. |
| **Complexity** | LOW |
| **Method** | Use json.loads followed by schema validation with pydantic models or manual key checks. |

#### 2. Implement stability logic that compares each performance metric against its corresponding threshold, applying business rules such as win_rate >= min_win_rate, max_drawdown <= max_drawdown_threshold, and sharpe_ratio >= min_sharpe_ratio.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality that determines if the strategy is performing within acceptable bounds. |
| **Impact** | Directly influences alert generation and recommendation outputs downstream. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over a mapping of metric names to threshold comparisons, short‑circuit on first failure, and compute a boolean flag is_stable. |

#### 3. Generate a concise JSON string containing the stability flag and an optional explanatory message, ensuring the output adheres to the expected STR format.

| Category | Details |
| --- | --- |
| **Reason** | Provides a standardized result for downstream nodes and user interfaces. |
| **Impact** | Enables consistent consumption of stability status across the system. |
| **Complexity** | LOW |
| **Method** | Construct a Python dictionary and serialize with json.dumps; return the resulting string as output. |


---

## generate_recommended_adjustments

### Description
Produces a list of strategy or risk management adjustments based on performance metrics and thresholds.

### Implementation Plan

#### 1. Implement a rule‑based mapping that evaluates key performance indicators (win rate, drawdown, Sharpe ratio, etc.) against the supplied thresholds and generates context‑appropriate adjustment suggestions.

| Category | Details |
| --- | --- |
| **Reason** | To translate quantitative metrics into actionable guidance for the trading strategy. |
| **Impact** | Provides clear, data‑driven recommendations that help maintain or improve performance. |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of conditions (e.g., win_rate < thresholds['win_rate_min']) mapping to suggestion strings and iterate over metrics to accumulate applicable suggestions. |

#### 2. Short‑circuit recommendations when stability_result indicates the performance is within acceptable ranges, returning an empty adjustment list or a 'no change needed' notice.

| Category | Details |
| --- | --- |
| **Reason** | To avoid unnecessary or counter‑productive adjustments during stable periods. |
| **Impact** | Reduces noise in the output and preserves the trader’s existing configuration when appropriate. |
| **Complexity** | LOW |
| **Method** | Check `stability_result['is_stable']`; if true, immediately set the output to an empty array or a single message. |

#### 3. Format the final suggestions as a JSON array string, ensuring the output adheres to the expected string type and can be parsed downstream.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output serialization simplifies integration with downstream nodes. |
| **Impact** | Guarantees that downstream components can reliably interpret the adjustment recommendations. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps(suggestions_list)` to produce a compact JSON string; include error handling for serialization failures. |


---

## check_alert_conditions

### Description
Evaluates performance metrics against alert thresholds and returns a boolean flag indicating whether an alert should be triggered.

### Implementation Plan

#### 1. Parse the JSON strings for metrics and alert_thresholds into Python dictionaries to enable programmatic comparison.

| Category | Details |
| --- | --- |
| **Reason** | Both inputs are JSON strings; parsing is essential to access individual metric values. |
| **Impact** | Ensures data integrity and allows dynamic metric handling, making the shim reusable for different performance metrics. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` with exception handling for invalid JSON. |

#### 2. Iterate over each metric key, compare its numeric value against the corresponding threshold, and determine if any metric breaches its limit.

| Category | Details |
| --- | --- |
| **Reason** | The core logic of alerting relies on threshold comparison for each metric. |
| **Impact** | Provides accurate alert conditions, preventing false positives or negatives. |
| **Complexity** | MEDIUM |
| **Method** | Implement a loop over `metrics_dict.items()`, retrieve threshold via `thresholds_dict.get(key)`, perform numeric comparison, and short‑circuit on first breach. |

#### 3. Return the alert flag as a string ('true' or 'false') and optionally log detailed comparison results for audit purposes.

| Category | Details |
| --- | --- |
| **Reason** | Output must be a primitive string to satisfy the node's output structure and logging aids debugging. |
| **Impact** | Standardizes the output format and improves traceability of alert decisions. |
| **Complexity** | LOW |
| **Method** | Set `alert_flag = 'true' if breach else 'false'`; optionally write to a log file or stdout. |


---

## get_current_iso_timestamp

### Description
Returns the current UTC timestamp formatted as an ISO‑8601 string.

### Implementation Plan

#### 1. Use Python's datetime module to obtain the current UTC time and format it as an ISO‑8601 string with seconds precision.

| Category | Details |
| --- | --- |
| **Reason** | Ensures consistent, timezone‑aware timestamps for all system outputs. |
| **Impact** | Standardizes time representation across all nodes, enabling accurate logging and metric correlation. |
| **Complexity** | LOW |
| **Method** | datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z') |

#### 2. Wrap the timestamp generation in a try/except block to provide a graceful fallback and guarantee a string is always returned.

| Category | Details |
| --- | --- |
| **Reason** | Prevents the shim from propagating runtime exceptions into calling nodes. |
| **Impact** | Maintains robustness of the monitoring pipeline even under unexpected system errors. |
| **Complexity** | LOW |
| **Method** | try: ... except Exception: return datetime.datetime.utcfromtimestamp(0).isoformat(timespec='seconds').replace('+00:00', 'Z') |
