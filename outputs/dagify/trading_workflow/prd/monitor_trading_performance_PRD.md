# monitor_trading_performance PRD

## Description
Continuously monitors executed trades to calculate performance statistics, detect deviations from expected behavior, recommend strategy adjustments, and trigger alerts when performance deteriorates.


## Implementation Plan

### 1. Initialize monitoring state with in‑memory data structures: a position map keyed by instrument to track open positions, a list of closed trade objects, an equity curve list for drawdown calculations, and configuration thresholds for win rate, drawdown, and Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | A clean, well‑structured state is essential for accurate real‑time computations and to avoid stale data accumulation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use Python dictionaries for position map, dataclasses for trade objects, NumPy arrays for equity curve, and load thresholds from a YAML configuration file. |

### 2. Ingest each batch of `execute_trades` output, filtering only trades where `trade_execution_status` is True to exclude failed executions.

| Category | Details |
| --- | --- |
| **Reason** | Failed trades can introduce incorrect P&L signals; they must be discarded before any calculation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Iterate over `trade_execution_status` list, aligning indices to other lists via a simple for‑loop. |

### 3. For each successful trade, update the position map: if the instrument has no open position, add a new entry with entry price, quantity, side; if there is an open position with the same side, aggregate quantity and recalculate a weighted average entry price.

| Category | Details |
| --- | --- |
| **Reason** | Accurate tracking of open positions is required to compute P&L when the position is closed. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a helper function that takes instrument, side, price, quantity and performs upsert logic into the map. |

### 4. Detect position closures by matching an incoming trade that has the opposite side to an existing open position with the same instrument and matching quantity (or the remaining quantity after partial close). Compute P&L per trade as (exit_price - entry_price) * quantity * sign, where sign is +1 for buy‑sell and -1 for sell‑buy.

| Category | Details |
| --- | --- |
| **Reason** | P&L calculation is the core of win/loss determination and subsequent metrics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a partial close algorithm that updates the open position quantity and emits a closed trade record when quantity reaches zero. |

### 5. Append each closed trade record to the closed trade list, incrementing `total_trades`; if P&L > 0, increment `winning_trades`; otherwise increment `losing_trades`.

| Category | Details |
| --- | --- |
| **Reason** | Maintaining a historical list allows batch metric computation and future trend analysis. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Simple append to list; use a dataclass with fields for instrument, return_fraction, pnl, timestamp. |

### 6. Calculate trade return fraction as `pnl / (entry_price * quantity)` and store it in the trade record for later use in Sharpe ratio and average return calculations.

| Category | Details |
| --- | --- |
| **Reason** | Return fraction normalizes P&L across different position sizes and instruments. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Compute using float division and store in dataclass. |

### 7. Update the equity curve by adding the current trade’s return fraction multiplied by the previous equity value; maintain a running maximum (peak) and current equity to compute drawdown at each step.

| Category | Details |
| --- | --- |
| **Reason** | An equity curve is needed to determine maximum drawdown, a key risk metric. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a list for equity values, apply cumulative product of (1 + return_fraction) starting from initial capital. |

### 8. After processing the batch, compute performance metrics: `win_rate = winning_trades / total_trades`; `average_return_per_trade = sum(return_fractions) / total_trades`; `max_drawdown = (peak - trough) / peak`; `sharpe_ratio = mean(return_fractions) / std(return_fractions)` assuming risk‑free rate = 0.

| Category | Details |
| --- | --- |
| **Reason** | These metrics provide the quantitative basis for stability assessment and adjustment recommendations. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use NumPy or pandas for efficient mean/std calculations; guard against division by zero. |

### 9. Evaluate performance stability by comparing each metric to predefined acceptable thresholds (e.g., win_rate >= 0.45, max_drawdown <= 0.15, sharpe_ratio >= 1.0). Set `is_performance_stable` to True only if all thresholds are met.

| Category | Details |
| --- | --- |
| **Reason** | A clear boolean flag simplifies downstream decision logic in `analyze_trading_results`. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Hard‑code thresholds in a config module; use logical AND to compute flag. |

### 10. Generate `recommended_adjustments` by mapping metric deviations to specific strategy tweaks: if win_rate < threshold, suggest tightening entry criteria; if max_drawdown > threshold, suggest reducing `risk_per_trade`; if Sharpe < threshold, suggest improving risk‑reward ratio. Include a short explanatory string for each.

| Category | Details |
| --- | --- |
| **Reason** | Providing actionable suggestions facilitates rapid iteration and human oversight. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a mapping dictionary that takes metric name and direction to output a recommendation string. |

### 11. Set `alert_flag` to True when any metric falls outside an even more stringent alert threshold (e.g., win_rate < 0.35 or max_drawdown > 0.25). This flag triggers an external alerting system.

| Category | Details |
| --- | --- |
| **Reason** | Early warning ensures that significant performance degradation is not missed. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use separate alert thresholds in config; compute boolean OR across conditions. |

### 12. Produce the final output dictionary populated with the current timestamp (ISO‑8601) and all computed metrics, ensuring that each field matches the declared PrimitiveType.

| Category | Details |
| --- | --- |
| **Reason** | The output must conform exactly to the defined schema for downstream nodes. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Serialize metrics to native Python types and wrap them in a dict; use `datetime.utcnow().isoformat()` for timestamp. |
