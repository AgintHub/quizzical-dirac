# extract_rental_prices PRD

## Description
Extracts rental prices from the given car rental results.


## Implementation Plan

### 1. Parse the input 'results' to identify the structure and location of rental prices.

| Category | Details |
| --- | --- |
| **Reason** | To accurately extract rental prices, we need to understand the format of the input data. |
| **Impact** | Correct parsing ensures that we can correctly identify and extract rental prices. |
| **Complexity** | MEDIUM |
| **Method** | Use a JSON parsing library to analyze the structure of the input data and locate the rental prices. |

### 2. Return the extracted rental prices as a list of float values.

| Category | Details |
| --- | --- |
| **Reason** | The output needs to be in the specified format (List[float]) to match the expected output structure. |
| **Impact** | Correct output formatting ensures compatibility with downstream processing. |
| **Complexity** | LOW |
| **Method** | Compile the extracted prices into a list and return it as the 'output' field. |
