# calculate_average_utilization PRD

## Description
Calculates the average utilization from a list of metrics.


## Implementation Plan

### 1. Implement a function to sum all the utilization metrics.

| Category | Details |
| --- | --- |
| **Reason** | To calculate the average, we first need to sum all the values. |
| **Impact** | Accurate summation is crucial for the correct average calculation. |
| **Complexity** | LOW |
| **Method** | Use a simple loop or the `sum()` function in Python to add up all the metrics. |

### 2. Count the number of utilization metrics provided.

| Category | Details |
| --- | --- |
| **Reason** | The count is necessary to divide the sum and find the average. |
| **Impact** | Correct count ensures the average is calculated over the right number of values. |
| **Complexity** | LOW |
| **Method** | Use the `len()` function in Python to get the count of metrics. |

### 3. Handle edge cases such as an empty list of metrics.

| Category | Details |
| --- | --- |
| **Reason** | To prevent division by zero or return a meaningful result when there are no metrics. |
| **Impact** | Ensures the function behaves predictably and doesn't crash on empty input. |
| **Complexity** | MEDIUM |
| **Method** | Check if the list is empty before calculating the average; return a specific value or throw a meaningful exception. |
