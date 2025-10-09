# -- PRD --
# 1. BULLET: Analyze the workflow objectives to determine the context in which 'world' is
#   being used.
#   Reason: Understanding the workflow objectives is crucial to identifying relevant
#           terms related to 'world'.
#   Impact: This analysis will directly affect the accuracy of the identified key
#           terms.
#   Complexity: MEDIUM
#   Method: Use Natural Language Processing (NLP) techniques to parse the objectives
#           and identify key concepts.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Examine the input data to find specific terms or phrases that relate to
#   'world'.
#   Reason: The input data may contain explicit or implicit references to 'world' that
#           need to be captured.
#   Impact: This examination will enhance the comprehensiveness of the identified
#           terms.
#   Complexity: LOW
#   Method: Implement a keyword extraction algorithm to identify relevant terms from
#           the input data.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Combine insights from both the workflow objectives and input data to compile
#   a comprehensive list of key terms related to 'world'.
#   Reason: A combined approach ensures that the identified terms are both relevant to
#           the workflow context and specific to the input data.
#   Impact: This synthesis will result in a robust set of key terms that accurately
#           represent 'world' in the given context.
#   Complexity: HIGH
#   Method: Use a machine learning model or a sophisticated NLP technique to integrate
#           the insights and generate the final list of key terms.
# -- END PRD --

import re
import json
from collections import Counter


def identify_world_related_terms(objectives: str, input_data: str) -> str:
    """
    Identifies key terms related to the concept of 'world' based on workflow objectives and input data.

    Args:
        objectives: Input parameter of type str
input_data: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Define world-related keywords and patterns
    world_keywords = [
        'world', 'global', 'international', 'worldwide', 'earth', 'planet',
        'universe', 'cosmos', 'society', 'humanity', 'civilization', 'culture',
        'environment', 'ecosystem', 'geography', 'continent', 'country', 'nation',
        'community', 'population', 'people', 'human', 'mankind', 'species'
    ]
    
    # Combine objectives and input data for analysis
    combined_text = f"{objectives} {input_data}"
    
    # Clean and tokenize the text
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', combined_text.lower())
    words = cleaned_text.split()
    
    # Find terms related to 'world' using keyword matching
    related_terms = set()
    
    # Direct keyword matching
    for word in words:
        if word in world_keywords:
            related_terms.add(word)
    
    # Find words that appear in context with world-related terms
    for i, word in enumerate(words):
        if word in world_keywords:
            # Add surrounding words (context window of 3 words)
            for j in range(max(0, i-3), min(len(words), i+4)):
                if j != i and len(words[j]) > 2:  # Exclude short words
                    related_terms.add(words[j])
    
    # Pattern-based extraction for compound terms
    compound_patterns = [
        r'\b(world|global|international)\s+\w+',
        r'\b\w+\s+(world|global|international)',
        r'\b\w*world\w*\b',
        r'\b\w*global\w*\b'
    ]
    
    for pattern in compound_patterns:
        matches = re.findall(pattern, combined_text.lower())
        for match in matches:
            if isinstance(match, tuple):
                related_terms.update(match)
            else:
                related_terms.add(match.strip())
    
    # Filter out very common words and short terms
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
    
    filtered_terms = [term for term in related_terms if term not in stop_words and len(term) > 2]
    
    # Sort by relevance (terms that appear more frequently are more relevant)
    term_counts = Counter(word for word in words if word in filtered_terms)
    sorted_terms = sorted(set(filtered_terms), key=lambda x: term_counts.get(x, 0), reverse=True)
    
    # Return as JSON string representing a list
    return json.dumps(sorted_terms[:20])  # Limit to top 20 terms