from ._define_travel_objectives.extract_primary_purpose import extract_primary_purpose
from ._define_travel_objectives.extract_number_of_travelers import extract_number_of_travelers
from ._define_travel_objectives.extract_trip_objectives import extract_trip_objectives
from ._define_travel_objectives.validate_travel_information import validate_travel_information

from pydantic import BaseModel, Field


# -- PRD --
# 1. BULLET: Identify the primary purpose of the trip by analyzing the input prompt for
#   keywords indicating the main reason for travel, such as 'business',
#   'vacation', 'honeymoon', etc.
#   Reason: The primary purpose is essential for determining the type of travel
#           arrangements and recommendations to be made.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use natural language processing (NLP) techniques to parse the input prompt
#           and extract the primary purpose.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Determine the number of travelers by parsing the input prompt for numerical
#   values or references to the number of people traveling.
#   Reason: The number of travelers affects booking arrangements, costs, and
#           recommendations.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Employ regular expressions or NLP to identify and extract the number of
#           travelers from the input prompt.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Extract a brief description of the trip's objectives from the input prompt,
#   focusing on details that outline what the travelers aim to achieve or
#   experience during the trip.
#   Reason: Understanding the trip's objectives helps in tailoring recommendations and
#           arrangements that meet the travelers' needs.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use NLP to analyze the input prompt, identify key phrases or sentences
#           describing the trip's objectives, and summarize them into a
#           concise description.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Validate the extracted information (primary purpose, number of travelers,
#   trip objectives) to ensure it is consistent, reasonable, and complete.
#   Reason: Validation is crucial for ensuring the quality and relevance of the travel
#           plan.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Implement checks for consistency (e.g., number of travelers is a positive
#           integer), reasonableness (e.g., trip objectives align with the
#           primary purpose), and completeness (all required information is
#           present).
# -- END PRD --



class DefineTravelObjectivesOutput(BaseModel):
    """Pydantic model for define_travel_objectives node outputs."""
    primary_purpose: str = Field(..., description="The primary purpose of the trip")
    number_of_travelers: int = Field(..., description="The number of people traveling")
    trip_objectives: str = Field(..., description="A brief description of the trip's objectives")


def define_travel_objectives(general_input: str, **kwargs) -> DefineTravelObjectivesOutput:
    """Define the purpose and scope of the trip

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineTravelObjectivesOutput: Object containing outputs for this node.
    """
    # Extract the primary purpose from the input
    primary_purpose: str = extract_primary_purpose(input_text=general_input)
    
    # Extract the number of travelers from the input
    number_of_travelers: int = extract_number_of_travelers(input_text=general_input)
    
    # Extract trip objectives from the input
    trip_objectives: str = extract_trip_objectives(input_text=general_input)
    
    # Validate the extracted information
    validate_travel_information(
        primary_purpose=primary_purpose,
        number_of_travelers=number_of_travelers,
        trip_objectives=trip_objectives
    )
    
    # Return the completed output
    return DefineTravelObjectivesOutput(
        primary_purpose=primary_purpose,
        number_of_travelers=number_of_travelers,
        trip_objectives=trip_objectives,
    )