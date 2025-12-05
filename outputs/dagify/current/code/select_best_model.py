# -- PRD --
# 1. BULLET: Retrieve candidate model performance metrics from the 'evaluate_models' node
#   output.
#   Reason: The `evaluate_models` node provides the necessary performance metrics
#           (Sharpe Ratio, Max Drawdown, and Annualized Return) for each
#           candidate model to determine the best performing one.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Access the `candidate_models`, `sharpe_ratios`, `max_drawdowns`, and
#           `annualized_returns` lists from the `evaluate_models` node's
#           output.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a selection criterion based on Sharpe ratio and maximum drawdown,
#   prioritizing Sharpe Ratio subject to a Max Drawdown threshold.
#   Reason: The prompt specifies selecting the model with the 'best combination of
#           Sharpe and low max drawdown'. A sensible approach is to
#           maximize the Sharpe Ratio while ensuring the Max Drawdown is
#           below a predefined risk tolerance threshold.  This reflects a
#           risk-adjusted return perspective.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Define a `max_drawdown_threshold` (e.g., 0.15 for 15%). Iterate through the
#           models. If a model's Max Drawdown is *less than or equal to*
#           the `max_drawdown_threshold`, store it in a list of valid model
#           candidates. From these valid model candidates, choose the model
#           with the highest Sharpe Ratio.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle the case where no model satisfies the risk tolerance threshold (max
#   drawdown constraint).
#   Reason: It's possible that none of the candidate models meets the Max Drawdown
#           threshold, especially if the financial climate was particularly
#           turbulent during backtesting.  The strategy should degrade
#           gracefully if no model meets the hard constraints.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: If no model satisfies the `max_drawdown_threshold`, select the model with
#           the absolute LOWEST max drawdown. If all the models have very
#           high drawdowns, choose one that has a 'reasonable' Sharpe
#           Ratio. If even that is not avaialble, return null/None for all
#           outputs. Log a warning message to indicate this exceptional
#           case.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Extract the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and
#   'annualized_return' for selected best model.
#   Reason: The output structure requires the model's identifier and its key metrics.
#           This step formats the selected values into the defined output
#           structure.
#   Impact: HIGH
#   Complexity: LOW
#   Method: After identifying the best model index, retrieve the corresponding values
#           from the `candidate_models`, `sharpe_ratios`, `max_drawdowns`,
#           and `annualized_returns` lists. Store the values into output
#           variables named: `best_model_identifier`, `sharpe_ratio`,
#           `max_drawdown`, and `annualized_return`
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Return the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and
#   'annualized_return'.
#   Reason: Deliver required data.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Return the variables created above. The return types must be enforced with
#           exception handling or type coercion to meet the requested
#           output structure types.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class EvaluateModelsOutput(BaseModel):
    """Pydantic model for evaluate_models node outputs."""
    candidate_models: List[str] = Field(..., description="Identifier or name of each evaluated model candidate.")
    sharpe_ratios: List[float] = Field(..., description="Sharpe ratio for each model on the test set.")
    annualized_returns: List[float] = Field(..., description="Annualized return (in percent) for each model on the test set.")
    max_drawdowns: List[float] = Field(..., description="Maximum drawdown (in percent) observed for each model on the test set.")
    turnovers: List[float] = Field(..., description="Average portfolio turnover (as a percent of portfolio per period) for each model.")
    hit_rates: List[float] = Field(..., description="Proportion of trades with positive return (hit\u2011rate) for each model.")
    ranks: List[int] = Field(..., description="Rank of each model based on the chosen composite performance criterion (1 = best).")


class SelectBestModelOutput(BaseModel):
    """Pydantic model for select_best_model node outputs."""
    best_model_identifier: str = Field(..., description="Identifier of the selected best model.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected model.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the selected model.")
    annualized_return: float = Field(..., description="Annualized return of the selected model.")


def select_best_model(evaluate_models_input: EvaluateModelsOutput, **kwargs) -> SelectBestModelOutput:
    """Pick the model with the highest risk‑adjusted performance according to a predefined criterion.

    Args:
        evaluate_models_input: Input from the 'evaluate_models' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SelectBestModelOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SelectBestModelOutput(
        best_model_identifier="",
        sharpe_ratio=0.0,
        max_drawdown=0.0,
        annualized_return=0.0,
    )