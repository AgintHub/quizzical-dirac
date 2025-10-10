# -- PRD --
# 1. BULLET: Parse container configuration manifests to extract resource limits.
#   Reason: To provide the necessary resource limits for further processing and
#           analysis.
#   Impact: Enables accurate resource allocation and monitoring.
#   Complexity: MEDIUM
#   Method: Use a parsing library (e.g., JSON or YAML parser) to extract resource limit
#           information from container configuration manifests.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle varying container configuration formats.
#   Reason: Container configurations may be in different formats (e.g., JSON, YAML).
#   Impact: Ensures compatibility with different container orchestration systems.
#   Complexity: MEDIUM
#   Method: Implement format detection and use appropriate parsing libraries for each
#           format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate extracted resource limits.
#   Reason: To ensure that the extracted resource limits are valid and reasonable.
#   Impact: Prevents incorrect resource allocation.
#   Complexity: LOW
#   Method: Check extracted values against known valid ranges and configurations.
# -- END PRD --

from typing import List

import json
import yaml
import re


def extract_resource_limits(configs: str) -> List[float]:
    """
    Extracts resource limits from container configuration manifests.

    Args:
        configs: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    
    resource_limits = []
    
    # Handle varying container configuration formats - detect format
    configs_stripped = configs.strip()
    
    try:
        # Try to parse as JSON first
        if configs_stripped.startswith('{') or configs_stripped.startswith('['):
            parsed_config = json.loads(configs_stripped)
        else:
            # Try to parse as YAML
            parsed_config = yaml.safe_load(configs_stripped)
    except (json.JSONDecodeError, yaml.YAMLError):
        # If both fail, return empty list
        return resource_limits
    
    # Extract resource limits from parsed configuration
    def extract_limits_recursive(data):
        limits = []
        
        if isinstance(data, dict):
            # Look for common resource limit keys
            resource_keys = ['cpu', 'memory', 'storage', 'limits', 'requests', 'resources']
            
            for key, value in data.items():
                if any(res_key in key.lower() for res_key in resource_keys):
                    if isinstance(value, (int, float)):
                        limits.append(float(value))
                    elif isinstance(value, str):
                        # Extract numeric values from strings (e.g., "100m", "1Gi")
                        numeric_match = re.findall(r'([0-9]*\.?[0-9]+)', value)
                        for match in numeric_match:
                            limits.append(float(match))
                    elif isinstance(value, (dict, list)):
                        limits.extend(extract_limits_recursive(value))
                else:
                    # Recursively search in nested structures
                    if isinstance(value, (dict, list)):
                        limits.extend(extract_limits_recursive(value))
        
        elif isinstance(data, list):
            for item in data:
                limits.extend(extract_limits_recursive(item))
        
        return limits
    
    extracted_limits = extract_limits_recursive(parsed_config)
    
    # Validate extracted resource limits
    for limit in extracted_limits:
        # Check if the limit is within reasonable ranges
        if 0 <= limit <= 1000000:  # Reasonable upper bound for resource limits
            resource_limits.append(limit)
    
    return resource_limits