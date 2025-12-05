# list_data_sources PRD

## Description
Identify all external datasets required for price action, cross‑asset correlation, regime detection, and volatility forecasting.


## Implementation Plan

### 1. Define a dictionary of potential data sources categorized by the analysis they support (price action, cross-asset correlation, regime detection, volatility forecasting). This will act as a knowledge base for required datasets.

| Category | Details |
| --- | --- |
| **Reason** | Provides a structured way to identify the necessary data sources based on the strategy's requirements. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python dictionary where keys are categories ('price_action', 'cross_asset', 'regime_detection', 'volatility_forecasting') and values are lists of potential data sources with provider information. EXAMPLE: {'price_action': [{'dataset': 'Price History', 'provider': 'Bloomberg', 'frequency': 'daily'}]} |

### 2. Access the 'define_strategy_objectives' node's output, specifically the 'asset_universe' and the 'primary_tradable_asset' fields.

| Category | Details |
| --- | --- |
| **Reason** | The asset universe dictates which cross-asset data will be considered and the primary tradable asset is the focus of price action and volatility analysis. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Retrieve the 'asset_universe' (LIST_STR) and 'primary_tradable_asset' (STR) output variables from the 'define_strategy_objectives' node. |

### 3. Based on the 'primary_tradable_asset', identify the primary data source for price history.

| Category | Details |
| --- | --- |
| **Reason** | Price history is fundamental. The selected asset determines the specific data source required. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'price_action'. Select the 'Price History' source and tailor it to the 'primary_tradable_asset'. Generate string output 'Price History: [Provider], [Frequency]' (e.g. 'Price History: Bloomberg, daily'). |

### 4. For each asset in 'asset_universe' *other* than the primary asset, identify appropriate providers of price data for computing cross-asset correlations.

| Category | Details |
| --- | --- |
| **Reason** | Cross-asset correlation requires price data for each asset under consideration within the strategy. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate through the 'asset_universe', excluding the 'primary_tradable_asset'.  For each secondary asset, check under cross_asset in the data souce dictionary for price data options. Generate strings of the format 'Price History for [Asset]: [Provider], [Frequency]' (e.g., 'Price History for SPY: Yahoo Finance, daily'). |

### 5. Identify data sources for regime indicators necessary for regime detection. Commonly used indicators include VIX, yield curve data, and PMI.

| Category | Details |
| --- | --- |
| **Reason** | Regime detection relies on macro-economic and market indicators. Accessing these data sources is essential. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'regime_detection'. Generate strings for each indicator of the format '[Indicator Name]: [Provider], [Frequency]' (e.g., 'VIX: CBOE, daily', 'US 10Y-2Y Yield Spread: FRED, daily', 'PMI: ISM, monthly'). |

### 6. Identify data sources for volatility forecasting, including implied volatility indices and potentially realized volatility data (if available).

| Category | Details |
| --- | --- |
| **Reason** | Volatility forecasting requires volatility data.  Having sources defined beforehand expedites retrieval. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'volatility_forecasting'. Generate strings for each source of the format '[Dataset Name]: [Provider], [Frequency]' (e.g., 'VIX: CBOE, daily', 'Realized Volatility: Bloomberg, daily'). |

### 7. Compile all identified data source strings into a single list, ensuring no duplicates. This list will be assigned to the 'data_sources' output variable.

| Category | Details |
| --- | --- |
| **Reason** | A unified list promotes efficient data retrieval in subsequent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python list. Append the data source string from price history, cross-asset price data, regime indicators, and volatility data while removing duplicates. Assign generated list to 'data_sources'. |
