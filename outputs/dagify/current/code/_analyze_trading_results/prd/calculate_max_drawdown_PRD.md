# calculate_max_drawdown PRD

## Description
Computes the maximum percentage drop from peak to trough of an equity curve.


## Implementation Plan

### 1. Parse `equity_curve` into a numeric list, handling both CSV and JSON formats.

| Category | Details |
| --- | --- |
| **Reason** | The function must interpret the input regardless of its textual representation. |
| **Impact** | Ensures robustness to different data serialization methods used by upstream nodes. |
| **Complexity** | LOW |
| **Method** | Use Python's `json.loads` for JSON arrays; if that fails, split the string by commas, strip whitespace, and convert each element to `float`. |

### 2. Compute the running maximum of the equity curve and calculate drawdowns as `(peak - current) / peak` for each point, then return the maximum drawdown value.

| Category | Details |
| --- | --- |
| **Reason** | This is the core mathematical operation needed to assess risk. |
| **Impact** | Provides an accurate, industry‑standard measure of portfolio risk over the period. |
| **Complexity** | MEDIUM |
| **Method** | Iterate over the numeric list while maintaining a `max_so_far` variable; at each step compute `drawdown = (max_so_far - value) / max_so_far`; keep track of the largest drawdown. |

### 3. Validate that the computed drawdown is a non‑negative float and optionally compare it against the provided `snapshot_drawdown`, returning the larger of the two if the snapshot value is supplied.

| Category | Details |
| --- | --- |
| **Reason** | Allows the function to serve as both a validator and a fallback when an existing drawdown is present. |
| **Impact** | Guarantees consistency between historical and computed metrics, preventing downstream logic errors. |
| **Complexity** | LOW |
| **Method** | Convert `snapshot_drawdown` to float if non‑empty; use `max(computed_drawdown, snapshot_drawdown)`; raise a ValueError if any result is not a float or is negative. |
