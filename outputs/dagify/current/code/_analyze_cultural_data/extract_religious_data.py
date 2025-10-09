# -- PRD --
# 1. BULLET: Parse the input string containing major religions into a list for processing.
#   Reason: The input is expected to be a string that needs to be converted into a list
#           for further processing.
#   Impact: Successful parsing will enable the function to process the religious data
#           correctly.
#   Complexity: LOW
#   Method: Use a string splitting method based on a delimiter (e.g., comma-separated
#           values) to create a list of religions.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a data processing logic to extract relevant information from the
#   list of religions.
#   Reason: To provide a structured output that can be used in subsequent analyses.
#   Impact: The processed data will be used to identify cultural patterns and themes.
#   Complexity: MEDIUM
#   Method: Apply natural language processing (NLP) techniques or simple data filtering
#           based on predefined criteria to extract relevant information.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the processed religious data as a list of strings.
#   Reason: The output needs to be in a format that can be easily consumed by
#           subsequent nodes in the workflow.
#   Impact: The output will be used as input for further analysis, such as identifying
#           cultural patterns.
#   Complexity: LOW
#   Method: Simply return the processed list of religious data as is, or format it
#           according to the required output structure.
# -- END PRD --

import re
from typing import List


def extract_religious_data(religions: str) -> List[str]:
    """
    A shim function that extracts and processes religious data from a given list of major religions.

    Args:
        religions: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse the input string containing major religions into a list for processing
    # Split by common delimiters (comma, semicolon, newline) and clean whitespace
    religions_list = re.split(r'[,;\n]+', religions)
    religions_list = [religion.strip() for religion in religions_list if religion.strip()]
    
    # Implement data processing logic to extract relevant information
    processed_religions = []
    for religion in religions_list:
        # Clean and normalize the religion name
        # Remove extra whitespace, convert to title case for consistency
        cleaned_religion = re.sub(r'\s+', ' ', religion).strip().title()
        
        # Filter out invalid entries (too short, non-alphabetic characters)
        if len(cleaned_religion) >= 2 and re.match(r'^[A-Za-z\s-]+$', cleaned_religion):
            processed_religions.append(cleaned_religion)
    
    # Return the processed religious data as a list of strings
    return processed_religions