from ._define_world_context.analyze_workflow_purpose import analyze_workflow_purpose
from ._define_world_context.extract_workflow_objectives import extract_workflow_objectives
from ._define_world_context.identify_world_related_terms import identify_world_related_terms
from ._define_world_context.extract_input_constraints import extract_input_constraints
from ._define_world_context.identify_world_hints import identify_world_hints
from ._define_world_context.analyze_predefined_values import analyze_predefined_values
from ._define_world_context.generate_world_interpretations import generate_world_interpretations
from ._define_world_context.evaluate_interpretation_relevance import evaluate_interpretation_relevance
from ._define_world_context.assess_interpretation_impact import assess_interpretation_impact
from ._define_world_context.combine_analysis_insights import combine_analysis_insights
from ._define_world_context.craft_world_definition import craft_world_definition
from ._define_world_context.validate_definition_alignment import validate_definition_alignment

from pydantic import BaseModel, Field


# -- PRD --
# 1. BULLET: Analyze the workflow's purpose and scope to determine the context of 'world'
#   Reason: Understanding the workflow's objective is crucial to defining 'world'
#           correctly
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Review the workflow's description and objectives, Identify key terms
#           related to 'world', Determine if 'world' refers to a specific
#           geographical, cultural, or other context
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Examine the input data and parameters to identify any constraints or hints
#   about 'world'
#   Reason: Input data may provide clues about the intended meaning of 'world'
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Inspect input data structures and parameters, Look for keywords or
#           categories related to 'world', Analyze any predefined values or
#           enumerations
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Consider the potential interpretations of 'world' (geographical, cultural,
#   etc.) and evaluate their relevance
#   Reason: Evaluating different interpretations ensures a comprehensive understanding
#   Impact: HIGH
#   Complexity: HIGH
#   Method: List possible interpretations of 'world', Assess the relevance of each
#           interpretation to the workflow's context, Evaluate the
#           implications of each interpretation on the workflow's output
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Synthesize the findings from the previous steps to formulate a clear
#   definition of 'world'
#   Reason: A clear definition is necessary for consistent interpretation throughout
#           the workflow
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Combine insights from the workflow's purpose, input data, and potential
#           interpretations, Craft a concise and unambiguous definition of
#           'world', Ensure the definition is aligned with the workflow's
#           objectives
# -- END PRD --



class DefineWorldContextOutput(BaseModel):
    """Pydantic model for define_world_context node outputs."""
    world_context: str = Field(..., description="Definition of 'world' for this workflow")


def define_world_context(general_input: str, **kwargs) -> DefineWorldContextOutput:
    """Define the context and scope of 'world' for this workflow

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineWorldContextOutput: Object containing outputs for this node.
    """
    # Analyze the workflow's purpose and scope to determine the context of 'world'
    workflow_purpose: str = analyze_workflow_purpose(input_data=general_input, kwargs=kwargs)
    workflow_objectives: list = extract_workflow_objectives(purpose=workflow_purpose)
    key_terms: list = identify_world_related_terms(objectives=workflow_objectives, input_data=general_input)
    
    # Examine the input data and parameters to identify constraints or hints about 'world'
    input_constraints: dict = extract_input_constraints(general_input=general_input, kwargs=kwargs)
    world_hints: list = identify_world_hints(input_data=general_input, constraints=input_constraints)
    predefined_values: dict = analyze_predefined_values(kwargs=kwargs)
    
    # Consider potential interpretations of 'world' and evaluate their relevance
    possible_interpretations: list = generate_world_interpretations(terms=key_terms, hints=world_hints)
    relevance_scores: dict = evaluate_interpretation_relevance(interpretations=possible_interpretations, context=workflow_purpose)
    impact_analysis: dict = assess_interpretation_impact(interpretations=possible_interpretations, workflow_objectives=workflow_objectives)
    
    # Synthesize findings to formulate a clear definition of 'world'
    combined_insights: dict = combine_analysis_insights(purpose=workflow_purpose, constraints=input_constraints, interpretations=possible_interpretations, relevance=relevance_scores)
    world_definition: str = craft_world_definition(insights=combined_insights, objectives=workflow_objectives)
    validated_definition: str = validate_definition_alignment(definition=world_definition, objectives=workflow_objectives)
    
    return DefineWorldContextOutput(
        world_context=validated_definition
    )