# define_hyperparameter_grid PRD

## Description
Set the search space for each model component's hyperparameters.


## Implementation Plan

### 1. Extract the model component list from the parent node `specify_model_architecture` output field `model_components` to verify that both "Gradient Boosting" and "LSTM" are present; abort with a clear error if either component is missing.

| Category | Details |
| --- | --- |
| **Reason** | Ensures alignment between the architecture definition and the hyper‑parameter grid, preventing downstream mismatches. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the `model_components` JSON array, perform a set containment check for the two expected strings, and raise an exception with a descriptive message if validation fails. |

### 2. Define a static dictionary of hyperparameter names and their allowed ranges for Gradient Boosting: {"n_estimators": "100-500", "learning_rate": "0.01-0.1", "max_depth": "3-10", "subsample": "0.6-1.0", "colsample_bytree": "0.6-1.0"}. Extend the dictionary only if the architecture explicitly requests additional GB parameters (e.g., `max_depth`).

| Category | Details |
| --- | --- |
| **Reason** | Provides a comprehensive yet deterministic search space that matches typical best‑practice ranges for tree‑based ensembles. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Hard‑code the mapping in code; optionally load from a configuration file for future extensibility. |

### 3. Define a static dictionary of hyperparameter names and their allowed ranges for the LSTM: {"layers": "1-3", "units": "32-128", "dropout": "0-0.3", "learning_rate": "0.0005-0.01", "batch_size": "32-256"}. Include only those keys that appear in the `model_components` list and that are relevant to an LSTM architecture.

| Category | Details |
| --- | --- |
| **Reason** | Captures the most influential architectural and training hyper‑parameters for recurrent networks while staying within realistic computational budgets. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Same as GB dictionary – hard‑code, with optional external config. |

### 4. Create ordered lists `gb_hyperparameters` and `gb_hyperparameter_ranges` by iterating over the GB dictionary preserving insertion order; similarly create `lstm_hyperparameters` and `lstm_hyperparameter_ranges` from the LSTM dictionary.

| Category | Details |
| --- | --- |
| **Reason** | The output specification explicitly requires ordered parallel arrays; preserving order guarantees deterministic mapping between names and ranges. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use Python's `list(dict.keys())` and `list(dict.values())` constructs. |

### 5. Assemble a combined JSON object with two top‑level keys: "gradient_boosting" mapping hyperparameter names to range strings, and "lstm" mapping hyperparameter names to range strings. Serialize this object with `json.dumps(..., separators=(',', ':'))` to produce a compact string for `hyperparameter_grid_json`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream `train_models` node expects a single JSON‑string representing the full grid; a compact representation reduces token usage and parsing overhead. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | ```python
import json
grid = {
    "gradient_boosting": dict(zip(gb_hyperparameters, gb_hyperparameter_ranges)),
    "lstm": dict(zip(lstm_hyperparameters, lstm_hyperparameter_ranges))
}
hyperparameter_grid_json = json.dumps(grid, separators=(",", ":"))
``` |

### 6. Validate the generated JSON string by loading it back with `json.loads` and confirming that the keys and value counts match the previously created lists; if any discrepancy is found, raise a descriptive exception.

| Category | Details |
| --- | --- |
| **Reason** | Defensive programming prevents silent bugs where list ordering or missing entries could corrupt the hyperparameter search. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Round‑trip parse and compare lengths of dicts to list variables. |

### 7. Return the five output fields (`hyperparameter_grid_json`, `gb_hyperparameters`, `gb_hyperparameter_ranges`, `lstm_hyperparameters`, `lstm_hyperparameter_ranges`) in the exact order defined in the node's output schema.

| Category | Details |
| --- | --- |
| **Reason** | Ensures downstream nodes receive data in the expected format; ordering matters for some orchestration engines. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Package outputs into a dict matching the schema and emit as the node's response. |
