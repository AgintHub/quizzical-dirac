# calculate_rsi PRD

## Description
Calculates the Relative Strength Index (RSI) of a given set of prices over a specified period.


## Implementation Plan

### 1. Implement the RSI calculation using the formula: RSI = 100 - (100 / (1 + RS)), where RS = average gain / average loss over the specified period.

| Category | Details |
| --- | --- |
| **Reason** | The RSI is a widely used technical indicator that measures the magnitude of recent price changes. |
| **Impact** | The calculated RSI value will be used to inform trading decisions. |
| **Complexity** | MEDIUM |
| **Method** | Use a Python library like Pandas to efficiently calculate the average gain and loss over the specified period, then apply the RSI formula. |

### 2. Handle edge cases such as an empty list of prices or a period less than 1.

| Category | Details |
| --- | --- |
| **Reason** | To prevent errors and ensure the function behaves as expected in these scenarios. |
| **Impact** | The function will be robust and able to handle invalid inputs. |
| **Complexity** | LOW |
| **Method** | Add input validation checks at the beginning of the function to raise informative errors for invalid inputs. |

### 3. Consider optimizing the calculation for large lists of prices.

| Category | Details |
| --- | --- |
| **Reason** | To improve performance when dealing with extensive historical price data. |
| **Impact** | The function will be more efficient and scalable. |
| **Complexity** | HIGH |
| **Method** | Explore using vectorized operations or parallel processing techniques to speed up the calculation. |
