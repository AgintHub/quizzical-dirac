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


def extract_image_names(configs: str) -> List[str]:
    """
    Extracts image names from container configuration manifests.

    Args:
        configs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
