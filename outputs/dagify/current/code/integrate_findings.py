from ._integrate_findings.preprocess_patterns import preprocess_patterns
from ._integrate_findings.identify_key_themes import identify_key_themes
from ._integrate_findings.craft_integrated_narrative import craft_integrated_narrative
from ._integrate_findings.format_narrative_output import format_narrative_output

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Extract geographical patterns from the output of 'analyze_geographical_data'
#   node
#   Reason: To utilize the geographical patterns identified in the previous step
#   Impact: HIGH
#   Complexity: LOW
#   Method: Access the 'geographical_patterns' output from 'analyze_geographical_data'
#           node, which is a list of strings representing geographical
#           patterns or features
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Extract cultural patterns from the output of 'analyze_cultural_data' node
#   Reason: To utilize the cultural patterns identified in the previous step
#   Impact: HIGH
#   Complexity: LOW
#   Method: Access the 'cultural_patterns' output from 'analyze_cultural_data' node,
#           which is a list of strings representing cultural patterns or
#           features
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Combine the extracted geographical and cultural patterns into a single
#   narrative
#   Reason: To form a comprehensive view of the world by integrating both geographical
#           and cultural analyses
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a natural language processing (NLP) approach to concatenate and
#           summarize the patterns. This involves: 1) Preprocessing the
#           lists to remove duplicates and irrelevant information, 2)
#           Identifying key themes or patterns that emerge from both lists,
#           3) Crafting a narrative that weaves together these themes into
#           a coherent story about the world.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Format the integrated narrative into a string output
#   Reason: To match the required output structure of 'integrated_findings'
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Convert the final narrative into a string format, ensuring it is well-
#           formatted and readable
# -- END PRD --



class AnalyzeGeographicalDataOutput(BaseModel):
    """Pydantic model for analyze_geographical_data node outputs."""
    geographical_patterns: List[str] = Field(..., description="List of geographical patterns or features")


class AnalyzeCulturalDataOutput(BaseModel):
    """Pydantic model for analyze_cultural_data node outputs."""
    cultural_patterns: List[str] = Field(..., description="List of cultural patterns or features")


class IntegrateFindingsOutput(BaseModel):
    """Pydantic model for integrate_findings node outputs."""
    integrated_findings: str = Field(..., description="Integrated findings about the world")


def integrate_findings(analyze_geographical_data_input: AnalyzeGeographicalDataOutput, analyze_cultural_data_input: AnalyzeCulturalDataOutput, **kwargs) -> IntegrateFindingsOutput:
    """Integrate geographical and cultural findings

    Args:
        analyze_geographical_data_input: Input from the 'analyze_geographical_data' node.
        analyze_cultural_data_input: Input from the 'analyze_cultural_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        IntegrateFindingsOutput: Object containing outputs for this node.
    """
    # Extract geographical patterns from the input
    geographical_patterns: List[str] = analyze_geographical_data_input.geographical_patterns
    
    # Extract cultural patterns from the input
    cultural_patterns: List[str] = analyze_cultural_data_input.cultural_patterns
    
    # Preprocess and clean the patterns to remove duplicates and irrelevant information
    cleaned_geo_patterns: List[str] = preprocess_patterns(patterns=geographical_patterns, pattern_type="geographical")
    cleaned_cultural_patterns: List[str] = preprocess_patterns(patterns=cultural_patterns, pattern_type="cultural")
    
    # Identify key themes that emerge from both geographical and cultural patterns
    key_themes: List[str] = identify_key_themes(geo_patterns=cleaned_geo_patterns, cultural_patterns=cleaned_cultural_patterns)
    
    # Craft a comprehensive narrative that weaves together the themes
    integrated_narrative: str = craft_integrated_narrative(themes=key_themes, geo_patterns=cleaned_geo_patterns, cultural_patterns=cleaned_cultural_patterns)
    
    # Format the narrative into a well-formatted string output
    formatted_findings: str = format_narrative_output(narrative=integrated_narrative)
    
    return IntegrateFindingsOutput(
        integrated_findings=formatted_findings
    )