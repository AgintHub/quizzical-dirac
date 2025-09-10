# -- PRD --
# 1. BULLET: Retrieve the flight details from the create_itinerary node's output,
#   specifically the flight_details field.
#   Reason: The create_itinerary node provides the necessary flight information to book
#           flights.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a JSON parser to extract the flight details from the create_itinerary
#           node's output.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Loop through the flight details and extract the necessary information, such
#   as flight numbers, departure and arrival times, and airlines.
#   Reason: This information is required to book flights and generate the flight
#           itinerary.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a programming language's built-in data structures, such as lists and
#           dictionaries, to store and manipulate the flight information.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Use the extracted flight information to book flights through a flight booking
#   API or website.
#   Reason: This step is necessary to secure the flights and generate a flight
#           itinerary.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a library or framework that provides a interface to the flight booking
#           API, such as a SOAP or REST API client.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Check if travel insurance is required and purchase it if necessary.
#   Reason: Travel insurance is optional but recommended to protect against unforeseen
#           circumstances.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a simple conditional statement to check if travel insurance is required
#           and purchase it through a travel insurance API or website.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Check if seat upgrades are available and purchase them if desired.
#   Reason: Seat upgrades can enhance the travel experience but are optional.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a simple conditional statement to check if seat upgrades are available
#           and purchase them through a flight booking API or website.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Generate the flight itinerary based on the booked flights and travel
#   insurance and seat upgrade information.
#   Reason: The flight itinerary is required as output to confirm the booked flights
#           and travel arrangements.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a template engine or a programming language's built-in string
#           manipulation functions to generate the flight itinerary.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CreateItineraryOutput(BaseModel):
    """Pydantic model for create_itinerary node outputs."""
    itinerary_id: str = Field(..., description="Unique identifier for the itinerary")
    flight_details: str = Field(..., description="List of flight information, including departure and arrival times, airlines, and flight numbers")
    hotel_reservations: str = Field(..., description="List of hotel reservation information, including hotel names, locations, and reservation numbers")
    car_rental_details: str = Field(..., description="List of car rental information, including car types, rental agencies, and pickup/drop-off details")
    activity_schedules: str = Field(..., description="List of activity schedules, including dates, times, and activity descriptions")
    immigration_requirements: str = Field(..., description="List of immigration requirements for each destination, including visa requirements and travel restrictions")
    travel_dates: str = Field(..., description="List of travel dates, including start and end dates for the trip")


class BookFlightsOutput(BaseModel):
    """Pydantic model for book_flights node outputs."""
    flight_booking_status: bool = Field(..., description="Whether the flight booking was successful")
    flight_itinerary: str = Field(..., description="Detailed itinerary of the booked flights")
    flight_numbers: List[str] = Field(..., description="List of flight numbers for the booked flights")
    departure_times: List[str] = Field(..., description="List of departure times for the booked flights")
    arrival_times: List[str] = Field(..., description="List of arrival times for the booked flights")
    airlines: List[str] = Field(..., description="List of airlines for the booked flights")
    travel_insurance: bool = Field(..., description="Whether travel insurance was purchased")
    seat_upgrades: bool = Field(..., description="Whether seat upgrades were purchased")


def book_flights(create_itinerary_input: CreateItineraryOutput, **kwargs) -> BookFlightsOutput:
    """Book flights for the trip

    Args:
        create_itinerary_input: Input from the 'create_itinerary' node.
        **kwargs: Additional keyword arguments.

    Returns:
        BookFlightsOutput: Object containing outputs for this node.
    """
    # Parse flight details from create_itinerary output
    parsed_flight_details: dict = parse_flight_details(flight_details=create_itinerary_input.flight_details)
    
    # Extract necessary flight information
    flight_info: List[dict] = extract_flight_information(parsed_data=parsed_flight_details)
    
    # Book flights through API
    booking_result: dict = book_flights_through_api(flight_info=flight_info)
    
    # Check if booking was successful
    is_booking_successful: bool = verify_booking_status(booking_result=booking_result)
    
    if is_booking_successful:
        # Check and purchase travel insurance if needed
        travel_insurance_purchased: bool = process_travel_insurance(booking_result=booking_result)
        
        # Check and purchase seat upgrades if desired
        seat_upgrades_purchased: bool = process_seat_upgrades(booking_result=booking_result)
        
        # Generate flight itinerary
        flight_itinerary_text: str = generate_flight_itinerary(
            booking_result=booking_result,
            insurance_status=travel_insurance_purchased,
            upgrades_status=seat_upgrades_purchased
        )
        
        # Extract flight details from booking result
        flight_numbers: List[str] = extract_flight_numbers(booking_result=booking_result)
        departure_times: List[str] = extract_departure_times(booking_result=booking_result)
        arrival_times: List[str] = extract_arrival_times(booking_result=booking_result)
        airlines: List[str] = extract_airlines(booking_result=booking_result)
    else:
        # Set empty values if booking failed
        flight_itinerary_text = "Flight booking failed"
        flight_numbers, departure_times, arrival_times, airlines = [], [], [], []
        travel_insurance_purchased, seat_upgrades_purchased = False, False

    return BookFlightsOutput(
        flight_booking_status=is_booking_successful,
        flight_itinerary=flight_itinerary_text,
        flight_numbers=flight_numbers,
        departure_times=departure_times,
        arrival_times=arrival_times,
        airlines=airlines,
        travel_insurance=travel_insurance_purchased,
        seat_upgrades=seat_upgrades_purchased,
    )