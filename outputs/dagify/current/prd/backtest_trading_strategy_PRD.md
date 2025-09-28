# backtest_trading_strategy PRD

## Description
Test the trading strategy on historical data to evaluate performance.


## Implementation Plan

### 1. Extract strategy definition from the parent node's output, ensuring all fields (strategy_name, entry_rules, exit_rules, position_sizing_rule, risk_management_rule, assets_traded) are available for use.

| Category | Details |
| --- | --- |
| **Reason** | The backtest logic relies on the precise trading rules and asset universe specified by the strategy; missing data would cause incorrect simulation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Validate presence of each field; use JSON schema validation to assert data types before proceeding. |

### 2. Retrieve clean historical price data for each asset in assets_traded from the data repository or by invoking collect_historical_market_data, filtering by the timeframes required by the strategy.

| Category | Details |
| --- | --- |
| **Reason** | Accurate backtesting demands high‑quality, time‑aligned price series; the strategy may depend on specific timeframes. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a data access layer to query the database by ticker and timeframe; apply resampling or interpolation if needed; verify is_clean flag and data_quality_score > 0.8. |

### 3. Simulate trade execution for the entire historical period by iterating over each time step, applying entry_rules to generate buy or sell signals, and exit_rules to close positions, while respecting position_sizing_rule and risk_management_rule.

| Category | Details |
| --- | --- |
| **Reason** | This step creates the chronological sequence of trades that will be used to compute performance metrics. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Implement an event‑driven simulator: for each bar, evaluate boolean expressions in entry_rules/exits using the bar's OHLCV data; compute position size using a risk‑based formula; apply stop‑loss and take‑profit logic from risk_management_rule; maintain a list of open positions and update PnL on each step. |

### 4. Calculate cumulative returns per trade, aggregate them to compute total_return, number_of_trades, win_rate, avg_profit_per_trade, avg_loss_per_trade, and win_loss_ratio.

| Category | Details |
| --- | --- |
| **Reason** | These core metrics directly reflect the strategy’s profitability and trade quality. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each closed trade, compute PnL = (exit_price - entry_price) * quantity; classify as win/loss; use numpy or pandas to aggregate statistics; ensure rounding to 6 decimal places for consistency. |

### 5. Determine max_drawdown by constructing the equity curve over time, computing rolling peaks, and measuring the largest drop from a peak to a trough.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown is a key risk metric that captures the worst equity loss experienced during the period. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use cumulative returns to build equity_curve; apply pandas .cummax() to track peaks; compute drawdown = (equity_curve - peaks)/peaks; take the minimum value. |

### 6. Compute the annualized_return by annualizing the cumulative return based on the number of trading days in the backtesting period and the typical market calendar.

| Category | Details |
| --- | --- |
| **Reason** | Annualized return allows comparison across strategies with different time horizons. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Annualized = (1 + total_return) ** (252 / total_trading_days) - 1, assuming 252 trading days per year. |

### 7. Calculate Sharpe ratio using the daily excess returns (return minus risk‑free rate) divided by the standard deviation of daily returns, then annualize the result.

| Category | Details |
| --- | --- |
| **Reason** | Sharpe ratio is a standard risk‑adjusted performance metric. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Set risk_free_rate = 0.0 (or fetch from treasury data); compute daily_excess = daily_return - risk_free_rate; sharpe_daily = mean(daily_excess)/std(daily_excess); annualized_sharpe = sharpe_daily * sqrt(252). |

### 8. Generate a concise performance_summary string summarizing the key metrics, formatted for human readability and future reporting.

| Category | Details |
| --- | --- |
| **Reason** | The summary provides a quick snapshot for stakeholders and is required by the output structure. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Template: "{strategy_name} achieved a total return of {total_return*100:.2f}%, an annualized return of {annualized_return*100:.2f}%, max drawdown {max_drawdown*100:.2f}%, Sharpe ratio {sharpe_ratio:.2f}. {number_of_trades} trades were executed with a win rate of {win_rate:.2%}." |
