# -- PRD --
# 1. BULLET: Parse container configuration manifests to identify container names.
#   Reason: Container names are essential metadata for understanding container
#           configurations.
#   Impact: Enables the extraction of relevant container information for further
#           analysis.
#   Complexity: MEDIUM
#   Method: Use a configuration parsing library (e.g., YAML or JSON parser) to extract
#           container names from the manifests.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different configuration file formats (e.g., YAML, JSON).
#   Reason: Container configurations can be represented in various formats.
#   Impact: Ensures the shim can work with different types of container configuration
#           files.
#   Complexity: MEDIUM
#   Method: Implement format detection and use appropriate parsing libraries for each
#           format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the input configuration manifests for correctness.
#   Reason: Invalid or malformed configurations could cause errors.
#   Impact: Improves the robustness of the shim by handling potential errors.
#   Complexity: HIGH
#   Method: Use schema validation techniques to check the input configurations against
#           expected formats.
# -- END PRD --

from typing import List

import json
import yaml
import re


def extract_container_names(configs: str) -> List[str]:
    """
    Extracts container names from a list of container configuration manifests.

    Args:
        configs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    container_names = []
    
    # Split configs by common delimiters to handle multiple manifests
    config_parts = re.split(r'\n---\n|\n\n(?=\{)|\n\n(?=[a-zA-Z])', configs.strip())
    
    for config_part in config_parts:
        config_part = config_part.strip()
        if not config_part:
            continue
            
        try:
            # Try to detect format and parse accordingly
            parsed_config = None
            
            # Try JSON first
            if config_part.startswith('{') or config_part.startswith('['):
                try:
                    parsed_config = json.loads(config_part)
                except json.JSONDecodeError:
                    pass
            
            # Try YAML if JSON failed
            if parsed_config is None:
                try:
                    parsed_config = yaml.safe_load(config_part)
                except yaml.YAMLError:
                    pass
            
            # Skip if we couldn't parse the config
            if parsed_config is None:
                continue
                
            # Extract container names from parsed config
            def extract_names_recursive(obj, names_list):
                if isinstance(obj, dict):
                    # Common container name fields
                    name_fields = ['name', 'container_name', 'containerName', 'image']
                    for field in name_fields:
                        if field in obj and isinstance(obj[field], str):
                            # Extract just the name part if it's an image reference
                            name_value = obj[field]
                            if '/' in name_value:
                                name_value = name_value.split('/')[-1]
                            if ':' in name_value:
                                name_value = name_value.split(':')[0]
                            if name_value and name_value not in names_list:
                                names_list.append(name_value)
                    
                    # Look for containers array/list
                    if 'containers' in obj and isinstance(obj['containers'], list):
                        for container in obj['containers']:
                            extract_names_recursive(container, names_list)
                    
                    # Look for spec section (common in Kubernetes)
                    if 'spec' in obj:
                        extract_names_recursive(obj['spec'], names_list)
                    
                    # Recursively search other dict values
                    for value in obj.values():
                        if isinstance(value, (dict, list)):
                            extract_names_recursive(value, names_list)
                            
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            extract_names_recursive(item, names_list)
            
            extract_names_recursive(parsed_config, container_names)
            
        except Exception:
            # Skip malformed configs
            continue
    
    # Remove duplicates while preserving order
    unique_names = []
    for name in container_names:
        if name not in unique_names:
            unique_names.append(name)
    
    return unique_names