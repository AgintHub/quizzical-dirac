from ._calculate_trading_indicators.calculate_rsi import calculate_rsi
from ._calculate_trading_indicators.calculate_ema import calculate_ema
from ._calculate_trading_indicators.calculate_macd_line import calculate_macd_line
from ._calculate_trading_indicators.calculate_signal_line import calculate_signal_line
from ._calculate_trading_indicators.get_current_macd_value import get_current_macd_value

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Retrieve market prices and trading volumes from the output of the
#   'fetch_market_data' node.
#   Reason: The 'fetch_market_data' node provides the necessary input data for
#           calculating technical indicators.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output of 'fetch_market_data' node, specifically 'market_prices'
#           and 'trading_volumes'.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Calculate the Relative Strength Index (RSI) using the market prices.
#   Reason: RSI is a widely used indicator for identifying overbought or oversold
#           conditions.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Apply the RSI calculation formula: RSI = 100 - (100 / (1 + RS)), where RS =
#           Average Gain / Average Loss. Use a 14-period window for the
#           calculation.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate the Moving Average Convergence Divergence (MACD) using the market
#   prices.
#   Reason: MACD is a trend-following momentum indicator that shows the relationship
#           between two moving averages.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Calculate the 12-period and 26-period Exponential Moving Averages (EMAs) of
#           the market prices. Then, compute MACD = 12-period EMA -
#           26-period EMA. Also, calculate the signal line as a 9-period
#           EMA of the MACD.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Compile the calculated indicators into 'indicator_values' and
#   'indicator_names'.
#   Reason: The output needs to be structured as per the defined output structure.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Create lists for 'indicator_values' and 'indicator_names'. Populate
#           'indicator_names' with the names of the calculated indicators
#           (e.g., 'RSI', 'MACD'). Populate 'indicator_values' with the
#           corresponding calculated values.
# -- END PRD --



class FetchMarketDataOutput(BaseModel):
    """Pydantic model for fetch_market_data node outputs."""
    market_prices: List[float] = Field(..., description="Current prices of relevant market assets")
    trading_volumes: List[int] = Field(..., description="Current trading volumes of relevant market assets")


class CalculateTradingIndicatorsOutput(BaseModel):
    """Pydantic model for calculate_trading_indicators node outputs."""
    indicator_values: List[float] = Field(..., description="Values of calculated technical indicators")
    indicator_names: List[str] = Field(..., description="Names of calculated technical indicators")


def calculate_trading_indicators(fetch_market_data_input: FetchMarketDataOutput, **kwargs) -> CalculateTradingIndicatorsOutput:
    """Calculate technical indicators used in trading decisions.

    Args:
        fetch_market_data_input: Input from the 'fetch_market_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CalculateTradingIndicatorsOutput: Object containing outputs for this node.
    """
    # Retrieve market prices and trading volumes from input
    market_prices: List[float] = fetch_market_data_input.market_prices
    trading_volumes: List[int] = fetch_market_data_input.trading_volumes
    
    # Calculate RSI using 14-period window
    rsi_value: float = calculate_rsi(prices=market_prices, period=14)
    
    # Calculate MACD with 12-period and 26-period EMAs
    ema_12: List[float] = calculate_ema(prices=market_prices, period=12)
    ema_26: List[float] = calculate_ema(prices=market_prices, period=26)
    macd_line: List[float] = calculate_macd_line(ema_12=ema_12, ema_26=ema_26)
    signal_line: List[float] = calculate_signal_line(macd_line=macd_line, period=9)
    current_macd: float = get_current_macd_value(macd_line=macd_line, signal_line=signal_line)
    
    # Compile indicators into output structure
    indicator_names: List[str] = ["RSI", "MACD"]
    indicator_values: List[float] = [rsi_value, current_macd]
    
    return CalculateTradingIndicatorsOutput(
        indicator_values=indicator_values,
        indicator_names=indicator_names
    )