# -- PRD --
# 1. BULLET: Review the output from the 'set_trading_parameters' node to understand the
#   quantitative trading parameters such as position size, stop-loss level,
#   and take-profit level.
#   Reason: This step ensures that the risk controls are aligned with the trading
#           parameters.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Verify that the output from 'set_trading_parameters' includes position
#           size, stop-loss level, and take-profit level.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify the target metrics for risk management, including position limits,
#   VaR limits, stop-loss rules, and liquidity thresholds.
#   Reason: This step ensures that the risk controls are aligned with the target
#           metrics.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the output from 'set_trading_parameters' to determine the target
#           metrics for risk management.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Define position limits as a risk control to limit the maximum exposure to a
#   single asset or asset class.
#   Reason: This step helps to mitigate the risk of large losses due to over-exposure
#           to a single asset or asset class.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a percentage of the overall portfolio value to determine the position
#           limit.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Define VaR limits as a risk control to limit the potential loss in value of
#   the portfolio over a specific time horizon with a given probability.
#   Reason: This step helps to mitigate the risk of large losses due to market
#           volatility.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use historical data and statistical models to determine the VaR limit.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Define stop-loss rules as a risk control to limit the loss on a single trade
#   or asset.
#   Reason: This step helps to mitigate the risk of large losses due to adverse market
#           movements.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a percentage of the position value to determine the stop-loss level.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Define liquidity thresholds as a risk control to ensure that the portfolio
#   can be liquidated quickly and at a fair price.
#   Reason: This step helps to mitigate the risk of large losses due to illiquidity.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use historical data and market analysis to determine the liquidity
#           thresholds.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class SetTradingParametersOutput(BaseModel):
    """Pydantic model for set_trading_parameters node outputs."""
    position_size: float = Field(..., description="The proportion or size of each position within the portfolio.")
    stop_loss_level: float = Field(..., description="The price level at which a position will be closed to prevent further losses.")
    take_profit_level: float = Field(..., description="The price level at which a position will be closed to lock in profits.")


class DesignRiskManagementFrameworkOutput(BaseModel):
    """Pydantic model for design_risk_management_framework node outputs."""
    risk_controls: List[str] = Field(..., description="List of core risk controls, such as position limits, VaR limits, stop-loss rules, and liquidity thresholds.")
    num_risk_controls: int = Field(..., description="The number of risk controls provided in the list.")


def design_risk_management_framework(set_trading_parameters_input: SetTradingParametersOutput, **kwargs) -> DesignRiskManagementFrameworkOutput:
    """Outline quantitative and qualitative risk controls.

    Args:
        set_trading_parameters_input: Input from the 'set_trading_parameters' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DesignRiskManagementFrameworkOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DesignRiskManagementFrameworkOutput(
        risk_controls=[],
        num_risk_controls=0,
    )