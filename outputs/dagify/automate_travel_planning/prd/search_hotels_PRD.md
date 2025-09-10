# search_hotels PRD

## Description
Search for hotels at each destination


## Implementation Plan

### 1. Use the output from the 'research_destination_options' node to get the list of potential destinations.

| Category | Details |
| --- | --- |
| **Reason** | The potential destinations are required to search for hotels. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Call the 'research_destination_options' node and retrieve the 'potential_destinations' output. |

### 2. For each potential destination, send a request to a hotel search API (e.g. Expedia, Booking.com) to retrieve a list of available hotels.

| Category | Details |
| --- | --- |
| **Reason** | The hotel search API will provide the necessary information about hotels at each destination. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use the 'requests' library to send a GET request to the hotel search API with the destination as a parameter. |

### 3. Parse the response from the hotel search API to extract the hotel names, locations, prices, and amenities.

| Category | Details |
| --- | --- |
| **Reason** | The response from the API will be in a structured format (e.g. JSON) that needs to be parsed to extract the relevant information. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a JSON parsing library (e.g. 'json') to extract the hotel information from the API response. |

### 4. Store the extracted hotel information in a data structure (e.g. a dictionary or a pandas DataFrame) for further processing.

| Category | Details |
| --- | --- |
| **Reason** | The hotel information needs to be stored in a structured format to be easily accessible and manipulable. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a dictionary or a pandas DataFrame to store the hotel information. |

### 5. Return the list of hotel names, locations, prices, and amenities as the output of the 'search_hotels' node.

| Category | Details |
| --- | --- |
| **Reason** | The output of the 'search_hotels' node is required by the downstream nodes (e.g. 'create_itinerary'). |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return the stored hotel information as a list of dictionaries or a pandas DataFrame. |
