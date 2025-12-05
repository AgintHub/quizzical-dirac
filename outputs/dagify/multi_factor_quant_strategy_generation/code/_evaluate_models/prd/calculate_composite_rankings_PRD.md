# calculate_composite_rankings PRD

## Description
Computes integer composite rankings for each model based on provided Sharpe ratios, maximum drawdowns, and annualized returns.


## Implementation Plan

### 1. Parse the three input JSON strings into numeric Python lists.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives metrics as serialized strings; they must be converted to usable numeric structures before any calculation. |
| **Impact** | Enables downstream arithmetic and ensures type safety for the ranking algorithm. |
| **Complexity** | LOW |
| **Method** | Use `json.loads` to deserialize each string; validate that each list has the same length and contains only numbers, raising a clear ValueError on mismatch. |

### 2. Normalize each metric (Sharpe, max drawdown, annualized return) to a common scale before aggregation.

| Category | Details |
| --- | --- |
| **Reason** | Metrics have different units and ranges; without normalization a single metric could dominate the composite score. |
| **Impact** | Produces a balanced composite score that fairly reflects all three performance aspects. |
| **Complexity** | MEDIUM |
| **Method** | Apply min‑max scaling ( (x - min) / (max - min) ) to each list; for max drawdown invert the scale (1 - normalized) because lower drawdown is better. |

### 3. Calculate a composite score for each model by weighting the normalized metrics and derive integer rankings.

| Category | Details |
| --- | --- |
| **Reason** | The final purpose of the shim is to output an ordered ranking based on a single aggregated performance indicator. |
| **Impact** | Provides a deterministic ranking list that downstream nodes (e.g., reporting or selection) can consume. |
| **Complexity** | LOW |
| **Method** | Combine the three normalized arrays using equal weights (or configurable weights via future parameters), compute the sum for each model, sort descending, and assign rank 1 to the highest score; return the ranks as a LIST_INT. |
