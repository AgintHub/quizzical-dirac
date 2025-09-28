# -- PRD --
# 1. BULLET: Initialize monitoring state with in‑memory data structures: a position map
#   keyed by instrument to track open positions, a list of closed trade
#   objects, an equity curve list for drawdown calculations, and
#   configuration thresholds for win rate, drawdown, and Sharpe ratio.
#   Reason: A clean, well‑structured state is essential for accurate real‑time
#           computations and to avoid stale data accumulation.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use Python dictionaries for position map, dataclasses for trade objects,
#           NumPy arrays for equity curve, and load thresholds from a YAML
#           configuration file.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Ingest each batch of `execute_trades` output, filtering only trades where
#   `trade_execution_status` is True to exclude failed executions.
#   Reason: Failed trades can introduce incorrect P&L signals; they must be discarded
#           before any calculation.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Iterate over `trade_execution_status` list, aligning indices to other lists
#           via a simple for‑loop.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: For each successful trade, update the position map: if the instrument has no
#   open position, add a new entry with entry price, quantity, side; if there
#   is an open position with the same side, aggregate quantity and
#   recalculate a weighted average entry price.
#   Reason: Accurate tracking of open positions is required to compute P&L when the
#           position is closed.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Implement a helper function that takes instrument, side, price, quantity
#           and performs upsert logic into the map.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Detect position closures by matching an incoming trade that has the opposite
#   side to an existing open position with the same instrument and matching
#   quantity (or the remaining quantity after partial close). Compute P&L per
#   trade as (exit_price - entry_price) * quantity * sign, where sign is +1
#   for buy‑sell and -1 for sell‑buy.
#   Reason: P&L calculation is the core of win/loss determination and subsequent
#           metrics.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a partial close algorithm that updates the open position quantity and
#           emits a closed trade record when quantity reaches zero.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Append each closed trade record to the closed trade list, incrementing
#   `total_trades`; if P&L > 0, increment `winning_trades`; otherwise
#   increment `losing_trades`.
#   Reason: Maintaining a historical list allows batch metric computation and future
#           trend analysis.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Simple append to list; use a dataclass with fields for instrument,
#           return_fraction, pnl, timestamp.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Calculate trade return fraction as `pnl / (entry_price * quantity)` and store
#   it in the trade record for later use in Sharpe ratio and average return
#   calculations.
#   Reason: Return fraction normalizes P&L across different position sizes and
#           instruments.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Compute using float division and store in dataclass.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Update the equity curve by adding the current trade’s return fraction
#   multiplied by the previous equity value; maintain a running maximum
#   (peak) and current equity to compute drawdown at each step.
#   Reason: An equity curve is needed to determine maximum drawdown, a key risk metric.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a list for equity values, apply cumulative product of (1 +
#           return_fraction) starting from initial capital.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: After processing the batch, compute performance metrics: `win_rate =
#   winning_trades / total_trades`; `average_return_per_trade =
#   sum(return_fractions) / total_trades`; `max_drawdown = (peak - trough) /
#   peak`; `sharpe_ratio = mean(return_fractions) / std(return_fractions)`
#   assuming risk‑free rate = 0.
#   Reason: These metrics provide the quantitative basis for stability assessment and
#           adjustment recommendations.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use NumPy or pandas for efficient mean/std calculations; guard against
#           division by zero.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Evaluate performance stability by comparing each metric to predefined
#   acceptable thresholds (e.g., win_rate >= 0.45, max_drawdown <= 0.15,
#   sharpe_ratio >= 1.0). Set `is_performance_stable` to True only if all
#   thresholds are met.
#   Reason: A clear boolean flag simplifies downstream decision logic in
#           `analyze_trading_results`.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Hard‑code thresholds in a config module; use logical AND to compute flag.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Generate `recommended_adjustments` by mapping metric deviations to specific
#   strategy tweaks: if win_rate < threshold, suggest tightening entry
#   criteria; if max_drawdown > threshold, suggest reducing `risk_per_trade`;
#   if Sharpe < threshold, suggest improving risk‑reward ratio. Include a
#   short explanatory string for each.
#   Reason: Providing actionable suggestions facilitates rapid iteration and human
#           oversight.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Implement a mapping dictionary that takes metric name and direction to
#           output a recommendation string.
# 
# -----------------------------------------------------------------------------
# 11. BULLET: Set `alert_flag` to True when any metric falls outside an even more stringent
#   alert threshold (e.g., win_rate < 0.35 or max_drawdown > 0.25). This flag
#   triggers an external alerting system.
#   Reason: Early warning ensures that significant performance degradation is not
#           missed.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use separate alert thresholds in config; compute boolean OR across
#           conditions.
# 
# -----------------------------------------------------------------------------
# 12. BULLET: Produce the final output dictionary populated with the current timestamp
#   (ISO‑8601) and all computed metrics, ensuring that each field matches the
#   declared PrimitiveType.
#   Reason: The output must conform exactly to the defined schema for downstream nodes.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Serialize metrics to native Python types and wrap them in a dict; use
#           `datetime.utcnow().isoformat()` for timestamp.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class ExecuteTradesOutput(BaseModel):
    """Pydantic model for execute_trades node outputs."""
    trade_execution_ids: List[str] = Field(..., description="Unique identifiers for each trade that was executed")
    trade_execution_status: List[bool] = Field(..., description="True if the trade was executed successfully, False otherwise")
    trade_execution_timestamps: List[str] = Field(..., description="ISO\u20118601 timestamps indicating when each trade was executed")
    trade_execution_prices: List[float] = Field(..., description="Price at which each trade was executed")
    trade_execution_quantities: List[float] = Field(..., description="Quantity (in units or shares) executed for each trade")
    trade_execution_instruments: List[str] = Field(..., description="Symbol or instrument identifier for each trade")
    trade_execution_sides: List[str] = Field(..., description="Side of the trade: 'buy' or 'sell' for each execution")
    overall_execution_success: bool = Field(..., description="True if all trades in this batch were executed without error")
    execution_error_messages: List[str] = Field(..., description="Error messages for any trades that failed to execute")


