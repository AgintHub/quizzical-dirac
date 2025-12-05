# -- PRD --
# 1. BULLET: Extract the model component list from the parent node
#   `specify_model_architecture` output field `model_components` to verify
#   that both "Gradient Boosting" and "LSTM" are present; abort with a clear
#   error if either component is missing.
#   Reason: Ensures alignment between the architecture definition and the
#           hyper‑parameter grid, preventing downstream mismatches.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Read the `model_components` JSON array, perform a set containment check for
#           the two expected strings, and raise an exception with a
#           descriptive message if validation fails.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Define a static dictionary of hyperparameter names and their allowed ranges
#   for Gradient Boosting: {"n_estimators": "100-500", "learning_rate":
#   "0.01-0.1", "max_depth": "3-10", "subsample": "0.6-1.0",
#   "colsample_bytree": "0.6-1.0"}. Extend the dictionary only if the
#   architecture explicitly requests additional GB parameters (e.g.,
#   `max_depth`).
#   Reason: Provides a comprehensive yet deterministic search space that matches
#           typical best‑practice ranges for tree‑based ensembles.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Hard‑code the mapping in code; optionally load from a configuration file
#           for future extensibility.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Define a static dictionary of hyperparameter names and their allowed ranges
#   for the LSTM: {"layers": "1-3", "units": "32-128", "dropout": "0-0.3",
#   "learning_rate": "0.0005-0.01", "batch_size": "32-256"}. Include only
#   those keys that appear in the `model_components` list and that are
#   relevant to an LSTM architecture.
#   Reason: Captures the most influential architectural and training hyper‑parameters
#           for recurrent networks while staying within realistic
#           computational budgets.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Same as GB dictionary – hard‑code, with optional external config.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Create ordered lists `gb_hyperparameters` and `gb_hyperparameter_ranges` by
#   iterating over the GB dictionary preserving insertion order; similarly
#   create `lstm_hyperparameters` and `lstm_hyperparameter_ranges` from the
#   LSTM dictionary.
#   Reason: The output specification explicitly requires ordered parallel arrays;
#           preserving order guarantees deterministic mapping between names
#           and ranges.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use Python's `list(dict.keys())` and `list(dict.values())` constructs.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Assemble a combined JSON object with two top‑level keys: "gradient_boosting"
#   mapping hyperparameter names to range strings, and "lstm" mapping
#   hyperparameter names to range strings. Serialize this object with
#   `json.dumps(..., separators=(',', ':'))` to produce a compact string for
#   `hyperparameter_grid_json`.
#   Reason: The downstream `train_models` node expects a single JSON‑string
#           representing the full grid; a compact representation reduces
#           token usage and parsing overhead.
#   Impact: HIGH
#   Complexity: LOW
#   Method: ```python import json grid = {     "gradient_boosting":
#           dict(zip(gb_hyperparameters, gb_hyperparameter_ranges)),
#           "lstm": dict(zip(lstm_hyperparameters,
#           lstm_hyperparameter_ranges)) } hyperparameter_grid_json =
#           json.dumps(grid, separators=(",", ":")) ```
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Validate the generated JSON string by loading it back with `json.loads` and
#   confirming that the keys and value counts match the previously created
#   lists; if any discrepancy is found, raise a descriptive exception.
#   Reason: Defensive programming prevents silent bugs where list ordering or missing
#           entries could corrupt the hyperparameter search.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Round‑trip parse and compare lengths of dicts to list variables.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Return the five output fields (`hyperparameter_grid_json`,
#   `gb_hyperparameters`, `gb_hyperparameter_ranges`, `lstm_hyperparameters`,
#   `lstm_hyperparameter_ranges`) in the exact order defined in the node's
#   output schema.
#   Reason: Ensures downstream nodes receive data in the expected format; ordering
#           matters for some orchestration engines.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Package outputs into a dict matching the schema and emit as the node's
#           response.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class SpecifyModelArchitectureOutput(BaseModel):
    """Pydantic model for specify_model_architecture node outputs."""
    model_ensemble_description: str = Field(..., description="A concise description of the chosen model ensemble architecture.")
    model_components: str = Field(..., description="List of individual model components (e.g., Gradient Boosting, LSTM).")
    input_shape: str = Field(..., description="The shape of the input data expected by the model.")
    prediction_combination_method: str = Field(..., description="How the predictions from individual components are combined (e.g., averaging, stacking).")


class DefineHyperparameterGridOutput(BaseModel):
    """Pydantic model for define_hyperparameter_grid node outputs."""
    hyperparameter_grid_json: str = Field(..., description="A JSON\u2011formatted string that contains the full hyperparameter search space for both Gradient Boosting and LSTM models.")
    gb_hyperparameters: List[str] = Field(..., description="List of Gradient Boosting hyperparameter names (e.g., "n_estimators", "learning_rate").")
    gb_hyperparameter_ranges: List[str] = Field(..., description="List of corresponding ranges for each Gradient Boosting hyperparameter, expressed as strings (e.g., "100-500", "0.01-0.1"). Order matches `gb_hyperparameters`.")
    lstm_hyperparameters: List[str] = Field(..., description="List of LSTM hyperparameter names (e.g., "layers", "units", "dropout").")
    lstm_hyperparameter_ranges: List[str] = Field(..., description="List of corresponding ranges for each LSTM hyperparameter, expressed as strings (e.g., "1-3", "32-128", "0-0.3"). Order matches `lstm_hyperparameters`.")


def define_hyperparameter_grid(specify_model_architecture_input: SpecifyModelArchitectureOutput, **kwargs) -> DefineHyperparameterGridOutput:
    """Set the search space for each model component's hyperparameters.

    Args:
        specify_model_architecture_input: Input from the 'specify_model_architecture' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineHyperparameterGridOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DefineHyperparameterGridOutput(
        hyperparameter_grid_json="",
        gb_hyperparameters=[],
        gb_hyperparameter_ranges=[],
        lstm_hyperparameters=[],
        lstm_hyperparameter_ranges=[],
    )