# -- PRD --
# 1. BULLET: Implement data parsing to extract CPU metrics from the input string
#   Reason: The input data needs to be parsed to identify and extract CPU utilization
#           metrics.
#   Impact: Successful extraction of CPU metrics will enable accurate calculation of
#           average CPU utilization.
#   Complexity: MEDIUM
#   Method: Use a JSON parsing library to deserialize the input string into a
#           structured format, then iterate through the data to extract CPU
#           metrics.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the extracted CPU metrics to ensure they are within valid ranges
#   Reason: Validation is necessary to prevent incorrect data from being processed
#           further.
#   Impact: Valid CPU metrics will improve the accuracy of subsequent analyses, such as
#           average CPU utilization calculation.
#   Complexity: LOW
#   Method: Implement range checks to verify that the extracted CPU metrics fall within
#           expected ranges (e.g., between 0 and 100%).
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle potential errors during data parsing and extraction
#   Reason: Error handling is crucial to prevent the application from crashing due to
#           malformed input data.
#   Impact: Robust error handling will ensure that the application remains stable even
#           when encountering invalid or malformed input.
#   Complexity: HIGH
#   Method: Use try-except blocks to catch parsing errors, and implement fallback
#           strategies to handle missing or invalid data.
# -- END PRD --

from typing import List

import json
import re


def extract_cpu_metrics(parsed_metrics: str) -> List[float]:
    """
    Extracts CPU utilization metrics from parsed resource utilization data.

    Args:
        parsed_metrics: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    
    cpu_metrics = []
    
    try:
        # Parse the input string as JSON
        data = json.loads(parsed_metrics)
        
        # Handle different data structures - list or dict
        if isinstance(data, list):
            items_to_process = data
        elif isinstance(data, dict):
            items_to_process = [data]
        else:
            return cpu_metrics
        
        # Extract CPU metrics from the data
        for item in items_to_process:
            if isinstance(item, dict):
                # Look for CPU-related keys
                for key, value in item.items():
                    key_lower = key.lower()
                    if any(cpu_term in key_lower for cpu_term in ['cpu', 'processor', 'utilization']):
                        try:
                            # Convert to float and validate
                            cpu_value = float(value)
                            # Validate range (0-100 for percentage)
                            if 0.0 <= cpu_value <= 100.0:
                                cpu_metrics.append(cpu_value)
                        except (ValueError, TypeError):
                            # Skip invalid values
                            continue
                
                # Also check nested structures
                if 'metrics' in item and isinstance(item['metrics'], dict):
                    for metric_key, metric_value in item['metrics'].items():
                        if 'cpu' in metric_key.lower():
                            try:
                                cpu_value = float(metric_value)
                                if 0.0 <= cpu_value <= 100.0:
                                    cpu_metrics.append(cpu_value)
                            except (ValueError, TypeError):
                                continue
    
    except json.JSONDecodeError:
        # Try to extract numbers using regex as fallback
        try:
            # Look for patterns like "cpu: 45.6" or "CPU utilization: 23.4%"
            cpu_pattern = r'(?i)cpu[^\d]*([\d]+\.?[\d]*)'  
            matches = re.findall(cpu_pattern, parsed_metrics)
            
            for match in matches:
                try:
                    cpu_value = float(match)
                    if 0.0 <= cpu_value <= 100.0:
                        cpu_metrics.append(cpu_value)
                except ValueError:
                    continue
        except Exception:
            # Return empty list if all parsing attempts fail
            pass
    
    except Exception:
        # Handle any other unexpected errors
        pass
    
    return cpu_metrics