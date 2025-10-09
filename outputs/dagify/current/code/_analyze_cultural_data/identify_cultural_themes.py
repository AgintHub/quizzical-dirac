# -- PRD --
# 1. BULLET: Process the combined cultural data to extract relevant information.
#   Reason: To identify cultural themes, it's necessary to analyze the combined
#           cultural data.
#   Impact: This will enable the system to understand cultural patterns and trends.
#   Complexity: MEDIUM
#   Method: Natural Language Processing (NLP) techniques can be used to analyze the
#           text data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Apply thematic analysis to identify recurring themes or patterns.
#   Reason: Thematic analysis is a suitable method for identifying cultural themes in
#           qualitative data.
#   Impact: This will provide insights into the cultural context and help in
#           understanding societal norms.
#   Complexity: HIGH
#   Method: Machine learning algorithms, such as clustering or topic modeling, can be
#           employed to identify themes.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the identified themes against known cultural patterns or expert
#   knowledge.
#   Reason: Validation is crucial to ensure the accuracy and relevance of the
#           identified themes.
#   Impact: This will enhance the credibility of the system's output and improve its
#           reliability.
#   Complexity: LOW
#   Method: Comparison with existing cultural databases or expert feedback can be used
#           for validation.
# -- END PRD --

from typing import List

import re
from collections import Counter


def identify_cultural_themes(cultural_data: str) -> List[str]:
    """
    Identifies cultural themes from the provided combined cultural data.

    Args:
        cultural_data: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Process the combined cultural data to extract relevant information
    # Clean and normalize the text data
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', cultural_data.lower())
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    # Split into words and filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    words = [word for word in cleaned_text.split() if word not in stop_words and len(word) > 2]
    
    # Apply thematic analysis to identify recurring themes or patterns
    # Use word frequency and n-gram analysis to identify themes
    word_freq = Counter(words)
    
    # Identify potential cultural theme keywords
    cultural_keywords = {
        'tradition': ['tradition', 'traditional', 'customs', 'heritage', 'ancestral', 'legacy'],
        'religion': ['religion', 'religious', 'spiritual', 'faith', 'belief', 'worship', 'sacred'],
        'family': ['family', 'kinship', 'relatives', 'parents', 'children', 'marriage', 'household'],
        'community': ['community', 'society', 'social', 'collective', 'group', 'tribe', 'clan'],
        'language': ['language', 'dialect', 'communication', 'linguistic', 'speech', 'words'],
        'art': ['art', 'artistic', 'creative', 'music', 'dance', 'painting', 'sculpture'],
        'food': ['food', 'cuisine', 'cooking', 'eating', 'meal', 'dish', 'recipe'],
        'celebration': ['celebration', 'festival', 'ceremony', 'ritual', 'holiday', 'feast'],
        'values': ['values', 'morals', 'ethics', 'principles', 'honor', 'respect', 'dignity'],
        'education': ['education', 'learning', 'knowledge', 'teaching', 'wisdom', 'school']
    }
    
    # Identify themes based on keyword presence and frequency
    identified_themes = []
    for theme, keywords in cultural_keywords.items():
        theme_score = sum(word_freq.get(keyword, 0) for keyword in keywords)
        if theme_score > 0:
            identified_themes.append(theme)
    
    # Apply simple clustering based on co-occurrence patterns
    # Look for phrases and compound themes
    text_lower = cultural_data.lower()
    compound_themes = {
        'traditional_ceremonies': ['traditional ceremony', 'ritual ceremony', 'cultural ritual'],
        'social_structure': ['social hierarchy', 'class system', 'social order'],
        'cultural_identity': ['cultural identity', 'ethnic identity', 'national identity'],
        'generational_values': ['generational difference', 'elder wisdom', 'youth culture'],
        'gender_roles': ['gender role', 'women role', 'men role', 'gender expectation']
    }
    
    for theme, phrases in compound_themes.items():
        if any(phrase in text_lower for phrase in phrases):
            identified_themes.append(theme)
    
    # Validate the identified themes against known cultural patterns
    # Filter themes based on minimum occurrence and relevance
    validated_themes = []
    min_relevance_threshold = 1  # Minimum occurrences to be considered relevant
    
    for theme in identified_themes:
        if theme in cultural_keywords:
            keywords = cultural_keywords[theme]
            relevance_score = sum(word_freq.get(keyword, 0) for keyword in keywords)
            if relevance_score >= min_relevance_threshold:
                validated_themes.append(theme)
        else:
            # For compound themes, include if found
            validated_themes.append(theme)
    
    # Remove duplicates and sort for consistency
    final_themes = sorted(list(set(validated_themes)))
    
    # Ensure we return at least some themes if cultural data is present
    if not final_themes and cultural_data.strip():
        # Fallback to most common cultural themes if no specific themes identified
        final_themes = ['general_culture']
    
    return final_themes