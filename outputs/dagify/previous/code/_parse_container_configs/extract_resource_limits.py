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


def extract_resource_limits(configs: str) -> List[float]:
    """
    Extracts resource limits from container configuration manifests.

    Args:
        configs: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
