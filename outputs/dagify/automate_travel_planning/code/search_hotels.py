# -- PRD --
# 1. BULLET: Use the output from the 'research_destination_options' node to get the list
#   of potential destinations.
#   Reason: The potential destinations are required to search for hotels.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Call the 'research_destination_options' node and retrieve the
#           'potential_destinations' output.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: For each potential destination, send a request to a hotel search API (e.g.
#   Expedia, Booking.com) to retrieve a list of available hotels.
#   Reason: The hotel search API will provide the necessary information about hotels at
#           each destination.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the 'requests' library to send a GET request to the hotel search API
#           with the destination as a parameter.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Parse the response from the hotel search API to extract the hotel names,
#   locations, prices, and amenities.
#   Reason: The response from the API will be in a structured format (e.g. JSON) that
#           needs to be parsed to extract the relevant information.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a JSON parsing library (e.g. 'json') to extract the hotel information
#           from the API response.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Store the extracted hotel information in a data structure (e.g. a dictionary
#   or a pandas DataFrame) for further processing.
#   Reason: The hotel information needs to be stored in a structured format to be
#           easily accessible and manipulable.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a dictionary or a pandas DataFrame to store the hotel information.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Return the list of hotel names, locations, prices, and amenities as the
#   output of the 'search_hotels' node.
#   Reason: The output of the 'search_hotels' node is required by the downstream nodes
#           (e.g. 'create_itinerary').
#   Impact: HIGH
#   Complexity: LOW
#   Method: Return the stored hotel information as a list of dictionaries or a pandas
#           DataFrame.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class ResearchDestinationOptionsOutput(BaseModel):
    """Pydantic model for research_destination_options node outputs."""
    potential_destinations: List[str] = Field(..., description="List of potential destinations that align with the trip's objectives")
    destination_details: List[str] = Field(..., description="List of details about each potential destination, including factors like weather, safety, and attractions")


class SearchHotelsOutput(BaseModel):
    """Pydantic model for search_hotels node outputs."""
    hotel_names: List[str] = Field(..., description="List of hotel names found at the destinations")
    hotel_locations: List[str] = Field(..., description="List of hotel locations corresponding to the hotels found")
    hotel_prices: List[float] = Field(..., description="List of hotel prices corresponding to the hotels found")
    hotel_amenities: List[str] = Field(..., description="List of amenities offered by each hotel found")


def search_hotels(research_destination_options_input: ResearchDestinationOptionsOutput, **kwargs) -> SearchHotelsOutput:
    """Search for hotels at each destination

    Args:
        research_destination_options_input: Input from the 'research_destination_options' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SearchHotelsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SearchHotelsOutput(
        hotel_names=[],
        hotel_locations=[],
        hotel_prices=[],
        hotel_amenities=[],
    )