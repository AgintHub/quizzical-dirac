# calculate_ema PRD

## Description
Calculates the Exponential Moving Average (EMA) of a given list of prices over a specified period.


## Implementation Plan

### 1. The shim function will take in a string of prices and a period, parse them into appropriate formats, and then calculate the EMA.

| Category | Details |
| --- | --- |
| **Reason** | To provide a flexible input interface that can handle different data formats. |
| **Impact** | Allows for easier integration with various data sources. |
| **Complexity** | MEDIUM |
| **Method** | Use a parsing library to convert input strings into numerical values, then apply the EMA formula. |

### 2. The EMA calculation will be performed using the parsed prices and period.

| Category | Details |
| --- | --- |
| **Reason** | To compute the EMA as required by the trading indicators calculation. |
| **Impact** | Enables the calculation of MACD and other indicators that rely on EMA. |
| **Complexity** | HIGH |
| **Method** | Implement the EMA algorithm using a loop that iteratively calculates the EMA for each period, using the previous EMA value and the current price. |

### 3. The output will be a list of float values representing the EMA over the specified period.

| Category | Details |
| --- | --- |
| **Reason** | To provide the calculated EMA values in a usable format for further analysis. |
| **Impact** | Facilitates the use of EMA in subsequent calculations like MACD. |
| **Complexity** | LOW |
| **Method** | Return the calculated EMA values as a list of floats. |
