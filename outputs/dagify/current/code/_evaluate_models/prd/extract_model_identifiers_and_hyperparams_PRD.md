# extract_model_identifiers_and_hyperparams PRD

## Description
Parses a list of hyperparameter strings into a JSON‑encoded dictionary that maps each generated model identifier to its hyperparameter configuration.


## Implementation Plan

### 1. Parse each hyperparameter string into a Python dictionary.

| Category | Details |
| --- | --- |
| **Reason** | The raw strings are not directly usable for model loading or evaluation; they must be converted to structured data. |
| **Impact** | Provides a reliable, programmatic representation of each model's configuration for downstream steps. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over the input list, clean each string, and use `ast.literal_eval` or `json.loads` with fallback handling to safely convert to a dict; raise a clear error for malformed entries. |

### 2. Generate a unique identifier for each model and associate it with its parsed hyperparameters.

| Category | Details |
| --- | --- |
| **Reason** | Models are stored and later retrieved by identifier; a deterministic ID ensures consistent mapping between storage and evaluation. |
| **Impact** | Enables accurate loading of the correct trained model files and aligns predictions with the right hyperparameter set. |
| **Complexity** | LOW |
| **Method** | Create IDs by enumerating the list (e.g., `model_0`, `model_1`, …) or by hashing the sorted hyperparameter dict; store the mapping in a `dict[str, dict]`. |

### 3. Serialize the identifier‑to‑hyperparameters mapping as a JSON string for the node output.

| Category | Details |
| --- | --- |
| **Reason** | The pipeline expects the output as a `str` type, not a native Python object. |
| **Impact** | Ensures compatibility with downstream nodes that will deserialize the string back into a dictionary. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps(mapping, ensure_ascii=False)` to produce the `output` string; optionally set `sort_keys=True` for deterministic output. |
