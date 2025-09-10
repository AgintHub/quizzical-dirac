# -- PRD --
# 1. BULLET: Retrieve the car rental details from the output of the create_itinerary node
#   Reason: The create_itinerary node provides the necessary car rental information,
#           including car type, rental agency, and pickup/drop-off details
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a data parsing algorithm to extract the relevant car rental information
#           from the create_itinerary node's output
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the car rental details to ensure they meet the user's requirements
#   Reason: Validation is necessary to ensure that the car rental details meet the
#           user's needs and to prevent any potential issues with the
#           booking
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Implement a validation function that checks the car rental details against
#           the user's requirements, using a rules-based approach
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Use the validated car rental details to book the car rental
#   Reason: Once the car rental details have been validated, they can be used to book
#           the car rental
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Integrate with a car rental booking API to book the car rental, using a
#           secure payment processing system to handle payments
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Add any necessary insurance or equipment upgrades to the car rental booking
#   Reason: Insurance and equipment upgrades may be required or desired by the user,
#           and must be added to the booking accordingly
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use a rules-based approach to determine which insurance and equipment
#           upgrades are required or desired, and add them to the booking
#           using the car rental booking API
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Calculate the total cost of the car rental, including any additional fees or
#   upgrades
#   Reason: The total cost of the car rental must be calculated to ensure that the user
#           is aware of the costs and to prevent any potential issues with
#           payment
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a pricing algorithm to calculate the total cost of the car rental,
#           taking into account any additional fees or upgrades
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Return the car rental booking reference number, car rental details, insurance
#   options, equipment upgrades, total cost, and booking status
#   Reason: The output of the book_cars node must include all relevant information
#           about the car rental booking
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a data formatting algorithm to format the output of the book_cars node,
#           including all relevant information about the car rental booking
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


class BookCarsOutput(BaseModel):
    """Pydantic model for book_cars node outputs."""
    car_rental_booking_reference: str = Field(..., description="Booking reference number for the car rental")
    car_rental_details: List[str] = Field(..., description="List of car rental details, including car type, rental agency, and pickup/drop-off information")
    insurance_options: List[str] = Field(..., description="List of insurance options selected for the car rental")
    equipment_upgrades: List[str] = Field(..., description="List of equipment upgrades selected for the car rental, such as GPS or child seats")
    total_cost: float = Field(..., description="Total cost of the car rental, including any additional fees or upgrades")
    booking_status: bool = Field(..., description="Whether the car rental booking was successful")


def book_cars(create_itinerary_input: CreateItineraryOutput, **kwargs) -> BookCarsOutput:
    """Book car rentals for the trip

    Args:
        create_itinerary_input: Input from the 'create_itinerary' node.
        **kwargs: Additional keyword arguments.

    Returns:
        BookCarsOutput: Object containing outputs for this node.
    """
    # Extract car rental details from create_itinerary output
    car_rental_details: List[str] = extract_car_rental_details(input_data=create_itinerary_input.car_rental_details)
    
    # Validate car rental details against user requirements
    validated_details: List[str] = validate_car_rental_details(car_details=car_rental_details, user_requirements=kwargs.get("user_requirements", {}))
    
    # Determine insurance options based on user preferences and requirements
    insurance_options: List[str] = determine_insurance_options(car_details=validated_details, user_preferences=kwargs.get("insurance_preferences", {}))
    
    # Determine equipment upgrades based on user preferences
    equipment_upgrades: List[str] = determine_equipment_upgrades(car_details=validated_details, user_preferences=kwargs.get("equipment_preferences", {}))
    
    # Book car rental through API
    booking_result: dict = book_car_rental(
        car_details=validated_details,
        insurance_options=insurance_options,
        equipment_upgrades=equipment_upgrades,
        payment_info=kwargs.get("payment_info", {})
    )
    
    # Calculate total cost including all fees and upgrades
    total_cost: float = calculate_total_cost(
        base_rental_cost=booking_result.get("base_cost", 0.0),
        insurance_cost=booking_result.get("insurance_cost", 0.0),
        upgrades_cost=booking_result.get("upgrades_cost", 0.0),
        additional_fees=booking_result.get("additional_fees", 0.0)
    )
    
    # Return output with booking details
    return BookCarsOutput(
        car_rental_booking_reference=booking_result.get("booking_reference", ""),
        car_rental_details=validated_details,
        insurance_options=insurance_options,
        equipment_upgrades=equipment_upgrades,
        total_cost=total_cost,
        booking_status=booking_result.get("booking_status", False),
    )