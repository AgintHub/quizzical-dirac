# calculate_performance_metrics PRD

## Description
Calculates performance metrics such as total return, average profit, win rate, and equity curve from trade execution data.


## Implementation Plan

### 1. Parse the trade_results JSON into structured trade objects and compute basic aggregates (total profit, number of trades, win/loss counts).

| Category | Details |
| --- | --- |
| **Reason** | Aggregate data is needed to derive higher‑level metrics. |
| **Impact** | Provides the foundation for all subsequent calculations and ensures data integrity. |
| **Complexity** | LOW |
| **Method** | Use json.loads to deserialize input; iterate through the list to accumulate totals and counts. |

### 2. Generate the equity curve and compute maximum drawdown from daily balance changes.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown is a key risk metric and requires accurate equity representation. |
| **Impact** | Enables risk assessment and informs capital allocation decisions. |
| **Complexity** | MEDIUM |
| **Method** | Sort trades by timestamp, compute cumulative P/L per day, track peak equity and calculate drawdowns using numpy or pandas. |

### 3. Return all metrics as a JSON string, including fields for total_return, avg_profit_per_trade, avg_loss_per_trade, win_rate, win_loss_ratio, number_of_trades, equity_curve, daily_returns, and total_trading_days.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output format is required by downstream nodes. |
| **Impact** | Standardizes data exchange and facilitates serialization in the overall pipeline. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary of metric values and json.dumps it. |
