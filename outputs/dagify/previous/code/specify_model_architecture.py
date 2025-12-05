# -- PRD --
# 1. BULLET: Define the specific model ensemble: Gradient Boosting Machine (GBM) followed
#   by a Long Short-Term Memory (LSTM) network.
#   Reason: This ensemble combines the strengths of GBM for feature importance and non-
#           linear relationships with LSTM's ability to capture temporal
#           dependencies in financial time series, fitting the strategy
#           objectives.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Choose GBM from the scikit-learn library and LSTM from TensorFlow/Keras.
#           Use a sequential model construction in Keras for easy stacking.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Determine the input shape for the ensemble. Assume a time series of N
#   features over a window of T days. Hence, the input shape will be (T, N).
#   The T value will likely be decided based on the asset's holding period as
#   derived from the output of `define_strategy_objectives`
#   Reason: The input shape is critical for both models. LSTM needs a time series of
#           data. Features are generated in prior nodes
#           (compute_price_action_features, compute_cross_asset_features,
#           compute_regime_features, compute_volatility_features), so shape
#           N is informed by the aggregate features.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Inspect the features computed by the previous nodes (price action, cross-
#           asset, regime, volatility) to determine the total number of
#           features (N). Set T based on a fraction of the
#           `holding_period_days` from `define_strategy_objectives`. For
#           instance if holding period is 60 days, then T can be set to 30
#           days.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Specify that the Gradient Boosting Machine will process the feature matrix
#   first. It will output feature importance scores and potentially
#   transformed features.
#   Reason: GBM offers good feature engineering. Choosing GBM allows transforming
#           existing features into a representation which improves the
#           LSTM's performance. LSTM learns better from well-engineered, or
#           pre-selected features.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Train GBM to produce a prediction. Extract the relative feature
#           importances. Optionally use Tree-based Feature
#           Selection/Transformation techniques from scikit-learn before
#           inputting to LSTM.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Describe how the predictions from GBM and LSTM will be combined using a
#   stacking approach. GBM output are treated as additional features and
#   input into LSTM, or averaged together.
#   Reason: Stacking enables the model to learn how to best combine information from
#           each component, creating a more robust and accurate prediction.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement stacking/averaging in Keras. For the staking approach, the
#           features from the GBM predictions are combined with the
#           original set of features and used together as input features
#           into the LSTM network. Train stacked LSTM to combine both
#           feature types.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Generate a textual `model_ensemble_description` summarizing the chosen
#   architecture, including the algorithm for each component, input shape,
#   and prediction combination method. Respect the 200 word limit.
#   Reason: The text description provides human-readable documentation of the model
#           ensemble.
#   Impact: LOW
#   Complexity: LOW
#   Method: Create a formatted string combining the model components, input shape, and
#           prediction combination method.  Use f-strings for string
#           formatting and truncate if string exceeds 200 words or less.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Populate the `model_components` list with string names, e.g., ['Gradient
#   Boosting Machine', 'LSTM'].
#   Reason: Provides a clear and structured list of separate model types.
#   Impact: LOW
#   Complexity: LOW
#   Method: Create a list literals.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Generate a clear representation of `input_shape` as a string. E.g., '(30,
#   15)' representing 30 days of 15 features.
#   Reason: Allows downstream systems to automatically configure the data based on
#           expected form.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Format N and T values derived in bullet 2 into a Tuple format for the
#           string representation.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Create a textual description of ``prediction_combination_method``, explaining
#   how component predictions are combined (e.g., 'Predictions from gradient
#   boosting are averaged with LSTM predictions').
#   Reason: Provides a downstream explanation of how final signal is generated from
#           constituent models.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a text description of stackng, weighting or averaging depending on the
#           specific implementation in bullet point 4.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class DefineStrategyObjectivesOutput(BaseModel):
    """Pydantic model for define_strategy_objectives node outputs."""
    primary_tradable_asset: str = Field(..., description="Ticker or identifier of the main asset the strategy will trade")
    asset_universe: List[str] = Field(..., description="List of all assets (tickers or identifiers) considered in the strategy")
    desired_annual_return_pct: float = Field(..., description="Target annualized return expressed as a percentage (e.g., 12.5 for 12.5%)")
    risk_tolerance_max_drawdown_pct: float = Field(..., description="Maximum acceptable drawdown expressed as a percentage of capital")
    holding_period_days: int = Field(..., description="Typical holding period for positions in days")
    regulatory_constraints: List[str] = Field(..., description="List of regulatory or compliance constraints affecting the strategy (e.g., short\u2011selling bans, leverage limits)")


class SpecifyModelArchitectureOutput(BaseModel):
    """Pydantic model for specify_model_architecture node outputs."""
    model_ensemble_description: str = Field(..., description="A concise description of the chosen model ensemble architecture.")
    model_components: str = Field(..., description="List of individual model components (e.g., Gradient Boosting, LSTM).")
    input_shape: str = Field(..., description="The shape of the input data expected by the model.")
    prediction_combination_method: str = Field(..., description="How the predictions from individual components are combined (e.g., averaging, stacking).")


def specify_model_architecture(define_strategy_objectives_input: DefineStrategyObjectivesOutput, **kwargs) -> SpecifyModelArchitectureOutput:
    """Choose a concrete predictive model type (e.g., Gradient Boosting + LSTM ensemble).

    Args:
        define_strategy_objectives_input: Input from the 'define_strategy_objectives' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SpecifyModelArchitectureOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SpecifyModelArchitectureOutput(
        model_ensemble_description="",
        model_components="",
        input_shape="",
        prediction_combination_method="",
    )