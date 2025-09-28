from ._analyze_trading_results.deserialize_monitoring_snapshot import deserialize_monitoring_snapshot
from ._analyze_trading_results.compute_total_trades import compute_total_trades
from ._analyze_trading_results.calculate_win_rate import calculate_win_rate
from ._analyze_trading_results.calculate_average_return_per_trade import calculate_average_return_per_trade
from ._analyze_trading_results.calculate_max_drawdown import calculate_max_drawdown
from ._analyze_trading_results.calculate_sharpe_ratio import calculate_sharpe_ratio
from ._analyze_trading_results.generate_improvement_suggestions import generate_improvement_suggestions
from ._analyze_trading_results.map_suggestions_to_actions import map_suggestions_to_actions
from ._analyze_trading_results.assess_statistical_significance import assess_statistical_significance
from ._analyze_trading_results.validate_output_schema import validate_output_schema

from pydantic import BaseModel, Field


# -- PRD --
# 1. BULLET: Retrieve the monitoring snapshot data from the parent node
#   "monitor_trading_performance" and deserialize it into a structured
#   dictionary using the predefined JSON schema.
#   Reason: Ensures type safety and consistency with downstream processing.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a JSON parsing library (e.g., Python's json module) and validate
#           against the schema; handle missing keys with default values.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Compute "total_trades" by summing the provided "total_trades" from the parent
#   snapshot; if missing, calculate as winning_trades + losing_trades.
#   Reason: Accurate trade count is essential for all subsequent metrics.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Apply integer addition; include a sanity check that the resulting count
#           matches the length of any trade ID list if available.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Derive "win_rate" by dividing the number of winning trades by the total
#   trades, ensuring a division‑by‑zero guard that returns 0.0 when
#   total_trades is zero.
#   Reason: Provides a normalized performance indicator.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use float division; encapsulate in a try/except block for
#           ZeroDivisionError.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate "average_return_per_trade" by taking the parent snapshot’s
#   "average_return_per_trade"; if not available, compute using the
#   cumulative profit/loss over all trades divided by total_trades.
#   Reason: Standardized metric for trade profitability.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: If cumulative return is provided, divide by total_trades; otherwise, parse
#           individual trade returns from the parent data if available.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Determine "max_drawdown" by retrieving the parent snapshot’s "max_drawdown"
#   value; if absent, compute it by scanning the equity curve provided in the
#   snapshot (e.g., using peak‑to‑trough algorithm).
#   Reason: Max drawdown is a critical risk metric.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement a one‑pass algorithm that tracks running maximum equity and
#           calculates drawdowns; handle missing equity data gracefully.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Compute "sharpe_ratio" by retrieving the parent snapshot’s "sharpe_ratio"; if
#   absent, compute it using the formula (mean return - risk‑free rate) / std
#   deviation of returns, assuming a risk‑free rate of 0.01 (1%).
#   Reason: Sharpe ratio contextualizes return relative to volatility.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use NumPy or Pandas to calculate mean and std; apply the Sharpe formula;
#           round to four decimals.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Generate "improvement_suggestions" by performing a rule‑based analysis:
#   compare computed metrics against target thresholds (e.g., win_rate >
#   0.55, max_drawdown < 0.15, Sharpe > 1.0). For any metric that falls below
#   its target, add a concise suggestion.
#   Reason: Provides actionable insights without requiring deep statistical modeling.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Define a dictionary of thresholds; iterate over metrics; append strings
#           like "Improve stop‑loss granularity" or "Increase position
#           sizing discipline" based on the shortfall.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Translate each suggestion in "improvement_suggestions" into a concrete
#   "action_item" by mapping common suggestions to specific tasks (e.g.,
#   "Adjust stop‑loss to 1.5% of entry price").
#   Reason: Transforms high‑level ideas into implementable actions.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a mapping table or simple templating; if a suggestion is already
#           actionable, reuse it verbatim.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Assess "is_significant_change" by conducting a simple statistical test: if
#   the difference between observed win_rate and expected win_rate (e.g.,
#   0.6) is greater than 2 standard deviations of win_rate across historical
#   periods, flag as true.
#   Reason: Provides a quantitative check for anomalous performance.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Fetch historical win_rate distribution from a persisted dataset; compute
#           mean and std; apply z‑score threshold (e.g., |z| > 2).
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Validate the final output dictionary against the defined schema, ensuring all
#   fields are present and correctly typed before serializing to JSON.
#   Reason: Guarantees compatibility with downstream nodes.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Implement a schema validator (e.g., jsonschema) that checks data types and
#           required fields.
# -- END PRD --



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


