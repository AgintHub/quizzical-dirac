# analyze_softness_levels PRD

## Description
Analyze the softness levels of different toilet paper brands.


## Implementation Plan

### 1. Retrieve the list of top toilet paper brand names and their corresponding softness levels from the output of the 'gather_toilet_paper_data' node.

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to obtain the required data for analysis. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use the output of the 'gather_toilet_paper_data' node, specifically the 'brand_names' and 'softness_levels' fields. |

### 2. Sort the toilet paper brands by their softness levels in descending order.

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to rank the brands from softest to least soft. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use a sorting algorithm, such as quicksort or mergesort, to sort the brands by their softness levels. |

### 3. Create a ranked list of toilet paper brands by softness level, with the softest brand first.

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to provide a clear ranking of the brands. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the sorted list of brands to create a new list with the brand names and their corresponding softness levels. |

### 4. Calculate the average softness level of all toilet paper brands.

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to provide a summary of the analysis. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use the list of softness levels to calculate the average value. |

### 5. Create a summary of the analysis, including key findings, such as the softest and least soft brands.

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to provide a clear summary of the analysis. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the ranked list of brands and the average softness level to create a summary of the analysis. |
