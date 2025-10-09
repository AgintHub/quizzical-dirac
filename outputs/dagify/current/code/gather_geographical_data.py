from ._gather_geographical_data.parse_world_context import parse_world_context
from ._gather_geographical_data.fetch_continents_from_geo_source import fetch_continents_from_geo_source
from ._gather_geographical_data.fetch_countries_by_scope import fetch_countries_by_scope
from ._gather_geographical_data.collect_major_landmarks import collect_major_landmarks
from ._gather_geographical_data.format_continents_list import format_continents_list
from ._gather_geographical_data.format_countries_list import format_countries_list
from ._gather_geographical_data.format_landmarks_list import format_landmarks_list

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Determine the scope of 'world' based on the output of 'define_world_context'
#   node
#   Reason: To ensure that the geographical data collected is relevant to the context
#           defined by the 'define_world_context' node
#   Impact: HIGH
#   Complexity: LOW
#   Method: Parse the 'world_context' output from 'define_world_context' node and use
#           it to guide the data collection process
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Use a reliable geographical data source to fetch the list of continents
#   Reason: To ensure accuracy and comprehensiveness of the geographical data
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Utilize a reputable geographical database or API that provides a list of
#           continents, such as a geographical information system (GIS)
#           dataset or a web service like GeoNames
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Fetch the list of countries within the determined scope of 'world'
#   Reason: To collect country-level geographical data relevant to the defined context
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the same geographical data source or API to retrieve a list of
#           countries, filtering by the scope determined in the first step
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Identify and collect major landmarks within the scope of 'world'
#   Reason: To include significant geographical features in the data collection
#   Impact: MEDIUM
#   Complexity: HIGH
#   Method: Utilize a combination of geographical databases and web services to
#           identify major landmarks, considering factors like popularity,
#           historical significance, and geographical prominence
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compile the collected data into the required output format
#   Reason: To ensure that the output is structured as required by the node's output
#           structure
#   Impact: HIGH
#   Complexity: LOW
#   Method: Organize the collected data into lists for continents, countries, and major
#           landmarks, ensuring that each list is correctly formatted as a
#           List[str]
# -- END PRD --



class DefineWorldContextOutput(BaseModel):
    """Pydantic model for define_world_context node outputs."""
    world_context: str = Field(..., description="Definition of 'world' for this workflow")


class GatherGeographicalDataOutput(BaseModel):
    """Pydantic model for gather_geographical_data node outputs."""
    continents: List[str] = Field(..., description="List of continents")
    countries: List[str] = Field(..., description="List of countries")
    major_landmarks: List[str] = Field(..., description="List of major landmarks")


def gather_geographical_data(define_world_context_input: DefineWorldContextOutput, **kwargs) -> GatherGeographicalDataOutput:
    """Collect geographical data about the world

    Args:
        define_world_context_input: Input from the 'define_world_context' node.
        **kwargs: Additional keyword arguments.

    Returns:
        GatherGeographicalDataOutput: Object containing outputs for this node.
    """
    # Parse the world context to determine scope
    world_scope: str = parse_world_context(context=define_world_context_input.world_context)
    
    # Fetch continents from reliable geographical data source
    continents_data: List[str] = fetch_continents_from_geo_source(scope=world_scope)
    
    # Fetch countries within the determined scope
    countries_data: List[str] = fetch_countries_by_scope(scope=world_scope, continents=continents_data)
    
    # Identify and collect major landmarks within scope
    landmarks_data: List[str] = collect_major_landmarks(scope=world_scope, countries=countries_data)
    
    # Compile data into required output format
    formatted_continents: List[str] = format_continents_list(data=continents_data)
    formatted_countries: List[str] = format_countries_list(data=countries_data)
    formatted_landmarks: List[str] = format_landmarks_list(data=landmarks_data)
    
    return GatherGeographicalDataOutput(
        continents=formatted_continents,
        countries=formatted_countries,
        major_landmarks=formatted_landmarks,
    )