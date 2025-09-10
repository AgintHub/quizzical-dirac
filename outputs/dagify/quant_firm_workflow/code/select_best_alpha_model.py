# -- PRD --
# 1. BULLET: Retrieve the list of performance metrics for each alpha model from the output
#   of the evaluate_alpha_models node
#   Reason: This is necessary to compare the performance of each alpha model
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the model_performance_metrics field from the evaluate_alpha_models
#           node's output
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify the performance metrics to use for selection, such as return, Sharpe
#   ratio, and risk
#   Reason: These metrics are relevant to evaluating the performance of alpha models
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use domain expertise to select the relevant performance metrics
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Sort the alpha models based on the selected performance metrics
#   Reason: This is necessary to rank the alpha models by their performance
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use a sorting algorithm to rank the alpha models based on the performance
#           metrics
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Select the alpha model with the best performance metrics
#   Reason: This is necessary to choose the best alpha model
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the sorted list of alpha models to select the top-performing model
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Create the output data structure with the selected alpha model's name, return
#   value, Sharpe ratio, risk value, and selection status
#   Reason: This is necessary to provide the output of the select_best_alpha_model node
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a data structure to store the output fields and their values
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class EvaluateAlphaModelsOutput(BaseModel):
    """Pydantic model for evaluate_alpha_models node outputs."""
    model_performance_metrics: List[float] = Field(..., description="List of performance metrics (return, risk, Sharpe ratio) for each alpha model")
    model_rankings: List[int] = Field(..., description="List of rankings for each alpha model based on performance metrics")
    top_performing_model_index: int = Field(..., description="Index of the top performing alpha model")
    evaluation_success: bool = Field(..., description="Whether the evaluation was successful")


class SelectBestAlphaModelOutput(BaseModel):
    """Pydantic model for select_best_alpha_model node outputs."""
    selected_alpha_model_name: str = Field(..., description="Name of the selected alpha model")
    return_value: float = Field(..., description="Return value of the selected alpha model")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected alpha model")
    risk_value: float = Field(..., description="Risk value of the selected alpha model")
    is_selected: bool = Field(..., description="Whether the alpha model is selected as the best")


def select_best_alpha_model(evaluate_alpha_models_input: EvaluateAlphaModelsOutput, **kwargs) -> SelectBestAlphaModelOutput:
    """Select the best alpha model based on performance metrics

    Args:
        evaluate_alpha_models_input: Input from the 'evaluate_alpha_models' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SelectBestAlphaModelOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SelectBestAlphaModelOutput(
        selected_alpha_model_name="",
        return_value=0.0,
        sharpe_ratio=0.0,
        risk_value=0.0,
        is_selected=False,
    )