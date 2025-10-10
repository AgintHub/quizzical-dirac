# -- PRD --
# 1. BULLET: Implement data parsing logic to extract resource utilization metrics from
#   input string data
#   Reason: To transform the input data into a structured format that can be used for
#           further analysis
#   Impact: Enables the analysis of resource utilization patterns and calculation of
#           key metrics
#   Complexity: MEDIUM
#   Method: Use a data parsing library (e.g., pandas) to read and process the input
#           data, handling potential errors and edge cases
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the input data format to ensure compatibility with the parsing logic
#   Reason: To prevent errors during parsing and ensure that the output is reliable
#   Impact: Improves the robustness of the function and reduces the likelihood of
#           downstream errors
#   Complexity: LOW
#   Method: Implement input validation checks using a schema validation library (e.g.,
#           Pydantic)
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Optimize the parsing logic for performance, considering large input datasets
#   Reason: To improve the efficiency and scalability of the function
#   Impact: Reduces processing time and enhances overall system performance
#   Complexity: HIGH
#   Method: Utilize efficient data processing techniques (e.g., vectorized operations)
#           and consider parallel processing for large datasets
# -- END PRD --

from typing import List
import re
import json


def parse_resource_metrics(utilization_data: str) -> List[str]:
    """
    A shim function that parses and extracts resource utilization metrics from input data.

    Args:
        utilization_data: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    
    # --- PURE IMPLEMENTATION ---
    
    # Validate input data format
    if not isinstance(utilization_data, str):
        raise ValueError("Input data must be a string")
    
    if not utilization_data.strip():
        raise ValueError("Input data cannot be empty")
    
    metrics = []
    
    try:
        # Parse the input data line by line
        lines = utilization_data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to parse as JSON first
            try:
                parsed_data = json.loads(line)
                if isinstance(parsed_data, dict):
                    # Extract resource metrics from JSON
                    metric_keys = ['cpu', 'memory', 'disk', 'network', 'utilization', 'usage', 'percent']
                    for key, value in parsed_data.items():
                        if any(metric_key in key.lower() for metric_key in metric_keys):
                            metrics.append(f"{key}: {value}")
                continue
            except json.JSONDecodeError:
                pass
            
            # Parse key-value pairs (e.g., "cpu_usage=75%")
            if '=' in line:
                key_value_pairs = re.findall(r'([\w_]+)\s*=\s*([\d.%]+)', line)
                for key, value in key_value_pairs:
                    if any(metric in key.lower() for metric in ['cpu', 'memory', 'disk', 'network', 'utilization', 'usage']):
                        metrics.append(f"{key}: {value}")
                continue
            
            # Parse colon-separated values (e.g., "CPU Usage: 75%")
            if ':' in line:
                colon_pairs = re.findall(r'([\w\s]+):\s*([\d.%]+)', line)
                for key, value in colon_pairs:
                    key = key.strip()
                    if any(metric in key.lower() for metric in ['cpu', 'memory', 'disk', 'network', 'utilization', 'usage']):
                        metrics.append(f"{key}: {value}")
                continue
            
            # Parse space-separated metrics (e.g., "cpu 75% memory 60%")
            space_metrics = re.findall(r'(cpu|memory|disk|network)\s+([\d.%]+)', line.lower())
            for metric, value in space_metrics:
                metrics.append(f"{metric}: {value}")
    
    except Exception as e:
        raise ValueError(f"Error parsing resource metrics: {str(e)}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_metrics = []
    for metric in metrics:
        if metric not in seen:
            seen.add(metric)
            unique_metrics.append(metric)
    
    return unique_metrics