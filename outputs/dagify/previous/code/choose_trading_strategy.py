# -- PRD --
# 1. BULLET: Review the trading objectives provided by the 'define_trading_objectives'
#   node to understand the purpose, risk tolerance, and long-term vision of
#   the trading system.
#   Reason: This step ensures that the selected trading strategy aligns with the
#           overall goals of the trading system.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Analyze the bullet list of trading objectives to identify key themes and
#           priorities.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Research and list potential high-level trading strategy categories that could
#   achieve the trading objectives (e.g., trend following, mean reversion,
#   statistical arbitrage).
#   Reason: This step provides a comprehensive set of potential strategies to consider.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Utilize domain expertise and literature review to compile a list of
#           relevant trading strategies.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Evaluate each potential trading strategy category against the trading
#   objectives, considering factors such as risk tolerance, potential
#   returns, and complexity.
#   Reason: This step enables an informed decision about which strategy best aligns
#           with the trading objectives.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Apply a decision-making framework, such as a weighted scoring model, to
#           assess each strategy's suitability.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Select the primary trading strategy category that best serves the trading
#   objectives and provide a one-sentence rationale for the selection.
#   Reason: This step formalizes the chosen strategy and justifies the decision.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Document the selected strategy and rationale in a clear and concise manner.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class DefineTradingObjectivesOutput(BaseModel):
    """Pydantic model for define_trading_objectives node outputs."""
    trading_objectives: List[str] = Field(..., description="A bullet list of the core trading system's objectives, including purpose, risk tolerance, and long-term vision. Max8 items.")


class ChooseTradingStrategyOutput(BaseModel):
    """Pydantic model for choose_trading_strategy node outputs."""
    selected_strategy: str = Field(..., description="The name of the selected high-level trading strategy category.")
    rationale: str = Field(..., description="A one-sentence explanation of why the selected trading strategy was chosen.")


def choose_trading_strategy(define_trading_objectives_input: DefineTradingObjectivesOutput, **kwargs) -> ChooseTradingStrategyOutput:
    """Identify the high-level trading strategy category.

    Args:
        define_trading_objectives_input: Input from the 'define_trading_objectives' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ChooseTradingStrategyOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return ChooseTradingStrategyOutput(
        selected_strategy="",
        rationale="",
    )