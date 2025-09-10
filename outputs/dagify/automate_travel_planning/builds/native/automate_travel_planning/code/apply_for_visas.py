# -- PRD --
# 1. BULLET: Extract destination countries and their respective visa requirements from the
#   output of 'check_immigration_requirements' node.
#   Reason: To determine which visas are required for the trip, we need to know the
#           destination countries and their visa requirements.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Parse the 'destination_countries' and 'visa_requirements' fields from the
#           output of 'check_immigration_requirements' node.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Identify the travel dates and itinerary details from the output of
#   'create_itinerary' node.
#   Reason: To apply for the correct type of visa, we need to understand the travel
#           dates and itinerary details.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Extract 'travel_dates' and 'itinerary_id' from the output of
#           'create_itinerary' node and correlate them with the destination
#           countries.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Determine the type of visa required for each destination based on the travel
#   purpose and duration of stay.
#   Reason: Different types of visas (tourist, business, transit) have different
#           requirements and application processes.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the 'visa_requirements' and 'travel_dates' to determine the appropriate
#           visa type for each destination.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Compile the required documentation for the visa application based on the visa
#   type and destination country's requirements.
#   Reason: Each visa type and destination country has specific documentation
#           requirements.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Refer to the 'visa_requirements' and 'required_documentation' guidelines
#           for each destination country to compile the necessary
#           documents.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Submit the visa application through the appropriate channels (online portal,
#   embassy, consulate) and obtain the application reference numbers.
#   Reason: To track the status of the visa application, we need the reference numbers.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the compiled documentation to submit the visa application through the
#           designated channels and record the application reference
#           numbers.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Track the status of the visa application and note the expected processing
#   time.
#   Reason: To inform the traveler about the status and expected timeline for visa
#           approval.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Monitor the visa application status through the provided reference numbers
#           and note the expected processing time as per the visa issuing
#           authority's guidelines.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Compile the final output including the visa application status, types of
#   visas applied for, required documentation, application reference numbers,
#   and expected processing time.
#   Reason: To provide a comprehensive summary of the visa application process for the
#           travel arrangements.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Aggregate the information gathered during the visa application process into
#           the required output fields.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


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


class ApplyForVisasOutput(BaseModel):
    """Pydantic model for apply_for_visas node outputs."""
    visa_application_status: bool = Field(..., description="Whether the visa application has been successfully submitted")
    visa_types_applied_for: str = Field(..., description="List of visa types applied for (e.g., tourist, business, transit)")
    required_documentation: str = Field(..., description="List of required documentation for the visa application (e.g., passport, proof of travel, financial statements)")
    visa_application_reference_numbers: str = Field(..., description="List of reference numbers for the submitted visa applications")
    expected_processing_time: int = Field(..., description="Expected processing time for the visa application in days")


def apply_for_visas(check_immigration_requirements_input: CheckImmigrationRequirementsOutput, create_itinerary_input: CreateItineraryOutput, **kwargs) -> ApplyForVisasOutput:
    """Apply for necessary visas for the trip

    Args:
        check_immigration_requirements_input: Input from the 'check_immigration_requirements' node.
        create_itinerary_input: Input from the 'create_itinerary' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ApplyForVisasOutput: Object containing outputs for this node.
    """
    # Extract destination countries and visa requirements
    countries: List[str] = check_immigration_requirements_input.destination_countries
    visa_requirements: List[str] = check_immigration_requirements_input.visa_requirements
    
    # Extract travel dates and itinerary details
    travel_dates: str = create_itinerary_input.travel_dates
    itinerary_id: str = create_itinerary_input.itinerary_id
    
    # Determine visa types needed based on purpose and duration
    visa_types: str = determine_visa_types(visa_requirements=visa_requirements, 
                                            travel_dates=travel_dates,
                                            countries=countries)
    
    # Compile required documentation for visa applications
    documentation: str = compile_required_documentation(countries=countries,
                                                        visa_requirements=visa_requirements,
                                                        visa_types=visa_types)
    
    # Submit visa applications through appropriate channels
    submission_results: dict = submit_visa_applications(countries=countries,
                                                         visa_types=visa_types,
                                                         documentation=documentation,
                                                         itinerary_id=itinerary_id)
    
    # Get application reference numbers
    reference_numbers: str = extract_reference_numbers(submission_results=submission_results)
    
    # Track application status and processing time
    processing_time: int = estimate_processing_time(countries=countries,
                                                     visa_types=visa_types,
                                                     submission_results=submission_results)
    
    # Check if all applications were submitted successfully
    application_status: bool = check_application_status(submission_results=submission_results)

    return ApplyForVisasOutput(
        visa_application_status=application_status,
        visa_types_applied_for=visa_types,
        required_documentation=documentation,
        visa_application_reference_numbers=reference_numbers,
        expected_processing_time=processing_time,
    )