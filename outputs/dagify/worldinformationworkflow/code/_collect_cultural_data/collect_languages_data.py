# -- PRD --
# 1. BULLET: Implement data collection from various sources such as databases, APIs, or
#   files based on the provided sources parameter.
#   Reason: To gather comprehensive language data relevant to the defined world
#           context.
#   Impact: Enhances the cultural data collection process by providing a flexible data
#           sourcing mechanism.
#   Complexity: MEDIUM
#   Method: Use a modular approach to handle different data sources, possibly
#           leveraging existing libraries or frameworks for data access.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the collected language data to ensure it is accurate and relevant to
#   the world context.
#   Reason: To maintain data quality and relevance.
#   Impact: Improves the reliability of the cultural data used in subsequent workflow
#           steps.
#   Complexity: HIGH
#   Method: Implement data validation rules based on the world context and cultural
#           requirements, potentially using machine learning models or
#           rule-based systems.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the collected language data into a standardized list format as
#   required by the output structure.
#   Reason: To comply with the specified output format.
#   Impact: Ensures compatibility with downstream processes expecting the standardized
#           output.
#   Complexity: LOW
#   Method: Use data transformation techniques to convert the collected data into the
#           required list format.
# -- END PRD --

from typing import List


def collect_languages_data(world_context: str, sources: str) -> List[str]:
    """
    A shim function to collect languages data for a given world context and sources.

    Args:
        world_context: Input parameter of type str
sources: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Initialize the languages data collection
    collected_languages = []
    
    # Parse sources parameter to determine data collection methods
    source_types = [s.strip().lower() for s in sources.split(',')]
    
    # Extract world context characteristics for validation
    world_context_lower = world_context.lower()
    
    # Define language data based on world context
    fantasy_languages = ['elvish', 'dwarvish', 'orcish', 'draconic', 'common', 'sylvan', 'celestial', 'infernal']
    scifi_languages = ['galactic basic', 'klingon', 'vulcan', 'binary', 'android', 'alien dialect', 'universal translator']
    modern_languages = ['english', 'spanish', 'french', 'german', 'japanese', 'chinese', 'arabic', 'russian']
    historical_languages = ['latin', 'ancient greek', 'old english', 'sanskrit', 'hebrew', 'egyptian hieroglyphs']
    
    # Collect data from various sources
    for source_type in source_types:
        if source_type == 'database':
            # Simulate database collection
            if 'fantasy' in world_context_lower or 'medieval' in world_context_lower:
                collected_languages.extend(fantasy_languages[:4])
            elif 'sci-fi' in world_context_lower or 'future' in world_context_lower:
                collected_languages.extend(scifi_languages[:3])
            elif 'modern' in world_context_lower or 'contemporary' in world_context_lower:
                collected_languages.extend(modern_languages[:5])
            elif 'historical' in world_context_lower or 'ancient' in world_context_lower:
                collected_languages.extend(historical_languages[:3])
                
        elif source_type == 'api':
            # Simulate API data collection
            if 'multicultural' in world_context_lower or 'diverse' in world_context_lower:
                collected_languages.extend(['mandarin', 'hindi', 'portuguese', 'bengali'])
            if 'gaming' in world_context_lower:
                collected_languages.extend(['common tongue', 'trade language'])
                
        elif source_type == 'files' or source_type == 'file':
            # Simulate file-based collection
            if 'regional' in world_context_lower:
                collected_languages.extend(['local dialect', 'regional variant'])
            if 'tribal' in world_context_lower:
                collected_languages.extend(['tribal language', 'ancestral tongue'])
    
    # Validate collected data against world context
    validated_languages = []
    for language in collected_languages:
        # Validation rules based on world context
        language_clean = language.strip().lower()
        
        # Check relevance to world context
        is_relevant = False
        
        if 'fantasy' in world_context_lower and language_clean in [l.lower() for l in fantasy_languages]:
            is_relevant = True
        elif 'sci-fi' in world_context_lower and language_clean in [l.lower() for l in scifi_languages]:
            is_relevant = True
        elif 'modern' in world_context_lower and language_clean in [l.lower() for l in modern_languages]:
            is_relevant = True
        elif 'historical' in world_context_lower and language_clean in [l.lower() for l in historical_languages]:
            is_relevant = True
        elif any(keyword in world_context_lower for keyword in ['multicultural', 'diverse', 'global']):
            is_relevant = True
        
        # Additional validation - ensure non-empty and properly formatted
        if is_relevant and language_clean and len(language_clean) > 1:
            # Format the language name properly
            formatted_language = ' '.join(word.capitalize() for word in language_clean.split())
            if formatted_language not in validated_languages:
                validated_languages.append(formatted_language)
    
    # If no specific languages found, provide default based on context
    if not validated_languages:
        if 'fantasy' in world_context_lower:
            validated_languages = ['Common', 'Elvish']
        elif 'sci-fi' in world_context_lower:
            validated_languages = ['Galactic Basic', 'Universal Translator']
        else:
            validated_languages = ['English', 'Common Tongue']
    
    # Format into standardized list (remove duplicates and sort)
    final_languages = sorted(list(set(validated_languages)))
    
    return final_languages