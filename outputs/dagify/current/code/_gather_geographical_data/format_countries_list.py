# -- PRD --
# 1. BULLET: The shim function will parse the input string containing country data and
#   convert it into a list of country names.
#   Reason: This is necessary to standardize the input data for further processing.
#   Impact: The output will be a list of country names that can be used for subsequent
#           operations.
#   Complexity: MEDIUM
#   Method: The function can use a combination of string manipulation and parsing
#           techniques, such as splitting the input string by a delimiter
#           or using a regular expression to extract country names.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The function will handle different input formats by implementing a flexible
#   parsing mechanism.
#   Reason: This allows the function to accommodate various input data formats.
#   Impact: The function will be able to process different types of input data, making
#           it more robust.
#   Complexity: HIGH
#   Method: The function can use techniques such as regular expressions or configurable
#           parsing rules to handle different input formats.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The output will be a list of country names in a standardized format, which
#   can be used for further processing or output.
#   Reason: Standardizing the output format is crucial for ensuring compatibility with
#           downstream processes.
#   Impact: The standardized output will enable seamless integration with other
#           components or systems.
#   Complexity: LOW
#   Method: The function can achieve this by using a consistent formatting approach,
#           such as converting all country names to title case or trimming
#           unnecessary whitespace.
# -- END PRD --

from typing import List

import re


def format_countries_list(data: str) -> List[str]:
    """
    A shim function that formats a list of countries into a standardized output format.

    Args:
        data: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Handle empty or None input
    if not data or not data.strip():
        return []
    
    # Clean the input data
    cleaned_data = data.strip()
    
    # Try multiple parsing approaches to handle different input formats
    countries = []
    
    # First, try splitting by common delimiters
    # Check for comma separation
    if ',' in cleaned_data:
        countries = [country.strip() for country in cleaned_data.split(',')]
    # Check for semicolon separation
    elif ';' in cleaned_data:
        countries = [country.strip() for country in cleaned_data.split(';')]
    # Check for pipe separation
    elif '|' in cleaned_data:
        countries = [country.strip() for country in cleaned_data.split('|')]
    # Check for newline separation
    elif '\n' in cleaned_data:
        countries = [country.strip() for country in cleaned_data.split('\n')]
    # Check for tab separation
    elif '\t' in cleaned_data:
        countries = [country.strip() for country in cleaned_data.split('\t')]
    # Try to extract using regex patterns for structured data
    else:
        # Look for patterns like "Country: CountryName" or "- CountryName"
        country_patterns = [
            r'(?:Country|country)\s*:?\s*([A-Za-z\s]+)',
            r'-\s*([A-Za-z\s]+)',
            r'\*\s*([A-Za-z\s]+)',
            r'\d+\.\s*([A-Za-z\s]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # Title case words
        ]
        
        for pattern in country_patterns:
            matches = re.findall(pattern, cleaned_data)
            if matches:
                countries.extend(matches)
                break
        
        # If no patterns match, treat the entire string as a single country
        if not countries:
            countries = [cleaned_data]
    
    # Standardize the output format
    standardized_countries = []
    for country in countries:
        if country and country.strip():
            # Remove extra whitespace and convert to title case
            standardized_country = ' '.join(country.strip().split()).title()
            # Remove any remaining unwanted characters
            standardized_country = re.sub(r'[^A-Za-z\s]', '', standardized_country).strip()
            if standardized_country:
                standardized_countries.append(standardized_country)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for country in standardized_countries:
        if country not in seen:
            seen.add(country)
            result.append(country)
    
    return result