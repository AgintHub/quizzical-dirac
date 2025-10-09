# -- PRD --
# 1. BULLET: Implement a data retrieval mechanism to fetch major landmarks based on the
#   given scope and countries.
#   Reason: This is necessary to fulfill the function's purpose of collecting major
#           landmarks.
#   Impact: The system will be able to gather relevant geographical data.
#   Complexity: MEDIUM
#   Method: Use an existing geographical data API or database to fetch the required
#           information.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle cases where the scope or countries are not specified or are invalid.
#   Reason: To ensure the function is robust and handles edge cases.
#   Impact: The function will be more reliable and less prone to errors.
#   Complexity: LOW
#   Method: Implement input validation and default values where applicable.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the output to match the required LIST_STR format.
#   Reason: To ensure compatibility with the expected output structure.
#   Impact: The output will be correctly formatted for further processing.
#   Complexity: LOW
#   Method: Use string manipulation and list formatting techniques.
# -- END PRD --

from typing import List


def collect_major_landmarks(scope: str, countries: str) -> List[str]:
    """
    A shim function that collects major landmarks within a given geographical scope and list of countries.

    Args:
        scope: Input parameter of type str
countries: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    # --- PURE IMPLEMENTATION ---
    
    # Input validation and default handling
    if not scope or not isinstance(scope, str):
        scope = "world"
    if not countries or not isinstance(countries, str):
        countries = ""
    
    # Parse countries string into a list
    country_list = [country.strip().lower() for country in countries.split(',') if country.strip()]
    
    # Hardcoded landmark database for major landmarks by country
    landmarks_db = {
        "usa": ["Statue of Liberty", "Grand Canyon", "Mount Rushmore", "Golden Gate Bridge"],
        "united states": ["Statue of Liberty", "Grand Canyon", "Mount Rushmore", "Golden Gate Bridge"],
        "france": ["Eiffel Tower", "Louvre Museum", "Arc de Triomphe", "Palace of Versailles"],
        "italy": ["Colosseum", "Leaning Tower of Pisa", "St. Peter's Basilica", "Trevi Fountain"],
        "egypt": ["Great Pyramid of Giza", "Sphinx", "Valley of the Kings", "Abu Simbel"],
        "china": ["Great Wall of China", "Forbidden City", "Terracotta Army", "Temple of Heaven"],
        "india": ["Taj Mahal", "Red Fort", "Gateway of India", "Qutub Minar"],
        "brazil": ["Christ the Redeemer", "Sugarloaf Mountain", "Iguazu Falls", "Copacabana Beach"],
        "australia": ["Sydney Opera House", "Uluru", "Great Barrier Reef", "Harbour Bridge"],
        "japan": ["Mount Fuji", "Tokyo Tower", "Fushimi Inari Shrine", "Kinkaku-ji Temple"],
        "uk": ["Big Ben", "Tower of London", "Stonehenge", "Buckingham Palace"],
        "united kingdom": ["Big Ben", "Tower of London", "Stonehenge", "Buckingham Palace"],
        "canada": ["CN Tower", "Niagara Falls", "Banff National Park", "Parliament Hill"],
        "russia": ["Red Square", "St. Basil's Cathedral", "Kremlin", "Hermitage Museum"],
        "germany": ["Brandenburg Gate", "Neuschwanstein Castle", "Cologne Cathedral", "Berlin Wall"]
    }
    
    # Collect landmarks based on scope and countries
    collected_landmarks = []
    
    if scope.lower() == "world" or scope.lower() == "global":
        if country_list:
            # Get landmarks for specified countries
            for country in country_list:
                if country in landmarks_db:
                    collected_landmarks.extend(landmarks_db[country])
        else:
            # Get landmarks from all countries if no specific countries specified
            for landmarks in landmarks_db.values():
                collected_landmarks.extend(landmarks)
    elif scope.lower() == "regional" or scope.lower() == "continent":
        # For regional scope, focus on specified countries or default to major global landmarks
        if country_list:
            for country in country_list:
                if country in landmarks_db:
                    collected_landmarks.extend(landmarks_db[country])
        else:
            # Default to some major world landmarks
            collected_landmarks = ["Eiffel Tower", "Great Wall of China", "Taj Mahal", "Statue of Liberty"]
    elif scope.lower() == "national" or scope.lower() == "country":
        # For national scope, only get landmarks from specified countries
        for country in country_list:
            if country in landmarks_db:
                collected_landmarks.extend(landmarks_db[country])
    else:
        # Default case for unknown scope
        if country_list:
            for country in country_list:
                if country in landmarks_db:
                    collected_landmarks.extend(landmarks_db[country])
        else:
            # Return some default major landmarks
            collected_landmarks = ["Eiffel Tower", "Great Wall of China", "Taj Mahal", "Statue of Liberty"]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_landmarks = []
    for landmark in collected_landmarks:
        if landmark not in seen:
            seen.add(landmark)
            unique_landmarks.append(landmark)
    
    return unique_landmarks