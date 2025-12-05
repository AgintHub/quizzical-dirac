# fetch_regime_indicator_data PRD

## Description
Collect macro‑economic and market‑regime indicators (e.g., VIX, yield curve, PMI).


## Implementation Plan

### 1. Identify regime indicators and their data sources from the `list_data_sources` output.

| Category | Details |
| --- | --- |
| **Reason** | The `list_data_sources` node provides the necessary information about the regime indicators to be fetched, including their source and frequency. This step ensures that we are using the correct indicators and data sources as defined by the user's strategy objectives. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the `data_sources` list from the output of the `list_data_sources` node. Filter for entries that are explicitly related to macro-economic and market-regime indicators. Extract the indicator name and data source details (e.g., provider, ticker). |

### 2. Implement data fetching for each identified regime indicator.

| Category | Details |
| --- | --- |
| **Reason** | Different indicators may require different data fetching methods. Some may be available through APIs, while others might require web scraping or database access. Implementing individual methods increases flexibility and robustness. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each indicator, determine the appropriate data fetching method based on the data source details. Use libraries like `requests` for API calls and `BeautifulSoup` for web scraping. Implement error handling and retry mechanisms for each method. Consider using a data provider library like `yfinance` or `FredPy` for easy data retrieval when appropriate. For Quandl data, use the `quandl` package. For FRED data, use the `fredapi`. |

### 3. Parse the data into a standardized format: Date and value.

| Category | Details |
| --- | --- |
| **Reason** | Data from different sources may be structured differently. Standardizing the data into a single format makes further processing easier and more reliable.  This facilitates alignment with the price data. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a function to parse the data returned from different data fetching methods into a consistent format: a list of (Date, Value) tuples. Handle different date formats and missing value representations appropriately. |

### 4. Align all regime indicator time series to a common calendar.

| Category | Details |
| --- | --- |
| **Reason** | Regime indicators and price data might have different trading calendars (e.g., different holidays). Aligning them to a common calendar ensures that the data is comparable and that features are correctly calculated. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Choose the calendar from the `fetch_price_data` output as the reference calendar. For each regime indicator, resample the time series to the reference calendar, filling missing values using forward fill, and truncating values to start and end dates found from the `fetch_price_data` output.  If the price data's dates are explicitly available as a output (e.g `dates`), use them for alignment. Otherwise, analyze the `fetch_price_data` CSV string representation to extract start and end dates for relevant alignment and padding operations. |

### 5. Create a Pandas DataFrame with 'Date' as the index and one column for each regime indicator. Ensure dates are stored as datetime objects.

| Category | Details |
| --- | --- |
| **Reason** | Pandas DataFrames provide efficient data manipulation and analysis capabilities. Using 'Date' as the index allows for easy time series operations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Pandas DataFrame with the aligned regime indicator data and dates. Ensure the 'Date' column is set as the index and converted to datetime objects. The column names should reflect the indicator names as extracted in the first step. |

### 6. Convert the DataFrame to a CSV string.

| Category | Details |
| --- | --- |
| **Reason** | The final output needs to be a CSV string as specified by the output structure. This format is easy to parse and use in subsequent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the `to_csv()` method of the Pandas DataFrame to convert it to a CSV string. The string should include the header row (column names) and the data rows. Set `index=True` to include the Date as the first column. |
