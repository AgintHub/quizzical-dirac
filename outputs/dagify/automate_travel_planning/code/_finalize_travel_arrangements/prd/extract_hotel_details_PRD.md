# extract_hotel_details PRD

## Description
Extracts relevant hotel details from the booking output based on required fields.


## Implementation Plan

### 1. Deserialize the input hotel_data from string to a Pydantic model (BookHotelsOutput) to access its attributes.

| Category | Details |
| --- | --- |
| **Reason** | To facilitate easy access to the hotel data attributes. |
| **Impact** | Enables structured data access and manipulation. |
| **Complexity** | LOW |
| **Method** | Use Pydantic's parse_raw or parse_obj method to deserialize the input string into a BookHotelsOutput object. |

### 2. Extract the required fields from the deserialized hotel data and compile them into a dictionary.

| Category | Details |
| --- | --- |
| **Reason** | To provide the necessary hotel details in a structured format. |
| **Impact** | Provides a flexible and structured output that can be easily consumed by downstream nodes. |
| **Complexity** | MEDIUM |
| **Method** | Iterate through the required_fields list, accessing corresponding attributes in the deserialized hotel data, and populate a dictionary with these values. |

### 3. Serialize the extracted hotel details dictionary into a string for output.

| Category | Details |
| --- | --- |
| **Reason** | To conform to the output structure requirement. |
| **Impact** | Ensures compatibility with the expected output format. |
| **Complexity** | LOW |
| **Method** | Use a serialization method such as json.dumps() to convert the dictionary into a string. |
