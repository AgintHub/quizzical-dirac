# -- PRD --
# 1. BULLET: The shim function will process the input significant patterns to compile them
#   into a list.
#   Reason: This is necessary to provide a structured output that can be used by
#           subsequent nodes in the workflow.
#   Impact: The compiled list of cultural patterns will be used to inform further
#           analysis or decision-making processes.
#   Complexity: LOW
#   Method: Implement a simple list processing algorithm that takes the input
#           significant patterns and returns them in a structured list
#           format.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The function will need to handle different types of input data, potentially
#   including data cleaning or normalization.
#   Reason: To ensure the output is accurate and reliable, the function must be able to
#           handle varying input formats or quality.
#   Impact: Proper handling of diverse input data will enhance the robustness and
#           flexibility of the overall system.
#   Complexity: MEDIUM
#   Method: Use data processing techniques such as data normalization or outlier
#           detection to handle diverse input data effectively.
# -- END PRD --

from typing import List

import re


def compile_cultural_patterns(significant_patterns: str) -> List[str]:
    """
    Compiles significant cultural patterns into a list based on the input significant patterns.

    Args:
        significant_patterns: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Handle empty or None input
    if not significant_patterns or not significant_patterns.strip():
        return []
    
    # Clean and normalize the input data
    cleaned_input = significant_patterns.strip()
    
    # Split patterns by common delimiters (newlines, semicolons, commas)
    # This handles different input formats
    patterns = re.split(r'[\n;,]+', cleaned_input)
    
    # Process each pattern: clean whitespace, filter out empty strings
    processed_patterns = []
    for pattern in patterns:
        cleaned_pattern = pattern.strip()
        if cleaned_pattern:  # Only add non-empty patterns
            processed_patterns.append(cleaned_pattern)
    
    # Remove duplicates while preserving order
    unique_patterns = []
    seen = set()
    for pattern in processed_patterns:
        if pattern.lower() not in seen:
            unique_patterns.append(pattern)
            seen.add(pattern.lower())
    
    return unique_patterns