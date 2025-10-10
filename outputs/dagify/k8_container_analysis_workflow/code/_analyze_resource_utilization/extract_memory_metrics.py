# -- PRD --
# 1. BULLET: Implement a function to parse the input string 'parsed_metrics' into a
#   structured data format.
#   Reason: The input data needs to be converted into a usable format for extracting
#           memory metrics.
#   Impact: Enables the extraction of memory utilization metrics from the parsed data.
#   Complexity: MEDIUM
#   Method: Use a JSON or dictionary parsing approach to convert the string into a
#           Python dictionary or list of dictionaries.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify and extract memory utilization metrics from the parsed data.
#   Reason: The specific memory metrics need to be isolated from other data.
#   Impact: Allows for the calculation of average memory utilization and other memory-
#           related statistics.
#   Complexity: MEDIUM
#   Method: Iterate through the parsed data to identify fields related to memory
#           utilization, and extract these values.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the extracted memory metrics as a list of floats.
#   Reason: The output needs to be in a format that is usable by subsequent nodes or
#           functions.
#   Impact: Facilitates further analysis or processing of the memory utilization data.
#   Complexity: LOW
#   Method: Use a list comprehension or a simple loop to convert the extracted memory
#           metrics into a list of floats.
# -- END PRD --

from typing import List

import json
import re


def extract_memory_metrics(parsed_metrics: str) -> List[float]:
    """
    Extracts memory utilization metrics from parsed resource metrics data.

    Args:
        parsed_metrics: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    
    # Parse the input string into a structured data format
    try:
        # First try to parse as JSON
        parsed_data = json.loads(parsed_metrics)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract numeric values using regex
        # Look for memory-related patterns like "memory: 85.5%" or "mem_util: 0.75"
        memory_pattern = r'(?:memory|mem|ram)(?:[_\s]*(?:util|usage|used|percent))?[:\s=]+([0-9]*\.?[0-9]+)'
        matches = re.findall(memory_pattern, parsed_metrics, re.IGNORECASE)
        if matches:
            return [float(match) for match in matches]
        
        # Fallback: extract all numeric values that could be percentages or ratios
        numeric_pattern = r'([0-9]*\.?[0-9]+)%?'
        all_numbers = re.findall(numeric_pattern, parsed_metrics)
        return [float(num) for num in all_numbers if num]
    
    # Extract memory metrics from parsed JSON/dict data
    memory_metrics = []
    
    def extract_from_dict(data_item):
        """Helper function to extract memory values from a dictionary"""
        if isinstance(data_item, dict):
            for key, value in data_item.items():
                # Check if key relates to memory
                if any(mem_keyword in key.lower() for mem_keyword in ['memory', 'mem', 'ram', 'util', 'usage']):
                    if isinstance(value, (int, float)):
                        memory_metrics.append(float(value))
                    elif isinstance(value, str):
                        # Try to extract numeric value from string (e.g., "85.5%")
                        numeric_match = re.search(r'([0-9]*\.?[0-9]+)', value)
                        if numeric_match:
                            memory_metrics.append(float(numeric_match.group(1)))
                elif isinstance(value, (dict, list)):
                    extract_from_dict(value)
        elif isinstance(data_item, list):
            for item in data_item:
                extract_from_dict(item)
    
    # Handle different data structures
    if isinstance(parsed_data, list):
        for item in parsed_data:
            extract_from_dict(item)
    elif isinstance(parsed_data, dict):
        extract_from_dict(parsed_data)
    else:
        # If it's a simple numeric value
        if isinstance(parsed_data, (int, float)):
            memory_metrics.append(float(parsed_data))
    
    return memory_metrics