class AnalyzeTradingResultsOutput(BaseModel):
    """Pydantic model for analyze_trading_results node outputs."""
    total_trades: int = Field(..., description="Total number of trades executed during the monitored period.")
    win_rate: float = Field(..., description="Ratio of winning trades to total trades, expressed as a decimal between 0 and 1.")
    average_return_per_trade: float = Field(..., description="Mean return (profit or loss) per trade expressed as a decimal (e.g., 0.02 for 2%).")
    max_drawdown: float = Field(..., description="Maximum percentage drop from a peak to a trough in equity during the period.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the strategy over the monitored period.")
    improvement_suggestions: str = Field(..., description="List of concise suggestions for strategy or risk management enhancements.")
    action_items: str = Field(..., description="Concrete action items derived from the suggestions, ready for implementation.")
    is_significant_change: bool = Field(..., description="Flag indicating whether the results show a statistically significant deviation from expected performance.")


def analyze_trading_results(monitor_trading_performance_input: MonitorTradingPerformanceOutput, **kwargs) -> AnalyzeTradingResultsOutput:
    """Analyze the results of trading activities to identify areas for improvement.

    Args:
        monitor_trading_performance_input: Input from the 'monitor_trading_performance' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AnalyzeTradingResultsOutput: Object containing outputs for this node.
    """
    # Retrieve and deserialize monitoring snapshot data
    snapshot_data: dict = deserialize_monitoring_snapshot(input_data=monitor_trading_performance_input)
    
    # Compute total trades with fallback calculation
    total_trades: int = compute_total_trades(
        snapshot_total=snapshot_data.get('total_trades'),
        winning_trades=monitor_trading_performance_input.winning_trades,
        losing_trades=monitor_trading_performance_input.losing_trades
    )
    
    # Calculate win rate with division-by-zero guard
    win_rate: float = calculate_win_rate(
        winning_trades=monitor_trading_performance_input.winning_trades,
        total_trades=total_trades
    )
    
    # Derive average return per trade
    average_return_per_trade: float = calculate_average_return_per_trade(
        snapshot_average=monitor_trading_performance_input.average_return_per_trade,
        snapshot_data=snapshot_data,
        total_trades=total_trades
    )
    
    # Determine max drawdown
    max_drawdown: float = calculate_max_drawdown(
        snapshot_drawdown=monitor_trading_performance_input.max_drawdown,
        equity_curve=snapshot_data.get('equity_curve')
    )
    
    # Compute Sharpe ratio
    sharpe_ratio: float = calculate_sharpe_ratio(
        snapshot_sharpe=monitor_trading_performance_input.sharpe_ratio,
        returns_data=snapshot_data.get('returns'),
        risk_free_rate=0.01
    )
    
    # Generate improvement suggestions based on thresholds
    improvement_suggestions: str = generate_improvement_suggestions(
        win_rate=win_rate,
        max_drawdown=max_drawdown,
        sharpe_ratio=sharpe_ratio
    )
    
    # Translate suggestions into concrete action items
    action_items: str = map_suggestions_to_actions(suggestions=improvement_suggestions)
    
    # Assess statistical significance of performance changes
    is_significant_change: bool = assess_statistical_significance(
        observed_win_rate=win_rate,
        historical_data=snapshot_data.get('historical_performance')
    )
    
    # Validate final output against schema
    output_data: dict = {
        'total_trades': total_trades,
        'win_rate': win_rate,
        'average_return_per_trade': average_return_per_trade,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'improvement_suggestions': improvement_suggestions,
        'action_items': action_items,
        'is_significant_change': is_significant_change
    }
    
    validate_output_schema(output_data=output_data)
    
    return AnalyzeTradingResultsOutput(
        total_trades=total_trades,
        win_rate=win_rate,
        average_return_per_trade=average_return_per_trade,
        max_drawdown=max_drawdown,
        sharpe_ratio=sharpe_ratio,
        improvement_suggestions=improvement_suggestions,
        action_items=action_items,
        is_significant_change=is_significant_change
    )