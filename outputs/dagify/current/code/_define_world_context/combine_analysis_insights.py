# -- PRD --
# 1. BULLET: Implement data aggregation logic to combine the purpose, constraints,
#   interpretations, and relevance into a single data structure.
#   Reason: To synthesize findings from various analyses into a coherent output that
#           can be used for defining the world context.
#   Impact: Enables the creation of a comprehensive world definition by integrating
#           multiple aspects of the workflow analysis.
#   Complexity: MEDIUM
#   Method: Use a Python dictionary to store the combined insights, with appropriate
#           key naming conventions to represent different analysis outputs.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Ensure the output is serializable to a string format as required by the
#   output structure.
#   Reason: To comply with the specified output type (STR) and facilitate further
#           processing or storage.
#   Impact: Allows for seamless integration with subsequent nodes or processes that
#           expect a string output.
#   Complexity: LOW
#   Method: Utilize JSON serialization (e.g., `json.dumps()`) to convert the dictionary
#           into a string.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the input parameters to ensure they are not empty or malformed.
#   Reason: To prevent errors during the combination process and ensure the quality of
#           the output.
#   Impact: Enhances the robustness and reliability of the node by handling potential
#           edge cases.
#   Complexity: LOW
#   Method: Implement basic checks at the beginning of the function to verify the
#           presence and type of input parameters.
# -- END PRD --

import json


def combine_analysis_insights(purpose: str, constraints: str, interpretations: str, relevance: str) -> str:
    """
    Combines multiple analysis insights into a comprehensive output for defining the world context.

    Args:
        purpose: Input parameter of type str
constraints: Input parameter of type str
interpretations: Input parameter of type str
relevance: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Validate input parameters to ensure they are not empty or malformed
    if not isinstance(purpose, str) or not purpose.strip():
        raise ValueError("Purpose parameter must be a non-empty string")
    if not isinstance(constraints, str) or not constraints.strip():
        raise ValueError("Constraints parameter must be a non-empty string")
    if not isinstance(interpretations, str) or not interpretations.strip():
        raise ValueError("Interpretations parameter must be a non-empty string")
    if not isinstance(relevance, str) or not relevance.strip():
        raise ValueError("Relevance parameter must be a non-empty string")
    
    # Implement data aggregation logic to combine insights into a single data structure
    combined_insights = {
        "analysis_purpose": purpose.strip(),
        "identified_constraints": constraints.strip(),
        "workflow_interpretations": interpretations.strip(),
        "context_relevance": relevance.strip(),
        "world_context_summary": {
            "synthesis_timestamp": None,  # Could be populated with current timestamp if needed
            "integration_status": "complete",
            "analysis_components": ["purpose", "constraints", "interpretations", "relevance"]
        }
    }
    
    # Ensure the output is serializable to a string format
    try:
        serialized_output = json.dumps(combined_insights, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to serialize combined insights to JSON: {e}") from e
    
    return serialized_output