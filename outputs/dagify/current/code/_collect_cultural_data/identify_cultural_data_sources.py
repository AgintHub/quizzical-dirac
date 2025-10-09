# -- PRD --
# 1. BULLET: Develop an algorithm to parse the world context and extract specific cultural
#   data requirements.
#   Reason: To accurately identify the type of cultural data needed.
#   Impact: Ensures that the data collection is focused and relevant to the workflow.
#   Complexity: MEDIUM
#   Method: Utilize Natural Language Processing (NLP) techniques to analyze the world
#           context and requirements.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create a database or utilize an existing knowledge base of reliable cultural
#   data sources.
#   Reason: To have a comprehensive list of sources to draw from based on the extracted
#           requirements.
#   Impact: Enhances the accuracy and reliability of the collected cultural data.
#   Complexity: HIGH
#   Method: Aggregate data from reputable sources such as academic journals, cultural
#           databases, and established encyclopedias.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Implement a filtering mechanism to match the identified requirements with the
#   available data sources.
#   Reason: To ensure that the sources used are relevant to the specific cultural data
#           needs.
#   Impact: Increases the efficiency of the data collection process by focusing on
#           relevant sources.
#   Complexity: MEDIUM
#   Method: Use a combination of keyword matching and semantic analysis to filter
#           sources.
# -- END PRD --

from typing import List


def identify_cultural_data_sources(world_context: str, requirements: str) -> List[str]:
    """
    Identifies reliable sources for cultural data collection based on the world context and specific cultural data requirements.

    Args:
        world_context: Input parameter of type str
requirements: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse world context and requirements to extract cultural data needs
    combined_text = f"{world_context} {requirements}".lower()
    
    # Extract key cultural themes using NLP techniques
    cultural_keywords = [
        'tradition', 'custom', 'ritual', 'belief', 'religion', 'language', 
        'festival', 'ceremony', 'heritage', 'folklore', 'mythology', 'art',
        'music', 'dance', 'food', 'clothing', 'architecture', 'history',
        'social', 'family', 'community', 'values', 'ethics', 'philosophy'
    ]
    
    # Identify relevant cultural themes present in the context
    identified_themes = []
    for keyword in cultural_keywords:
        if keyword in combined_text:
            identified_themes.append(keyword)
    
    # Comprehensive database of reliable cultural data sources
    cultural_data_sources = {
        'academic': [
            'JSTOR Academic Papers on Cultural Studies',
            'Anthropology Plus Database',
            'Oxford Bibliography of Anthropology',
            'Cambridge Cultural History Collections',
            'Sage Cultural Studies Database'
        ],
        'encyclopedias': [
            'Encyclopedia Britannica Cultural Entries',
            'Encyclopedia of World Cultures',
            'Countries and Their Cultures Database',
            'Cultural Atlas by National Geographic',
            'World Culture Encyclopedia'
        ],
        'institutional': [
            'UNESCO Cultural Heritage Database',
            'Smithsonian Center for Folklife and Cultural Heritage',
            'Library of Congress Country Studies',
            'CIA World Factbook Cultural Sections',
            'National Geographic Society Cultural Resources'
        ],
        'specialized': [
            'Ethnologue Language Database',
            'Religious Studies Database',
            'World Music Central',
            'Traditional Arts and Crafts Database',
            'Folklore and Mythology Electronic Texts'
        ]
    }
    
    # Flatten all sources into a single list
    all_sources = []
    for category in cultural_data_sources.values():
        all_sources.extend(category)
    
    # Filter sources based on identified themes and requirements
    relevant_sources = []
    
    # If specific themes were identified, prioritize sources that match
    if identified_themes:
        # Use semantic matching for theme-specific sources
        theme_source_mapping = {
            'religion': ['Religious Studies Database', 'Encyclopedia Britannica Cultural Entries'],
            'language': ['Ethnologue Language Database', 'Library of Congress Country Studies'],
            'music': ['World Music Central', 'Smithsonian Center for Folklife and Cultural Heritage'],
            'art': ['Traditional Arts and Crafts Database', 'National Geographic Society Cultural Resources'],
            'history': ['Cambridge Cultural History Collections', 'CIA World Factbook Cultural Sections'],
            'tradition': ['Encyclopedia of World Cultures', 'UNESCO Cultural Heritage Database'],
            'folklore': ['Folklore and Mythology Electronic Texts', 'Cultural Atlas by National Geographic']
        }
        
        for theme in identified_themes:
            if theme in theme_source_mapping:
                relevant_sources.extend(theme_source_mapping[theme])
    
    # Always include core reliable sources
    core_sources = [
        'Encyclopedia Britannica Cultural Entries',
        'UNESCO Cultural Heritage Database',
        'Library of Congress Country Studies',
        'Encyclopedia of World Cultures',
        'JSTOR Academic Papers on Cultural Studies'
    ]
    
    relevant_sources.extend(core_sources)
    
    # Remove duplicates while preserving order
    final_sources = []
    seen = set()
    for source in relevant_sources:
        if source not in seen:
            final_sources.append(source)
            seen.add(source)
    
    # If no specific themes identified, return a balanced set of reliable sources
    if not final_sources:
        final_sources = [
            'Encyclopedia Britannica Cultural Entries',
            'UNESCO Cultural Heritage Database', 
            'Library of Congress Country Studies',
            'JSTOR Academic Papers on Cultural Studies',
            'Encyclopedia of World Cultures',
            'Smithsonian Center for Folklife and Cultural Heritage',
            'National Geographic Society Cultural Resources'
        ]
    
    return final_sources[:10]  # Return top 10 most relevant sources