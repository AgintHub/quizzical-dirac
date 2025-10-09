# -- PRD --
# 1. BULLET: Analyze the input data to extract relevant information that could indicate
#   the context of 'world'.
#   Reason: The input data may contain keywords or phrases that hint at the 'world'
#           context.
#   Impact: This will help in generating a more accurate definition of 'world' for the
#           workflow.
#   Complexity: MEDIUM
#   Method: Use natural language processing techniques to parse the input data and
#           identify relevant terms.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Examine the constraints to identify any limitations or specific requirements
#   related to the 'world' context.
#   Reason: Constraints may provide crucial information about what the 'world' context
#           should or should not include.
#   Impact: This will ensure that the identified hints are aligned with the workflow's
#           specific needs and limitations.
#   Complexity: LOW
#   Method: Parse the constraints to extract relevant information and correlate it with
#           the input data analysis.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Combine the insights from the input data and constraints analysis to
#   formulate a comprehensive list of hints about the 'world' context.
#   Reason: A combined analysis will provide a more complete understanding of the
#           'world' context.
#   Impact: This will enhance the accuracy and relevance of the 'world' definition
#           generated for the workflow.
#   Complexity: MEDIUM
#   Method: Use a systematic approach to merge the findings from both analyses,
#           ensuring that all relevant hints are captured.
# -- END PRD --

import re
import json


def identify_world_hints(input_data: str, constraints: str) -> str:
    """
    Identifies hints about the 'world' context from the input data and constraints.

    Args:
        input_data: Input parameter of type str
constraints: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Initialize lists to store hints
    input_hints = []
    constraint_hints = []
    
    # Analyze input data to extract relevant information
    # Look for world-related keywords and context clues
    world_keywords = [
        'world', 'universe', 'reality', 'environment', 'setting', 'context',
        'domain', 'realm', 'sphere', 'space', 'place', 'location', 'scenario',
        'situation', 'conditions', 'circumstances', 'background', 'framework'
    ]
    
    # Process input data - extract sentences and phrases containing world-related terms
    input_sentences = re.split(r'[.!?]+', input_data.lower())
    for sentence in input_sentences:
        sentence = sentence.strip()
        if sentence:
            # Check for world-related keywords
            for keyword in world_keywords:
                if keyword in sentence:
                    # Extract context around the keyword
                    words = sentence.split()
                    if keyword in words:
                        keyword_index = words.index(keyword)
                        # Get surrounding context (3 words before and after)
                        start_idx = max(0, keyword_index - 3)
                        end_idx = min(len(words), keyword_index + 4)
                        context = ' '.join(words[start_idx:end_idx])
                        input_hints.append(f"Input context: {context}")
            
            # Look for descriptive phrases that might indicate world characteristics
            descriptive_patterns = [
                r'\b(is|are|was|were)\s+([^.!?]+)',
                r'\b(has|have|had)\s+([^.!?]+)',
                r'\b(contains|includes|features)\s+([^.!?]+)',
                r'\b(characterized by|defined by)\s+([^.!?]+)'
            ]
            
            for pattern in descriptive_patterns:
                matches = re.finditer(pattern, sentence)
                for match in matches:
                    if len(match.groups()) >= 2:
                        description = match.group(2).strip()
                        if description and len(description) > 3:
                            input_hints.append(f"Description: {description}")
    
    # Examine constraints to identify limitations and requirements
    constraint_sentences = re.split(r'[.!?]+', constraints.lower())
    constraint_keywords = [
        'must', 'should', 'cannot', 'must not', 'required', 'forbidden',
        'allowed', 'restricted', 'limited', 'only', 'except', 'excluding',
        'including', 'specifically', 'particularly', 'constraint', 'limitation'
    ]
    
    for sentence in constraint_sentences:
        sentence = sentence.strip()
        if sentence:
            # Check for constraint-related keywords
            for keyword in constraint_keywords:
                if keyword in sentence:
                    constraint_hints.append(f"Constraint: {sentence}")
            
            # Look for specific world requirements or limitations
            requirement_patterns = [
                r'\b(world|universe|reality|environment)\s+(must|should|cannot|needs?)\s+([^.!?]+)',
                r'\b(must|should|cannot)\s+([^.!?]*(?:world|universe|reality|environment)[^.!?]*)',
                r'\b(only|specifically|particularly)\s+([^.!?]+)'
            ]
            
            for pattern in requirement_patterns:
                matches = re.finditer(pattern, sentence)
                for match in matches:
                    if len(match.groups()) >= 2:
                        requirement = match.group(-1).strip()  # Get the last group
                        if requirement and len(requirement) > 3:
                            constraint_hints.append(f"Requirement: {requirement}")
    
    # Combine insights from both analyses
    all_hints = []
    
    # Add input data hints
    if input_hints:
        all_hints.extend(input_hints)
    
    # Add constraint hints
    if constraint_hints:
        all_hints.extend(constraint_hints)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_hints = []
    for hint in all_hints:
        if hint.lower() not in seen:
            seen.add(hint.lower())
            unique_hints.append(hint)
    
    # If no specific hints found, provide general analysis
    if not unique_hints:
        unique_hints.append("General analysis: No specific world context hints found in input data")
        unique_hints.append("General analysis: No specific world constraints identified")
        unique_hints.append("Suggestion: Consider providing more detailed input data or constraints")
    
    # Format the output as a string representation of the hints list
    result = json.dumps(unique_hints, indent=2)
    return result