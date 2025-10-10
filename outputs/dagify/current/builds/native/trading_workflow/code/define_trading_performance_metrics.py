# -- PRD --
# 1. BULLET: Review the trading plan and objectives to understand the context for
#   performance metrics.
#   Reason: This ensures that the performance metrics align with the trading plan and
#           objectives.
#   Impact: LOW
#   Complexity: LOW
#   Method: Analyze the trading plan and objectives document.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Research and gather information on the four key performance metrics: return,
#   volatility, Sharpe ratio, and maximum drawdown.
#   Reason: This provides a comprehensive understanding of each metric and its
#           significance in evaluating trading performance.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Conduct a literature review of financial texts, academic papers, and
#           reputable online resources.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Write a one-sentence explanation for each of the four key performance
#   metrics.
#   Reason: This provides a concise and clear description of each metric.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use simple and clear language to describe each metric, ensuring that the
#           explanation is concise and accurate.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Ensure that the explanations for each metric are accurate, concise, and
#   relevant to the trading plan and objectives.
#   Reason: This ensures that the performance metrics are properly understood and
#           applied in the context of the trading plan.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Review and revise the explanations for each metric, using expert judgment
#           and feedback from stakeholders.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Format the output according to the specified output structure.
#   Reason: This ensures that the output is organized and easy to understand.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a template or format guide to ensure consistency in the output
#           structure.
# -- END PRD --

from pydantic import BaseModel, Field


class DevelopTradingPlanOutput(BaseModel):
    """Pydantic model for develop_trading_plan node outputs."""
    strategy_description: str = Field(..., description="A concise description of the chosen trading strategy.")
    risk_management_controls: str = Field(..., description="A list of key risk management controls, including position limits, stop-loss rules, and liquidity thresholds.")
    execution_details: str = Field(..., description="A summary of execution details, outlining how trades will be executed within the trading plan.")
    target_assets: str = Field(..., description="The list of asset classes and tradable instruments identified for the trading strategy.")
    trading_parameters: str = Field(..., description="Defined numerical trading parameters such as position size, stop-loss level, and take-profit level.")


class DefineTradingPerformanceMetricsOutput(BaseModel):
    """Pydantic model for define_trading_performance_metrics node outputs."""
    returns_description: str = Field(..., description="Description of the metric 'return' and its importance for evaluating trading performance.")
    volatility_description: str = Field(..., description="Description of the metric 'volatility' and its role in understanding risk.")
    sharpe_ratio_description: str = Field(..., description="Explanation of how the Sharpe ratio is used as a performance metric.")
    maximum_drawdown_description: str = Field(..., description="Details about the maximum drawdown metric and its significance in performance evaluation.")


def define_trading_performance_metrics(develop_trading_plan_input: DevelopTradingPlanOutput, **kwargs) -> DefineTradingPerformanceMetricsOutput:
    """Specify metrics for evaluating trading performance.

    Args:
        develop_trading_plan_input: Input from the 'develop_trading_plan' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineTradingPerformanceMetricsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DefineTradingPerformanceMetricsOutput(
        returns_description="",
        volatility_description="",
        sharpe_ratio_description="",
        maximum_drawdown_description="",
    )