class MonitorTradingPerformanceOutput(BaseModel):
    """Pydantic model for monitor_trading_performance node outputs."""
    timestamp: str = Field(..., description="Current timestamp of the monitoring snapshot")
    total_trades: int = Field(..., description="Total number of trades executed in the monitoring period")
    winning_trades: int = Field(..., description="Number of trades that closed with a profit")
    losing_trades: int = Field(..., description="Number of trades that closed with a loss")
    win_rate: float = Field(..., description="Percentage of winning trades out of total trades (0 to 1)")
    average_return_per_trade: float = Field(..., description="Average profit or loss per trade expressed as a return fraction")
    max_drawdown: float = Field(..., description="Maximum drawdown observed in the monitoring period")
    sharpe_ratio: float = Field(..., description="Sharpe ratio calculated over the monitoring period")
    is_performance_stable: bool = Field(..., description="Flag indicating whether performance metrics are within acceptable ranges")
    recommended_adjustments: str = Field(..., description="List of suggested changes to strategy or risk management rules")
    alert_flag: bool = Field(..., description="Flag indicating if an alert should be triggered due to significant performance deviation")


def monitor_trading_performance(execute_trades_input: ExecuteTradesOutput, **kwargs) -> MonitorTradingPerformanceOutput:
    """Continuously monitors executed trades to calculate performance statistics, detect deviations from expected behavior, recommend strategy adjustments, and trigger alerts when performance deteriorates.

    Args:
        execute_trades_input: Input from the 'execute_trades' node.
        **kwargs: Additional keyword arguments.

    Returns:
        MonitorTradingPerformanceOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return MonitorTradingPerformanceOutput(
        timestamp="",
        total_trades=0,
        winning_trades=0,
        losing_trades=0,
        win_rate=0.0,
        average_return_per_trade=0.0,
        max_drawdown=0.0,
        sharpe_ratio=0.0,
        is_performance_stable=False,
        recommended_adjustments="",
        alert_flag=False,
    )