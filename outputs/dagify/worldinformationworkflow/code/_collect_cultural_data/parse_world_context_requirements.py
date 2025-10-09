# -- PRD --
# 1. BULLET: Analyze the input world context string to identify key elements that define
#   cultural data requirements.
#   Reason: To accurately determine what cultural data is needed based on the world
#           context provided.
#   Impact: Ensures that subsequent data collection steps are focused on relevant
#           cultural aspects.
#   Complexity: MEDIUM
#   Method: Use natural language processing techniques to parse the world context
#           string and extract relevant information.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Map the identified elements to specific cultural data requirements.
#   Reason: To translate the world context elements into actionable data requirements.
#   Impact: Enables the system to know exactly what cultural data to collect.
#   Complexity: MEDIUM
#   Method: Implement a mapping logic that correlates world context elements with
#           predefined cultural data categories.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the cultural data requirements into a structured output.
#   Reason: To provide a standardized output that can be easily consumed by subsequent
#           processes.
#   Impact: Facilitates the integration with other components that rely on the
#           structured output.
#   Complexity: LOW
#   Method: Use a dictionary or a similar data structure to organize the cultural data
#           requirements and convert it to a JSON string.
# -- END PRD --

import json


def parse_world_context_requirements(world_context: str) -> str:
    """
    Parses the world context to determine specific cultural data requirements.

    Args:
        world_context: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Analyze the input world context string to identify key elements
    # Use natural language processing techniques to parse the world context
    
    # Define cultural data categories and keywords
    cultural_categories = {
        'language': ['language', 'speak', 'tongue', 'dialect', 'linguistic', 'communication'],
        'religion': ['religion', 'faith', 'belief', 'worship', 'spiritual', 'sacred', 'temple', 'church'],
        'traditions': ['tradition', 'custom', 'ritual', 'ceremony', 'festival', 'celebration'],
        'social_structure': ['social', 'hierarchy', 'class', 'caste', 'nobility', 'peasant', 'structure'],
        'governance': ['government', 'ruler', 'king', 'democracy', 'monarchy', 'law', 'politics'],
        'economics': ['trade', 'economy', 'currency', 'merchant', 'commerce', 'market'],
        'arts': ['art', 'music', 'dance', 'literature', 'poetry', 'craft', 'artistic'],
        'food': ['food', 'cuisine', 'cooking', 'meal', 'diet', 'culinary'],
        'clothing': ['clothing', 'dress', 'fashion', 'attire', 'garment', 'wear'],
        'architecture': ['architecture', 'building', 'construction', 'structure', 'design']
    }
    
    # Convert world context to lowercase for case-insensitive matching
    context_lower = world_context.lower()
    
    # Map identified elements to specific cultural data requirements
    cultural_requirements = {}
    
    for category, keywords in cultural_categories.items():
        # Check if any keywords from this category appear in the world context
        found_keywords = []
        for keyword in keywords:
            if keyword in context_lower:
                found_keywords.append(keyword)
        
        if found_keywords:
            cultural_requirements[category] = {
                'required': True,
                'keywords_found': found_keywords,
                'description': f'Cultural data for {category} is required based on context analysis'
            }
    
    # If no specific categories are identified, include basic requirements
    if not cultural_requirements:
        cultural_requirements = {
            'general': {
                'required': True,
                'keywords_found': [],
                'description': 'General cultural data required as no specific elements identified'
            }
        }
    
    # Format the cultural data requirements into a structured output
    # Use dictionary structure and convert to JSON string
    structured_output = {
        'cultural_data_requirements': cultural_requirements,
        'total_categories': len(cultural_requirements),
        'world_context_analyzed': world_context[:100] + '...' if len(world_context) > 100 else world_context
    }
    
    # Convert to JSON string for standardized output
    return json.dumps(structured_output, indent=2)