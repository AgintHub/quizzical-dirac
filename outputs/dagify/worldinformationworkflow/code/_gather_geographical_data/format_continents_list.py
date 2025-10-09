# -- PRD --
# 1. BULLET: The shim will take a list of continents as input and format it according to a
#   predefined structure.
#   Reason: This is necessary to ensure consistency in the output format across
#           different geographical data sources.
#   Impact: The formatted list of continents will be used in the
#           GatherGeographicalDataOutput model, which is crucial for
#           downstream processing.
#   Complexity: LOW
#   Method: Implement a simple string processing function that takes a list of
#           continent names and returns a formatted list.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The shim will handle variations in input data, such as different casing or
#   special characters.
#   Reason: To ensure the output is clean and standardized, regardless of the input
#           quality.
#   Impact: This will improve the overall robustness of the geographical data
#           processing pipeline.
#   Complexity: MEDIUM
#   Method: Use regular expressions and string normalization techniques to clean the
#           input data before formatting.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The shim will be designed to be extensible for future changes in output
#   format requirements.
#   Reason: To avoid potential rework if the output format specifications change.
#   Impact: This will make the system more adaptable to changing requirements.
#   Complexity: MEDIUM
#   Method: Implement the formatting logic using a modular design, allowing for easy
#           modification or extension of the formatting rules.
# -- END PRD --

from typing import List

import re


def format_continents_list(data: str) -> List[str]:
    """
    Formats a list of continents into a standardized output format.

    Args:
        data: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Handle empty or None input
    if not data or not data.strip():
        return []
    
    # Split the input string by common delimiters (comma, semicolon, newline, pipe)
    raw_continents = re.split(r'[,;\n|]+', data)
    
    # Clean and standardize each continent name
    formatted_continents = []
    
    for continent in raw_continents:
        # Remove leading/trailing whitespace
        cleaned = continent.strip()
        
        # Skip empty strings
        if not cleaned:
            continue
            
        # Remove special characters except spaces, hyphens, and apostrophes
        cleaned = re.sub(r'[^a-zA-Z\s\-\']+', '', cleaned)
        
        # Normalize whitespace (replace multiple spaces with single space)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Capitalize each word (title case)
        cleaned = cleaned.title()
        
        # Handle common continent name variations and standardize
        continent_mapping = {
            'N America': 'North America',
            'N. America': 'North America',
            'S America': 'South America', 
            'S. America': 'South America',
            'Australia/Oceania': 'Australia',
            'Oceania': 'Australia',
            'Antarctic': 'Antarctica',
            'Europe/Asia': 'Eurasia'
        }
        
        # Apply mapping if exists
        if cleaned in continent_mapping:
            cleaned = continent_mapping[cleaned]
            
        # Only add non-empty, valid continent names
        if cleaned and len(cleaned) > 1:
            formatted_continents.append(cleaned)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for continent in formatted_continents:
        if continent not in seen:
            seen.add(continent)
            result.append(continent)
    
    return result