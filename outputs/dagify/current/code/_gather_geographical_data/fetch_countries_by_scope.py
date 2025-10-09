# -- PRD --
# 1. BULLET: Implement a geographical data retrieval mechanism that can fetch countries
#   based on a given scope and list of continents.
#   Reason: This functionality is necessary to populate the list of countries in the
#           GatherGeographicalDataOutput.
#   Impact: The system will be able to provide a list of countries relevant to the
#           defined world context.
#   Complexity: MEDIUM
#   Method: Utilize a geographical data API or database that supports querying by scope
#           and continent.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Ensure the shim can handle different types of scope definitions (e.g.,
#   global, regional) and varying continent inputs.
#   Reason: The shim needs to be flexible to accommodate different world contexts.
#   Impact: The system will be more robust and able to handle a variety of inputs.
#   Complexity: HIGH
#   Method: Implement conditional logic to handle different scope types and continent
#           combinations, potentially using a data-driven approach.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the inputs (scope and continents) to ensure they are valid and
#   correctly formatted.
#   Reason: To prevent errors and ensure the shim operates correctly.
#   Impact: The system will be more reliable and less prone to errors due to invalid
#           inputs.
#   Complexity: LOW
#   Method: Use input validation techniques such as checking against predefined lists
#           or using regular expressions.
# -- END PRD --

from typing import List

import re


def fetch_countries_by_scope(scope: str, continents: str) -> List[str]:
    """
    Fetches a list of countries based on the given scope and continents.

    Args:
        scope: Input parameter of type str
continents: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Define geographical data mapping
    continent_country_map = {
        'africa': ['Nigeria', 'Egypt', 'South Africa', 'Kenya', 'Morocco', 'Ghana', 'Ethiopia', 'Tunisia', 'Algeria', 'Uganda'],
        'asia': ['China', 'India', 'Japan', 'South Korea', 'Indonesia', 'Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Philippines'],
        'europe': ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain', 'Netherlands', 'Poland', 'Belgium', 'Sweden', 'Norway'],
        'north america': ['United States', 'Canada', 'Mexico', 'Guatemala', 'Cuba', 'Honduras', 'Nicaragua', 'Costa Rica', 'Panama', 'Jamaica'],
        'south america': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Venezuela', 'Ecuador', 'Bolivia', 'Uruguay', 'Paraguay'],
        'oceania': ['Australia', 'New Zealand', 'Fiji', 'Papua New Guinea', 'Samoa', 'Tonga', 'Vanuatu', 'Solomon Islands', 'Palau', 'Micronesia'],
        'antarctica': ['Antarctica Research Stations']
    }
    
    # Validate and normalize scope input
    valid_scopes = ['global', 'regional', 'continental', 'local']
    scope_normalized = scope.lower().strip()
    if scope_normalized not in valid_scopes:
        raise ValueError(f"Invalid scope '{scope}'. Valid scopes are: {valid_scopes}")
    
    # Parse and validate continents input
    if not continents or not isinstance(continents, str):
        raise ValueError("Continents parameter must be a non-empty string")
    
    # Split continents by common delimiters and normalize
    continent_list = re.split(r'[,;\|]+', continents.lower())
    continent_list = [c.strip() for c in continent_list if c.strip()]
    
    if not continent_list:
        raise ValueError("No valid continents found in the input")
    
    # Validate continent names
    valid_continents = list(continent_country_map.keys())
    invalid_continents = [c for c in continent_list if c not in valid_continents]
    if invalid_continents:
        raise ValueError(f"Invalid continents: {invalid_continents}. Valid continents are: {valid_continents}")
    
    # Fetch countries based on scope and continents
    result_countries = []
    
    for continent in continent_list:
        if continent in continent_country_map:
            countries = continent_country_map[continent]
            
            # Apply scope-based filtering
            if scope_normalized == 'global':
                # Return all countries from specified continents
                result_countries.extend(countries)
            elif scope_normalized == 'regional':
                # Return top 5 countries per continent (regional focus)
                result_countries.extend(countries[:5])
            elif scope_normalized == 'continental':
                # Return all countries from the continent
                result_countries.extend(countries)
            elif scope_normalized == 'local':
                # Return top 3 countries per continent (local focus)
                result_countries.extend(countries[:3])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_countries = []
    for country in result_countries:
        if country not in seen:
            seen.add(country)
            unique_countries.append(country)
    
    return unique_countries