# -- PRD --
# 1. BULLET: Import necessary libraries and load the engineered features and selected
#   alpha factors
#   Reason: This step is necessary to ensure that all required libraries are imported
#           and data is loaded correctly
#   Impact: LOW
#   Complexity: LOW
#   Method: Use Python's scikit-learn library for machine learning, pandas for data
#           manipulation, and numpy for numerical computations
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Preprocess the engineered features and selected alpha factors by handling
#   missing values and scaling/normalizing the data
#   Reason: This step is necessary to ensure that the data is clean and in a suitable
#           format for training machine learning models
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use techniques such as mean/median imputation for missing values, and
#           StandardScaler or MinMaxScaler for scaling/normalizing data
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Split the preprocessed data into training and testing sets
#   Reason: This step is necessary to evaluate the performance of the trained models on
#           unseen data
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use techniques such as train_test_split from scikit-learn
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Train machine learning models using the training data, including linear
#   regression, decision trees, and random forests
#   Reason: This step is necessary to build the alpha models
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use techniques such as LinearRegression, DecisionTreeRegressor, and
#           RandomForestRegressor from scikit-learn
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Evaluate the performance of the trained models on the testing data
#   Reason: This step is necessary to assess the performance of the alpha models
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use techniques such as mean squared error, mean absolute error, and
#           R-squared to evaluate model performance
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Store the trained models, their performance metrics, and the engineered
#   features used
#   Reason: This step is necessary to save the results of the alpha model training
#   Impact: LOW
#   Complexity: LOW
#   Method: Use techniques such as pickling or saving to a file
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class FeatureEngineeringOutput(BaseModel):
    """Pydantic model for feature_engineering node outputs."""
    feature_names: List[str] = Field(..., description="List of engineered feature names")
    feature_values: List[float] = Field(..., description="List of engineered feature values corresponding to each feature name")
    feature_descriptions: List[str] = Field(..., description="List of descriptions for each engineered feature")


class SelectAlphaFactorsOutput(BaseModel):
    """Pydantic model for select_alpha_factors node outputs."""
    selected_alpha_factors: List[str] = Field(..., description="List of selected alpha factors (e.g., momentum, mean reversion, statistical arbitrage)")
    alpha_factor_descriptions: List[str] = Field(..., description="List of descriptions for each selected alpha factor")
    is_valid_selection: bool = Field(..., description="Whether the selected alpha factors are valid and suitable for alpha discovery")


class BuildAlphaModelsOutput(BaseModel):
    """Pydantic model for build_alpha_models node outputs."""
    model_names: List[str] = Field(..., description="List of names of the trained alpha models")
    model_types: List[str] = Field(..., description="List of types of the trained alpha models (e.g., linear regression, decision trees, random forests)")
    performance_metrics: List[float] = Field(..., description="List of performance metrics for each trained alpha model (e.g., accuracy, precision, recall)")
    features_used: List[str] = Field(..., description="List of engineered features used in the trained alpha models")
    is_valid: bool = Field(..., description="Whether the alpha models are valid and properly trained")


def build_alpha_models(feature_engineering_input: FeatureEngineeringOutput, select_alpha_factors_input: SelectAlphaFactorsOutput, **kwargs) -> BuildAlphaModelsOutput:
    """Build alpha models using the selected alpha factors and engineered features

    Args:
        feature_engineering_input: Input from the 'feature_engineering' node.
        select_alpha_factors_input: Input from the 'select_alpha_factors' node.
        **kwargs: Additional keyword arguments.

    Returns:
        BuildAlphaModelsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return BuildAlphaModelsOutput(
        model_names=[],
        model_types=[],
        performance_metrics=[],
        features_used=[],
        is_valid=False,
    )