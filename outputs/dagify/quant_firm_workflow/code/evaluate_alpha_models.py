# -- PRD --
# 1. BULLET: Retrieve the list of alpha model names, types, and performance metrics from
#   the output of the 'build_alpha_models' node
#   Reason: This is necessary to calculate the performance metrics for each alpha model
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output of the 'build_alpha_models' node to get the list of alpha
#           model names, types, and performance metrics
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Calculate the return, risk, and Sharpe ratio for each alpha model using the
#   performance metrics
#   Reason: This is necessary to evaluate the performance of each alpha model
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use financial formulas to calculate the return, risk, and Sharpe ratio for
#           each alpha model
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Rank the alpha models based on their performance metrics
#   Reason: This is necessary to determine the top performing alpha model
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use sorting algorithms to rank the alpha models based on their performance
#           metrics
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Determine the index of the top performing alpha model
#   Reason: This is necessary to identify the best alpha model
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the ranked list of alpha models to determine the index of the top
#           performing alpha model
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Set the evaluation success flag to True if all performance metrics are
#   calculated successfully
#   Reason: This is necessary to indicate whether the evaluation was successful
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a boolean flag to indicate whether the evaluation was successful
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class BuildAlphaModelsOutput(BaseModel):
    """Pydantic model for build_alpha_models node outputs."""
    model_names: List[str] = Field(..., description="List of names of the trained alpha models")
    model_types: List[str] = Field(..., description="List of types of the trained alpha models (e.g., linear regression, decision trees, random forests)")
    performance_metrics: List[float] = Field(..., description="List of performance metrics for each trained alpha model (e.g., accuracy, precision, recall)")
    features_used: List[str] = Field(..., description="List of engineered features used in the trained alpha models")
    is_valid: bool = Field(..., description="Whether the alpha models are valid and properly trained")


class EvaluateAlphaModelsOutput(BaseModel):
    """Pydantic model for evaluate_alpha_models node outputs."""
    model_performance_metrics: List[float] = Field(..., description="List of performance metrics (return, risk, Sharpe ratio) for each alpha model")
    model_rankings: List[int] = Field(..., description="List of rankings for each alpha model based on performance metrics")
    top_performing_model_index: int = Field(..., description="Index of the top performing alpha model")
    evaluation_success: bool = Field(..., description="Whether the evaluation was successful")


def evaluate_alpha_models(build_alpha_models_input: BuildAlphaModelsOutput, **kwargs) -> EvaluateAlphaModelsOutput:
    """Evaluate the performance of the built alpha models

    Args:
        build_alpha_models_input: Input from the 'build_alpha_models' node.
        **kwargs: Additional keyword arguments.

    Returns:
        EvaluateAlphaModelsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return EvaluateAlphaModelsOutput(
        model_performance_metrics=[],
        model_rankings=[],
        top_performing_model_index=0,
        evaluation_success=False,
    )