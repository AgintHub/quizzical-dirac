from ._fetch_market_data.identify_reliable_data_sources import identify_reliable_data_sources
from ._fetch_market_data.select_best_data_source import select_best_data_source
from ._fetch_market_data.fetch_data_from_api import fetch_data_from_api
from ._fetch_market_data.parse_market_prices import parse_market_prices
from ._fetch_market_data.parse_trading_volumes import parse_trading_volumes
from ._fetch_market_data.validate_price_data import validate_price_data
from ._fetch_market_data.validate_volume_data import validate_volume_data
from ._fetch_market_data.store_market_data import store_market_data

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Identify reliable data sources for market data, such as financial APIs (e.g.,
#   Alpha Vantage, Yahoo Finance) or data feeds (e.g., Quandl).
#   Reason: To ensure data accuracy and reliability, it's crucial to select reputable
#           sources.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Research and list potential data sources, evaluate their credibility, and
#           select the most appropriate ones based on the specific
#           requirements of the trading workflow.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement API calls or data feed connections to fetch the latest market
#   prices and trading volumes.
#   Reason: Direct data retrieval is necessary for up-to-date market information.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use HTTP request libraries (e.g., requests in Python) for API calls or
#           relevant libraries for data feeds (e.g., Quandl's Python
#           library). Handle authentication, rate limiting, and error
#           handling appropriately.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Parse the retrieved data into the required format, specifically lists of
#   floats for market prices and lists of integers for trading volumes.
#   Reason: The output needs to conform to the specified data types to be usable by
#           dependent nodes.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use data parsing libraries (e.g., pandas for data manipulation) to convert
#           raw data into the required formats. Implement data cleaning and
#           validation to ensure data integrity.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Implement data storage or caching mechanisms to store fetched market data for
#   potential reuse or debugging purposes.
#   Reason: Having a record of fetched data can be useful for analysis, debugging, and
#           potentially improving the trading workflow.
#   Impact: LOW
#   Complexity: MEDIUM
#   Method: Use databases (e.g., relational databases like MySQL or NoSQL databases
#           like MongoDB) or caching solutions (e.g., Redis) to store the
#           data. Implement data models or schemas as necessary.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Handle errors and exceptions that may occur during data fetching, parsing, or
#   storage, such as network errors, data format issues, or storage failures.
#   Reason: Robust error handling is crucial for maintaining the reliability and
#           stability of the trading workflow.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement try-except blocks and error handling mechanisms for anticipated
#           exceptions. Use logging to track errors and potentially
#           implement retry mechanisms for transient errors.
# -- END PRD --



class FetchMarketDataOutput(BaseModel):
    """Pydantic model for fetch_market_data node outputs."""
    market_prices: List[float] = Field(..., description="Current prices of relevant market assets")
    trading_volumes: List[int] = Field(..., description="Current trading volumes of relevant market assets")


def fetch_market_data(general_input: str, **kwargs) -> FetchMarketDataOutput:
    """Retrieve current market data, including prices and trading volumes.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        FetchMarketDataOutput: Object containing outputs for this node.
    """
    # Identify and select reliable data sources
    data_sources: List[str] = identify_reliable_data_sources(input_criteria=general_input)
    selected_source: str = select_best_data_source(sources=data_sources, requirements=kwargs)
    
    # Fetch market data from selected source
    raw_market_data: dict = fetch_data_from_api(source=selected_source, symbols=general_input)
    
    # Parse and format the retrieved data
    parsed_prices: List[float] = parse_market_prices(raw_data=raw_market_data)
    parsed_volumes: List[int] = parse_trading_volumes(raw_data=raw_market_data)
    
    # Validate and clean the data
    validated_prices: List[float] = validate_price_data(prices=parsed_prices)
    validated_volumes: List[int] = validate_volume_data(volumes=parsed_volumes)
    
    # Store data for caching and debugging
    store_market_data(prices=validated_prices, volumes=validated_volumes, source=selected_source)
    
    return FetchMarketDataOutput(
        market_prices=validated_prices,
        trading_volumes=validated_volumes,
    )