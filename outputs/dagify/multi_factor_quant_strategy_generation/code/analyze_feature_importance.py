# -- PRD --
# 1. BULLET: Retrieve the best model identifier from the output of the `select_best_model`
#   node.
#   Reason: The `model_id` is required to load the selected model for feature
#           importance analysis.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Access the `best_model_identifier` field from the `select_best_model`
#           node's output.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Load the feature matrix from the CSV string provided in the
#   `feature_matrix_csv` field of the `assemble_feature_matrix` node's
#   output.
#   Reason: The model needs the feature data used for training to determine feature
#           importances. Loading from CSV ensures consistent data format.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a CSV parsing library (e.g., pandas in Python) to load the
#           `feature_matrix_csv` into a dataframe.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Load the selected model based on the `model_id` retrieved earlier. Assume a
#   model registry or loading function exists. If the model ID contains
#   information about the model type, use that.
#   Reason: The model needs to be loaded to calculate feature importances based on its
#           internal structure or through permutation methods.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement a model registry or loading function that maps `model_id` to a
#           corresponding model object. Handle potential errors like model
#           not found.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Determine feature importance ranking method. If the model is a tree-based
#   model (e.g., Gradient Boosting), use 'gain' (mean decrease in impurity).
#   If the model is linear/logistic regression, use coefficients as the
#   importance score. If the above are not applicable, or if specified in
#   configuration, use SHAP values.
#   Reason: Different model types have different methods for determining feature
#           importance. This step selects the appropriate method.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Implement a conditional logic to select the feature importance method based
#           on the model type. Account for cases where feature importance
#           is not available through direct model introspection. Allow
#           overriding this choice using external config parameters.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compute feature importances using the chosen method. For 'gain', extract the
#   feature importances directly from the model. For SHAP values, use a SHAP
#   explainer on a subset of the feature matrix.
#   Reason: This is the core step where the feature importances are calculated.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use model-specific methods to compute feature importances. For tree based
#           models, use `model.feature_importances_`. For SHAP, instantiate
#           a `shap.Explainer` object with the model (or model's prediction
#           function) and compute SHAP values for a representative sample
#           of the data.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Rank the features based on their importance scores in descending order.
#   Reason: The ranked list provides the most relevant features at the top.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Sort the feature names based on the corresponding importance scores using a
#           sorting algorithm (e.g., `sorted` function in Python with
#           `reverse=True`).
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Extract the sorted feature names and corresponding importance scores into
#   separate lists.
#   Reason: This prepares the data for the output structure.
#   Impact: LOW
#   Complexity: LOW
#   Method: Unzip the sorted list of tuples (feature name, importance score).
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Populate the output structure with the `model_id`, sorted `feature_names`,
#   `importance_scores`, and `ranking_method`.
#   Reason: This provides the results in the required format.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Assign the calculated values to the corresponding fields in the output
#           dictionary.
# -- END PRD --

from pydantic import BaseModel, Field


class SelectBestModelOutput(BaseModel):
    """Pydantic model for select_best_model node outputs."""
    best_model_identifier: str = Field(..., description="Identifier of the selected best model.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected model.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the selected model.")
    annualized_return: float = Field(..., description="Annualized return of the selected model.")


class AssembleFeatureMatrixOutput(BaseModel):
    """Pydantic model for assemble_feature_matrix node outputs."""
    feature_matrix_csv: str = Field(..., description="CSV\u2011formatted string containing the complete feature matrix with a Date column, all merged feature columns, and a Target column for the next\u2011day return.")


class AnalyzeFeatureImportanceOutput(BaseModel):
    """Pydantic model for analyze_feature_importance node outputs."""
    model_id: str = Field(..., description="Identifier of the model selected as best (e.g., \"GBM_v1\" or \"LSTM_ensemble\")")
    feature_names: str = Field(..., description="List of feature names sorted from most to least important")
    importance_scores: float = Field(..., description="Corresponding importance scores for each feature in feature_names (higher means more important)")
    ranking_method: str = Field(..., description="Method used to compute importance (e.g., \"SHAP\", \"gain\", \"permutation\")")


def analyze_feature_importance(select_best_model_input: SelectBestModelOutput, assemble_feature_matrix_input: AssembleFeatureMatrixOutput, **kwargs) -> AnalyzeFeatureImportanceOutput:
    """Compute and report the importance of each feature for the selected model.

    Args:
        select_best_model_input: Input from the 'select_best_model' node.
        assemble_feature_matrix_input: Input from the 'assemble_feature_matrix' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AnalyzeFeatureImportanceOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return AnalyzeFeatureImportanceOutput(
        model_id="",
        feature_names="",
        importance_scores=0.0,
        ranking_method="",
    )