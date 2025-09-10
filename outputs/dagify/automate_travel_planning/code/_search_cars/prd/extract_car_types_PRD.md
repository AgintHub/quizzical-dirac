# extract_car_types PRD

## Description
A shim function that extracts car types from a list of car rental results.


## Implementation Plan

### 1. Parse the input string into a list of dictionaries representing car rental results.

| Category | Details |
| --- | --- |
| **Reason** | The input is a string representation of a list of dictionaries, and we need to access the data within. |
| **Impact** | Allows the function to process the input data correctly. |
| **Complexity** | MEDIUM |
| **Method** | Use a JSON parsing library to convert the input string into a Python list of dictionaries. |

### 2. Extract car types from the parsed list of dictionaries.

| Category | Details |
| --- | --- |
| **Reason** | The primary function of this shim is to identify and return the car types available in the rental results. |
| **Impact** | Provides the necessary car type information for further processing. |
| **Complexity** | LOW |
| **Method** | Iterate through the list of dictionaries, accessing the relevant key (e.g., 'car_type') to extract the car types. |

### 3. Handle cases where the input data is malformed or missing required information.

| Category | Details |
| --- | --- |
| **Reason** | To ensure the function's robustness and prevent errors when dealing with unexpected input. |
| **Impact** | Enhances the reliability and stability of the function. |
| **Complexity** | HIGH |
| **Method** | Implement error handling to catch and manage exceptions related to JSON parsing errors or missing keys in the dictionaries. |
