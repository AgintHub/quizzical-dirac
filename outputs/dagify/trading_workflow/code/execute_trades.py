from ._execute_trades.validate_trading_signals import validate_trading_signals
from ._execute_trades.check_market_conditions import check_market_conditions
from ._execute_trades.get_trading_constraints import get_trading_constraints
from ._execute_trades.filter_executable_signals import filter_executable_signals
from ._execute_trades.execute_trade_orders import execute_trade_orders
from ._execute_trades.extract_trade_outcomes import extract_trade_outcomes
from ._execute_trades.format_trade_details import format_trade_details

from pydantic import BaseModel, Field
from typing import List


class GenerateTradingSignalsOutput(BaseModel):
    """Pydantic model for generate_trading_signals node outputs."""
    signal_types: List[str] = Field(..., description="Types of generated trading signals (buy, sell, hold)")
    signal_strengths: List[float] = Field(..., description="Strengths or confidence levels of generated trading signals")


class ExecuteTradesOutput(BaseModel):
    """Pydantic model for execute_trades node outputs."""
    trade_outcomes: List[str] = Field(..., description="Outcomes of executed trades (success, failure, partial fill)")
    trade_details: List[str] = Field(..., description="Details of executed trades, including size, price, and timing")


def execute_trades(generate_trading_signals_input: GenerateTradingSignalsOutput, **kwargs) -> ExecuteTradesOutput:
    """Execute trades based on generated trading signals.

    Args:
        generate_trading_signals_input: Input from the 'generate_trading_signals' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ExecuteTradesOutput: Object containing outputs for this node.
    """
    # Validate and prepare trading signals for execution
    validated_signals: List[dict] = validate_trading_signals(
        signal_types=generate_trading_signals_input.signal_types,
        signal_strengths=generate_trading_signals_input.signal_strengths
    )
    
    # Check market conditions and trading constraints
    market_status: dict = check_market_conditions()
    trading_constraints: dict = get_trading_constraints(**kwargs)
    
    # Filter signals based on market conditions and constraints
    executable_signals: List[dict] = filter_executable_signals(
        signals=validated_signals,
        market_status=market_status,
        constraints=trading_constraints
    )
    
    # Execute trades for each valid signal
    execution_results: List[dict] = execute_trade_orders(
        signals=executable_signals,
        market_conditions=market_status
    )
    
    # Process execution results and extract outcomes
    trade_outcomes: List[str] = extract_trade_outcomes(results=execution_results)
    trade_details: List[str] = format_trade_details(results=execution_results)
    
    return ExecuteTradesOutput(
        trade_outcomes=trade_outcomes,
        trade_details=trade_details,
    )