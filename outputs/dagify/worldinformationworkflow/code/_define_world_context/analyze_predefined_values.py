# -- PRD --
# 1. BULLET: Parse the input keyword arguments to identify predefined values.
#   Reason: To extract relevant information that could influence the definition of
#           'world'.
#   Impact: Provides crucial data for understanding the context and scope of the
#           workflow.
#   Complexity: MEDIUM
#   Method: Use a parsing mechanism to iterate through the keyword arguments and
#           identify key-value pairs that represent predefined values.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Analyze the extracted predefined values to determine their relevance to the
#   'world' context.
#   Reason: To understand how these values constrain or hint at the interpretation of
#           'world'.
#   Impact: Helps in formulating a more accurate and relevant definition of 'world' for
#           the workflow.
#   Complexity: HIGH
#   Method: Implement a logic-based analysis that correlates the predefined values with
#           the workflow's purpose and objectives.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the analyzed predefined values into a structured output.
#   Reason: To provide a clear and usable output that can be integrated with other
#           components of the workflow definition process.
#   Impact: Facilitates the synthesis of findings from various analyses to craft a
#           comprehensive definition of 'world'.
#   Complexity: LOW
#   Method: Use a data serialization technique (e.g., JSON) to structure the output in
#           a dict format.
# -- END PRD --

import json
import re


def analyze_predefined_values(kwargs: str) -> str:
    """
    Analyzes the predefined values from the input keyword arguments to extract relevant information.

    Args:
        kwargs: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Parse the input keyword arguments to identify predefined values
    try:
        # Attempt to parse as JSON first
        if kwargs.strip().startswith('{') or kwargs.strip().startswith('['):
            parsed_kwargs = json.loads(kwargs)
        else:
            # Parse key=value pairs separated by commas or spaces
            parsed_kwargs = {}
            # Split by comma or semicolon, then parse key=value pairs
            pairs = re.split(r'[,;]', kwargs)
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Try to convert value to appropriate type
                    try:
                        # Try parsing as JSON value (handles strings, numbers, booleans)
                        parsed_kwargs[key] = json.loads(value)
                    except json.JSONDecodeError:
                        # If that fails, treat as string
                        parsed_kwargs[key] = value
    except (json.JSONDecodeError, ValueError):
        # If parsing fails, return empty analysis
        parsed_kwargs = {}
    
    # Analyze the extracted predefined values to determine their relevance to the 'world' context
    world_relevant_keys = [
        'environment', 'context', 'domain', 'scope', 'world', 'universe', 
        'reality', 'state', 'conditions', 'parameters', 'constraints',
        'settings', 'config', 'configuration', 'setup'
    ]
    
    relevant_values = {}
    context_hints = {}
    
    for key, value in parsed_kwargs.items():
        key_lower = key.lower()
        # Check if key is directly relevant to world context
        if any(relevant_key in key_lower for relevant_key in world_relevant_keys):
            relevant_values[key] = value
        # Check if value contains world-related information
        elif isinstance(value, str) and any(relevant_key in value.lower() for relevant_key in world_relevant_keys):
            context_hints[key] = value
        # Include numeric or boolean values that might represent constraints
        elif isinstance(value, (int, float, bool)):
            context_hints[key] = value
    
    # Determine relevance level and impact
    analysis_result = {
        'relevant_predefined_values': relevant_values,
        'context_hints': context_hints,
        'total_values_analyzed': len(parsed_kwargs),
        'world_relevance_score': len(relevant_values) + (len(context_hints) * 0.5),
        'analysis_summary': {
            'has_direct_world_context': len(relevant_values) > 0,
            'has_contextual_hints': len(context_hints) > 0,
            'complexity_level': 'HIGH' if len(relevant_values) > 2 else 'MEDIUM' if len(relevant_values) > 0 or len(context_hints) > 0 else 'LOW'
        }
    }
    
    # Format the analyzed predefined values into a structured output
    return json.dumps(analysis_result, indent=2)