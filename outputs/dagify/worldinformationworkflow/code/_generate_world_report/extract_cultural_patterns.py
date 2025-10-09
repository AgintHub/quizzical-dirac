# -- PRD --
# 1. BULLET: Identify and extract cultural patterns from the parsed findings.
#   Reason: Cultural patterns are essential for understanding the societal aspects of
#           the world being analyzed.
#   Impact: This will enable the generation of a comprehensive report that includes
#           cultural insights.
#   Complexity: MEDIUM
#   Method: Utilize natural language processing techniques to identify cultural
#           keywords and themes within the parsed patterns.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Return the extracted cultural patterns in a structured list format.
#   Reason: A structured output is necessary for further processing and integration
#           into the final report.
#   Impact: This will facilitate the organization of report sections and the drafting
#           of the report content.
#   Complexity: LOW
#   Method: Convert the extracted cultural patterns into a list of strings, ensuring
#           each pattern is clearly represented.
# -- END PRD --

import re
import json


def extract_cultural_patterns(patterns: str) -> str:
    """
    Extracts cultural patterns from the given parsed patterns.

    Args:
        patterns: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Define cultural keywords and themes to identify
    cultural_keywords = [
        'tradition', 'ritual', 'ceremony', 'festival', 'celebration', 'custom',
        'belief', 'religion', 'spiritual', 'sacred', 'holy', 'worship',
        'family', 'community', 'social', 'society', 'clan', 'tribe',
        'language', 'dialect', 'communication', 'storytelling', 'oral',
        'art', 'music', 'dance', 'performance', 'craft', 'artisan',
        'food', 'cuisine', 'cooking', 'feast', 'meal', 'dietary',
        'clothing', 'dress', 'attire', 'costume', 'fashion', 'textile',
        'architecture', 'building', 'structure', 'dwelling', 'temple',
        'governance', 'leadership', 'authority', 'hierarchy', 'power',
        'education', 'learning', 'knowledge', 'wisdom', 'teaching',
        'marriage', 'wedding', 'courtship', 'kinship', 'inheritance',
        'agriculture', 'farming', 'harvest', 'seasonal', 'calendar'
    ]
    
    # Split patterns into sentences for analysis
    sentences = re.split(r'[.!?]+', patterns)
    
    extracted_patterns = []
    
    for sentence in sentences:
        sentence = sentence.strip().lower()
        if not sentence:
            continue
            
        # Check if sentence contains cultural keywords
        cultural_score = 0
        found_keywords = []
        
        for keyword in cultural_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', sentence):
                cultural_score += 1
                found_keywords.append(keyword)
        
        # If sentence has cultural relevance (contains cultural keywords)
        if cultural_score > 0:
            # Clean and format the pattern
            cleaned_pattern = re.sub(r'\s+', ' ', sentence.strip())
            if cleaned_pattern and len(cleaned_pattern) > 10:  # Filter out very short patterns
                pattern_entry = {
                    'pattern': cleaned_pattern.capitalize(),
                    'keywords': found_keywords,
                    'cultural_score': cultural_score
                }
                extracted_patterns.append(pattern_entry)
    
    # Remove duplicates while preserving order
    seen_patterns = set()
    unique_patterns = []
    
    for pattern in extracted_patterns:
        pattern_text = pattern['pattern']
        if pattern_text not in seen_patterns:
            seen_patterns.add(pattern_text)
            unique_patterns.append(pattern['pattern'])
    
    # Sort by relevance (could be enhanced with more sophisticated scoring)
    # For now, keep the order as found
    
    # Return as string representation of list as indicated by return type
    return json.dumps(unique_patterns, ensure_ascii=False, indent=2)