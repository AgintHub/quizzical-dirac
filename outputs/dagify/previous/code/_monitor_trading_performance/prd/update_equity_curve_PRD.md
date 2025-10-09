# update_equity_curve PRD

## Description
Updates the equity curve data structure by incorporating the return fraction of a closed trade.


## Implementation Plan

### 1. Validate input types and convert string representations of return_fraction and equity_curve into numeric data structures.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the shim operates on correctly typed data, preventing runtime errors. |
| **Impact** | Guarantees data integrity and consistency for subsequent calculations. |
| **Complexity** | LOW |
| **Method** | Use Python's json.loads to parse the equity_curve and float() to convert return_fraction. |

### 2. Calculate the cumulative equity value by applying the return_fraction to the last equity point and append the new value to the equity_curve list.

| Category | Details |
| --- | --- |
| **Reason** | Accurately reflects the portfolio's value after the trade. |
| **Impact** | Provides an up‑to‑date equity trajectory for performance monitoring. |
| **Complexity** | LOW |
| **Method** | Retrieve the last element of the equity_curve list, compute new_equity = last_equity * (1 + return_fraction), and append new_equity. |

### 3. Serialize the updated equity_curve back to a JSON string and return it along with a success status message.

| Category | Details |
| --- | --- |
| **Reason** | Maintains the expected string interface for downstream nodes. |
| **Impact** | Ensures compatibility with other components that consume the equity_curve as a string. |
| **Complexity** | LOW |
| **Method** | Use json.dumps to convert the equity_curve list to a string and return it together with a simple "success" message. |
