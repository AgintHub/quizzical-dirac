from ._search_cars.search_car_rentals_api import search_car_rentals_api
from ._search_cars.extract_car_types import extract_car_types
from ._search_cars.extract_rental_prices import extract_rental_prices
from ._search_cars.extract_rental_agencies import extract_rental_agencies

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Extract the list of potential destinations from the output of the
#   'research_destination_options' node
#   Reason: The 'research_destination_options' node provides the list of potential
#           destinations that we need to search for car rentals
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the 'potential_destinations' output from 'research_destination_options'
#           node
# 
# -----------------------------------------------------------------------------
# 2. BULLET: For each potential destination, search for car rental options using a car
#   rental API or service
#   Reason: We need to find available car rental options for each destination
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a car rental API (e.g., Expedia, Kayak) to search for car rentals at
#           each destination
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Extract car rental options details including car types, rental agencies, and
#   prices
#   Reason: We need to gather detailed information about the available car rental
#           options
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Parse the car rental search results to extract car types, rental agencies,
#           and prices
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Compile the extracted car rental options into the required output format
#   Reason: We need to format the car rental information according to the specified
#           output structure
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Map the extracted car rental details to the output fields:
#           'destination_names', 'car_rental_options', 'car_rental_prices',
#           and 'rental_agencies'
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Return the compiled car rental information as the output of the 'search_cars'
#   node
#   Reason: This is the final step in executing the 'search_cars' node
#   Impact: HIGH
#   Complexity: LOW
#   Method: Output the compiled car rental information in the required format
# -- END PRD --



class ResearchDestinationOptionsOutput(BaseModel):
    """Pydantic model for research_destination_options node outputs."""
    potential_destinations: List[str] = Field(..., description="List of potential destinations that align with the trip's objectives")
    destination_details: List[str] = Field(..., description="List of details about each potential destination, including factors like weather, safety, and attractions")


class SearchCarsOutput(BaseModel):
    """Pydantic model for search_cars node outputs."""
    destination_names: List[str] = Field(..., description="List of destination names where car rentals were searched")
    car_rental_options: List[str] = Field(..., description="List of available car rental options, including car types and rental agencies")
    car_rental_prices: List[float] = Field(..., description="List of prices for the available car rental options")
    rental_agencies: List[str] = Field(..., description="List of rental agencies offering car rentals at each destination")


def search_cars(research_destination_options_input: ResearchDestinationOptionsOutput, **kwargs) -> SearchCarsOutput:
    """Search for car rental options at each destination

    Args:
        research_destination_options_input: Input from the 'research_destination_options' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SearchCarsOutput: Object containing outputs for this node.
    """
    # Extract destinations from the research_destination_options_input
    destinations: List[str] = research_destination_options_input.potential_destinations
    
    # Initialize lists to store results
    all_destination_names: List[str] = []
    all_car_rental_options: List[str] = []
    all_car_rental_prices: List[float] = []
    all_rental_agencies: List[str] = []
    
    # Search for car rentals at each destination
    for destination in destinations:
        # Call car rental API to get available options
        rental_results: List[dict] = search_car_rentals_api(destination=destination, **kwargs)
        
        # Process results if any car rentals are found
        if rental_results:
            # Extract car rental details
            car_options: List[str] = extract_car_types(results=rental_results)
            prices: List[float] = extract_rental_prices(results=rental_results)
            agencies: List[str] = extract_rental_agencies(results=rental_results)
            
            # Compile results
            for car_option, price, agency in zip(car_options, prices, agencies):
                all_destination_names.append(destination)
                all_car_rental_options.append(car_option)
                all_car_rental_prices.append(price)
                all_rental_agencies.append(agency)
    
    # Return compiled car rental information
    return SearchCarsOutput(
        destination_names=all_destination_names,
        car_rental_options=all_car_rental_options,
        car_rental_prices=all_car_rental_prices,
        rental_agencies=all_rental_agencies,
    )