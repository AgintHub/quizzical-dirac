from ._generate_trading_signals.combine_trend_and_indicator_data import combine_trend_and_indicator_data
from ._generate_trading_signals.apply_trading_rules import apply_trading_rules
from ._generate_trading_signals.filter_signals_by_confidence import filter_signals_by_confidence
from ._generate_trading_signals.extract_signal_types import extract_signal_types
from ._generate_trading_signals.extract_signal_strengths import extract_signal_strengths

from pydantic import BaseModel, Field
from typing import List


class AnalyzeMarketTrendsOutput(BaseModel):
    """Pydantic model for analyze_market_trends node outputs."""
    trend_directions: List[str] = Field(..., description="Directions of identified market trends (up, down, neutral)")
    trend_strengths: List[float] = Field(..., description="Strengths of identified market trends")


class CalculateTradingIndicatorsOutput(BaseModel):
    """Pydantic model for calculate_trading_indicators node outputs."""
    indicator_values: List[float] = Field(..., description="Values of calculated technical indicators")
    indicator_names: List[str] = Field(..., description="Names of calculated technical indicators")


class GenerateTradingSignalsOutput(BaseModel):
    """Pydantic model for generate_trading_signals node outputs."""
    signal_types: List[str] = Field(..., description="Types of generated trading signals (buy, sell, hold)")
    signal_strengths: List[float] = Field(..., description="Strengths or confidence levels of generated trading signals")


def generate_trading_signals(analyze_market_trends_input: AnalyzeMarketTrendsOutput, calculate_trading_indicators_input: CalculateTradingIndicatorsOutput, **kwargs) -> GenerateTradingSignalsOutput:
    """Generate trading signals based on analyzed trends and indicators.

    Args:
        analyze_market_trends_input: Input from the 'analyze_market_trends' node.
        calculate_trading_indicators_input: Input from the 'calculate_trading_indicators' node.
        **kwargs: Additional keyword arguments.

    Returns:
        GenerateTradingSignalsOutput: Object containing outputs for this node.
    """
    # Combine trend and indicator data for signal generation
    combined_data: dict = combine_trend_and_indicator_data(
        trend_directions=analyze_market_trends_input.trend_directions,
        trend_strengths=analyze_market_trends_input.trend_strengths,
        indicator_values=calculate_trading_indicators_input.indicator_values,
        indicator_names=calculate_trading_indicators_input.indicator_names
    )
    
    # Apply trading signal generation rules
    raw_signals: List[dict] = apply_trading_rules(combined_data=combined_data)
    
    # Filter and validate signals based on confidence thresholds
    filtered_signals: List[dict] = filter_signals_by_confidence(
        signals=raw_signals,
        min_confidence=0.6
    )
    
    # Extract signal types and strengths from filtered results
    signal_types: List[str] = extract_signal_types(signals=filtered_signals)
    signal_strengths: List[float] = extract_signal_strengths(signals=filtered_signals)
    
    return GenerateTradingSignalsOutput(
        signal_types=signal_types,
        signal_strengths=signal_strengths
    )