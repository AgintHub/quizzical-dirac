# -- PRD --
# 1. BULLET: Analyze the input purpose string to identify key objectives.
#   Reason: To understand the core goals of the workflow.
#   Impact: Enables the workflow to focus on relevant tasks and outcomes.
#   Complexity: MEDIUM
#   Method: Use Natural Language Processing (NLP) techniques to parse the purpose
#           string and extract relevant objectives.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a parsing mechanism to handle various input formats.
#   Reason: To accommodate different structures and styles of input purpose strings.
#   Impact: Increases the versatility and robustness of the workflow objective
#           extraction process.
#   Complexity: HIGH
#   Method: Utilize regular expressions or machine learning-based text analysis to
#           handle diverse input formats.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate extracted objectives against a predefined set of relevant terms or
#   ontology.
#   Reason: To ensure the extracted objectives are meaningful and relevant to the
#           workflow context.
#   Impact: Enhances the accuracy and relevance of the extracted workflow objectives.
#   Complexity: MEDIUM
#   Method: Compare extracted objectives against a knowledge graph or ontology related
#           to the workflow domain.
# -- END PRD --

import re


def extract_workflow_objectives(purpose: str) -> str:
    """
    Extracts workflow objectives from the given purpose string.

    Args:
        purpose: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Analyze the input purpose string to identify key objectives
    # Use NLP techniques to parse and extract relevant objectives
    
    # Define predefined relevant terms/ontology for validation
    relevant_terms = {
        'data', 'process', 'analyze', 'extract', 'transform', 'load', 'validate',
        'compute', 'calculate', 'generate', 'create', 'update', 'delete', 'retrieve',
        'filter', 'sort', 'aggregate', 'merge', 'split', 'classify', 'predict',
        'optimize', 'monitor', 'report', 'visualize', 'export', 'import', 'sync',
        'workflow', 'automation', 'pipeline', 'task', 'operation', 'function'
    }
    
    # Handle various input formats with parsing mechanism
    # Clean and normalize the input text
    normalized_purpose = purpose.lower().strip()
    
    # Extract objectives using pattern matching and NLP techniques
    objectives = []
    
    # Split into sentences and analyze each
    sentences = re.split(r'[.!?;]', normalized_purpose)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Extract action verbs and relevant terms
        words = re.findall(r'\b\w+\b', sentence)
        
        # Look for objective patterns (verb + object combinations)
        for i, word in enumerate(words):
            if word in relevant_terms:
                # Build objective context
                context_start = max(0, i-2)
                context_end = min(len(words), i+3)
                context = ' '.join(words[context_start:context_end])
                
                # Validate against relevant terms
                if any(term in context for term in relevant_terms):
                    objectives.append(context)
    
    # Remove duplicates and filter meaningful objectives
    unique_objectives = list(set(objectives))
    
    # Validate extracted objectives against predefined ontology
    validated_objectives = []
    for obj in unique_objectives:
        # Check if objective contains meaningful workflow-related terms
        obj_words = set(re.findall(r'\b\w+\b', obj.lower()))
        if obj_words.intersection(relevant_terms):
            validated_objectives.append(obj)
    
    # Return as string representation of list
    if not validated_objectives:
        # Fallback: extract key phrases if no structured objectives found
        key_phrases = re.findall(r'\b(?:to |will |should |must |need to )([^.!?;]+)', normalized_purpose)
        if key_phrases:
            validated_objectives = [phrase.strip() for phrase in key_phrases]
        else:
            validated_objectives = [normalized_purpose]
    
    return str(validated_objectives)