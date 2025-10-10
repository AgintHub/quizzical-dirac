# -- PRD --
# 1. BULLET: Implement a function to sum all the utilization metrics.
#   Reason: To calculate the average, we first need to sum all the values.
#   Impact: Accurate summation is crucial for the correct average calculation.
#   Complexity: LOW
#   Method: Use a simple loop or the `sum()` function in Python to add up all the
#           metrics.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Count the number of utilization metrics provided.
#   Reason: The count is necessary to divide the sum and find the average.
#   Impact: Correct count ensures the average is calculated over the right number of
#           values.
#   Complexity: LOW
#   Method: Use the `len()` function in Python to get the count of metrics.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle edge cases such as an empty list of metrics.
#   Reason: To prevent division by zero or return a meaningful result when there are no
#           metrics.
#   Impact: Ensures the function behaves predictably and doesn't crash on empty input.
#   Complexity: MEDIUM
#   Method: Check if the list is empty before calculating the average; return a
#           specific value or throw a meaningful exception.
# -- END PRD --

import json


def calculate_average_utilization(metrics: str) -> float:
    """
    Calculates the average utilization from a list of metrics.

    Args:
        metrics: Input parameter of type str

    Returns:
        float: Output of type float
    """
    
    # Parse the input string to get a list of metrics
    try:
        metrics_list = json.loads(metrics)
    except json.JSONDecodeError:
        # If it's not valid JSON, try to parse as comma-separated values
        try:
            metrics_list = [float(x.strip()) for x in metrics.split(',') if x.strip()]
        except ValueError:
            raise ValueError("Invalid metrics format")
    
    # Handle edge case: empty list of metrics
    if not metrics_list or len(metrics_list) == 0:
        return 0.0
    
    # Sum all the utilization metrics
    total_sum = sum(metrics_list)
    
    # Count the number of utilization metrics
    count = len(metrics_list)
    
    # Calculate and return the average
    average = total_sum / count
    
    return average