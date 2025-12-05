# calculate_turnovers PRD

## Description
Computes the average portfolio turnover (as a percent of portfolio per period) for each model based on their position signals.


## Implementation Plan

### 1. Parse the `positions` JSON string into a dictionary of model → list of position vectors.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives raw string data; it must be deserialized before any numeric computation. |
| **Impact** | Ensures downstream calculations operate on correctly typed data and prevents runtime JSON errors. |
| **Complexity** | LOW |
| **Method** | Use Python's built‑in `json.loads` with error handling; validate that each model key maps to a list of equal‑length numeric arrays. |

### 2. For each model, compute turnover as the mean of the absolute differences between consecutive position vectors, expressed as a percentage of the total portfolio.

| Category | Details |
| --- | --- |
| **Reason** | Turnover measures how frequently the portfolio composition changes; averaging across periods yields a comparable metric across models. |
| **Impact** | Provides the `turnovers` metric required by `evaluate_models`, influencing model ranking and selection. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over each model's position list, calculate `np.abs(np.diff(vector, axis=0)).sum()` for each time step, divide by the portfolio size (assumed 1.0 for normalized weights), and then average over all steps; return results as a list of floats preserving model order. |

### 3. Handle edge cases such as single‑period data, missing positions, or non‑numeric entries by returning a turnover of 0.0 for that model and logging a warning.

| Category | Details |
| --- | --- |
| **Reason** | Real‑world data can be incomplete or malformed; graceful degradation prevents the entire evaluation pipeline from failing. |
| **Impact** | Improves robustness of the evaluation workflow and ensures consistent output lengths. |
| **Complexity** | LOW |
| **Method** | Check the length of each position list; if length < 2 or conversion to float fails, append 0.0 to the result list and use the `logging` module to emit a descriptive warning. |
