# create_position_sizing_rule PRD

## Description
Generates a position sizing rule string for a trading strategy based on a specified risk tolerance and chosen sizing method.


## Implementation Plan

### 1. Validate input parameters: ensure risk_tolerance can be parsed to a float between 0 and 1 and that method is one of the supported strategies.

| Category | Details |
| --- | --- |
| **Reason** | Prevents invalid or nonsensical inputs from propagating through the strategy. |
| **Impact** | Guarantees downstream nodes receive reliable, well‑typed sizing rules, reducing runtime errors. |
| **Complexity** | LOW |
| **Method** | Use Python type hints and runtime checks (e.g., try/except for float conversion, membership test against a predefined set of methods). |

### 2. Implement the fixed‑fractional sizing logic: compute the allocation as `allocation = risk_tolerance * portfolio_value` and format it into a human‑readable rule string.

| Category | Details |
| --- | --- |
| **Reason** | Fixed‑fractional is the most common method and forms the core use case. |
| **Impact** | Provides traders with a clear, reproducible rule that ties position size directly to risk tolerance. |
| **Complexity** | MEDIUM |
| **Method** | Define a helper function that takes risk_tolerance float and portfolio_value placeholder, then returns a formatted string such as `'Allocate {risk_tolerance*100}% of equity per trade'`. Use f‑strings for readability. |

### 3. Extend support for additional methods (e.g., fixed_capital, volatility_adjusted) by mapping method identifiers to rule templates and incorporating optional parameters.

| Category | Details |
| --- | --- |
| **Reason** | Allows future growth and customization without altering the core interface. |
| **Impact** | Enables flexible strategy design and easier integration with other nodes that may require different sizing conventions. |
| **Complexity** | HIGH |
| **Method** | Create a dispatch dictionary that maps method names to lambda functions or template strings, and allow the function to accept an optional `parameters` JSON that can be passed into the template rendering. Validate these parameters with Pydantic models. |
