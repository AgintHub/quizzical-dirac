# -- PRD --
# 1. BULLET: Validate input lists for CPU and memory utilization metrics to ensure they
#   are of the same length and contain valid float values
#   Reason: To prevent errors during the combination process and ensure data
#           consistency
#   Impact: Ensures that the output is reliable and accurate
#   Complexity: LOW
#   Method: Implement input validation using Python's built-in type checking and length
#           comparison
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Combine the CPU and memory utilization metrics into a single list by
#   averaging corresponding elements from both lists
#   Reason: To provide a comprehensive view of resource utilization
#   Impact: Enables the system to analyze overall resource utilization
#   Complexity: MEDIUM
#   Method: Use a list comprehension or a library like NumPy to average corresponding
#           elements from both input lists
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle edge cases where input lists are empty or contain inconsistent data
#   Reason: To prevent the function from failing or producing incorrect results
#   Impact: Ensures the function's robustness and reliability
#   Complexity: MEDIUM
#   Method: Implement conditional checks to handle empty lists or inconsistent data,
#           returning appropriate values or errors as needed
# -- END PRD --

from typing import List

import json


def combine_resource_metrics(cpu: str, memory: str) -> List[float]:
    """
    This node combines CPU and memory resource utilization metrics into a single list of floats.

    Args:
        cpu: Input parameter of type str
memory: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    
    # Parse CPU and memory strings into lists
    try:
        cpu_list = json.loads(cpu)
        memory_list = json.loads(memory)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"Invalid JSON format in input strings: {e}")
    
    # Validate that inputs are lists
    if not isinstance(cpu_list, list) or not isinstance(memory_list, list):
        raise ValueError("Input strings must represent JSON lists")
    
    # Handle edge case of empty lists
    if len(cpu_list) == 0 and len(memory_list) == 0:
        return []
    
    # Validate that lists are of the same length
    if len(cpu_list) != len(memory_list):
        raise ValueError(f"CPU and memory lists must be of the same length. CPU: {len(cpu_list)}, Memory: {len(memory_list)}")
    
    # Validate that all elements are valid float values
    try:
        cpu_floats = [float(x) for x in cpu_list]
        memory_floats = [float(x) for x in memory_list]
    except (ValueError, TypeError) as e:
        raise ValueError(f"All elements in CPU and memory lists must be convertible to float: {e}")
    
    # Combine metrics by averaging corresponding elements
    combined_metrics = [(cpu_val + memory_val) / 2.0 for cpu_val, memory_val in zip(cpu_floats, memory_floats)]
    
    return combined_metrics