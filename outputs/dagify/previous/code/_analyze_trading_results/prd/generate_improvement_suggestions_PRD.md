# generate_improvement_suggestions PRD

## Description
Generate a concise set of improvement suggestions based on win rate, maximum drawdown, and Sharpe ratio.


## Implementation Plan

### 1. Define performance thresholds for win rate, max drawdown, and Sharpe ratio to classify strategy health.

| Category | Details |
| --- | --- |
| **Reason** | Thresholds provide a decision framework for generating relevant suggestions. |
| **Impact** | Ensures the suggestions are tailored to actual performance gaps. |
| **Complexity** | LOW |
| **Method** | Implement simple conditional checks against hardcoded threshold values. |

### 2. Map each performance category to a set of templated improvement suggestions using a lookup dictionary.

| Category | Details |
| --- | --- |
| **Reason** | Allows systematic translation of categories into actionable recommendations. |
| **Impact** | Produces consistent, high‑quality suggestions without manual drafting. |
| **Complexity** | MEDIUM |
| **Method** | Create a dictionary where keys are category identifiers and values are formatted strings; lookup based on evaluated thresholds. |

### 3. Format the final suggestion list as a single comma‑separated string and return it alongside the input parameters.

| Category | Details |
| --- | --- |
| **Reason** | Matches the expected output structure and simplifies downstream parsing. |
| **Impact** | Provides a uniform API response for consuming nodes. |
| **Complexity** | LOW |
| **Method** | Use string.join on the list of suggestions and return the resulting string. |
