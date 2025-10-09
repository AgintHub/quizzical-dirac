# -- PRD --
# 1. BULLET: Implement a pattern detection algorithm that can analyze the combined
#   cultural data and identified themes to detect significant cultural
#   patterns.
#   Reason: This is necessary to fulfill the requirement of identifying cultural
#           patterns in the analyze_cultural_data function.
#   Impact: The detected cultural patterns will be used to analyze their significance
#           and relevance, ultimately contributing to the output of the
#           AnalyzeCulturalDataOutput.
#   Complexity: MEDIUM
#   Method: Utilize natural language processing (NLP) techniques or machine learning
#           algorithms to identify patterns in the cultural data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Ensure the function can handle varying input sizes and types of cultural
#   data.
#   Reason: The function needs to be robust and adaptable to different inputs to ensure
#           reliability.
#   Impact: This will improve the function's versatility and ability to handle diverse
#           cultural datasets.
#   Complexity: MEDIUM
#   Method: Implement input validation and normalization techniques to handle different
#           types of cultural data.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Optimize the function for performance, especially for large datasets.
#   Reason: Large datasets are likely to be encountered, and slow performance could
#           hinder the overall analysis process.
#   Impact: This will ensure that the analysis process remains efficient even with
#           substantial cultural data.
#   Complexity: HIGH
#   Method: Apply optimization techniques such as parallel processing or data chunking
#           to improve performance on large datasets.
# -- END PRD --

from typing import List

import re
from collections import Counter


def detect_cultural_patterns(themes: str, data: str) -> List[str]:
    """
    Detects cultural patterns based on the identified themes and combined cultural data.

    Args:
        themes: Input parameter of type str
data: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Input validation and normalization
    if not themes or not data:
        return []
    
    # Normalize input data
    themes_normalized = themes.lower().strip()
    data_normalized = data.lower().strip()
    
    # Extract individual themes from the themes string
    theme_list = [theme.strip() for theme in re.split(r'[,;\n]', themes_normalized) if theme.strip()]
    
    # Split data into sentences/segments for analysis
    data_segments = re.split(r'[.!?\n]', data_normalized)
    data_segments = [segment.strip() for segment in data_segments if segment.strip()]
    
    detected_patterns = []
    
    # Pattern 1: Theme co-occurrence patterns
    theme_cooccurrence = []
    for segment in data_segments:
        present_themes = [theme for theme in theme_list if theme in segment]
        if len(present_themes) >= 2:
            theme_cooccurrence.append(tuple(sorted(present_themes)))
    
    # Find frequent theme combinations
    theme_counter = Counter(theme_cooccurrence)
    for combo, count in theme_counter.items():
        if count >= 2:  # Threshold for significance
            detected_patterns.append(f"Co-occurrence pattern: {' + '.join(combo)} (frequency: {count})")
    
    # Pattern 2: Cultural context patterns
    cultural_keywords = {
        'tradition': r'\b(tradition|traditional|heritage|ancestral|custom|ritual)\b',
        'modernization': r'\b(modern|contemporary|digital|technology|innovation|change)\b',
        'social': r'\b(community|society|social|group|collective|family)\b',
        'religious': r'\b(religious|spiritual|sacred|belief|faith|worship)\b',
        'economic': r'\b(economic|financial|trade|commerce|business|market)\b'
    }
    
    context_patterns = {}
    for context, pattern in cultural_keywords.items():
        matches = len(re.findall(pattern, data_normalized))
        if matches > 0:
            context_patterns[context] = matches
    
    # Identify dominant cultural contexts
    if context_patterns:
        total_matches = sum(context_patterns.values())
        for context, count in context_patterns.items():
            percentage = (count / total_matches) * 100
            if percentage >= 20:  # Threshold for significance
                detected_patterns.append(f"Cultural context pattern: {context} dominance ({percentage:.1f}%)")
    
    # Pattern 3: Temporal/evolutionary patterns
    temporal_indicators = {
        'past': r'\b(ancient|old|historical|past|before|traditional|ancestral)\b',
        'present': r'\b(current|now|today|contemporary|modern|recent)\b',
        'future': r'\b(future|upcoming|evolving|changing|new|emerging)\b'
    }
    
    temporal_counts = {}
    for period, pattern in temporal_indicators.items():
        count = len(re.findall(pattern, data_normalized))
        temporal_counts[period] = count
    
    # Detect temporal evolution patterns
    total_temporal = sum(temporal_counts.values())
    if total_temporal > 0:
        past_ratio = temporal_counts['past'] / total_temporal
        future_ratio = temporal_counts['future'] / total_temporal
        
        if past_ratio > 0.4:
            detected_patterns.append("Temporal pattern: Strong historical/traditional orientation")
        elif future_ratio > 0.4:
            detected_patterns.append("Temporal pattern: Forward-looking/modernization focus")
        elif abs(past_ratio - future_ratio) < 0.2:
            detected_patterns.append("Temporal pattern: Balanced traditional-modern perspective")
    
    # Pattern 4: Thematic intensity patterns
    theme_intensity = {}
    for theme in theme_list:
        if theme:
            count = len(re.findall(re.escape(theme), data_normalized))
            if count > 0:
                theme_intensity[theme] = count
    
    if theme_intensity:
        max_intensity = max(theme_intensity.values())
        dominant_themes = [theme for theme, count in theme_intensity.items() if count >= max_intensity * 0.7]
        
        if len(dominant_themes) == 1:
            detected_patterns.append(f"Thematic pattern: Single dominant theme - {dominant_themes[0]}")
        elif len(dominant_themes) > 1:
            detected_patterns.append(f"Thematic pattern: Multiple dominant themes - {', '.join(dominant_themes)}")
    
    # Pattern 5: Linguistic/stylistic patterns
    word_count = len(data_normalized.split())
    sentence_count = len([s for s in re.split(r'[.!?]', data) if s.strip()])
    
    if sentence_count > 0:
        avg_sentence_length = word_count / sentence_count
        if avg_sentence_length > 20:
            detected_patterns.append("Stylistic pattern: Complex, detailed cultural descriptions")
        elif avg_sentence_length < 10:
            detected_patterns.append("Stylistic pattern: Concise, direct cultural references")
    
    # Remove duplicates and return
    return list(set(detected_patterns)) if detected_patterns else ["No significant cultural patterns detected"]