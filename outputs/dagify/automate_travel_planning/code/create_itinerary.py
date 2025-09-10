from ._create_itinerary.parse_flight_information import parse_flight_information
from ._create_itinerary.parse_hotel_information import parse_hotel_information
from ._create_itinerary.parse_car_rental_information import parse_car_rental_information
from ._create_itinerary.parse_immigration_requirements import parse_immigration_requirements
from ._create_itinerary.generate_unique_identifier import generate_unique_identifier
from ._create_itinerary.generate_activity_schedules import generate_activity_schedules
from ._create_itinerary.generate_travel_dates import generate_travel_dates
from ._create_itinerary.format_itinerary_to_human_readable import format_itinerary_to_human_readable

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Retrieve flight information from the search_flights node and parse it into a
#   usable format
#   Reason: This step is necessary to gather flight details for the itinerary
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use JSON parsing to extract flight information from the search_flights node
#           output
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Retrieve hotel reservation information from the search_hotels node and parse
#   it into a usable format
#   Reason: This step is necessary to gather hotel reservation details for the
#           itinerary
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use JSON parsing to extract hotel reservation information from the
#           search_hotels node output
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Retrieve car rental information from the search_cars node and parse it into a
#   usable format
#   Reason: This step is necessary to gather car rental details for the itinerary
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use JSON parsing to extract car rental information from the search_cars
#           node output
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Retrieve immigration requirements from the check_immigration_requirements
#   node and parse it into a usable format
#   Reason: This step is necessary to gather immigration requirements for the itinerary
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use JSON parsing to extract immigration requirements from the
#           check_immigration_requirements node output
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Combine the parsed flight, hotel, car rental, and immigration requirements
#   information into a single itinerary
#   Reason: This step is necessary to create a comprehensive itinerary for the trip
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use a templating engine to combine the parsed information into a single
#           JSON object
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Generate a unique identifier for the itinerary
#   Reason: This step is necessary to uniquely identify the itinerary
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a UUID generator to create a unique identifier
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Format the itinerary into a human-readable format
#   Reason: This step is necessary to make the itinerary easy to understand for the
#           user
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use a formatting library to format the itinerary into a human-readable
#           format
# -- END PRD --



class SearchFlightsOutput(BaseModel):
    """Pydantic model for search_flights node outputs."""
    flight_options: List[str] = Field(..., description="List of available flight options, including flight numbers, departure and arrival times, airlines, and prices")
    airline_names: List[str] = Field(..., description="List of airline names")
    departure_times: List[str] = Field(..., description="List of departure times")
    arrival_times: List[str] = Field(..., description="List of arrival times")
    prices: List[float] = Field(..., description="List of prices for each flight option")


class SearchHotelsOutput(BaseModel):
    """Pydantic model for search_hotels node outputs."""
    hotel_names: List[str] = Field(..., description="List of hotel names found at the destinations")
    hotel_locations: List[str] = Field(..., description="List of hotel locations corresponding to the hotels found")
    hotel_prices: List[float] = Field(..., description="List of hotel prices corresponding to the hotels found")
    hotel_amenities: List[str] = Field(..., description="List of amenities offered by each hotel found")


class SearchCarsOutput(BaseModel):
    """Pydantic model for search_cars node outputs."""
    destination_names: List[str] = Field(..., description="List of destination names where car rentals were searched")
    car_rental_options: List[str] = Field(..., description="List of available car rental options, including car types and rental agencies")
    car_rental_prices: List[float] = Field(..., description="List of prices for the available car rental options")
    rental_agencies: List[str] = Field(..., description="List of rental agencies offering car rentals at each destination")


class CheckImmigrationRequirementsOutput(BaseModel):
    """Pydantic model for check_immigration_requirements node outputs."""
    destination_countries: List[str] = Field(..., description="List of destination countries")
    visa_requirements: List[str] = Field(..., description="List of visa requirements for each destination country")
    travel_restrictions: List[str] = Field(..., description="List of travel restrictions for each destination country")
    health_certificates_required: List[bool] = Field(..., description="List of whether health certificates are required for each destination country")


