# calculate_total_cost PRD

## Description
This shim calculates the total cost of a car rental by summing up the base rental cost, insurance cost, upgrades cost, and additional fees.


## Implementation Plan

### 1. Parse the base rental cost from string to float

| Category | Details |
| --- | --- |
| **Reason** | The input base rental cost is of type string and needs to be converted to a numerical type for calculation |
| **Impact** | Incorrect type will lead to calculation errors |
| **Complexity** | LOW |
| **Method** | Use Python's built-in float() function to convert the string to a float |

### 2. Sum up the base rental cost, insurance cost, upgrades cost, and additional fees

| Category | Details |
| --- | --- |
| **Reason** | To get the total cost, all individual costs need to be added together |
| **Impact** | Incorrect total cost will be returned if any of the costs are not included |
| **Complexity** | LOW |
| **Method** | Use basic arithmetic addition to sum up all the costs |

### 3. Handle potential errors during cost parsing and calculation

| Category | Details |
| --- | --- |
| **Reason** | To ensure robustness, potential errors such as non-numeric input for costs should be handled |
| **Impact** | Unhandled errors could lead to the function crashing or returning incorrect results |
| **Complexity** | MEDIUM |
| **Method** | Use try-except blocks to catch and handle exceptions, providing a default value or error message as needed |
