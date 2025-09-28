# -- PRD --
# 1. BULLET: Retrieve the output fields from the collect_order_book_data node.
#   Reason: This is necessary to get the historical data required for generating
#           trading signals.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use the DAG's API to fetch the output fields from the
#           collect_order_book_data node.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Parse the instrument_symbols, best_bid_prices, and best_ask_prices from the
#   collect_order_book_data node's output.
#   Reason: These fields are required for generating trading signals.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a data parsing library to extract the required fields from the
#           collect_order_book_data node's output.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate the RSI for each instrument's best_bid_prices and best_ask_prices.
#   Reason: This is a common technical indicator for determining trading signals.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a technical indicator library to calculate the RSI for each
#           instrument's best_bid_prices and best_ask_prices.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Compare the RSI values with other technical indicators to generate trading
#   signals.
#   Reason: This is necessary to determine the strength of the trading signals.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a trading signal generation algorithm to compare the RSI values with
#           other technical indicators.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Package the generated trading signals into the specified output fields.
#   Reason: This is necessary to provide the trading signals in the required format.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use the DAG's API to package the generated trading signals into the
#           specified output fields.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CollectOrderBookDataOutput(BaseModel):
    """Pydantic model for collect_order_book_data node outputs."""
    instrument_symbols: List[str] = Field(..., description="List of instrument symbols")
    best_bid_prices: List[float] = Field(..., description="Bid prices for each instrument (in order)")
    best_ask_prices: List[float] = Field(..., description="Ask prices for each instrument (in order)")
    total_volume: float = Field(..., description="Total volume across all instruments")
    is_data_collection_successful: bool = Field(..., description="Whether data collection was successful")


class GenerateTradingSignalsOutput(BaseModel):
    """Pydantic model for generate_trading_signals node outputs."""
    instrument_symbols_to_buy: List[str] = Field(..., description="List of instrument symbols to buy")
    instrument_symbols_to_sell: List[str] = Field(..., description="List of instrument symbols to sell")
    buy_signals: List[float] = Field(..., description="Signal strength for buy trades (same order as instrument_symbols_to_buy)")
    sell_signals: List[float] = Field(..., description="Signal strength for sell trades (same order as instrument_symbols_to_sell)")


def generate_trading_signals(collect_order_book_data_input: CollectOrderBookDataOutput, **kwargs) -> GenerateTradingSignalsOutput:
    """Use historical data to generate trading signals based on trends, RSI, and other technical indicators.

    Args:
        collect_order_book_data_input: Input from the 'collect_order_book_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        GenerateTradingSignalsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return GenerateTradingSignalsOutput(
        instrument_symbols_to_buy=[],
        instrument_symbols_to_sell=[],
        buy_signals=[],
        sell_signals=[],
    )