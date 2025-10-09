# -- PRD --
# 1. BULLET: The shim will receive a list of cultural practices as input and return a
#   processed list of cultural practices data.
#   Reason: This is necessary to transform the raw cultural practices data into a
#           format that can be analyzed further.
#   Impact: The output will be used to identify cultural patterns and themes, which
#           will be crucial for understanding the cultural context.
#   Complexity: MEDIUM
#   Method: The implementation will involve parsing the input string, potentially using
#           NLP techniques or simple string manipulation to extract
#           relevant information.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The shim should handle diverse cultural practices data, including different
#   formats and structures.
#   Reason: Cultural practices data can vary significantly in terms of content and
#           format, and the shim needs to be able to accommodate this
#           variability.
#   Impact: This will ensure that the shim can be used in different cultural contexts
#           without requiring significant modifications.
#   Complexity: HIGH
#   Method: The implementation will involve developing a flexible parsing mechanism
#           that can handle different data formats, potentially using
#           machine learning models or rule-based approaches.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The output of the shim should be a list of strings that can be easily
#   integrated into the subsequent analysis pipeline.
#   Reason: The subsequent analysis steps require the cultural practices data to be in
#           a specific format.
#   Impact: This will enable seamless integration with the downstream analysis
#           components, facilitating the identification of cultural
#           patterns and themes.
#   Complexity: LOW
#   Method: The implementation will involve ensuring that the output is correctly
#           formatted as a list of strings, potentially involving data type
#           conversions or simple data transformations.
# -- END PRD --

from typing import List

import re
import json


def extract_cultural_practices_data(practices: str) -> List[str]:
    """
    Extracts and processes cultural practices data from the input list of cultural practices.

    Args:
        practices: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Handle empty or None input
    if not practices or not practices.strip():
        return []
    
    # Initialize result list
    extracted_practices = []
    
    # Try to parse as JSON first (structured data)
    try:
        parsed_data = json.loads(practices)
        if isinstance(parsed_data, list):
            for item in parsed_data:
                if isinstance(item, str):
                    extracted_practices.append(item.strip())
                elif isinstance(item, dict):
                    # Extract text values from dictionary
                    for value in item.values():
                        if isinstance(value, str) and value.strip():
                            extracted_practices.append(value.strip())
                else:
                    extracted_practices.append(str(item).strip())
        elif isinstance(parsed_data, dict):
            # Extract values from dictionary
            for value in parsed_data.values():
                if isinstance(value, str) and value.strip():
                    extracted_practices.append(value.strip())
                elif isinstance(value, list):
                    for sub_item in value:
                        if isinstance(sub_item, str) and sub_item.strip():
                            extracted_practices.append(sub_item.strip())
        else:
            extracted_practices.append(str(parsed_data).strip())
    except (json.JSONDecodeError, TypeError):
        # If not JSON, treat as plain text and extract practices
        
        # Split by common delimiters
        text = practices.replace('\n', '|').replace('\r', '|')
        
        # Split by various delimiters
        delimiters = r'[;,\|\n\r]|\d+\.|\*|\-\s'
        segments = re.split(delimiters, text)
        
        for segment in segments:
            segment = segment.strip()
            if segment and len(segment) > 3:  # Filter out very short segments
                # Clean up the segment
                cleaned_segment = re.sub(r'^[\d\W]+', '', segment)  # Remove leading numbers/symbols
                cleaned_segment = cleaned_segment.strip()
                if cleaned_segment and len(cleaned_segment) > 3:
                    extracted_practices.append(cleaned_segment)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_practices = []
    for practice in extracted_practices:
        if practice and practice.lower() not in seen:
            seen.add(practice.lower())
            unique_practices.append(practice)
    
    # Filter out very short or meaningless entries
    filtered_practices = [
        practice for practice in unique_practices 
        if len(practice) > 3 and not re.match(r'^[\d\W]+$', practice)
    ]
    
    return filtered_practices