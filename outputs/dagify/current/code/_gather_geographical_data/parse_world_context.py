# -- PRD --
# 1. BULLET: Analyze the input world context to identify key geographical parameters.
#   Reason: To accurately determine the scope for geographical data collection, the
#           input context must be thoroughly analyzed.
#   Impact: This analysis will directly affect the quality and relevance of the
#           geographical data collected in subsequent steps.
#   Complexity: MEDIUM
#   Method: Implement a parsing algorithm that can handle various formats of input
#           world context, potentially using regular expressions or a
#           parsing library.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the parsed geographical scope against a predefined set of valid
#   scopes or criteria.
#   Reason: To ensure that the determined scope is valid and meaningful for
#           geographical data collection.
#   Impact: This validation will help prevent errors or irrelevant data collection in
#           subsequent steps.
#   Complexity: LOW
#   Method: Use a predefined list or criteria to validate the parsed scope, potentially
#           leveraging an existing validation library or service.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the determined geographical scope in a standardized format.
#   Reason: To facilitate consistent processing of the scope in subsequent steps.
#   Impact: This standardization will improve the interoperability and reliability of
#           the geographical data collection process.
#   Complexity: LOW
#   Method: Define a standard format for representing geographical scopes and ensure
#           the output conforms to this format.
# -- END PRD --

import re


def parse_world_context(context: str) -> str:
    """
    This shim parses the world context to determine the geographical scope for further data collection.

    Args:
        context: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Analyze the input world context to identify key geographical parameters
    # Convert to lowercase for consistent processing
    normalized_context = context.lower().strip()
    
    # Define patterns for different geographical scopes
    scope_patterns = {
        'global': r'\b(world|global|worldwide|international|earth|planet)\b',
        'continental': r'\b(continent|africa|asia|europe|north america|south america|australia|antarctica)\b',
        'national': r'\b(country|nation|state|united states|usa|canada|mexico|brazil|china|india|russia|japan)\b',
        'regional': r'\b(region|area|zone|province|territory|district)\b',
        'local': r'\b(city|town|village|local|municipality|urban|rural)\b'
    }
    
    # Analyze context to determine geographical scope
    detected_scope = 'unknown'
    
    # Check for each scope pattern in order of specificity (most specific first)
    for scope, pattern in scope_patterns.items():
        if re.search(pattern, normalized_context):
            detected_scope = scope
            break
    
    # Validate the parsed geographical scope against predefined criteria
    valid_scopes = ['global', 'continental', 'national', 'regional', 'local', 'unknown']
    
    if detected_scope not in valid_scopes:
        detected_scope = 'unknown'
    
    # If no specific scope detected, try to infer from context size
    if detected_scope == 'unknown':
        if len(normalized_context) > 200:
            detected_scope = 'global'  # Assume larger contexts are global
        elif len(normalized_context) > 50:
            detected_scope = 'regional'  # Medium contexts are regional
        else:
            detected_scope = 'local'  # Small contexts are local
    
    # Return the determined geographical scope in standardized format
    return detected_scope