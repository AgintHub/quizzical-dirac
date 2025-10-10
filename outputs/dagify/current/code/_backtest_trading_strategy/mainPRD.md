# _backtest_trading_strategy - Complete PRD Documentation

## Overview
PRDs for nodes in the '_backtest_trading_strategy' module.

## Table of Contents

- [validate_strategy_definition](#validate_strategy_definition)

- [retrieve_historical_price_data](#retrieve_historical_price_data)

- [simulate_trade_execution](#simulate_trade_execution)

- [calculate_performance_metrics](#calculate_performance_metrics)

- [calculate_max_drawdown](#calculate_max_drawdown)

- [calculate_annualized_return](#calculate_annualized_return)

- [calculate_sharpe_ratio](#calculate_sharpe_ratio)

- [generate_performance_summary](#generate_performance_summary)



---

## validate_strategy_definition

### Description
Validates and normalizes the trading strategy definition, ensuring all required fields are present and correctly formatted, and determines any additional required timeframes.

### Implementation Plan

#### 1. Parse the input JSON into a Python dict and perform schema validation using Pydantic or a custom validator to ensure all required fields are present and non‑empty.

| Category | Details |
| --- | --- |
| **Reason** | Ensures the strategy definition adheres to the expected structure before any downstream processing. |
| **Impact** | Prevents runtime errors in backtesting due to missing or malformed strategy components. |
| **Complexity** | MEDIUM |
| **Method** | Define a Pydantic model matching DefineTradingStrategyOutput, then use `json.loads` to parse the input and validate it against the model; raise ValueError on failure. |

#### 2. Parse the `assets_traded` string into a list of symbols and derive `required_timeframes` by scanning entry and exit rule text for known timeframe tokens (e.g., '1D', '1H', '5M').

| Category | Details |
| --- | --- |
| **Reason** | Backtesting functions expect a list of assets and explicit timeframes; converting and extracting these ensures compatibility. |
| **Impact** | Provides consistent inputs for data retrieval and simulation modules, improving reliability. |
| **Complexity** | MEDIUM |
| **Method** | Use regex to split `assets_traded` on commas or whitespace; scan `entry_rules` and `exit_rules` for patterns like `(?i)(\d+[DHMS])` to build a set of timeframes; default to ['1D'] if none found. |

#### 3. Return a JSON string of the validated dict with all fields, including the derived `required_timeframes`, ensuring the output is JSON‑serializable.

| Category | Details |
| --- | --- |
| **Reason** | The shim's contract requires a JSON string output for downstream nodes that consume the validated strategy. |
| **Impact** | Facilitates seamless integration with other components that expect a standardized string format. |
| **Complexity** | LOW |
| **Method** | Construct a Python dict with the validated fields, then use `json.dumps` to serialize it and return the resulting string. |


---

## retrieve_historical_price_data

### Description
Retrieve historical price data for a set of assets over specified timeframes and return the data as a JSON string.

### Implementation Plan

#### 1. Implement a data retrieval engine that connects to an external market data provider (e.g., Yahoo Finance via yfinance or Alpha Vantage) or an internal database to fetch price series for each asset and timeframe specified.

| Category | Details |
| --- | --- |
| **Reason** | The shim must obtain up‑to‑date price data from a reliable source to enable backtesting and strategy evaluation. |
| **Impact** | Provides accurate and consistent historical data, directly influencing strategy performance metrics. |
| **Complexity** | MEDIUM |
| **Method** | Use the `yfinance` library for free Yahoo Finance data, or `requests` with proper authentication for paid APIs. Abstract the provider behind a simple interface to allow future swapping. |

#### 2. Validate and normalize the `retrieve_stock_data_input` JSON, ensuring that asset symbols and timeframe identifiers are supported and correctly formatted.

| Category | Details |
| --- | --- |
| **Reason** | Invalid input can cause runtime errors and corrupt downstream computations. |
| **Impact** | Improves robustness and user experience by providing clear error messages for malformed requests. |
| **Complexity** | LOW |
| **Method** | Parse the JSON string with `json.loads`, check that `assets` is a list of non‑empty strings and `timeframes` matches an allowed set. Use regex or a predefined schema for validation. |

#### 3. Cache retrieved data to avoid redundant API calls and respect rate limits, formatting the final output as a deterministic JSON string.

| Category | Details |
| --- | --- |
| **Reason** | Historical data for the same assets/timeframes is often reused; caching reduces latency and API costs. |
| **Impact** | Improves performance and scalability of the backtesting pipeline, especially when backtesting multiple strategies. |
| **Complexity** | MEDIUM |
| **Method** | Implement an in‑memory cache using `functools.lru_cache` or a lightweight Redis store keyed by a hash of the input. Serialize the result with `json.dumps` using sorted keys for consistency. |


---

## simulate_trade_execution

### Description
Simulates the execution of trades over historical price data using specified entry, exit, position sizing, and risk management rules, returning a list of trade outcomes.

### Implementation Plan

#### 1. Parse and validate all input strings into structured objects, converting JSON data and interpreting rule descriptions using a lightweight rule‑engine or simple parser.

| Category | Details |
| --- | --- |
| **Reason** | Input validation prevents runtime errors and ensures that subsequent simulation logic receives correctly typed data. |
| **Impact** | Robustness of the simulator and easier debugging for users. |
| **Complexity** | MEDIUM |
| **Method** | Use `json.loads` for historical data, `pydantic` models for rule strings, and a simple domain‑specific language (DSL) parser or `eval` with safety checks for entry/exit/position sizing/risk rules. |

#### 2. Iterate over the historical price series to identify trade entry and exit points by evaluating the parsed rules for each asset, constructing a chronological list of trade objects.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality that simulates the execution of the strategy over time. |
| **Impact** | Provides the foundational data used for all performance metrics. |
| **Complexity** | HIGH |
| **Method** | Leverage vectorized pandas operations to evaluate conditions across all timestamps; when conditions are complex, use a custom event loop that checks each rule per bar and records trade events. |

#### 3. Apply position sizing and risk management logic to each identified trade, calculating trade size, stop‑loss levels, and resulting profit or loss, and aggregate the results into the final output list.

| Category | Details |
| --- | --- |
| **Reason** | Realistic trade simulation requires accurate sizing and risk control to produce meaningful PnL and risk metrics. |
| **Impact** | Ensures that the simulated outcomes reflect the intended strategy constraints. |
| **Complexity** | MEDIUM |
| **Method** | Implement utility functions that parse sizing formulas (e.g., fixed %, fixed amount) and risk rules (e.g., stop‑loss %, fixed dollar amount), applying them to each trade and updating equity curves. |


---

## calculate_performance_metrics

### Description
Calculates performance metrics such as total return, average profit, win rate, and equity curve from trade execution data.

### Implementation Plan

#### 1. Parse the trade_results JSON into structured trade objects and compute basic aggregates (total profit, number of trades, win/loss counts).

| Category | Details |
| --- | --- |
| **Reason** | Aggregate data is needed to derive higher‑level metrics. |
| **Impact** | Provides the foundation for all subsequent calculations and ensures data integrity. |
| **Complexity** | LOW |
| **Method** | Use json.loads to deserialize input; iterate through the list to accumulate totals and counts. |

#### 2. Generate the equity curve and compute maximum drawdown from daily balance changes.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown is a key risk metric and requires accurate equity representation. |
| **Impact** | Enables risk assessment and informs capital allocation decisions. |
| **Complexity** | MEDIUM |
| **Method** | Sort trades by timestamp, compute cumulative P/L per day, track peak equity and calculate drawdowns using numpy or pandas. |

#### 3. Return all metrics as a JSON string, including fields for total_return, avg_profit_per_trade, avg_loss_per_trade, win_rate, win_loss_ratio, number_of_trades, equity_curve, daily_returns, and total_trading_days.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output format is required by downstream nodes. |
| **Impact** | Standardizes data exchange and facilitates serialization in the overall pipeline. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary of metric values and json.dumps it. |


---

## calculate_max_drawdown

### Description
Calculates the maximum drawdown from a given equity curve string representation.

### Implementation Plan

#### 1. Parse the equity_curve string into a numeric array using pandas or numpy, ensuring the format is valid CSV or JSON.

| Category | Details |
| --- | --- |
| **Reason** | The function needs numeric values to perform drawdown calculations. |
| **Impact** | Provides a reliable numeric basis for subsequent computations. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv(StringIO(equity_curve)) if CSV or json.loads(equity_curve) for JSON, then convert to a NumPy array. |

#### 2. Compute the cumulative maximum of the equity series and then calculate drawdowns by subtracting the current equity from its cumulative max, taking the minimum of these drawdowns as the maximum drawdown.

| Category | Details |
| --- | --- |
| **Reason** | Standard method to determine the largest peak‑to‑trough decline. |
| **Impact** | Delivers the core metric used for risk assessment in backtesting. |
| **Complexity** | MEDIUM |
| **Method** | Use vectorized NumPy operations: cummax = np.maximum.accumulate(equity_array); drawdowns = cummax - equity_array; max_drawdown = np.min(drawdowns). |

#### 3. Validate the result to ensure it is a finite float, handle edge cases such as constant equity or empty input by returning 0.0 or raising a descriptive error.

| Category | Details |
| --- | --- |
| **Reason** | Prevents downstream failures from invalid or nonsensical inputs. |
| **Impact** | Increases robustness and provides clear feedback to callers. |
| **Complexity** | LOW |
| **Method** | Check with np.isfinite and raise ValueError if not; default to 0.0 when equity_array is constant. |


---

## calculate_annualized_return

### Description
Calculates the annualized return of a trading strategy using its cumulative total return and the total number of trading days.

### Implementation Plan

#### 1. Parse and validate input strings for numeric values, ensuring `total_return` and `trading_days` are convertible to floats and that `trading_days` is a positive integer.

| Category | Details |
| --- | --- |
| **Reason** | Input validation prevents runtime errors and incorrect calculations. |
| **Impact** | Ensures reliability and robustness of the shim when integrated into larger pipelines. |
| **Complexity** | LOW |
| **Method** | Use `float()` conversion wrapped in a try/except block and assert `trading_days > 0`; raise a descriptive ValueError if validation fails. |

#### 2. Implement the annualized return formula using a 252-trading-day year: `(1 + total_return) ** (252 / trading_days) - 1`.

| Category | Details |
| --- | --- |
| **Reason** | The formula correctly annualizes a cumulative return over an arbitrary number of trading days. |
| **Impact** | Provides an industry-standard metric for performance comparison across strategies with different backtest lengths. |
| **Complexity** | LOW |
| **Method** | Calculate the exponent as `252 / trading_days`, then compute `math.pow(1 + total_return, exponent) - 1`. Use the `math` module for accurate floating‑point math. |

#### 3. Wrap the computation in a try/except block to gracefully handle edge cases such as division by zero or math domain errors, returning `None` or raising a custom exception with context.

| Category | Details |
| --- | --- |
| **Reason** | Robust error handling is essential for downstream nodes that may not anticipate NaN or infinite values. |
| **Impact** | Improves fault tolerance of the entire backtesting workflow. |
| **Complexity** | MEDIUM |
| **Method** | Catch `ZeroDivisionError`, `OverflowError`, and `ValueError`; log the error with a context‑rich message and re‑raise a custom `AnnualizedReturnError` containing the problematic inputs. |


---

## calculate_sharpe_ratio

### Description
Calculates the Sharpe ratio of a strategy from daily return values and an annual risk‑free rate.

### Implementation Plan

#### 1. Parse the `daily_returns` and `risk_free_rate` strings into numeric types (list of floats and float) using Python's `ast.literal_eval` or pandas `read_csv` for robustness.

| Category | Details |
| --- | --- |
| **Reason** | Input data must be converted to numerical form before performing calculations. |
| **Impact** | Ensures downstream numeric operations function correctly and reduces errors from malformed input. |
| **Complexity** | LOW |
| **Method** | Use `ast.literal_eval(daily_returns)` to get a list of floats and `float(risk_free_rate)` for the risk‑free rate. |

#### 2. Compute the mean and standard deviation of the daily returns, then apply the standard Sharpe ratio formula: `(mean - risk_free_rate/252) / std * sqrt(252)`.

| Category | Details |
| --- | --- |
| **Reason** | This is the mathematical definition of the Sharpe ratio for daily data. |
| **Impact** | Provides a standardized risk‑adjusted performance metric for the strategy. |
| **Complexity** | LOW |
| **Method** | Use NumPy: `mean = np.mean(returns)`; `std = np.std(returns, ddof=1)`; `sharpe = (mean - rf/252) / std * np.sqrt(252)`. |

#### 3. Handle edge cases where the standard deviation is zero or data is insufficient by returning `0.0` and logging a warning.

| Category | Details |
| --- | --- |
| **Reason** | Division by zero would raise an exception and mislead users if not handled. |
| **Impact** | Increases robustness and prevents crashes during backtesting pipelines. |
| **Complexity** | MEDIUM |
| **Method** | Check `if std == 0` or `len(returns) < 2` before calculation, log a warning using the standard `logging` module, and return `0.0`. |


---

## generate_performance_summary

### Description
Generates a concise textual performance summary for a trading strategy based on provided performance metrics.

### Implementation Plan

#### 1. Parse the `metrics` JSON string into a dictionary and validate the presence of required keys (`total_return`, `annualized_return`, `max_drawdown`, `sharpe_ratio`, `number_of_trades`, `win_rate`).

| Category | Details |
| --- | --- |
| **Reason** | Ensures that all necessary data points are available for summary generation and prevents downstream errors. |
| **Impact** | Guarantees accurate and reliable summary creation, improving user trust and reducing runtime failures. |
| **Complexity** | LOW |
| **Method** | Use `json.loads()` with a try/except block; check for key existence and numeric types. |

#### 2. Create a flexible natural‑language template using Jinja2 or f‑string formatting to embed metric values into a readable summary.

| Category | Details |
| --- | --- |
| **Reason** | Allows consistent, human‑friendly summaries while keeping the code maintainable. |
| **Impact** | Provides clear, actionable insights to traders and stakeholders, enhancing the interpretability of backtest results. |
| **Complexity** | MEDIUM |
| **Method** | Define a Jinja2 template string that references each metric; render with the parsed dictionary. |

#### 3. Handle edge cases such as missing metrics, non‑numeric values, or extreme values by providing fallback text or warnings in the summary.

| Category | Details |
| --- | --- |
| **Reason** | Improves robustness and prevents the shim from crashing on malformed input. |
| **Impact** | Ensures graceful degradation, maintaining system stability and user experience. |
| **Complexity** | LOW |
| **Method** | Implement validation checks and default values; if validation fails, insert a standardized error message into the summary. |
