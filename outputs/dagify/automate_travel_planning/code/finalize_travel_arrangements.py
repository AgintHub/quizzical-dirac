from ._finalize_travel_arrangements.extract_flight_details import extract_flight_details
from ._finalize_travel_arrangements.extract_hotel_details import extract_hotel_details
from ._finalize_travel_arrangements.extract_car_rental_details import extract_car_rental_details
from ._finalize_travel_arrangements.extract_visa_details import extract_visa_details
from ._finalize_travel_arrangements.get_confirmation_numbers import get_confirmation_numbers
from ._finalize_travel_arrangements.calculate_total_travel_cost import calculate_total_travel_cost
from ._finalize_travel_arrangements.determine_travel_arrangement_status import determine_travel_arrangement_status
from ._finalize_travel_arrangements.compile_visa_status_info import compile_visa_status_info

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Retrieve the output from the 'book_flights' node, including
#   'flight_booking_status', 'flight_numbers', and other relevant details.
#   Reason: To finalize travel arrangements, we need the details of the booked flights.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'book_flights' to get the required flight information.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Retrieve the output from the 'book_hotels' node, including 'booking_status',
#   'hotel_names', and other relevant details.
#   Reason: To finalize travel arrangements, we need the details of the booked hotels.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'book_hotels' to get the required hotel information.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Retrieve the output from the 'book_cars' node, including 'booking_status',
#   'car_rental_details', and other relevant details.
#   Reason: To finalize travel arrangements, we need the details of the booked car
#           rentals.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'book_cars' to get the required car rental information.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Retrieve the output from the 'apply_for_visas' node, including
#   'visa_application_status', 'visa_types_applied_for', and other relevant
#   details.
#   Reason: To finalize travel arrangements, we need the status of the visa
#           applications.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'apply_for_visas' to get the required visa application
#           information.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Aggregate the confirmation numbers for flights, hotels, and car rentals from
#   their respective booking nodes.
#   Reason: To provide a comprehensive summary of travel arrangements.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Extract and compile the confirmation numbers from the outputs of
#           'book_flights', 'book_hotels', and 'book_cars'.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Calculate the total travel cost by summing the costs of flights, hotels, car
#   rentals, and any other relevant expenses.
#   Reason: To provide a total cost for the travel arrangements.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Sum the 'total_cost' from 'book_hotels' and 'book_cars', and add any other
#           relevant costs from other nodes.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Determine the overall travel arrangement status based on the booking statuses
#   of flights, hotels, car rentals, and visa applications.
#   Reason: To indicate whether all travel arrangements have been successfully
#           finalized.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Evaluate the 'booking_status' from 'book_flights', 'book_hotels',
#           'book_cars', and 'visa_application_status' from
#           'apply_for_visas' to determine the overall status.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Compile the final output structure with 'travel_arrangement_status',
#   'flight_confirmation_numbers', 'hotel_confirmation_numbers',
#   'car_rental_confirmation_numbers', 'visa_application_status', and
#   'total_travel_cost'.
#   Reason: To provide a comprehensive and structured output that summarizes the travel
#           arrangements.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the information gathered from previous steps to populate the output
#           structure.
# -- END PRD --



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


class BookHotelsOutput(BaseModel):
    """Pydantic model for book_hotels node outputs."""
    hotel_names: List[str] = Field(..., description="List of booked hotel names")
    room_types: List[str] = Field(..., description="List of room types booked")
    check_in_dates: List[str] = Field(..., description="List of check-in dates for each hotel")
    check_out_dates: List[str] = Field(..., description="List of check-out dates for each hotel")
    total_cost: float = Field(..., description="Total cost of all hotel bookings")
    booking_status: bool = Field(..., description="Whether the hotel booking was successful")


class BookCarsOutput(BaseModel):
    """Pydantic model for book_cars node outputs."""
    car_rental_booking_reference: str = Field(..., description="Booking reference number for the car rental")
    car_rental_details: List[str] = Field(..., description="List of car rental details, including car type, rental agency, and pickup/drop-off information")
    insurance_options: List[str] = Field(..., description="List of insurance options selected for the car rental")
    equipment_upgrades: List[str] = Field(..., description="List of equipment upgrades selected for the car rental, such as GPS or child seats")
    total_cost: float = Field(..., description="Total cost of the car rental, including any additional fees or upgrades")
    booking_status: bool = Field(..., description="Whether the car rental booking was successful")


