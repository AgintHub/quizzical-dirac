from ._collect_historical_market_data.parse_market_data_request import parse_market_data_request
from ._collect_historical_market_data.select_optimal_data_source import select_optimal_data_source
from ._collect_historical_market_data.fetch_raw_market_data import fetch_raw_market_data
from ._collect_historical_market_data.clean_and_validate_market_data import clean_and_validate_market_data
from ._collect_historical_market_data.calculate_data_quality_score import calculate_data_quality_score
from ._collect_historical_market_data.format_market_data_output import format_market_data_output

from pydantic import BaseModel, Field


class CollectHistoricalMarketDataOutput(BaseModel):
    """Pydantic model for collect_historical_market_data node outputs."""
    assets: str = Field(..., description="List of asset tickers collected")
    timeframes: str = Field(..., description="List of timeframes requested")
    timestamps: str = Field(..., description="ISO 8601 timestamps for each data point")
    price_values: float = Field(..., description="Price values corresponding to timestamps and assets in order")
    record_count: int = Field(..., description="Total number of records collected")
    is_clean: bool = Field(..., description="Whether the data has been cleaned and validated")
    source_name: str = Field(..., description="Name of data source or provider")
    data_quality_score: float = Field(..., description="Quality score between 0 and 1")


def collect_historical_market_data(general_input: str, **kwargs) -> CollectHistoricalMarketDataOutput:
    """Gather historical market data for analysis and strategy development.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        CollectHistoricalMarketDataOutput: Object containing outputs for this node.
    """
    # Parse input parameters to extract asset tickers and timeframes
    parsed_params: dict = parse_market_data_request(input_string=general_input, kwargs=kwargs)
    
    # Determine the best data source for the requested assets
    data_source: str = select_optimal_data_source(assets=parsed_params["assets"])
    
    # Fetch raw historical market data from the selected source
    raw_data: dict = fetch_raw_market_data(
        assets=parsed_params["assets"],
        timeframes=parsed_params["timeframes"],
        source=data_source
    )
    
    # Clean and validate the collected data
    cleaned_data: dict = clean_and_validate_market_data(raw_data=raw_data)
    
    # Calculate data quality metrics
    quality_score: float = calculate_data_quality_score(data=cleaned_data)
    
    # Format the data for output
    formatted_output: dict = format_market_data_output(data=cleaned_data)
    
    return CollectHistoricalMarketDataOutput(
        assets=formatted_output["assets"],
        timeframes=formatted_output["timeframes"],
        timestamps=formatted_output["timestamps"],
        price_values=formatted_output["price_values"],
        record_count=formatted_output["record_count"],
        is_clean=cleaned_data["is_clean"],
        source_name=data_source,
        data_quality_score=quality_score
    )