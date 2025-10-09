# -- PRD --
# 1. BULLET: Review the selected trading strategy from the 'choose_trading_strategy' node
#   to understand the asset classes and instruments that align with the
#   strategy.
#   Reason: Ensure that the asset universe is consistent with the chosen trading
#           strategy.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'choose_trading_strategy' node, specifically the
#           'selected_strategy' field.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify a list of asset classes and instruments that are relevant to the
#   selected trading strategy, keeping in mind market liquidity, trading
#   hours, and other factors.
#   Reason: Create a relevant and tradable asset universe.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use market data and research to identify asset classes and instruments,
#           consider factors such as market capitalization, liquidity, and
#           volatility.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Limit the list of asset classes and instruments to 10 or fewer items to
#   ensure a focused asset universe.
#   Reason: Prevent over-diversification and ensure manageability.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a filtering process to narrow down the list of asset classes and
#           instruments.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Validate the asset universe by checking for duplicates, ensuring that the
#   listed asset classes and instruments are tradable, and verifying that
#   they align with the selected trading strategy.
#   Reason: Ensure accuracy and validity of the asset universe.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use data validation techniques and review the list against the trading
#           strategy and market data.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Output the list of asset classes and instruments, the number of assets in the
#   list, and a boolean indicating whether the asset universe is valid.
#   Reason: Provide a clear and usable output for downstream nodes.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output structure defined for this node to format the output.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class ChooseTradingStrategyOutput(BaseModel):
    """Pydantic model for choose_trading_strategy node outputs."""
    selected_strategy: str = Field(..., description="The name of the selected high-level trading strategy category.")
    rationale: str = Field(..., description="A one-sentence explanation of why the selected trading strategy was chosen.")


class DefineAssetUniverseOutput(BaseModel):
    """Pydantic model for define_asset_universe node outputs."""
    asset_classes: List[str] = Field(..., description="List of asset classes and instruments")
    num_assets: int = Field(..., description="Number of assets in the list")
    is_valid: bool = Field(..., description="Whether the asset universe is valid")


def define_asset_universe(choose_trading_strategy_input: ChooseTradingStrategyOutput, **kwargs) -> DefineAssetUniverseOutput:
    """Enumerate tradable assets and instruments.

    Args:
        choose_trading_strategy_input: Input from the 'choose_trading_strategy' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineAssetUniverseOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DefineAssetUniverseOutput(
        asset_classes=[],
        num_assets=0,
        is_valid=False,
    )