from ._analyze_market_trends.handle_missing_values import handle_missing_values
from ._analyze_market_trends.normalize_data import normalize_data
from ._analyze_market_trends.apply_transformation import apply_transformation
from ._analyze_market_trends.apply_statistical_model import apply_statistical_model
from ._analyze_market_trends.determine_trend_direction import determine_trend_direction
from ._analyze_market_trends.determine_trend_strength import determine_trend_strength

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Retrieve historical market data from the output of the 'fetch_market_data'
#   node, specifically using 'market_prices' and 'trading_volumes'.
#   Reason: The historical market data is necessary for analyzing market trends and
#           patterns.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output of 'fetch_market_data' node directly as input for analysis.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Preprocess the retrieved market data by handling missing values, normalizing
#   data, and potentially transforming it (e.g., log transformation for
#   skewed distributions).
#   Reason: Preprocessing ensures the quality and consistency of the data, which is
#           crucial for accurate trend analysis.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Apply data preprocessing techniques such as imputation for missing values,
#           normalization using Min-Max Scaler or Standard Scaler, and
#           transformation if necessary.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Apply statistical models (e.g., ARIMA, Prophet, linear regression) to the
#   preprocessed data to identify trends and patterns.
#   Reason: Statistical models provide a structured approach to analyzing time series
#           data and identifying trends.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use libraries like statsmodels for ARIMA, Prophet for time series
#           forecasting, or scikit-learn for linear regression. Select the
#           most appropriate model based on data characteristics and trend
#           complexity.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Determine the direction (up, down, neutral) and strength of identified trends
#   based on the output of the statistical models.
#   Reason: Trend direction and strength are critical for generating trading signals.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Analyze the slope and confidence intervals of the trend lines or forecasts
#           from the statistical models to determine direction and
#           strength.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Output the trend directions as a list of strings and trend strengths as a
#   list of floats.
#   Reason: The output needs to be in a format that can be easily consumed by the
#           dependent node 'generate_trading_signals'.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Ensure that the output lists are correctly aligned and that the data types
#           match the expected output structure.
# -- END PRD --



class FetchMarketDataOutput(BaseModel):
    """Pydantic model for fetch_market_data node outputs."""
    market_prices: List[float] = Field(..., description="Current prices of relevant market assets")
    trading_volumes: List[int] = Field(..., description="Current trading volumes of relevant market assets")


class AnalyzeMarketTrendsOutput(BaseModel):
    """Pydantic model for analyze_market_trends node outputs."""
    trend_directions: List[str] = Field(..., description="Directions of identified market trends (up, down, neutral)")
    trend_strengths: List[float] = Field(..., description="Strengths of identified market trends")


def analyze_market_trends(fetch_market_data_input: FetchMarketDataOutput, **kwargs) -> AnalyzeMarketTrendsOutput:
    """Analyze market trends using historical data and statistical models.

    Args:
        fetch_market_data_input: Input from the 'fetch_market_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AnalyzeMarketTrendsOutput: Object containing outputs for this node.
    """
    # Retrieve historical market data from input
    market_prices: List[float] = fetch_market_data_input.market_prices
    trading_volumes: List[int] = fetch_market_data_input.trading_volumes
    
    # Preprocess the market data
    cleaned_prices: List[float] = handle_missing_values(data=market_prices)
    cleaned_volumes: List[float] = handle_missing_values(data=[float(v) for v in trading_volumes])
    
    normalized_prices: List[float] = normalize_data(data=cleaned_prices, method="min_max")
    normalized_volumes: List[float] = normalize_data(data=cleaned_volumes, method="min_max")
    
    transformed_prices: List[float] = apply_transformation(data=normalized_prices, transformation="log")
    transformed_volumes: List[float] = apply_transformation(data=normalized_volumes, transformation="log")
    
    # Apply statistical models to identify trends
    price_trend_model: dict = apply_statistical_model(data=transformed_prices, model_type="arima")
    volume_trend_model: dict = apply_statistical_model(data=transformed_volumes, model_type="linear_regression")
    
    # Determine trend directions and strengths
    price_direction: str = determine_trend_direction(model_output=price_trend_model)
    price_strength: float = determine_trend_strength(model_output=price_trend_model)
    
    volume_direction: str = determine_trend_direction(model_output=volume_trend_model)
    volume_strength: float = determine_trend_strength(model_output=volume_trend_model)
    
    # Compile final trend directions and strengths
    trend_directions: List[str] = [price_direction, volume_direction]
    trend_strengths: List[float] = [price_strength, volume_strength]
    
    return AnalyzeMarketTrendsOutput(
        trend_directions=trend_directions,
        trend_strengths=trend_strengths
    )