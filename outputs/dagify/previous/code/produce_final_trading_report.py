from pydantic import BaseModel, Field
from typing import List


class DevelopTradingPlanOutput(BaseModel):
    """Pydantic model for develop_trading_plan node outputs."""
    strategy_description: str = Field(..., description="A concise description of the chosen trading strategy.")
    risk_management_controls: str = Field(..., description="A list of key risk management controls, including position limits, stop-loss rules, and liquidity thresholds.")
    execution_details: str = Field(..., description="A summary of execution details, outlining how trades will be executed within the trading plan.")
    target_assets: str = Field(..., description="The list of asset classes and tradable instruments identified for the trading strategy.")
    trading_parameters: str = Field(..., description="Defined numerical trading parameters such as position size, stop-loss level, and take-profit level.")


class CompileTradingDashboardOutlineOutput(BaseModel):
    """Pydantic model for compile_trading_dashboard_outline node outputs."""
    dashboard_slide_titles: List[str] = Field(..., description="A list of slide titles outlining the trading performance dashboard, covering strategy, risk, and performance metrics.")


class DefineTradingPerformanceMetricsOutput(BaseModel):
    """Pydantic model for define_trading_performance_metrics node outputs."""
    returns_description: str = Field(..., description="Description of the metric 'return' and its importance for evaluating trading performance.")
    volatility_description: str = Field(..., description="Description of the metric 'volatility' and its role in understanding risk.")
    sharpe_ratio_description: str = Field(..., description="Explanation of how the Sharpe ratio is used as a performance metric.")
    maximum_drawdown_description: str = Field(..., description="Details about the maximum drawdown metric and its significance in performance evaluation.")


class ProduceFinalTradingReportOutput(BaseModel):
    """Pydantic model for produce_final_trading_report node outputs."""
    trading_strategy_summary: str = Field(..., description="A concise summary of the trading strategy.")
    risk_management_summary: str = Field(..., description="A concise summary of the risk management framework.")
    performance_metrics_summary: str = Field(..., description="A concise summary of the trading performance metrics.")
    key_insights: List[str] = Field(..., description="A list of key takeaways or insights from the trading system summary.")


def produce_final_trading_report(develop_trading_plan_input: DevelopTradingPlanOutput, compile_trading_dashboard_outline_input: CompileTradingDashboardOutlineOutput, define_trading_performance_metrics_input: DefineTradingPerformanceMetricsOutput, **kwargs) -> ProduceFinalTradingReportOutput:
    """Generate an all-in summary of the trading system.

    Args:
        develop_trading_plan_input: Input from the 'develop_trading_plan' node.
        compile_trading_dashboard_outline_input: Input from the 'compile_trading_dashboard_outline' node.
        define_trading_performance_metrics_input: Input from the 'define_trading_performance_metrics' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ProduceFinalTradingReportOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return ProduceFinalTradingReportOutput(
        trading_strategy_summary="",
        risk_management_summary="",
        performance_metrics_summary="",
        key_insights=[],
    )