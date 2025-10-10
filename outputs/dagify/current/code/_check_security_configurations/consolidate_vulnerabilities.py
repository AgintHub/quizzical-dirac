# -- PRD --
# 1. BULLET: Parse input vulnerability lists from string format to a list format for
#   processing.
#   Reason: The inputs are provided as strings and need to be converted into a usable
#           format for consolidation.
#   Impact: Allows for the proper handling and merging of different vulnerability
#           sources.
#   Complexity: LOW
#   Method: Use a parsing function to convert the input strings into lists.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Merge the parsed lists of vulnerabilities into a single list, removing any
#   duplicates.
#   Reason: To provide a comprehensive view of all vulnerabilities without redundancy.
#   Impact: Ensures that the output is a unified, non-redundant list of
#           vulnerabilities.
#   Complexity: MEDIUM
#   Method: Utilize a set data structure to eliminate duplicates and then convert back
#           to a list.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the consolidated list of vulnerabilities in the required output
#   format.
#   Reason: To match the expected output structure for further processing.
#   Impact: Facilitates the seamless integration of this node's output with subsequent
#           nodes.
#   Complexity: LOW
#   Method: Format the consolidated list according to the specified output structure.
# -- END PRD --

from typing import List

import json


def consolidate_vulnerabilities(image_vulns: str, resource_vulns: str, port_vulns: str) -> List[str]:
    """
    Consolidates various types of vulnerabilities into a single list.

    Args:
        image_vulns: Input parameter of type str
resource_vulns: Input parameter of type str
port_vulns: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse input vulnerability lists from string format to list format
    parsed_image_vulns = []
    parsed_resource_vulns = []
    parsed_port_vulns = []
    
    # Parse image_vulns
    if image_vulns:
        try:
            # Try parsing as JSON first
            parsed_image_vulns = json.loads(image_vulns)
            if not isinstance(parsed_image_vulns, list):
                parsed_image_vulns = [str(parsed_image_vulns)]
        except (json.JSONDecodeError, TypeError):
            # If not JSON, split by common delimiters
            parsed_image_vulns = [vuln.strip() for vuln in image_vulns.replace(',', '\n').replace(';', '\n').split('\n') if vuln.strip()]
    
    # Parse resource_vulns
    if resource_vulns:
        try:
            # Try parsing as JSON first
            parsed_resource_vulns = json.loads(resource_vulns)
            if not isinstance(parsed_resource_vulns, list):
                parsed_resource_vulns = [str(parsed_resource_vulns)]
        except (json.JSONDecodeError, TypeError):
            # If not JSON, split by common delimiters
            parsed_resource_vulns = [vuln.strip() for vuln in resource_vulns.replace(',', '\n').replace(';', '\n').split('\n') if vuln.strip()]
    
    # Parse port_vulns
    if port_vulns:
        try:
            # Try parsing as JSON first
            parsed_port_vulns = json.loads(port_vulns)
            if not isinstance(parsed_port_vulns, list):
                parsed_port_vulns = [str(parsed_port_vulns)]
        except (json.JSONDecodeError, TypeError):
            # If not JSON, split by common delimiters
            parsed_port_vulns = [vuln.strip() for vuln in port_vulns.replace(',', '\n').replace(';', '\n').split('\n') if vuln.strip()]
    
    # Merge the parsed lists and remove duplicates using set
    all_vulnerabilities = parsed_image_vulns + parsed_resource_vulns + parsed_port_vulns
    
    # Use set to eliminate duplicates, then convert back to list
    unique_vulnerabilities = list(set(all_vulnerabilities))
    
    # Return the consolidated list in the required output format
    return unique_vulnerabilities