class ApplyForVisasOutput(BaseModel):
    """Pydantic model for apply_for_visas node outputs."""
    visa_application_status: bool = Field(..., description="Whether the visa application has been successfully submitted")
    visa_types_applied_for: str = Field(..., description="List of visa types applied for (e.g., tourist, business, transit)")
    required_documentation: str = Field(..., description="List of required documentation for the visa application (e.g., passport, proof of travel, financial statements)")
    visa_application_reference_numbers: str = Field(..., description="List of reference numbers for the submitted visa applications")
    expected_processing_time: int = Field(..., description="Expected processing time for the visa application in days")


class FinalizeTravelArrangementsOutput(BaseModel):
    """Pydantic model for finalize_travel_arrangements node outputs."""
    travel_arrangement_status: bool = Field(..., description="Whether all travel arrangements have been successfully finalized")
    flight_confirmation_numbers: List[str] = Field(..., description="List of confirmation numbers for booked flights")
    hotel_confirmation_numbers: List[str] = Field(..., description="List of confirmation numbers for booked hotels")
    car_rental_confirmation_numbers: List[str] = Field(..., description="List of confirmation numbers for booked car rentals")
    visa_application_status: List[str] = Field(..., description="List of status updates for visa applications")
    total_travel_cost: float = Field(..., description="Total cost of all travel arrangements")


def finalize_travel_arrangements(book_flights_input: BookFlightsOutput, book_hotels_input: BookHotelsOutput, book_cars_input: BookCarsOutput, apply_for_visas_input: ApplyForVisasOutput, **kwargs) -> FinalizeTravelArrangementsOutput:
    """Finalize all travel arrangements for the trip

    Args:
        book_flights_input: Input from the 'book_flights' node.
        book_hotels_input: Input from the 'book_hotels' node.
        book_cars_input: Input from the 'book_cars' node.
        apply_for_visas_input: Input from the 'apply_for_visas' node.
        **kwargs: Additional keyword arguments.

    Returns:
        FinalizeTravelArrangementsOutput: Object containing outputs for this node.
    """
    # Retrieve flight details from book_flights output
    flight_details: dict = extract_flight_details(
        flight_data=book_flights_input,
        required_fields=["flight_booking_status", "flight_numbers"]
    )
    
    # Retrieve hotel details from book_hotels output
    hotel_details: dict = extract_hotel_details(
        hotel_data=book_hotels_input,
        required_fields=["booking_status", "hotel_names"]
    )
    
    # Retrieve car rental details from book_cars output
    car_rental_details: dict = extract_car_rental_details(
        car_data=book_cars_input,
        required_fields=["booking_status", "car_rental_details"]
    )
    
    # Retrieve visa application details from apply_for_visas output
    visa_details: dict = extract_visa_details(
        visa_data=apply_for_visas_input,
        required_fields=["visa_application_status", "visa_types_applied_for"]
    )
    
    # Aggregate confirmation numbers from bookings
    flight_confirmation_numbers: List[str] = get_confirmation_numbers(
        booking_type="flight", 
        booking_data=flight_details
    )
    
    hotel_confirmation_numbers: List[str] = get_confirmation_numbers(
        booking_type="hotel", 
        booking_data=hotel_details
    )
    
    car_rental_confirmation_numbers: List[str] = get_confirmation_numbers(
        booking_type="car_rental", 
        booking_data=car_rental_details
    )
    
    # Calculate total travel cost
    total_cost: float = calculate_total_travel_cost(
        hotel_cost=book_hotels_input.total_cost,
        car_rental_cost=book_cars_input.total_cost,
        additional_costs={}
    )
    
    # Determine overall travel arrangement status
    travel_status: bool = determine_travel_arrangement_status(
        flight_status=book_flights_input.flight_booking_status,
        hotel_status=book_hotels_input.booking_status,
        car_rental_status=book_cars_input.booking_status,
        visa_status=apply_for_visas_input.visa_application_status
    )
    
    # Compile visa application status information
    visa_status_info: List[str] = compile_visa_status_info(
        visa_data=apply_for_visas_input
    )
    
    # Return the finalized travel arrangements
    return FinalizeTravelArrangementsOutput(
        travel_arrangement_status=travel_status,
        flight_confirmation_numbers=flight_confirmation_numbers,
        hotel_confirmation_numbers=hotel_confirmation_numbers,
        car_rental_confirmation_numbers=car_rental_confirmation_numbers,
        visa_application_status=visa_status_info,
        total_travel_cost=total_cost
    )
