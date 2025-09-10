# -- PRD --
# 1. BULLET: Retrieve cleaned and processed stock data from the output of the
#   `clean_and_process_stock_data` node.
#   Reason: The `clean_and_process_stock_data` node provides the necessary input data
#           for calculating stock metrics.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use the output of `clean_and_process_stock_data` node as input
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Calculate daily returns for each stock using the formula: `(current_price -
#   previous_price) / previous_price`.
#   Reason: Daily returns are a key metric for analyzing stock performance.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use pandas library to calculate daily returns
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate volatility (standard deviation of returns) for each stock using a
#   30-day window.
#   Reason: Volatility is a key metric for analyzing stock risk.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use pandas library to calculate standard deviation of returns
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate 50-day and 200-day moving averages for each stock using the
#   formula: `moving_average = (sum(prices) / number_of_days)`.
#   Reason: Moving averages are a key metric for analyzing stock trends.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use pandas library to calculate moving averages
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Store the calculated metrics in the output structure.
#   Reason: The calculated metrics need to be stored in a structured format for
#           downstream use.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a dictionary to store the calculated metrics
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CleanAndProcessStockDataOutput(BaseModel):
    """Pydantic model for clean_and_process_stock_data node outputs."""
    cleaned_data: List[float] = Field(..., description="List of cleaned stock prices")
    processed_data: List[float] = Field(..., description="List of processed stock prices with normalized values")
    date_formats: str = Field(..., description="List of date formats used for conversion")
    missing_value_handling_status: bool = Field(..., description="Whether missing values were handled successfully")


class CalculateStockMetricsOutput(BaseModel):
    """Pydantic model for calculate_stock_metrics node outputs."""
    stock_metrics: List[str] = Field(..., description="List of stock symbols with calculated metrics")
    daily_returns: List[float] = Field(..., description="List of daily returns for each stock")
    volatility: List[float] = Field(..., description="List of volatility (standard deviation of returns) for each stock")
    moving_averages_50_day: List[float] = Field(..., description="List of 50-day moving averages for each stock")
    moving_averages_200_day: List[float] = Field(..., description="List of 200-day moving averages for each stock")


def calculate_stock_metrics(clean_and_process_stock_data_input: CleanAndProcessStockDataOutput, **kwargs) -> CalculateStockMetricsOutput:
    """Calculate key metrics for each stock, such as daily returns and volatility.

    Args:
        clean_and_process_stock_data_input: Input from the 'clean_and_process_stock_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CalculateStockMetricsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return CalculateStockMetricsOutput(
        stock_metrics=[],
        daily_returns=[],
        volatility=[],
        moving_averages_50_day=[],
        moving_averages_200_day=[],
    )