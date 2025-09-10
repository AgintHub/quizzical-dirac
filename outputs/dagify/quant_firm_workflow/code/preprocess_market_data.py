# -- PRD --
# 1. BULLET: Detect and handle missing values in the market data using imputation
#   techniques such as mean, median, or interpolation
#   Reason: Missing values can affect the accuracy of analysis and modeling, and
#           handling them is crucial for reliable results
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use Pandas library to detect missing values, and apply imputation
#           techniques using Scikit-learn or Pandas built-in functions
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Normalize prices using techniques such as Min-Max Scaler or Standard Scaler
#   to ensure consistency and prevent feature dominance
#   Reason: Normalization ensures that all features are on the same scale, preventing
#           feature dominance and improving model performance
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use Scikit-learn library to apply Min-Max Scaler or Standard Scaler to the
#           price data
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Convert the preprocessed market data into a suitable format for analysis,
#   such as a Pandas DataFrame or CSV file
#   Reason: A suitable format for analysis is necessary for efficient data manipulation
#           and processing
#   Impact: LOW
#   Complexity: LOW
#   Method: Use Pandas library to convert the preprocessed data into a DataFrame or CSV
#           file
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Validate the preprocessed data to ensure that it meets the required criteria
#   for analysis and modeling
#   Reason: Validation ensures that the preprocessed data is accurate, complete, and
#           consistent, and meets the requirements for analysis and
#           modeling
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use data validation techniques such as data profiling, data quality checks,
#           and data visualization to validate the preprocessed data
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CollectMarketDataOutput(BaseModel):
    """Pydantic model for collect_market_data node outputs."""
    market_data: List[float] = Field(..., description="List of market data points, including open, high, low, and close prices")
    data_frequency: str = Field(..., description="Frequency of the market data (e.g. 1-minute, 1-hour, daily)")
    index_symbol: str = Field(..., description="Symbol of the market index (e.g. S&P500)")
    collection_date_range: str = Field(..., description="Date range for which the market data was collected (e.g. 2022-01-01 to 2022-06-30)")
    is_data_valid: bool = Field(..., description="Whether the collected market data is valid and complete")


class PreprocessMarketDataOutput(BaseModel):
    """Pydantic model for preprocess_market_data node outputs."""
    preprocessed_data: str = Field(..., description="The preprocessed market data in a suitable format for analysis")
    handled_missing_values: bool = Field(..., description="Whether missing values have been handled")
    normalized_prices: bool = Field(..., description="Whether prices have been normalized")
    data_format: str = Field(..., description="The format of the preprocessed data (e.g., CSV, Pandas DataFrame)")


def preprocess_market_data(collect_market_data_input: CollectMarketDataOutput, **kwargs) -> PreprocessMarketDataOutput:
    """Clean and preprocess the collected market data

    Args:
        collect_market_data_input: Input from the 'collect_market_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PreprocessMarketDataOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return PreprocessMarketDataOutput(
        preprocessed_data="",
        handled_missing_values=False,
        normalized_prices=False,
        data_format="",
    )