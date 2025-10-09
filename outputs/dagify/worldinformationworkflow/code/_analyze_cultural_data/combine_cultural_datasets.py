# -- PRD --
# 1. BULLET: The shim function will take three input parameters: religions, languages, and
#   practices, all of type str, representing lists of cultural data.
#   Reason: These inputs are necessary to combine the different aspects of cultural
#           data into a single dataset.
#   Impact: The combined dataset will be used for further analysis, such as identifying
#           cultural themes and patterns.
#   Complexity: MEDIUM
#   Method: The function will need to parse the input strings into lists, merge them,
#           and then output the combined list. This may involve handling
#           different data formats and potential inconsistencies in the
#           input data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The function will output a single list of type List[str] containing the
#   combined cultural data.
#   Reason: A unified list is required for subsequent analysis steps, such as theme
#           identification and pattern detection.
#   Impact: The output will directly influence the quality and accuracy of the cultural
#           analysis performed in later stages.
#   Complexity: LOW
#   Method: The output can be achieved by simply concatenating the input lists after
#           parsing them into a suitable format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Error handling will be necessary to manage cases where the input data is
#   malformed or inconsistent.
#   Reason: Robust error handling ensures the function remains reliable even when faced
#           with unexpected input.
#   Impact: Proper error handling will prevent the function from failing unexpectedly
#           and provide useful feedback instead.
#   Complexity: HIGH
#   Method: Implementing try-except blocks and input validation checks will be crucial
#           for managing potential errors and exceptions.
# -- END PRD --

from typing import List

import json
import ast


def combine_cultural_datasets(religions: str, languages: str, practices: str) -> List[str]:
    """
    Combines cultural datasets from various categories into a unified list.

    Args:
        religions: Input parameter of type str
languages: Input parameter of type str
practices: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    combined_data = []
    
    # Process each input parameter
    for data_str in [religions, languages, practices]:
        if not data_str:
            continue
            
        try:
            # Try to parse as JSON array first
            if data_str.strip().startswith('[') and data_str.strip().endswith(']'):
                try:
                    parsed_data = json.loads(data_str)
                    if isinstance(parsed_data, list):
                        combined_data.extend([str(item) for item in parsed_data])
                        continue
                except json.JSONDecodeError:
                    pass
                
                # Try using ast.literal_eval for Python list format
                try:
                    parsed_data = ast.literal_eval(data_str)
                    if isinstance(parsed_data, list):
                        combined_data.extend([str(item) for item in parsed_data])
                        continue
                except (ValueError, SyntaxError):
                    pass
            
            # Try comma-separated values
            if ',' in data_str:
                items = [item.strip() for item in data_str.split(',')]
                combined_data.extend([item for item in items if item])
            else:
                # Treat as single item if not empty
                data_str = data_str.strip()
                if data_str:
                    combined_data.append(data_str)
                    
        except Exception as e:
            # Error handling for malformed data
            print(f"Warning: Could not parse data '{data_str}': {e}")
            # Try to salvage by treating as single string item
            data_str = data_str.strip()
            if data_str:
                combined_data.append(data_str)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for item in combined_data:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result