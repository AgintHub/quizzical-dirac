# -- PRD --
# 1. BULLET: Review and synthesize the outputs from the parent nodes, including the chosen
#   trading strategy, asset universe, trading parameters, and risk management
#   framework.
#   Reason: This step ensures that all necessary information is gathered and considered
#           before creating the trading plan.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a checklist to ensure all required information is present and correct.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create a concise description of the chosen trading strategy, including its
#   key components and objectives.
#   Reason: This step provides a clear and concise overview of the trading strategy.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a template to ensure the description covers all necessary points.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Outline the key risk management controls, including position limits, stop-
#   loss rules, and liquidity thresholds.
#   Reason: This step ensures that the trading plan includes effective risk management
#           measures.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a risk management framework template to ensure all necessary controls
#           are included.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Summarize the execution details, outlining how trades will be executed within
#   the trading plan.
#   Reason: This step provides clarity on how the trading plan will be implemented.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a standard template for execution details.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: List the target asset classes and tradable instruments identified for the
#   trading strategy.
#   Reason: This step ensures that the trading plan is specific to the chosen asset
#           universe.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a standard template for listing asset classes and instruments.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Define the numerical trading parameters, including position size, stop-loss
#   level, and take-profit level.
#   Reason: This step ensures that the trading plan includes specific and measurable
#           trading parameters.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a standard template for defining trading parameters.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class DefineAssetUniverseOutput(BaseModel):
    """Pydantic model for define_asset_universe node outputs."""
    asset_classes: List[str] = Field(..., description="List of asset classes and instruments")
    num_assets: int = Field(..., description="Number of assets in the list")
    is_valid: bool = Field(..., description="Whether the asset universe is valid")


class SetTradingParametersOutput(BaseModel):
    """Pydantic model for set_trading_parameters node outputs."""
    position_size: float = Field(..., description="The proportion or size of each position within the portfolio.")
    stop_loss_level: float = Field(..., description="The price level at which a position will be closed to prevent further losses.")
    take_profit_level: float = Field(..., description="The price level at which a position will be closed to lock in profits.")


class DesignRiskManagementFrameworkOutput(BaseModel):
    """Pydantic model for design_risk_management_framework node outputs."""
    risk_controls: List[str] = Field(..., description="List of core risk controls, such as position limits, VaR limits, stop-loss rules, and liquidity thresholds.")
    num_risk_controls: int = Field(..., description="The number of risk controls provided in the list.")


class DevelopTradingPlanOutput(BaseModel):
    """Pydantic model for develop_trading_plan node outputs."""
    strategy_description: str = Field(..., description="A concise description of the chosen trading strategy.")
    risk_management_controls: str = Field(..., description="A list of key risk management controls, including position limits, stop-loss rules, and liquidity thresholds.")
    execution_details: str = Field(..., description="A summary of execution details, outlining how trades will be executed within the trading plan.")
    target_assets: str = Field(..., description="The list of asset classes and tradable instruments identified for the trading strategy.")
    trading_parameters: str = Field(..., description="Defined numerical trading parameters such as position size, stop-loss level, and take-profit level.")


def develop_trading_plan(define_asset_universe_input: DefineAssetUniverseOutput, set_trading_parameters_input: SetTradingParametersOutput, design_risk_management_framework_input: DesignRiskManagementFrameworkOutput, **kwargs) -> DevelopTradingPlanOutput:
    """Create a detailed trading plan including strategy, risk management, and execution details.

    Args:
        define_asset_universe_input: Input from the 'define_asset_universe' node.
        set_trading_parameters_input: Input from the 'set_trading_parameters' node.
        design_risk_management_framework_input: Input from the 'design_risk_management_framework' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DevelopTradingPlanOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DevelopTradingPlanOutput(
        strategy_description="",
        risk_management_controls="",
        execution_details="",
        target_assets="",
        trading_parameters="",
    )