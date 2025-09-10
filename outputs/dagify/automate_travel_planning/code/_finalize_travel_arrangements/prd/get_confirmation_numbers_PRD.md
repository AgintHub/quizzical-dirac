# get_confirmation_numbers PRD

## Description
Retrieves confirmation numbers for various booking types based on the provided booking data.


## Implementation Plan

### 1. Implement a function that accepts booking type and booking data as inputs and returns a list of confirmation numbers.

| Category | Details |
| --- | --- |
| **Reason** | This is necessary to aggregate confirmation numbers from different booking sources (flights, hotels, car rentals) in a standardized way. |
| **Impact** | This allows for a unified handling of confirmation numbers across different travel arrangements, simplifying the finalize travel arrangements process. |
| **Complexity** | MEDIUM |
| **Method** | Use a switch or if-else statement to determine the booking type and then apply the appropriate logic to extract or generate confirmation numbers from the booking data. The booking data may need to be parsed or processed to extract relevant information. |

### 2. Handle different booking data formats for various booking types.

| Category | Details |
| --- | --- |
| **Reason** | Different booking sources (flights, hotels, car rentals) may provide data in different formats, requiring flexible handling to extract confirmation numbers. |
| **Impact** | This ensures that the function can work with data from various sources, making it versatile and robust. |
| **Complexity** | HIGH |
| **Method** | Implement data parsing logic that can handle different data formats. This could involve using adapters or parsers for each booking type or developing a generic parsing mechanism that can adapt to different data structures. |

### 3. Return confirmation numbers in a standardized format.

| Category | Details |
| --- | --- |
| **Reason** | To ensure consistency in the output, regardless of the booking type or data format. |
| **Impact** | This simplifies downstream processing by providing a consistent output format for further use. |
| **Complexity** | LOW |
| **Method** | Ensure that the output is always a list of strings, representing the confirmation numbers. This may involve converting numbers to strings or formatting the output in a specific way. |
