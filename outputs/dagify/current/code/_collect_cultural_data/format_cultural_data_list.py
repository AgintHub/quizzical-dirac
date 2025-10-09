# -- PRD --
# 1. BULLET: Validate the input data and data type to ensure they are not empty or null.
#   Reason: To prevent processing invalid or missing data.
#   Impact: Ensures the function operates on valid inputs, reducing potential errors.
#   Complexity: LOW
#   Method: Implement simple null checks at the beginning of the function.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Standardize the cultural data formatting based on the specified data type.
#   Reason: To maintain consistency in the output format regardless of the input data
#           type.
#   Impact: Enables downstream processes to rely on a consistent data format.
#   Complexity: MEDIUM
#   Method: Use a data type-driven approach with predefined formatting rules or
#           templates.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle specific formatting requirements for different cultural data types.
#   Reason: To accommodate varying formatting needs based on the cultural data type.
#   Impact: Enhances the flexibility and applicability of the function to different
#           cultural contexts.
#   Complexity: HIGH
#   Method: Implement a modular design with type-specific formatting functions or
#           classes.
# -- END PRD --

from typing import List

import re
import json


def format_cultural_data_list(data: str, data_type: str) -> List[str]:
    """
    Formats cultural data into a standardized list based on the input data type.

    Args:
        data: Input parameter of type str
data_type: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Validate input data and data_type to ensure they are not empty or null
    if not data or data is None:
        raise ValueError("Input data cannot be empty or null")
    if not data_type or data_type is None:
        raise ValueError("Data type cannot be empty or null")
    
    # Convert data_type to lowercase for consistent processing
    normalized_data_type = data_type.lower().strip()
    
    # Handle specific formatting requirements for different cultural data types
    if normalized_data_type == "name":
        # For names, split by common delimiters and standardize capitalization
        names = re.split(r'[,;\n\r]+', data)
        formatted_list = [name.strip().title() for name in names if name.strip()]
    
    elif normalized_data_type == "location" or normalized_data_type == "place":
        # For locations, split by common delimiters and standardize formatting
        locations = re.split(r'[,;\n\r]+', data)
        formatted_list = [location.strip().title() for location in locations if location.strip()]
    
    elif normalized_data_type == "date" or normalized_data_type == "event":
        # For dates/events, split by lines or semicolons and preserve original case
        events = re.split(r'[;\n\r]+', data)
        formatted_list = [event.strip() for event in events if event.strip()]
    
    elif normalized_data_type == "tradition" or normalized_data_type == "custom":
        # For traditions/customs, split by paragraphs or major delimiters
        traditions = re.split(r'\n\s*\n|;', data)
        formatted_list = [tradition.strip() for tradition in traditions if tradition.strip()]
    
    elif normalized_data_type == "language":
        # For languages, split and capitalize properly
        languages = re.split(r'[,;\n\r]+', data)
        formatted_list = [lang.strip().title() for lang in languages if lang.strip()]
    
    elif normalized_data_type == "artifact" or normalized_data_type == "item":
        # For artifacts/items, preserve formatting but clean up
        items = re.split(r'[,;\n\r]+', data)
        formatted_list = [item.strip() for item in items if item.strip()]
    
    elif normalized_data_type == "json" or normalized_data_type == "structured":
        # Try to parse as JSON and extract values
        try:
            parsed_data = json.loads(data)
            if isinstance(parsed_data, list):
                formatted_list = [str(item) for item in parsed_data]
            elif isinstance(parsed_data, dict):
                formatted_list = [str(value) for value in parsed_data.values() if value]
            else:
                formatted_list = [str(parsed_data)]
        except json.JSONDecodeError:
            # Fall back to simple splitting if JSON parsing fails
            formatted_list = [item.strip() for item in data.split(',') if item.strip()]
    
    else:
        # Default formatting: split by common delimiters and clean up
        items = re.split(r'[,;\n\r]+', data)
        formatted_list = [item.strip() for item in items if item.strip()]
    
    # Standardize the cultural data formatting - remove duplicates and ensure consistency
    # Remove empty strings and duplicates while preserving order
    seen = set()
    standardized_list = []
    for item in formatted_list:
        if item and item not in seen:
            seen.add(item)
            standardized_list.append(item)
    
    return standardized_list