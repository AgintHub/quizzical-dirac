# -- PRD --
# 1. BULLET: Develop a function to parse the input string containing major landmarks data.
#   Reason: The input data needs to be processed into a usable format for
#           standardization.
#   Impact: This will enable the function to correctly identify and format individual
#           landmarks.
#   Complexity: MEDIUM
#   Method: Use a parsing library or regular expressions to extract individual
#           landmarks from the input string.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Standardize the formatting of the landmarks list.
#   Reason: Consistent formatting is necessary for downstream processing and analysis.
#   Impact: This will ensure that the output is uniform and easily consumable by
#           subsequent nodes.
#   Complexity: LOW
#   Method: Apply a standard template or formatting rule to each landmark, such as
#           title casing or trimming unnecessary characters.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the output to ensure it meets the required List[str] format.
#   Reason: The output must conform to the expected data type to avoid errors in
#           subsequent processing.
#   Impact: This will guarantee that the function produces output that is compatible
#           with the expected output structure.
#   Complexity: LOW
#   Method: Implement type checking and validation to confirm that the output is a list
#           of strings.
# -- END PRD --

from typing import List

import re


def format_landmarks_list(data: str) -> List[str]:
    """
    Formats a list of major landmarks into a standardized string list.

    Args:
        data: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse the input string containing major landmarks data
    # Handle various delimiters and formats
    if not data or not isinstance(data, str):
        return []
    
    # Split by common delimiters (comma, semicolon, newline, pipe)
    landmarks = re.split(r'[,;\n|]+', data)
    
    # Standardize the formatting of each landmark
    formatted_landmarks = []
    for landmark in landmarks:
        # Clean and standardize each landmark
        cleaned = landmark.strip()
        if cleaned:  # Skip empty strings
            # Remove extra whitespace and standardize format
            cleaned = re.sub(r'\s+', ' ', cleaned)
            # Apply title case formatting for consistency
            standardized = cleaned.title()
            formatted_landmarks.append(standardized)
    
    # Validate the output to ensure it meets the required List[str] format
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for landmark in formatted_landmarks:
        if landmark not in seen:
            seen.add(landmark)
            result.append(landmark)
    
    # Final validation - ensure all items are strings
    validated_result = [str(item) for item in result if item]
    
    return validated_result