class CreateItineraryOutput(BaseModel):
    """Pydantic model for create_itinerary node outputs."""
    itinerary_id: str = Field(..., description="Unique identifier for the itinerary")
    flight_details: str = Field(..., description="List of flight information, including departure and arrival times, airlines, and flight numbers")
    hotel_reservations: str = Field(..., description="List of hotel reservation information, including hotel names, locations, and reservation numbers")
    car_rental_details: str = Field(..., description="List of car rental information, including car types, rental agencies, and pickup/drop-off details")
    activity_schedules: str = Field(..., description="List of activity schedules, including dates, times, and activity descriptions")
    immigration_requirements: str = Field(..., description="List of immigration requirements for each destination, including visa requirements and travel restrictions")
    travel_dates: str = Field(..., description="List of travel dates, including start and end dates for the trip")


def create_itinerary(search_flights_input: SearchFlightsOutput, search_hotels_input: SearchHotelsOutput, search_cars_input: SearchCarsOutput, check_immigration_requirements_input: CheckImmigrationRequirementsOutput, **kwargs) -> CreateItineraryOutput:
    """Create a detailed itinerary for the trip

    Args:
        search_flights_input: Input from the 'search_flights' node.
        search_hotels_input: Input from the 'search_hotels' node.
        search_cars_input: Input from the 'search_cars' node.
        check_immigration_requirements_input: Input from the 'check_immigration_requirements' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CreateItineraryOutput: Object containing outputs for this node.
    """
    # Parse flight information from search_flights node
    flight_details_str: str = parse_flight_information(
        flight_options=search_flights_input.flight_options,
        airline_names=search_flights_input.airline_names,
        departure_times=search_flights_input.departure_times,
        arrival_times=search_flights_input.arrival_times,
        prices=search_flights_input.prices
    )
    
    # Parse hotel reservation information from search_hotels node
    hotel_reservations_str: str = parse_hotel_information(
        hotel_names=search_hotels_input.hotel_names,
        hotel_locations=search_hotels_input.hotel_locations,
        hotel_prices=search_hotels_input.hotel_prices,
        hotel_amenities=search_hotels_input.hotel_amenities
    )
    
    # Parse car rental information from search_cars node
    car_rental_details_str: str = parse_car_rental_information(
        destination_names=search_cars_input.destination_names,
        car_rental_options=search_cars_input.car_rental_options,
        car_rental_prices=search_cars_input.car_rental_prices,
        rental_agencies=search_cars_input.rental_agencies
    )
    
    # Parse immigration requirements from check_immigration_requirements node
    immigration_requirements_str: str = parse_immigration_requirements(
        destination_countries=check_immigration_requirements_input.destination_countries,
        visa_requirements=check_immigration_requirements_input.visa_requirements,
        travel_restrictions=check_immigration_requirements_input.travel_restrictions,
        health_certificates_required=check_immigration_requirements_input.health_certificates_required
    )
    
    # Generate unique identifier for the itinerary
    itinerary_id: str = generate_unique_identifier()
    
    # Generate activity schedules based on parsed information
    activity_schedules_str: str = generate_activity_schedules(
        flight_details=flight_details_str,
        hotel_reservations=hotel_reservations_str,
        car_rental_details=car_rental_details_str
    )
    
    # Generate travel dates information
    travel_dates_str: str = generate_travel_dates(
        departure_times=search_flights_input.departure_times,
        arrival_times=search_flights_input.arrival_times
    )
    
    # Format the entire itinerary into a human-readable format
    final_itinerary: dict = format_itinerary_to_human_readable(
        itinerary_id=itinerary_id,
        flight_details=flight_details_str,
        hotel_reservations=hotel_reservations_str,
        car_rental_details=car_rental_details_str,
        activity_schedules=activity_schedules_str,
        immigration_requirements=immigration_requirements_str,
        travel_dates=travel_dates_str
    )
    
    # Return the complete itinerary
    return CreateItineraryOutput(
        itinerary_id=itinerary_id,
        flight_details=flight_details_str,
        hotel_reservations=hotel_reservations_str,
        car_rental_details=car_rental_details_str,
        activity_schedules=activity_schedules_str,
        immigration_requirements=immigration_requirements_str,
        travel_dates=travel_dates_str
    )
