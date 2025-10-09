# -- PRD --
# 1. BULLET: Develop an algorithm to assess the significance of cultural patterns based on
#   their frequency, context, and relevance.
#   Reason: To provide a meaningful analysis of the detected patterns.
#   Impact: Enables the filtering of significant patterns that are crucial for
#           understanding cultural dynamics.
#   Complexity: MEDIUM
#   Method: Utilize natural language processing techniques and machine learning
#           algorithms to analyze pattern significance.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a data structure to store and manage the analysis results
#   efficiently.
#   Reason: To handle the output of the analysis in a structured and accessible manner.
#   Impact: Facilitates the subsequent steps of filtering and compiling significant
#           cultural patterns.
#   Complexity: LOW
#   Method: Use a list of dictionaries where each dictionary contains relevant
#           information about a pattern's significance.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Ensure the algorithm is flexible to accommodate different types of cultural
#   patterns and their varying significance.
#   Reason: To make the analysis robust and applicable to diverse cultural contexts.
#   Impact: Enhances the versatility and reliability of the cultural pattern analysis.
#   Complexity: HIGH
#   Method: Incorporate modular design and adaptive learning mechanisms to handle
#           diverse patterns and significance levels.
# -- END PRD --

from typing import List

import re
from collections import Counter


def analyze_pattern_significance(patterns: str) -> List[str]:
    """
    Analyzes the significance of detected cultural patterns to determine their relevance and importance.

    Args:
        patterns: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    
    # Parse input patterns - assume they are newline or delimiter separated
    if not patterns or not patterns.strip():
        return []
    
    # Split patterns by newlines or semicolons
    pattern_list = [p.strip() for p in re.split(r'[\n;]', patterns) if p.strip()]
    
    if not pattern_list:
        return []
    
    # Calculate frequency-based significance
    pattern_frequency = Counter(pattern_list)
    total_patterns = len(pattern_list)
    
    significant_patterns = []
    
    for pattern in set(pattern_list):
        # Calculate frequency score (0-1)
        frequency_score = pattern_frequency[pattern] / total_patterns
        
        # Calculate context score based on pattern length and complexity
        context_score = min(len(pattern.split()) / 10.0, 1.0)  # Normalize by word count
        
        # Calculate relevance score based on cultural keywords
        cultural_keywords = ['tradition', 'culture', 'ritual', 'custom', 'belief', 'practice', 
                           'ceremony', 'heritage', 'community', 'social', 'religious', 'spiritual']
        pattern_lower = pattern.lower()
        relevance_matches = sum(1 for keyword in cultural_keywords if keyword in pattern_lower)
        relevance_score = min(relevance_matches / 5.0, 1.0)  # Normalize
        
        # Calculate overall significance (weighted average)
        significance = (frequency_score * 0.4 + context_score * 0.3 + relevance_score * 0.3)
        
        # Filter significant patterns (threshold of 0.3)
        if significance >= 0.3:
            significant_patterns.append(pattern)
    
    # Sort by calculated significance (recalculate for sorting)
    def calculate_significance(pattern):
        freq_score = pattern_frequency[pattern] / total_patterns
        ctx_score = min(len(pattern.split()) / 10.0, 1.0)
        pattern_lower = pattern.lower()
        rel_matches = sum(1 for kw in cultural_keywords if kw in pattern_lower)
        rel_score = min(rel_matches / 5.0, 1.0)
        return freq_score * 0.4 + ctx_score * 0.3 + rel_score * 0.3
    
    significant_patterns.sort(key=calculate_significance, reverse=True)
    
    return significant_patterns