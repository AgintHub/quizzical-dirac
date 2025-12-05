# convert_predictions_to_positions PRD

## Description
Transforms model prediction values into discrete position signals (long, short, or flat) for portfolio construction.


## Implementation Plan

### 1. Parse the JSON‑encoded predictions string into a Python dictionary of asset identifiers to numeric forecast values.

| Category | Details |
| --- | --- |
| **Reason** | The downstream position logic requires a structured, type‑safe mapping rather than raw text. |
| **Impact** | Enables reliable downstream calculations of portfolio returns and risk metrics. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` with error handling to convert the string; validate that each value is a float or int. |

### 2. Apply a configurable signal‑generation rule (e.g., threshold‑based, top‑N selection, or quantile binning) to map each forecast value to a position signal of -1, 0, or 1.

| Category | Details |
| --- | --- |
| **Reason** | Different strategies may be required for various trading styles; the shim must be flexible. |
| **Impact** | Produces position signals that directly affect portfolio turnover, hit‑rate, and overall performance metrics. |
| **Complexity** | MEDIUM |
| **Method** | Implement a function that accepts parameters `threshold_long`, `threshold_short`, and `top_n`; use NumPy/Pandas vectorised operations for efficiency and expose these parameters via a configuration dict. |

### 3. Serialize the resulting position dictionary back to a JSON string to match the declared `output` type.

| Category | Details |
| --- | --- |
| **Reason** | The rest of the pipeline expects a string representation consistent with other node interfaces. |
| **Impact** | Maintains interface contract, preventing type mismatches during downstream validation. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps` with `ensure_ascii=False`; optionally sort keys for reproducibility. |
