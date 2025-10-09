# trading_workflow - Complete PRD Documentation

## Overview
PRDs for nodes in the 'trading_workflow' module.

## Table of Contents

- [analyze_trading_results](#analyze_trading_results)

- [backtest_trading_strategy](#backtest_trading_strategy)

- [configure_trading_infrastructure](#configure_trading_infrastructure)

- [define_trading_strategy](#define_trading_strategy)

- [execute_trades](#execute_trades)

- [implement_risk_management](#implement_risk_management)

- [monitor_trading_performance](#monitor_trading_performance)

- [refine_trading_strategy](#refine_trading_strategy)



---

## analyze_trading_results

### Description
Analyze the results of trading activities to identify areas for improvement.

### Implementation Plan

#### 1. Retrieve the monitoring snapshot data from the parent node "monitor_trading_performance" and deserialize it into a structured dictionary using the predefined JSON schema.

| Category | Details |
| --- | --- |
| **Reason** | Ensures type safety and consistency with downstream processing. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a JSON parsing library (e.g., Python's json module) and validate against the schema; handle missing keys with default values. |

#### 2. Compute "total_trades" by summing the provided "total_trades" from the parent snapshot; if missing, calculate as winning_trades + losing_trades.

| Category | Details |
| --- | --- |
| **Reason** | Accurate trade count is essential for all subsequent metrics. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Apply integer addition; include a sanity check that the resulting count matches the length of any trade ID list if available. |

#### 3. Derive "win_rate" by dividing the number of winning trades by the total trades, ensuring a division‑by‑zero guard that returns 0.0 when total_trades is zero.

| Category | Details |
| --- | --- |
| **Reason** | Provides a normalized performance indicator. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use float division; encapsulate in a try/except block for ZeroDivisionError. |

#### 4. Calculate "average_return_per_trade" by taking the parent snapshot’s "average_return_per_trade"; if not available, compute using the cumulative profit/loss over all trades divided by total_trades.

| Category | Details |
| --- | --- |
| **Reason** | Standardized metric for trade profitability. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | If cumulative return is provided, divide by total_trades; otherwise, parse individual trade returns from the parent data if available. |

#### 5. Determine "max_drawdown" by retrieving the parent snapshot’s "max_drawdown" value; if absent, compute it by scanning the equity curve provided in the snapshot (e.g., using peak‑to‑trough algorithm).

| Category | Details |
| --- | --- |
| **Reason** | Max drawdown is a critical risk metric. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a one‑pass algorithm that tracks running maximum equity and calculates drawdowns; handle missing equity data gracefully. |

#### 6. Compute "sharpe_ratio" by retrieving the parent snapshot’s "sharpe_ratio"; if absent, compute it using the formula (mean return - risk‑free rate) / std deviation of returns, assuming a risk‑free rate of 0.01 (1%).

| Category | Details |
| --- | --- |
| **Reason** | Sharpe ratio contextualizes return relative to volatility. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use NumPy or Pandas to calculate mean and std; apply the Sharpe formula; round to four decimals. |

#### 7. Generate "improvement_suggestions" by performing a rule‑based analysis: compare computed metrics against target thresholds (e.g., win_rate > 0.55, max_drawdown < 0.15, Sharpe > 1.0). For any metric that falls below its target, add a concise suggestion.

| Category | Details |
| --- | --- |
| **Reason** | Provides actionable insights without requiring deep statistical modeling. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of thresholds; iterate over metrics; append strings like "Improve stop‑loss granularity" or "Increase position sizing discipline" based on the shortfall. |

#### 8. Translate each suggestion in "improvement_suggestions" into a concrete "action_item" by mapping common suggestions to specific tasks (e.g., "Adjust stop‑loss to 1.5% of entry price").

| Category | Details |
| --- | --- |
| **Reason** | Transforms high‑level ideas into implementable actions. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a mapping table or simple templating; if a suggestion is already actionable, reuse it verbatim. |

#### 9. Assess "is_significant_change" by conducting a simple statistical test: if the difference between observed win_rate and expected win_rate (e.g., 0.6) is greater than 2 standard deviations of win_rate across historical periods, flag as true.

| Category | Details |
| --- | --- |
| **Reason** | Provides a quantitative check for anomalous performance. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Fetch historical win_rate distribution from a persisted dataset; compute mean and std; apply z‑score threshold (e.g., |z| > 2). |

#### 10. Validate the final output dictionary against the defined schema, ensuring all fields are present and correctly typed before serializing to JSON.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees compatibility with downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Implement a schema validator (e.g., jsonschema) that checks data types and required fields. |


---

## backtest_trading_strategy

### Description
Test the trading strategy on historical data to evaluate performance.

### Implementation Plan

#### 1. Extract strategy definition from the parent node's output, ensuring all fields (strategy_name, entry_rules, exit_rules, position_sizing_rule, risk_management_rule, assets_traded) are available for use.

| Category | Details |
| --- | --- |
| **Reason** | The backtest logic relies on the precise trading rules and asset universe specified by the strategy; missing data would cause incorrect simulation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Validate presence of each field; use JSON schema validation to assert data types before proceeding. |

#### 2. Retrieve clean historical price data for each asset in assets_traded from the data repository or by invoking collect_historical_market_data, filtering by the timeframes required by the strategy.

| Category | Details |
| --- | --- |
| **Reason** | Accurate backtesting demands high‑quality, time‑aligned price series; the strategy may depend on specific timeframes. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a data access layer to query the database by ticker and timeframe; apply resampling or interpolation if needed; verify is_clean flag and data_quality_score > 0.8. |

#### 3. Simulate trade execution for the entire historical period by iterating over each time step, applying entry_rules to generate buy or sell signals, and exit_rules to close positions, while respecting position_sizing_rule and risk_management_rule.

| Category | Details |
| --- | --- |
| **Reason** | This step creates the chronological sequence of trades that will be used to compute performance metrics. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Implement an event‑driven simulator: for each bar, evaluate boolean expressions in entry_rules/exits using the bar's OHLCV data; compute position size using a risk‑based formula; apply stop‑loss and take‑profit logic from risk_management_rule; maintain a list of open positions and update PnL on each step. |

#### 4. Calculate cumulative returns per trade, aggregate them to compute total_return, number_of_trades, win_rate, avg_profit_per_trade, avg_loss_per_trade, and win_loss_ratio.

| Category | Details |
| --- | --- |
| **Reason** | These core metrics directly reflect the strategy’s profitability and trade quality. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each closed trade, compute PnL = (exit_price - entry_price) * quantity; classify as win/loss; use numpy or pandas to aggregate statistics; ensure rounding to 6 decimal places for consistency. |

#### 5. Determine max_drawdown by constructing the equity curve over time, computing rolling peaks, and measuring the largest drop from a peak to a trough.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown is a key risk metric that captures the worst equity loss experienced during the period. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use cumulative returns to build equity_curve; apply pandas .cummax() to track peaks; compute drawdown = (equity_curve - peaks)/peaks; take the minimum value. |

#### 6. Compute the annualized_return by annualizing the cumulative return based on the number of trading days in the backtesting period and the typical market calendar.

| Category | Details |
| --- | --- |
| **Reason** | Annualized return allows comparison across strategies with different time horizons. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Annualized = (1 + total_return) ** (252 / total_trading_days) - 1, assuming 252 trading days per year. |

#### 7. Calculate Sharpe ratio using the daily excess returns (return minus risk‑free rate) divided by the standard deviation of daily returns, then annualize the result.

| Category | Details |
| --- | --- |
| **Reason** | Sharpe ratio is a standard risk‑adjusted performance metric. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Set risk_free_rate = 0.0 (or fetch from treasury data); compute daily_excess = daily_return - risk_free_rate; sharpe_daily = mean(daily_excess)/std(daily_excess); annualized_sharpe = sharpe_daily * sqrt(252). |

#### 8. Generate a concise performance_summary string summarizing the key metrics, formatted for human readability and future reporting.

| Category | Details |
| --- | --- |
| **Reason** | The summary provides a quick snapshot for stakeholders and is required by the output structure. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Template: "{strategy_name} achieved a total return of {total_return*100:.2f}%, an annualized return of {annualized_return*100:.2f}%, max drawdown {max_drawdown*100:.2f}%, Sharpe ratio {sharpe_ratio:.2f}. {number_of_trades} trades were executed with a win rate of {win_rate:.2%}." |


---

## configure_trading_infrastructure

### Description
Set up the necessary infrastructure for executing trades.

### Implementation Plan

#### 1. Compile a list of supported brokerage APIs from a central configuration file or environment variable, then present the options to the user or select a default based on predefined criteria (e.g., lowest latency, best commission structure).

| Category | Details |
| --- | --- |
| **Reason** | Centralizing the API registry guarantees consistency and allows future expansion without code changes. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Read JSON/YAML config; filter by `enabled: true`; sort by user preferences; if no explicit choice, pick first in list. |

#### 2. Retrieve the API key and secret for the chosen brokerage from a secure vault (e.g., AWS Secrets Manager, HashiCorp Vault) or environment variables, and perform a simple format validation (length, alphanumeric).

| Category | Details |
| --- | --- |
| **Reason** | Ensures that credentials are available before attempting to instantiate the client, avoiding costly runtime errors. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use SDK of the vault; catch `SecretNotFound` and `InvalidFormat` exceptions; set `api_key_status` and `api_secret_status` accordingly. |

#### 3. Instantiate the brokerage API client using the retrieved credentials, initializing any SDK-specific session or connection parameters.

| Category | Details |
| --- | --- |
| **Reason** | Establishing the client object is the first step toward executing any API call. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Call broker-specific factory method (e.g., `ibapi.wrapper` for Interactive Brokers); wrap in try/except to capture authentication failures; log detailed error messages. |

#### 4. Validate the API client by making a lightweight request such as fetching the account summary or market data; interpret a successful response as a live connection.

| Category | Details |
| --- | --- |
| **Reason** | Immediate validation catches network or credential issues early. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Send a `get_account_summary` or `get_market_depth` call; if response status is 200 and contains expected fields, set `connectivity_status` to true. |

#### 5. Set up the local trading platform wrapper (e.g., a lightweight order routing module) by importing necessary dependencies, configuring logging, and initializing any in-memory data structures needed for order tracking.

| Category | Details |
| --- | --- |
| **Reason** | A robust wrapper abstracts brokerage-specific quirks and provides a stable interface for `execute_trades`. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Instantiate a `TradingPlatform` class; configure logging level to DEBUG for troubleshooting; ensure the class exposes `place_order`, `cancel_order`, and `get_order_status` methods. |

#### 6. Populate the output fields: set `brokerage_api_name` to the selected API's name; set `api_key_status` and `api_secret_status` based on validation results; set `platform_configured` to true only if the wrapper instantiation succeeded; set `connectivity_status` to the result of the lightweight request.

| Category | Details |
| --- | --- |
| **Reason** | Consolidates all status flags into the node's defined output schema. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Assign boolean variables directly; wrap final assignment in a dictionary matching the output structure. |


---

## define_trading_strategy

### Description
Develop a trading strategy based on analysis of historical data.

### Implementation Plan

#### 1. Validate and structure the raw historical data from the parent node into a clean DataFrame, ensuring that each asset's timestamps align with its price values and that there are no missing or NaN entries.

| Category | Details |
| --- | --- |
| **Reason** | Data integrity is foundational for any reliable strategy definition; any gaps can bias indicator calculations or risk assessments. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use pandas read_csv/merge operations; check len(timestamps) == len(price_values) for each asset; drop rows with NaNs; convert timestamps to datetime. |

#### 2. Compute descriptive statistics (mean, standard deviation, skewness, kurtosis) for each asset and timeframe to understand volatility, liquidity and tail behavior.

| Category | Details |
| --- | --- |
| **Reason** | Statistical profiles inform parameter selection for indicators and risk limits. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Apply pandas .describe() and scipy.stats.skew/kurtosis; store results in a metadata dictionary. |

#### 3. Generate a comprehensive set of technical indicators (SMA, EMA, RSI, MACD, ATR, Bollinger Bands) for each asset using the chosen timeframes, ensuring indicator values are aligned with price timestamps.

| Category | Details |
| --- | --- |
| **Reason** | Indicators provide the quantitative signals that will form the core of entry and exit rules. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Leverage pandas_ta or ta-lib to compute each indicator; add columns to DataFrame; handle lag by forward-filling the first few rows. |

#### 4. Perform a correlation and predictive power analysis between each indicator and future price returns over a sliding window to identify the most statistically significant signals.

| Category | Details |
| --- | --- |
| **Reason** | Reduces the risk of overfitting by selecting only the signals that historically move the market. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Calculate Pearson/Spearman correlations for each indicator vs. next-period returns; perform a simple cross‑validation split to confirm predictive stability. |

#### 5. Formulate a composite entry rule that combines the top-performing indicators using logical operators (e.g., SMA crossover AND RSI threshold) and includes a minimum volume filter to ensure liquidity.

| Category | Details |
| --- | --- |
| **Reason** | Combining trend and momentum signals typically yields stronger entry quality than a single indicator. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Encode the rule in a human‑readable string, e.g., "(SMA_20 > SMA_50) AND (RSI_14 < 30) AND (Volume > 1.5×MA_Vol)". |

#### 6. Design exit rules that incorporate both time‑based (e.g., hold for N days) and price‑based (e.g., take profit 3×ATR, stop‑loss 1×ATR) conditions to capture gains while limiting downside risk.

| Category | Details |
| --- | --- |
| **Reason** | Clear exit criteria prevent emotional or ad‑hoc trade closures and lock in profitability. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Provide textual description plus numeric formulas; e.g., "TP = entry_price + 3*ATR; SL = entry_price - 1*ATR; close if price >= TP or price <= SL or holding period >= 5 days." |

#### 7. Specify a position sizing rule using a fixed‑fractional approach where a fixed % of capital is risked per trade, calculated from the stop‑loss distance and account equity.

| Category | Details |
| --- | --- |
| **Reason** | Consistent position sizing maintains risk uniformity across trades. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Explain rule: "size = (risk_per_trade * equity) / (stop_loss_distance * entry_price)"; include example calculation in the output. |

#### 8. Create a risk_management_rule string that details maximum drawdown limit, stop‑loss per trade, portfolio diversification (e.g., max 5 assets), and any other constraints such as maximum daily loss.

| Category | Details |
| --- | --- |
| **Reason** | Consolidating risk limits into a single rule facilitates enforcement by the execution engine. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Format as: "Max_drawdown = 20% of equity; Stop_loss = 2% per trade; Diversify across <=5 assets; Max_daily_loss = 5% of equity." |

#### 9. Filter the assets_traded list from the parent node to include only those with data_quality_score >= 0.8 and average daily volume above a set threshold, ensuring the strategy trades only liquid and reliable instruments.

| Category | Details |
| --- | --- |
| **Reason** | Trading illiquid or low‑quality data can lead to slippage and execution issues. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Apply a boolean mask on the parent output lists; return the filtered list. |

#### 10. Assemble the final strategy dictionary mapping each required output key to its corresponding value, ensuring correct data types (e.g., strings for rules, list for assets).

| Category | Details |
| --- | --- |
| **Reason** | Matches the node's output schema, allowing downstream nodes to parse the result unambiguously. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use a Python dict: {"strategy_name":..., "entry_rules":..., "exit_rules":..., "position_sizing_rule":..., "risk_management_rule":..., "assets_traded":...} and serialize to JSON if needed. |


---

## execute_trades

### Description
Execute trades based on the defined strategy and risk management rules.

### Implementation Plan

#### 1. Validate the brokerage infrastructure: ensure that `connectivity_status`, `api_key_status`, `api_secret_status`, and `platform_configured` from the `configure_trading_infrastructure` node are all true before any order is sent.

| Category | Details |
| --- | --- |
| **Reason** | Prevent futile order attempts and provide clear early failure if the system is not ready. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Check Boolean flags, abort and return an error list if any flag is false; log each failure reason. |

#### 2. Retrieve risk parameters from the `implement_risk_management` node, specifically `risk_per_trade`, `stop_loss_percentage`, and the `position_sizing_strategy`.

| Category | Details |
| --- | --- |
| **Reason** | These parameters dictate how much capital to allocate per trade and what stop‑loss to set. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Destructure the risk object; validate numeric ranges (0 < risk_per_trade <= 1). |

#### 3. Generate a list of pending trade signals by invoking the live strategy engine (or a cached signal queue). Each signal includes instrument, side, and target entry price.

| Category | Details |
| --- | --- |
| **Reason** | The node's prompt assumes trade signals are available; this step bridges strategy output to execution. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the strategy definition (`define_trading_strategy.entry_rules`) to parse the current market data and produce a list of actionable orders. |

#### 4. For each signal, compute the position size using the chosen `position_sizing_strategy` (e.g., fixed fractional). Multiply the total account equity by `risk_per_trade` and divide by the product of `stop_loss_percentage` and the instrument's price to obtain the quantity.

| Category | Details |
| --- | --- |
| **Reason** | Ensures each trade adheres to the maximum risk per trade constraint. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a helper function that accepts equity, risk_per_trade, stop_loss_percentage, price; return rounded quantity. |

#### 5. Determine the stop‑loss price for each position: if `stop_loss_levels` is provided for that instrument, use the specific level; otherwise, calculate `entry_price * (1 - stop_loss_percentage)` for long positions and `entry_price * (1 + stop_loss_percentage)` for short positions.

| Category | Details |
| --- | --- |
| **Reason** | Provides explicit exit points to limit downside. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Conditional logic based on side; apply rounding to two decimal places. |

#### 6. Submit each order to the brokerage API using the broker's SDK or REST endpoint, passing instrument, side, quantity, limit price (entry price), and stop‑loss as a trailing or conditional order.

| Category | Details |
| --- | --- |
| **Reason** | Actual execution is performed through the configured broker. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Wrap API calls in try/catch; capture the response ID, execution status, filled price, and timestamp. |

#### 7. Collect execution results: aggregate `trade_execution_ids`, `trade_execution_status`, `trade_execution_timestamps`, `trade_execution_prices`, `trade_execution_quantities`, `trade_execution_instruments`, and `trade_execution_sides` into corresponding lists.

| Category | Details |
| --- | --- |
| **Reason** | Matches the required output schema. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Append to mutable lists as each API response is processed. |

#### 8. After all orders are processed, set `overall_execution_success` to true if every `trade_execution_status` is true; otherwise set false.

| Category | Details |
| --- | --- |
| **Reason** | Provides a single flag summarizing batch health. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use all() function on status list. |

#### 9. Compile any error messages from failed orders into `execution_error_messages`; if no failures, return an empty list.

| Category | Details |
| --- | --- |
| **Reason** | Facilitates downstream monitoring and alerting. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Collect error strings from caught exceptions. |


---

## implement_risk_management

### Description
Develop and implement risk management rules to control exposure.

### Implementation Plan

#### 1. Parse the `risk_management_rule` text from the parent `define_trading_strategy` output to extract explicit numeric risk thresholds using a combination of regular expressions and a lightweight NLP parser.

| Category | Details |
| --- | --- |
| **Reason** | The strategy definition contains human‑readable risk constraints that need to be programmatically interpreted to populate numeric fields. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use regex patterns such as `risk per trade[:=]\s*(\d+%|\d*\.?\d+)`, `stop‑loss[:=]\s*(\d+%|\d*\.?\d+)`, `max drawdown[:=]\s*(\d+%|\d*\.?\d+)`, and `diversification[:=]\s*(\d+)` to capture numbers; if percentages are present, convert to decimal; otherwise default to 0.01 for risk per trade. |

#### 2. Validate the extracted numeric values and apply default fallbacks where necessary (e.g., 1% risk per trade, 2% stop‑loss, 20% max drawdown, 10 diversification assets).

| Category | Details |
| --- | --- |
| **Reason** | Ensures the risk management configuration is robust even if the strategy text omits some parameters. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If a key is missing or cannot be parsed, assign hard‑coded defaults; log a warning for auditability. |

#### 3. Determine the `position_sizing_strategy` by mapping the parsed risk parameters to a chosen sizing model (default to "fixed fractional").

| Category | Details |
| --- | --- |
| **Reason** | A clear strategy name is required for downstream systems to interpret how position sizes are calculated. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If the strategy text contains keywords like "Kelly" or "equity curve", set `position_sizing_strategy` accordingly; otherwise default to "fixed fractional". |

#### 4. Compute the `stop_loss_levels` list for each asset in `assets_traded` by applying the parsed `stop_loss_percentage` to a placeholder or expected entry price.

| Category | Details |
| --- | --- |
| **Reason** | Stop‑loss price levels must be concrete for the execution engine to enforce. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each asset symbol, retrieve the most recent closing price from a cached data source; compute stop price = entry_price * (1 - stop_loss_percentage). If entry price is unavailable, flag the asset for manual review. |

#### 5. Apply the `max_drawdown` and `diversification_assets` values to create an internal portfolio constraint model that will be passed to the execution layer.

| Category | Details |
| --- | --- |
| **Reason** | These constraints limit overall exposure and enforce diversification, which are critical for risk control. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Instantiate a `PortfolioRiskConstraint` object with attributes `max_drawdown_pct` and `min_asset_count`; expose its API to the execution engine via a shared configuration store (e.g., Redis or a JSON file). |

#### 6. Set `diversification_strategy` by inferring the strategy type from the strategy name or by checking if the assets span multiple sectors.

| Category | Details |
| --- | --- |
| **Reason** | The diversification approach should align with the intended portfolio structure. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | If the strategy name contains "sector" or the asset list includes at least 3 distinct sectors, set to "sector‑based"; otherwise set to "beta‑neutral". |

#### 7. Persist all computed risk parameters to a secure configuration repository and return `is_implemented = true` if no errors occur during persistence.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the risk rules are applied before any trade execution takes place. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a transactional write to a configuration database; on success set `is_implemented` to true; on failure log the error and set `is_implemented` to false. |

#### 8. Expose a validation endpoint that `execute_trades` can call to confirm that risk rules are in place before placing orders.

| Category | Details |
| --- | --- |
| **Reason** | Prevents trades from being executed without the associated risk controls. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a lightweight REST or gRPC service that returns the current risk configuration and an `is_valid` flag; integrate this call into the trade‑ordering workflow. |


---

## monitor_trading_performance

### Description
Continuously monitors executed trades to calculate performance statistics, detect deviations from expected behavior, recommend strategy adjustments, and trigger alerts when performance deteriorates.

### Implementation Plan

#### 1. Initialize monitoring state with in‑memory data structures: a position map keyed by instrument to track open positions, a list of closed trade objects, an equity curve list for drawdown calculations, and configuration thresholds for win rate, drawdown, and Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | A clean, well‑structured state is essential for accurate real‑time computations and to avoid stale data accumulation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use Python dictionaries for position map, dataclasses for trade objects, NumPy arrays for equity curve, and load thresholds from a YAML configuration file. |

#### 2. Ingest each batch of `execute_trades` output, filtering only trades where `trade_execution_status` is True to exclude failed executions.

| Category | Details |
| --- | --- |
| **Reason** | Failed trades can introduce incorrect P&L signals; they must be discarded before any calculation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Iterate over `trade_execution_status` list, aligning indices to other lists via a simple for‑loop. |

#### 3. For each successful trade, update the position map: if the instrument has no open position, add a new entry with entry price, quantity, side; if there is an open position with the same side, aggregate quantity and recalculate a weighted average entry price.

| Category | Details |
| --- | --- |
| **Reason** | Accurate tracking of open positions is required to compute P&L when the position is closed. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a helper function that takes instrument, side, price, quantity and performs upsert logic into the map. |

#### 4. Detect position closures by matching an incoming trade that has the opposite side to an existing open position with the same instrument and matching quantity (or the remaining quantity after partial close). Compute P&L per trade as (exit_price - entry_price) * quantity * sign, where sign is +1 for buy‑sell and -1 for sell‑buy.

| Category | Details |
| --- | --- |
| **Reason** | P&L calculation is the core of win/loss determination and subsequent metrics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a partial close algorithm that updates the open position quantity and emits a closed trade record when quantity reaches zero. |

#### 5. Append each closed trade record to the closed trade list, incrementing `total_trades`; if P&L > 0, increment `winning_trades`; otherwise increment `losing_trades`.

| Category | Details |
| --- | --- |
| **Reason** | Maintaining a historical list allows batch metric computation and future trend analysis. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Simple append to list; use a dataclass with fields for instrument, return_fraction, pnl, timestamp. |

#### 6. Calculate trade return fraction as `pnl / (entry_price * quantity)` and store it in the trade record for later use in Sharpe ratio and average return calculations.

| Category | Details |
| --- | --- |
| **Reason** | Return fraction normalizes P&L across different position sizes and instruments. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Compute using float division and store in dataclass. |

#### 7. Update the equity curve by adding the current trade’s return fraction multiplied by the previous equity value; maintain a running maximum (peak) and current equity to compute drawdown at each step.

| Category | Details |
| --- | --- |
| **Reason** | An equity curve is needed to determine maximum drawdown, a key risk metric. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a list for equity values, apply cumulative product of (1 + return_fraction) starting from initial capital. |

#### 8. After processing the batch, compute performance metrics: `win_rate = winning_trades / total_trades`; `average_return_per_trade = sum(return_fractions) / total_trades`; `max_drawdown = (peak - trough) / peak`; `sharpe_ratio = mean(return_fractions) / std(return_fractions)` assuming risk‑free rate = 0.

| Category | Details |
| --- | --- |
| **Reason** | These metrics provide the quantitative basis for stability assessment and adjustment recommendations. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use NumPy or pandas for efficient mean/std calculations; guard against division by zero. |

#### 9. Evaluate performance stability by comparing each metric to predefined acceptable thresholds (e.g., win_rate >= 0.45, max_drawdown <= 0.15, sharpe_ratio >= 1.0). Set `is_performance_stable` to True only if all thresholds are met.

| Category | Details |
| --- | --- |
| **Reason** | A clear boolean flag simplifies downstream decision logic in `analyze_trading_results`. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Hard‑code thresholds in a config module; use logical AND to compute flag. |

#### 10. Generate `recommended_adjustments` by mapping metric deviations to specific strategy tweaks: if win_rate < threshold, suggest tightening entry criteria; if max_drawdown > threshold, suggest reducing `risk_per_trade`; if Sharpe < threshold, suggest improving risk‑reward ratio. Include a short explanatory string for each.

| Category | Details |
| --- | --- |
| **Reason** | Providing actionable suggestions facilitates rapid iteration and human oversight. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a mapping dictionary that takes metric name and direction to output a recommendation string. |

#### 11. Set `alert_flag` to True when any metric falls outside an even more stringent alert threshold (e.g., win_rate < 0.35 or max_drawdown > 0.25). This flag triggers an external alerting system.

| Category | Details |
| --- | --- |
| **Reason** | Early warning ensures that significant performance degradation is not missed. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use separate alert thresholds in config; compute boolean OR across conditions. |

#### 12. Produce the final output dictionary populated with the current timestamp (ISO‑8601) and all computed metrics, ensuring that each field matches the declared PrimitiveType.

| Category | Details |
| --- | --- |
| **Reason** | The output must conform exactly to the defined schema for downstream nodes. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Serialize metrics to native Python types and wrap them in a dict; use `datetime.utcnow().isoformat()` for timestamp. |


---

## refine_trading_strategy

### Description
Refine the trading strategy based on analysis of trading results.

### Implementation Plan

#### 1. Retrieve baseline strategy metadata from a configuration store or versioned strategy repository.

| Category | Details |
| --- | --- |
| **Reason** | The refinement process must preserve the original strategy context so that updates are applied incrementally rather than from scratch. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a key/value store (e.g., Redis, a JSON file, or a database table) indexed by strategy_name to fetch current entry_rule, exit_rule, position_size_rule, stop_loss_level, take_profit_level, max_drawdown_limit, risk_per_trade. Validate that all required fields exist; if not, abort refinement. |

#### 2. Validate that `improvement_suggestions` from `analyze_trading_results` contains actionable items; if empty or null, set `is_strategy_updated` to False and terminate.

| Category | Details |
| --- | --- |
| **Reason** | Refinement should only occur when there are concrete improvement points. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Perform a simple list length check. If zero, construct a minimal output with original strategy values and `confidence_level` set to 0.5. |

#### 3. Map each suggestion string to a rule category using a predefined keyword-to-category dictionary (e.g., 'entry timing' → 'entry', 'stop loss' → 'risk', 'position size' → 'position').

| Category | Details |
| --- | --- |
| **Reason** | Structured mapping enables systematic rule updates and prevents ambiguous interpretation of natural language suggestions. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use regex patterns and a lookup table. For each suggestion, identify the dominant keyword and assign it to a category. Store mapping results in a list of (category, suggestion) tuples. |

#### 4. Generate updated textual rules for each mapped category by applying template-based transformations.

| Category | Details |
| --- | --- |
| **Reason** | Consistent rule language reduces ambiguity for downstream execution systems. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a set of rule templates: e.g., if category is 'entry', use "Enter long when {condition} and {indicator} crosses above {threshold}". Replace placeholders with values extracted from suggestions (e.g., threshold from numeric tokens). Concatenate multiple suggestions within the same category into a single rule string. |

#### 5. Recalculate `stop_loss_level` by combining suggested risk adjustments with baseline values, ensuring it does not exceed 20% of equity or violate the `max_drawdown_limit`.

| Category | Details |
| --- | --- |
| **Reason** | Maintaining risk discipline is critical to prevent catastrophic losses. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | If any suggestion contains a numeric risk value (e.g., '2% stop loss'), parse it; otherwise, use baseline stop_loss_percentage. Then, enforce a hard cap: `stop_loss_level = min(parsed_value, 0.20)`. Convert to float percentage. |

#### 6. Set `take_profit_level` as a multiple of the new `stop_loss_level` (e.g., 2:1 reward-to-risk ratio), or override with a numeric value from suggestions if present.

| Category | Details |
| --- | --- |
| **Reason** | Balanced reward-to-risk encourages sustainable profitability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If a suggestion contains 'take profit at X%', use that; otherwise, compute `take_profit_level = stop_loss_level * 2`. Ensure the value is a positive float. |

#### 7. Update `max_drawdown_limit` by applying any suggested percentage or defaulting to baseline if no suggestion exists.

| Category | Details |
| --- | --- |
| **Reason** | Alignment with overall portfolio risk tolerance. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Search for numeric tokens followed by '%' in `improvement_suggestions` labeled as 'drawdown'; if found, use that; otherwise, keep baseline. |

#### 8. Adjust `risk_per_trade` based on suggested changes to position sizing or stop loss, ensuring it stays within 1–3% of equity.

| Category | Details |
| --- | --- |
| **Reason** | Avoid overexposure while allowing flexibility to capitalize on identified opportunities. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | If a suggestion includes 'risk per trade', parse the percentage; else, calculate as `risk_per_trade = stop_loss_level * position_size_fraction` where `position_size_fraction` is derived from the baseline `position_size_rule` (e.g., fixed fractional). Clamp to 0.01–0.03. |

#### 9. Estimate `expected_return` using `average_return_per_trade` and an annualization heuristic based on the number of trades per year inferred from `total_trades` over the monitoring period.

| Category | Details |
| --- | --- |
| **Reason** | Provides a realistic expectation for stakeholders. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Assume the monitoring period length is known (e.g., one month). Compute trades_per_year = total_trades / period_months * 12. Then `expected_return = average_return_per_trade * trades_per_year * 100`. Convert to a percentage. |

#### 10. Compute `expected_sharpe_ratio` by applying a conservative multiplier (e.g., +10%) to the current `sharpe_ratio` if suggestions focus on volatility reduction; otherwise, keep the same.

| Category | Details |
| --- | --- |
| **Reason** | Reflects modest gains from the applied refinements without overpromising. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | If any suggestion contains words like 'reduce volatility' or 'improve Sharpe', multiply current sharpe_ratio by 1.10. Cap the result at a maximum of 3.0 to stay realistic. |

#### 11. Determine `confidence_level` as a weighted score: 0.5 × `is_significant_change` + 0.3 × (number_of_suggestions / max_possible_suggestions) + 0.2 × (expected_sharpe_ratio / 3).

| Category | Details |
| --- | --- |
| **Reason** | Combines statistical significance, actionable density, and expected performance improvement into a single metric. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Normalize each component to [0,1] and compute the weighted sum. Ensure the final value is clipped to [0,1]. |

#### 12. Construct `adjustments_summary` by concatenating human‑readable bullet points for each category that received an update, using the new rule text and parameter values.

| Category | Details |
| --- | --- |
| **Reason** | Provides transparency for auditors and traders. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Iterate over updated categories and append lines like '- Updated entry rule: {entry_rule}'. Join with newline separators. |

#### 13. Set `is_strategy_updated` to True if any rule or parameter has changed compared to baseline; otherwise, set to False.

| Category | Details |
| --- | --- |
| **Reason** | Prevents unnecessary redeployment when no changes were made. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Compare each output field to its baseline value. If any differ, flag True. |
