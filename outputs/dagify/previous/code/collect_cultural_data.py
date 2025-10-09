from ._collect_cultural_data.parse_world_context_requirements import parse_world_context_requirements
from ._collect_cultural_data.identify_cultural_data_sources import identify_cultural_data_sources
from ._collect_cultural_data.collect_religions_data import collect_religions_data
from ._collect_cultural_data.collect_languages_data import collect_languages_data
from ._collect_cultural_data.collect_cultural_practices_data import collect_cultural_practices_data
from ._collect_cultural_data.validate_cultural_data import validate_cultural_data
from ._collect_cultural_data.format_cultural_data_list import format_cultural_data_list

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Determine the specific cultural data requirements based on the world context
#   defined by the parent node 'define_world_context'
#   Reason: The world context will influence what cultural data is relevant and how it
#           should be categorized
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Parse the output of 'define_world_context' to understand the scope and
#           context of 'world'
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify reliable sources for cultural data such as major religions,
#   languages, and cultural practices
#   Reason: Accurate data collection depends on using credible and up-to-date sources
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use databases, academic publications, and reputable websites that
#           specialize in cultural information
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Collect data on major religions within the defined world context
#   Reason: Major religions are a significant aspect of cultural identity
#   Impact: HIGH
#   Complexity: LOW
#   Method: Utilize religious demographic data and studies to compile a list of major
#           religions
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Gather information on languages spoken within the defined world context
#   Reason: Languages are crucial to understanding cultural diversity
#   Impact: HIGH
#   Complexity: LOW
#   Method: Consult linguistic databases and demographic studies to list languages
#           spoken in the world context
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compile data on cultural practices prevalent in the defined world context
#   Reason: Cultural practices provide insight into the daily lives and traditions of
#           people
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Analyze ethnographic studies and cultural reports to identify significant
#           cultural practices
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Organize and format the collected cultural data into the required output
#   structure
#   Reason: The output must be structured to be usable by subsequent nodes
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use data processing techniques to ensure the data is correctly formatted as
#           List[str] for major_religions, languages, and
#           cultural_practices
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Validate the collected data for accuracy and relevance to the defined world
#   context
#   Reason: Ensuring data quality is crucial for downstream analyses
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Cross-check data against multiple sources and use data validation
#           techniques
# -- END PRD --



class DefineWorldContextOutput(BaseModel):
    """Pydantic model for define_world_context node outputs."""
    world_context: str = Field(..., description="Definition of 'world' for this workflow")


class CollectCulturalDataOutput(BaseModel):
    """Pydantic model for collect_cultural_data node outputs."""
    major_religions: List[str] = Field(..., description="List of major religions in the defined world context")
    languages: List[str] = Field(..., description="List of languages spoken in the defined world context")
    cultural_practices: List[str] = Field(..., description="List of cultural practices prevalent in the defined world context")


def collect_cultural_data(define_world_context_input: DefineWorldContextOutput, **kwargs) -> CollectCulturalDataOutput:
    """Collect cultural data about the world

    Args:
        define_world_context_input: Input from the 'define_world_context' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CollectCulturalDataOutput: Object containing outputs for this node.
    """
    # Parse world context to determine specific cultural data requirements
    cultural_requirements: dict = parse_world_context_requirements(
        world_context=define_world_context_input.world_context
    )
    
    # Identify and validate reliable sources for cultural data collection
    data_sources: List[str] = identify_cultural_data_sources(
        world_context=define_world_context_input.world_context,
        requirements=cultural_requirements
    )
    
    # Collect major religions data for the defined world context
    raw_religions_data: List[str] = collect_religions_data(
        world_context=define_world_context_input.world_context,
        sources=data_sources
    )
    
    # Gather languages spoken within the world context
    raw_languages_data: List[str] = collect_languages_data(
        world_context=define_world_context_input.world_context,
        sources=data_sources
    )
    
    # Compile cultural practices data for the world context
    raw_cultural_practices_data: List[str] = collect_cultural_practices_data(
        world_context=define_world_context_input.world_context,
        sources=data_sources
    )
    
    # Validate collected data for accuracy and relevance
    validated_religions: List[str] = validate_cultural_data(
        data=raw_religions_data,
        data_type="religions",
        world_context=define_world_context_input.world_context
    )
    
    validated_languages: List[str] = validate_cultural_data(
        data=raw_languages_data,
        data_type="languages",
        world_context=define_world_context_input.world_context
    )
    
    validated_practices: List[str] = validate_cultural_data(
        data=raw_cultural_practices_data,
        data_type="cultural_practices",
        world_context=define_world_context_input.world_context
    )
    
    # Format and organize data into required output structure
    formatted_religions: List[str] = format_cultural_data_list(
        data=validated_religions,
        data_type="religions"
    )
    
    formatted_languages: List[str] = format_cultural_data_list(
        data=validated_languages,
        data_type="languages"
    )
    
    formatted_practices: List[str] = format_cultural_data_list(
        data=validated_practices,
        data_type="cultural_practices"
    )
    
    return CollectCulturalDataOutput(
        major_religions=formatted_religions,
        languages=formatted_languages,
        cultural_practices=formatted_practices
    )