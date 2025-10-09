# filter_successful_trades PRD

## Description
Filters successful trades from a batch of executed trades and returns them as a JSON string.


## Implementation Plan

### 1. Validate that all input JSON arrays are non-empty and of equal length before processing.

| Category | Details |
| --- | --- |
| **Reason** | Ensures data consistency and prevents misalignment of trade attributes. |
| **Impact** | Prevents runtime errors and incorrect trade mapping. |
| **Complexity** | LOW |
| **Method** | Parse each JSON string into a Python list using `json.loads()` and compare their lengths; raise `ValueError` if mismatched. |

### 2. Iterate through the arrays using a single index loop or list comprehension to filter trades where the corresponding status is `true`.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality to isolate successful trades. |
| **Impact** | Produces a list of dictionaries with trade details that are ready for downstream consumption. |
| **Complexity** | LOW |
| **Method** | Use a list comprehension that zips all arrays and selects elements with `status == True`. |

### 3. Serialize the filtered list of trade dictionaries back into a JSON string for the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The output contract expects a string representation. |
| **Impact** | Provides a standard, machine‑readable format that can be parsed by subsequent nodes. |
| **Complexity** | LOW |
| **Method** | Apply `json.dumps()` to the filtered list and return it as the `output` value. |
