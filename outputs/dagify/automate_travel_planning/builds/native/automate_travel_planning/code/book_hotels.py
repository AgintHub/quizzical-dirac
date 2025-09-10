# -- PRD --
# 1. BULLET: Retrieve the list of selected hotels from the create_itinerary node
#   Reason: The create_itinerary node provides the list of selected hotels based on the
#           trip's objectives and destination options
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use API calls to retrieve the list of selected hotels from the
#           create_itinerary node
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Loop through each selected hotel and retrieve its details, including room
#   types and availability
#   Reason: Hotel details are necessary to book the hotel and provide the user with the
#           most up-to-date information
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use hotel APIs to retrieve hotel details, including room types and
#           availability
# 
# -----------------------------------------------------------------------------
# 3. BULLET: For each hotel, check if the desired room type is available and book the room
#   if available
#   Reason: Booking the hotel room is the primary objective of this node
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use hotel APIs to check room availability and book the room if available
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate the total cost of all hotel bookings
#   Reason: The total cost is necessary to provide the user with the overall cost of
#           the trip
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Sum the costs of each hotel booking
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Return the list of booked hotel names, room types, check-in and check-out
#   dates, total cost, and booking status
#   Reason: The output structure is necessary to provide the user with the most up-to-
#           date information about their hotel bookings
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the retrieved and calculated data to create the output structure
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


class BookHotelsOutput(BaseModel):
    """Pydantic model for book_hotels node outputs."""
    hotel_names: List[str] = Field(..., description="List of booked hotel names")
    room_types: List[str] = Field(..., description="List of room types booked")
    check_in_dates: List[str] = Field(..., description="List of check-in dates for each hotel")
    check_out_dates: List[str] = Field(..., description="List of check-out dates for each hotel")
    total_cost: float = Field(..., description="Total cost of all hotel bookings")
    booking_status: bool = Field(..., description="Whether the hotel booking was successful")


def book_hotels(create_itinerary_input: CreateItineraryOutput, **kwargs) -> BookHotelsOutput:
    """Book hotels for the trip

    Args:
        create_itinerary_input: Input from the 'create_itinerary' node.
        **kwargs: Additional keyword arguments.

    Returns:
        BookHotelsOutput: Object containing outputs for this node.
    """
    # Retrieve the list of selected hotels from the create_itinerary node
    selected_hotels: List[dict] = extract_selected_hotels(hotel_reservations=create_itinerary_input.hotel_reservations)
    
    # Initialize output lists
    hotel_names: List[str] = []
    room_types: List[str] = []
    check_in_dates: List[str] = []
    check_out_dates: List[str] = []
    total_cost: float = 0.0
    all_bookings_successful: bool = True
    
    # Loop through each selected hotel and book it
    for hotel in selected_hotels:
        # Retrieve hotel details, including room types and availability
        hotel_details: dict = retrieve_hotel_details(hotel_id=hotel["id"])
        
        # Check if the desired room type is available
        available: bool = check_room_availability(
            hotel_id=hotel["id"],
            room_type=hotel["room_type"],
            check_in=hotel["check_in"],
            check_out=hotel["check_out"]
        )
        
        if available:
            # Book the room if available
            booking_result: dict = book_hotel_room(
                hotel_id=hotel["id"],
                room_type=hotel["room_type"],
                check_in=hotel["check_in"],
                check_out=hotel["check_out"]
            )
            
            if booking_result["success"]:
                # Add booking details to output lists
                hotel_names.append(hotel_details["name"])
                room_types.append(hotel["room_type"])
                check_in_dates.append(hotel["check_in"])
                check_out_dates.append(hotel["check_out"])
                
                # Add cost to total
                total_cost += booking_result["cost"]
            else:
                all_bookings_successful = False
        else:
            all_bookings_successful = False
    
    # Calculate the total cost of all hotel bookings
    final_total_cost: float = calculate_total_cost(costs=[booking["cost"] for booking in selected_hotels if booking.get("success", False)])
    
    # Return the output
    return BookHotelsOutput(
        hotel_names=hotel_names,
        room_types=room_types,
        check_in_dates=check_in_dates,
        check_out_dates=check_out_dates,
        total_cost=total_cost,
        booking_status=all_bookings_successful,
    )