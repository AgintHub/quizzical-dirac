# -- PRD --
# 1. BULLET: Develop a scoring system to evaluate the relevance of each interpretation
#   based on the workflow's context and purpose.
#   Reason: To quantify the relevance of interpretations and enable comparison.
#   Impact: Will allow for a systematic evaluation of interpretations, improving the
#           accuracy of the world definition.
#   Complexity: MEDIUM
#   Method: Use a weighted scoring system based on factors such as keyword matching,
#           semantic similarity, and contextual relevance.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a natural language processing (NLP) or machine learning approach to
#   analyze the interpretations and context.
#   Reason: To leverage advanced techniques for text analysis and comparison.
#   Impact: Will enhance the sophistication and accuracy of the relevance evaluation.
#   Complexity: HIGH
#   Method: Utilize libraries such as NLTK, spaCy, or TensorFlow to develop an NLP
#           model that can effectively analyze and compare text.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Ensure the output is a dictionary with interpretations as keys and their
#   relevance scores as values.
#   Reason: To provide a structured output that can be easily consumed by subsequent
#           nodes.
#   Impact: Will facilitate the integration of this node's output with other components
#           of the workflow.
#   Complexity: LOW
#   Method: Use a Python dictionary to store the results and convert it to a JSON
#           string if necessary for output.
# -- END PRD --

import json
import re
from collections import Counter


def evaluate_interpretation_relevance(interpretations: str, context: str) -> str:
    """
    Evaluates the relevance of possible interpretations of 'world' in the context of the workflow's purpose.

    Args:
        interpretations: Input parameter of type str
context: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Parse interpretations - assume they are separated by newlines or semicolons
    interpretation_list = []
    if '\n' in interpretations:
        interpretation_list = [interp.strip() for interp in interpretations.split('\n') if interp.strip()]
    elif ';' in interpretations:
        interpretation_list = [interp.strip() for interp in interpretations.split(';') if interp.strip()]
    else:
        interpretation_list = [interpretations.strip()]
    
    # Normalize context for analysis
    context_lower = context.lower()
    context_words = re.findall(r'\b\w+\b', context_lower)
    context_word_freq = Counter(context_words)
    
    # Scoring system for interpretations
    scores = {}
    
    for interpretation in interpretation_list:
        if not interpretation:
            continue
            
        interpretation_lower = interpretation.lower()
        interpretation_words = re.findall(r'\b\w+\b', interpretation_lower)
        
        # Initialize score
        relevance_score = 0.0
        
        # Factor 1: Keyword matching (weight: 0.4)
        keyword_matches = 0
        for word in interpretation_words:
            if word in context_words:
                keyword_matches += context_word_freq[word]
        
        keyword_score = min(keyword_matches / max(len(context_words), 1), 1.0)
        relevance_score += keyword_score * 0.4
        
        # Factor 2: Semantic similarity - simple approach (weight: 0.35)
        # Check for related terms and concepts
        semantic_keywords = {
            'physical': ['environment', 'location', 'space', 'place', 'geography', 'earth', 'planet'],
            'digital': ['virtual', 'online', 'software', 'application', 'system', 'platform', 'technology'],
            'conceptual': ['domain', 'realm', 'field', 'area', 'scope', 'context', 'framework'],
            'social': ['society', 'community', 'culture', 'people', 'human', 'social'],
            'business': ['market', 'industry', 'commercial', 'enterprise', 'organization']
        }
        
        semantic_score = 0.0
        for category, related_words in semantic_keywords.items():
            # Check if interpretation relates to this semantic category
            interpretation_in_category = any(word in interpretation_lower for word in related_words)
            context_in_category = any(word in context_lower for word in related_words)
            
            if interpretation_in_category and context_in_category:
                semantic_score += 0.2
            elif interpretation_in_category or context_in_category:
                semantic_score += 0.1
        
        relevance_score += min(semantic_score, 1.0) * 0.35
        
        # Factor 3: Contextual relevance - length and specificity (weight: 0.25)
        # More specific interpretations get higher scores if they contain context-relevant terms
        specificity_score = 0.0
        
        # Bonus for reasonable length (not too short, not too long)
        word_count = len(interpretation_words)
        if 3 <= word_count <= 15:
            specificity_score += 0.3
        elif 1 <= word_count <= 20:
            specificity_score += 0.1
        
        # Bonus for containing workflow-related terms
        workflow_terms = ['workflow', 'process', 'task', 'step', 'procedure', 'operation', 'function']
        if any(term in context_lower for term in workflow_terms):
            if any(term in interpretation_lower for term in workflow_terms):
                specificity_score += 0.4
        
        relevance_score += min(specificity_score, 1.0) * 0.25
        
        # Normalize score to 0-1 range
        relevance_score = min(max(relevance_score, 0.0), 1.0)
        
        # Round to 3 decimal places for cleaner output
        scores[interpretation] = round(relevance_score, 3)
    
    # Convert to JSON string for output
    return json.dumps(scores, indent=2)