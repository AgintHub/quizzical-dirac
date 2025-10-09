# -- PRD --
# 1. BULLET: Implement a data source connector to fetch geographical data.
#   Reason: To provide the required functionality, we need to connect to a reliable
#           geographical data source.
#   Impact: Enables the node to retrieve accurate geographical data.
#   Complexity: MEDIUM
#   Method: Utilize an existing geographical data API or database, such as GeoNames or
#           Natural Earth, to fetch the required data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Parse the geographical scope to determine the relevant continents.
#   Reason: The scope will dictate which continents are relevant, requiring parsing to
#           identify the correct data.
#   Impact: Ensures that the node returns the correct continents based on the provided
#           scope.
#   Complexity: LOW
#   Method: Use a simple string comparison or a more complex parsing logic depending on
#           the scope's format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle errors and exceptions from the data source connection.
#   Reason: To ensure robustness, the node must handle potential errors from the data
#           source.
#   Impact: Prevents the node from failing unexpectedly due to external data source
#           issues.
#   Complexity: MEDIUM
#   Method: Implement try-except blocks to catch and handle exceptions, potentially
#           retrying the connection or returning a default value.
# -- END PRD --

from typing import List

import requests


def fetch_continents_from_geo_source(scope: str) -> List[str]:
    """
    Fetches a list of continents based on the geographical scope provided.

    Args:
        scope: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Define all continents for reference
    all_continents = [
        "Africa", "Antarctica", "Asia", "Europe", 
        "North America", "Oceania", "South America"
    ]
    
    try:
        # Parse the geographical scope to determine relevant continents
        scope_lower = scope.lower().strip()
        
        # Handle different scope formats
        if scope_lower in ["global", "world", "all", "worldwide"]:
            return all_continents
        elif scope_lower in ["africa", "african"]:
            return ["Africa"]
        elif scope_lower in ["antarctica", "antarctic"]:
            return ["Antarctica"]
        elif scope_lower in ["asia", "asian"]:
            return ["Asia"]
        elif scope_lower in ["europe", "european"]:
            return ["Europe"]
        elif scope_lower in ["north america", "north american", "northamerica"]:
            return ["North America"]
        elif scope_lower in ["oceania", "oceanic", "australia", "australian"]:
            return ["Oceania"]
        elif scope_lower in ["south america", "south american", "southamerica"]:
            return ["South America"]
        elif "america" in scope_lower and "north" not in scope_lower and "south" not in scope_lower:
            return ["North America", "South America"]
        else:
            # Try to extract continent names from the scope string
            found_continents = []
            for continent in all_continents:
                if continent.lower() in scope_lower:
                    found_continents.append(continent)
            
            if found_continents:
                return found_continents
            else:
                # If no specific continents found, try external geo data source
                try:
                    # Attempt to use a geographical data API (fallback implementation)
                    # Using REST Countries API as a reliable free source
                    response = requests.get(f"https://restcountries.com/v3.1/name/{scope}", timeout=5)
                    if response.status_code == 200:
                        countries_data = response.json()
                        continents_found = set()
                        for country in countries_data:
                            if 'continents' in country:
                                continents_found.update(country['continents'])
                        return list(continents_found) if continents_found else ["Europe"]  # Default fallback
                    else:
                        return ["Europe"]  # Default fallback
                except requests.exceptions.RequestException:
                    # Fallback to default if external API fails
                    return ["Europe"]  # Default fallback
    
    except Exception as e:
        # Handle any unexpected errors and return a default value
        print(f"Error processing geographical scope: {e}")
        return ["Europe"]  # Default fallback continent