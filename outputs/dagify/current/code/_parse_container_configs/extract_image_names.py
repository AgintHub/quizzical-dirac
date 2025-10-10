# -- PRD --
# 1. BULLET: Parse container configuration manifests to identify image names.
#   Reason: The function needs to analyze the configuration data to extract relevant
#           image information.
#   Impact: Successful extraction enables further processing and analysis of container
#           configurations.
#   Complexity: MEDIUM
#   Method: Utilize a parsing library (e.g., YAML or JSON parser) to read the
#           configuration manifests and identify image names.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle various configuration formats (e.g., YAML, JSON).
#   Reason: Container configurations may be represented in different formats, and the
#           function needs to be flexible.
#   Impact: The function will be able to process a wide range of configuration files.
#   Complexity: MEDIUM
#   Method: Implement format detection and use the appropriate parsing library for each
#           detected format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return a list of extracted image names.
#   Reason: The output needs to be in a format that can be easily consumed by
#           subsequent processing steps.
#   Impact: The extracted image names will be available for further analysis or
#           processing.
#   Complexity: LOW
#   Method: Store the extracted image names in a list and return it as the output.
# -- END PRD --

from typing import List

import json
import yaml
import re


def extract_image_names(configs: str) -> List[str]:
    """
    Extracts image names from container configuration manifests.

    Args:
        configs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    image_names = []
    
    # Try to detect and parse the configuration format
    configs = configs.strip()
    
    # Try JSON first
    try:
        config_data = json.loads(configs)
    except json.JSONDecodeError:
        # Try YAML
        try:
            config_data = yaml.safe_load(configs)
        except yaml.YAMLError:
            # If both fail, return empty list
            return image_names
    
    # Extract image names from the parsed configuration
    def extract_images_recursive(data):
        if isinstance(data, dict):
            for key, value in data.items():
                # Common keys that contain image names
                if key.lower() in ['image', 'container_image', 'docker_image', 'from']:
                    if isinstance(value, str):
                        image_names.append(value)
                elif isinstance(value, (dict, list)):
                    extract_images_recursive(value)
        elif isinstance(data, list):
            for item in data:
                extract_images_recursive(item)
        elif isinstance(data, str):
            # Look for image patterns in strings (e.g., in commands or scripts)
            image_pattern = r'(?:FROM|image:|docker pull)\s+([\w\-./]+(?::[\w\-./]+)?(?:@sha256:[a-f0-9]+)?)'
            matches = re.findall(image_pattern, data, re.IGNORECASE)
            image_names.extend(matches)
    
    extract_images_recursive(config_data)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_images = []
    for img in image_names:
        if img not in seen:
            seen.add(img)
            unique_images.append(img)
    
    return unique_images