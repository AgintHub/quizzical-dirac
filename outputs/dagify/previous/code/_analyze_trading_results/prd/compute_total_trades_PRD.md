# compute_total_trades PRD

## Description
Computes the total number of trades for a monitoring period, using an optional snapshot total or falling back to the sum of winning and losing trades.


## Implementation Plan

### 1. Parse the snapshot_total string into an integer and validate its positivity; if parsing fails or the value is non‑positive, compute total_trades by adding winning_trades and losing_trades.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the function can work with both pre‑computed snapshot data and raw win/loss counts. |
| **Impact** | Provides a reliable total_trades count regardless of input format, preventing downstream division-by-zero or negative trade count errors. |
| **Complexity** | LOW |
| **Method** | Use Python's int() conversion with exception handling; apply a simple >0 check; fall back to summation of provided counts. |

### 2. Return the computed total_trades as a primitive INT and preserve the original snapshot_total string in the output for traceability.

| Category | Details |
| --- | --- |
| **Reason** | Maintains consistency with the defined output schema and enables debugging by keeping the raw input. |
| **Impact** | Allows downstream nodes to verify that the shim used the correct source for total trade calculation. |
| **Complexity** | LOW |
| **Method** | Construct a dictionary with keys 'output' and 'snapshot_total', then return it. |

### 3. Add unit tests covering scenarios where snapshot_total is valid, missing, invalid, or zero, and where winning_trades or losing_trades are zero.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees robustness and catches regressions during future implementation. |
| **Impact** | Increases confidence in the shim's correctness and aids continuous integration pipelines. |
| **Complexity** | MEDIUM |
| **Method** | Create pytest functions that call compute_total_trades with various inputs and assert expected outputs. |
