# -- PRD --
# 1. BULLET: Develop an algorithm to analyze and identify common themes between
#   geographical and cultural patterns.
#   Reason: To extract meaningful insights from the patterns, a sophisticated analysis
#           is required.
#   Impact: This will enable the integration of findings into a cohesive narrative.
#   Complexity: MEDIUM
#   Method: Utilize natural language processing (NLP) techniques to analyze the
#           patterns and identify recurring themes.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a method to handle and process the input patterns, potentially
#   involving data cleaning and preprocessing.
#   Reason: The quality of the input data directly affects the accuracy of the
#           identified themes.
#   Impact: This ensures that the themes identified are reliable and relevant.
#   Complexity: LOW
#   Method: Apply data preprocessing techniques to remove irrelevant information and
#           normalize the data.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Design the output to be a list of themes that can be easily consumed by
#   subsequent processes.
#   Reason: The output needs to be in a format that is usable by the next steps in the
#           pipeline.
#   Impact: This facilitates the creation of a comprehensive narrative in later stages.
#   Complexity: LOW
#   Method: Format the identified themes into a list of strings, ensuring they are
#           clearly defined and easily accessible.
# -- END PRD --

from typing import List

import re
from collections import Counter


def identify_key_themes(geo_patterns: str, cultural_patterns: str) -> List[str]:
    """
    Identifies key themes emerging from both geographical and cultural patterns.

    Args:
        geo_patterns: Input parameter of type str
cultural_patterns: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Data preprocessing - clean and normalize input patterns
    def clean_text(text: str) -> str:
        # Remove special characters and normalize whitespace
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Convert to lowercase and remove extra whitespace
        cleaned = ' '.join(cleaned.lower().split())
        return cleaned
    
    # Clean both input patterns
    clean_geo = clean_text(geo_patterns)
    clean_cultural = clean_text(cultural_patterns)
    
    # Combine patterns for analysis
    combined_text = clean_geo + ' ' + clean_cultural
    
    # Extract potential themes using NLP techniques
    # Split into words and filter out common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    words = combined_text.split()
    meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Identify recurring themes using frequency analysis
    word_counts = Counter(meaningful_words)
    
    # Extract n-grams (2-word and 3-word phrases) for more complex themes
    bigrams = []
    trigrams = []
    
    for i in range(len(meaningful_words) - 1):
        bigram = ' '.join(meaningful_words[i:i+2])
        bigrams.append(bigram)
    
    for i in range(len(meaningful_words) - 2):
        trigram = ' '.join(meaningful_words[i:i+3])
        trigrams.append(trigram)
    
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)
    
    # Identify key themes based on frequency and relevance
    themes = []
    
    # Add most frequent single words as themes (top 5)
    for word, count in word_counts.most_common(5):
        if count >= 2:  # Only include words that appear multiple times
            themes.append(word)
    
    # Add most frequent bigrams as themes (top 3)
    for bigram, count in bigram_counts.most_common(3):
        if count >= 2:  # Only include phrases that appear multiple times
            themes.append(bigram)
    
    # Add most frequent trigrams as themes (top 2)
    for trigram, count in trigram_counts.most_common(2):
        if count >= 2:  # Only include phrases that appear multiple times
            themes.append(trigram)
    
    # Look for domain-specific patterns related to geography and culture
    geo_keywords = ['location', 'region', 'area', 'place', 'territory', 'land', 'geographic', 
                   'spatial', 'climate', 'terrain', 'urban', 'rural', 'city', 'country']
    cultural_keywords = ['tradition', 'custom', 'belief', 'practice', 'ritual', 'heritage', 
                        'community', 'social', 'cultural', 'ethnic', 'religious', 'language']
    
    for keyword in geo_keywords + cultural_keywords:
        if keyword in combined_text and keyword not in themes:
            themes.append(keyword)
    
    # Remove duplicates while preserving order
    unique_themes = []
    seen = set()
    for theme in themes:
        if theme not in seen:
            unique_themes.append(theme)
            seen.add(theme)
    
    # Limit to most relevant themes (max 10)
    final_themes = unique_themes[:10]
    
    # Ensure we return at least some themes even if input is minimal
    if not final_themes:
        final_themes = ['geographic patterns', 'cultural patterns']
    
    return final_themes