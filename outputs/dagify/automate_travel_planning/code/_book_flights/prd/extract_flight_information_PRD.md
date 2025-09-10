# extract_flight_information PRD

## Description
Extracts relevant flight information from the parsed flight details for further processing.


## Implementation Plan

### 1. The shim will parse the input string into a dictionary or a structured format to extract relevant flight information.

| Category | Details |
| --- | --- |
| **Reason** | This is necessary to access and manipulate the flight details contained within the input string. |
| **Impact** | Successful parsing will enable the extraction of required flight information, which is crucial for booking flights. |
| **Complexity** | MEDIUM |
| **Method** | Use a parsing library such as JSON or XML parser depending on the input format, or implement a custom parser if the format is proprietary. |

### 2. The shim will identify and extract specific flight details such as flight numbers, departure and arrival times, and airlines.

| Category | Details |
| --- | --- |
| **Reason** | These details are necessary for booking flights and generating the flight itinerary. |
| **Impact** | Accurate extraction of flight details will directly affect the success of the flight booking process and the quality of the generated itinerary. |
| **Complexity** | HIGH |
| **Method** | Implement a robust data extraction algorithm that can handle various input formats and potential discrepancies in the data. |

### 3. The shim will return the extracted flight information in a structured format (List[dict]) for further processing.

| Category | Details |
| --- | --- |
| **Reason** | This format is required for compatibility with downstream processes such as booking flights through an API. |
| **Impact** | Proper formatting ensures seamless integration with subsequent steps in the workflow. |
| **Complexity** | LOW |
| **Method** | Use standard data structures (e.g., List[dict]) and ensure that the data is correctly populated with the extracted flight information. |
