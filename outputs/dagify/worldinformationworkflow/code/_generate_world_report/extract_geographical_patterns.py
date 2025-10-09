# -- PRD --
# 1. BULLET: Identify and parse the input patterns to understand the structure and
#   content.
#   Reason: To accurately extract geographical patterns, the input data must be
#           properly understood.
#   Impact: Correct parsing will lead to more accurate extraction of geographical
#           patterns.
#   Complexity: MEDIUM
#   Method: Use a parsing library or implement a custom parser based on the expected
#           format of the input patterns.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a filtering mechanism to identify geographical patterns within the
#   parsed data.
#   Reason: Geographical patterns need to be distinguished from other types of
#           patterns.
#   Impact: Effective filtering will ensure that only relevant geographical patterns
#           are extracted.
#   Complexity: HIGH
#   Method: Utilize natural language processing (NLP) techniques or predefined
#           geographical keywords to filter the patterns.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the extracted geographical patterns into a list for output.
#   Reason: The output needs to be in a structured format as per the node's output
#           structure.
#   Impact: Proper formatting will ensure compatibility with downstream nodes.
#   Complexity: LOW
#   Method: Use standard list data structures and ensure that all extracted patterns
#           are correctly appended to the output list.
# -- END PRD --

import re
import json


def extract_geographical_patterns(patterns: str) -> str:
    """
    Extract geographical patterns from the given input patterns.

    Args:
        patterns: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Parse the input patterns to understand structure and content
    lines = patterns.strip().split('\n')
    parsed_patterns = []
    for line in lines:
        if line.strip():
            parsed_patterns.append(line.strip())
    
    # Define geographical keywords and patterns for filtering
    geographical_keywords = {
        'continents': ['africa', 'asia', 'europe', 'north america', 'south america', 'antarctica', 'oceania'],
        'countries': ['usa', 'united states', 'canada', 'mexico', 'brazil', 'argentina', 'china', 'india', 'japan', 'germany', 'france', 'italy', 'spain', 'uk', 'united kingdom', 'russia', 'australia'],
        'cities': ['new york', 'london', 'paris', 'tokyo', 'beijing', 'mumbai', 'delhi', 'shanghai', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 'san antonio', 'san diego', 'dallas', 'san jose'],
        'geographical_terms': ['mountain', 'river', 'ocean', 'sea', 'lake', 'desert', 'forest', 'valley', 'plateau', 'peninsula', 'island', 'coast', 'bay', 'gulf', 'strait', 'canyon', 'plain', 'hill', 'beach', 'harbor']
    }
    
    # Flatten all geographical keywords for easier searching
    all_geo_keywords = []
    for category in geographical_keywords.values():
        all_geo_keywords.extend(category)
    
    # Extract geographical patterns from parsed data
    extracted_geographical_patterns = []
    
    for pattern in parsed_patterns:
        pattern_lower = pattern.lower()
        
        # Check if pattern contains geographical keywords
        contains_geo = False
        for keyword in all_geo_keywords:
            if keyword in pattern_lower:
                contains_geo = True
                break
        
        # Check for coordinate patterns (latitude/longitude)
        coordinate_pattern = r'[-+]?\d{1,3}\.\d+[°]?\s*[NS]?\s*,?\s*[-+]?\d{1,3}\.\d+[°]?\s*[EW]?'
        if re.search(coordinate_pattern, pattern, re.IGNORECASE):
            contains_geo = True
        
        # Check for postal codes and area codes
        postal_pattern = r'\b\d{5}(-\d{4})?\b|\b[A-Z]\d[A-Z]\s?\d[A-Z]\d\b'
        if re.search(postal_pattern, pattern):
            contains_geo = True
        
        # Check for directional indicators
        directional_pattern = r'\b(north|south|east|west|northeast|northwest|southeast|southwest|central|northern|southern|eastern|western)\b'
        if re.search(directional_pattern, pattern, re.IGNORECASE):
            contains_geo = True
        
        if contains_geo:
            extracted_geographical_patterns.append(pattern)
    
    # Format the extracted geographical patterns into a list for output
    # Convert list to string representation as required by return type
    return json.dumps(extracted_geographical_patterns)