# feature_engineering PRD

## Description
Engineer relevant features from the preprocessed market data


## Implementation Plan

### 1. Import necessary libraries and load the preprocessed market data from the parent node

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to access the preprocessed market data and perform feature engineering |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use Python libraries such as Pandas and NumPy to load and manipulate the data |

### 2. Calculate moving averages for different time windows (e.g., 50-day, 200-day)

| Category | Details |
| --- | --- |
| **Reason** | Moving averages are a common technical indicator used to identify trends and patterns in market data |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the Pandas library to calculate moving averages using the `rolling` and `mean` functions |

### 3. Calculate Relative Strength Index (RSI) for different time windows

| Category | Details |
| --- | --- |
| **Reason** | RSI is a popular technical indicator used to measure the magnitude of recent price changes |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the Pandas library to calculate RSI using the `diff` and `rolling` functions |

### 4. Calculate Bollinger Bands for different time windows

| Category | Details |
| --- | --- |
| **Reason** | Bollinger Bands are a technical indicator used to measure volatility and identify potential trading opportunities |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the Pandas library to calculate Bollinger Bands using the `rolling` and `std` functions |

### 5. Engineer other relevant technical indicators (e.g., MACD, Stochastic Oscillator)

| Category | Details |
| --- | --- |
| **Reason** | Other technical indicators can provide additional insights into market trends and patterns |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use Python libraries such as Pandas and NumPy to implement additional technical indicators |

### 6. Store the engineered feature names, values, and descriptions in the output structure

| Category | Details |
| --- | --- |
| **Reason** | This step is necessary to provide the output of the feature engineering process |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use Python dictionaries and lists to store the engineered feature names, values, and descriptions |
