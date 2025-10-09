# -- PRD --
# 1. BULLET: Analyze the input data to identify any explicit or implicit constraints that
#   could influence the definition of 'world'.
#   Reason: To ensure that the workflow's context is properly understood and defined
#           based on the input provided.
#   Impact: The extracted constraints will directly influence the synthesis of the
#           'world' definition.
#   Complexity: MEDIUM
#   Method: Implement a parsing mechanism that can handle various input formats (e.g.,
#           JSON, plain text) to identify and extract relevant constraints.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Process the keyword arguments (kwargs) to uncover additional constraints or
#   parameters that might affect the 'world' context.
#   Reason: kwargs may contain critical information not present in the general input.
#   Impact: Incorporating kwargs into the constraint extraction process will provide a
#           more comprehensive understanding of the workflow's context.
#   Complexity: MEDIUM
#   Method: Develop a flexible processing system for kwargs that can adapt to different
#           types of input data and structures.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the extracted constraints into a dictionary for easy access and
#   utilization by subsequent nodes.
#   Reason: A structured output is necessary for efficient data exchange between nodes.
#   Impact: This will facilitate the integration of the extracted constraints into the
#           overall workflow analysis.
#   Complexity: LOW
#   Method: Use a standard data serialization format like JSON to represent the
#           constraints dictionary.
# -- END PRD --

import json
import re


def extract_input_constraints(general_input: str, kwargs: str) -> str:
    """
    Extracts constraints from the input data and parameters that affect the definition of 'world' in the workflow.

    Args:
        general_input: Input parameter of type str
kwargs: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Initialize constraints dictionary
    constraints = {}
    
    # Process general_input to extract constraints
    if general_input:
        try:
            # Try to parse as JSON first
            parsed_input = json.loads(general_input)
            if isinstance(parsed_input, dict):
                # Extract world-related constraints from JSON structure
                for key, value in parsed_input.items():
                    if any(keyword in key.lower() for keyword in ['world', 'context', 'scope', 'domain', 'environment']):
                        constraints[f'input_{key}'] = value
                    # Look for constraint-like keys
                    if any(keyword in key.lower() for keyword in ['constraint', 'limit', 'restriction', 'boundary']):
                        constraints[f'input_{key}'] = value
        except json.JSONDecodeError:
            # If not JSON, treat as plain text and extract keywords
            text = general_input.lower()
            # Look for explicit constraint patterns
            constraint_patterns = [
                r'world\s*(?:is|means|refers to)\s*([^.\n]+)',
                r'context\s*(?:is|includes)\s*([^.\n]+)',
                r'scope\s*(?:is|limited to)\s*([^.\n]+)',
                r'constraint[s]?\s*(?::|include)\s*([^.\n]+)'
            ]
            
            for i, pattern in enumerate(constraint_patterns):
                matches = re.findall(pattern, text)
                if matches:
                    constraints[f'text_constraint_{i}'] = matches
            
            # Extract domain-specific terms
            if 'domain' in text:
                domain_match = re.search(r'domain\s*(?:is|of)\s*([^.\n]+)', text)
                if domain_match:
                    constraints['domain'] = domain_match.group(1).strip()
    
    # Process kwargs to extract additional constraints
    if kwargs:
        try:
            # Try to parse kwargs as JSON
            parsed_kwargs = json.loads(kwargs)
            if isinstance(parsed_kwargs, dict):
                for key, value in parsed_kwargs.items():
                    # Add all kwargs as potential constraints with 'kwargs_' prefix
                    constraints[f'kwargs_{key}'] = value
        except json.JSONDecodeError:
            # If kwargs is not JSON, try to parse as key-value pairs
            # Handle formats like "key1=value1,key2=value2" or "key1:value1;key2:value2"
            kwargs_clean = kwargs.strip()
            if kwargs_clean:
                # Try different separators
                if ',' in kwargs_clean and '=' in kwargs_clean:
                    pairs = kwargs_clean.split(',')
                    for pair in pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            constraints[f'kwargs_{key.strip()}'] = value.strip()
                elif ';' in kwargs_clean and ':' in kwargs_clean:
                    pairs = kwargs_clean.split(';')
                    for pair in pairs:
                        if ':' in pair:
                            key, value = pair.split(':', 1)
                            constraints[f'kwargs_{key.strip()}'] = value.strip()
                else:
                    # Store as single constraint
                    constraints['kwargs_raw'] = kwargs_clean
    
    # Add metadata about extraction
    constraints['_extraction_metadata'] = {
        'input_processed': bool(general_input),
        'kwargs_processed': bool(kwargs),
        'total_constraints': len([k for k in constraints.keys() if not k.startswith('_')])
    }
    
    # Return as JSON string (since return type is str but represents dict)
    return json.dumps(constraints, indent=2)