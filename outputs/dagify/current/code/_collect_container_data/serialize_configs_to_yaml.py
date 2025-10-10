# -- PRD --
# 1. BULLET: The function will take a list of dictionaries representing container
#   configurations and serialize them into YAML format.
#   Reason: This is necessary to convert the raw configuration data into a human-
#           readable and easily parseable format.
#   Impact: The output will be used to store or display container configuration
#           manifests in a readable format.
#   Complexity: MEDIUM
#   Method: Utilize a YAML serialization library (e.g., PyYAML) to convert the list of
#           dictionaries into YAML-formatted strings.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Error handling will be implemented to manage cases where the input is not a
#   valid list of dictionaries.
#   Reason: To ensure the function is robust and can handle potential input errors.
#   Impact: The function will be able to gracefully handle invalid inputs and provide
#           meaningful error messages.
#   Complexity: LOW
#   Method: Use try-except blocks to catch exceptions during the serialization process
#           and return or raise informative error messages.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The function will be designed to handle large lists of container
#   configurations efficiently.
#   Reason: To prevent performance issues when dealing with a large number of
#           configurations.
#   Impact: The function will be scalable and able to handle large inputs without
#           significant performance degradation.
#   Complexity: HIGH
#   Method: Implement streaming or chunking to process large lists in manageable
#           chunks, reducing memory usage and improving performance.
# -- END PRD --

from typing import List
import yaml
import json


def serialize_configs_to_yaml(configs: str) -> List[str]:
    """
    Serializes container configuration manifests from a list of dictionaries to a list of YAML-formatted strings.

    Args:
        configs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    try:
        # Parse the input string as JSON to get list of dictionaries
        config_list = json.loads(configs)
        
        # Validate that input is a list
        if not isinstance(config_list, list):
            raise ValueError("Input must be a JSON string representing a list of dictionaries")
        
        # Validate that each item in the list is a dictionary
        for i, config in enumerate(config_list):
            if not isinstance(config, dict):
                raise ValueError(f"Item at index {i} is not a dictionary")
        
        # Process configurations in chunks for large lists (performance optimization)
        chunk_size = 100  # Process 100 configs at a time
        yaml_results = []
        
        for i in range(0, len(config_list), chunk_size):
            chunk = config_list[i:i + chunk_size]
            
            # Convert each config dictionary to YAML format
            for config in chunk:
                try:
                    yaml_string = yaml.dump(config, default_flow_style=False, allow_unicode=True)
                    yaml_results.append(yaml_string.strip())
                except Exception as e:
                    raise ValueError(f"Failed to serialize config to YAML: {str(e)}")
        
        return yaml_results
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing configurations: {str(e)}")