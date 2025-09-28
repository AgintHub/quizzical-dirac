# -- PRD --
# 1. BULLET: Validate and structure the raw historical data from the parent node into a
#   clean DataFrame, ensuring that each asset's timestamps align with its
#   price values and that there are no missing or NaN entries.
#   Reason: Data integrity is foundational for any reliable strategy definition; any
#           gaps can bias indicator calculations or risk assessments.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use pandas read_csv/merge operations; check len(timestamps) ==
#           len(price_values) for each asset; drop rows with NaNs; convert
#           timestamps to datetime.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Compute descriptive statistics (mean, standard deviation, skewness, kurtosis)
#   for each asset and timeframe to understand volatility, liquidity and tail
#   behavior.
#   Reason: Statistical profiles inform parameter selection for indicators and risk
#           limits.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Apply pandas .describe() and scipy.stats.skew/kurtosis; store results in a
#           metadata dictionary.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Generate a comprehensive set of technical indicators (SMA, EMA, RSI, MACD,
#   ATR, Bollinger Bands) for each asset using the chosen timeframes,
#   ensuring indicator values are aligned with price timestamps.
#   Reason: Indicators provide the quantitative signals that will form the core of
#           entry and exit rules.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Leverage pandas_ta or ta-lib to compute each indicator; add columns to
#           DataFrame; handle lag by forward-filling the first few rows.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Perform a correlation and predictive power analysis between each indicator
#   and future price returns over a sliding window to identify the most
#   statistically significant signals.
#   Reason: Reduces the risk of overfitting by selecting only the signals that
#           historically move the market.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Calculate Pearson/Spearman correlations for each indicator vs. next-period
#           returns; perform a simple cross‑validation split to confirm
#           predictive stability.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Formulate a composite entry rule that combines the top-performing indicators
#   using logical operators (e.g., SMA crossover AND RSI threshold) and
#   includes a minimum volume filter to ensure liquidity.
#   Reason: Combining trend and momentum signals typically yields stronger entry
#           quality than a single indicator.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Encode the rule in a human‑readable string, e.g., "(SMA_20 > SMA_50) AND
#           (RSI_14 < 30) AND (Volume > 1.5×MA_Vol)".
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Design exit rules that incorporate both time‑based (e.g., hold for N days)
#   and price‑based (e.g., take profit 3×ATR, stop‑loss 1×ATR) conditions to
#   capture gains while limiting downside risk.
#   Reason: Clear exit criteria prevent emotional or ad‑hoc trade closures and lock in
#           profitability.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Provide textual description plus numeric formulas; e.g., "TP = entry_price
#           + 3*ATR; SL = entry_price - 1*ATR; close if price >= TP or
#           price <= SL or holding period >= 5 days."
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Specify a position sizing rule using a fixed‑fractional approach where a
#   fixed % of capital is risked per trade, calculated from the stop‑loss
#   distance and account equity.
#   Reason: Consistent position sizing maintains risk uniformity across trades.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Explain rule: "size = (risk_per_trade * equity) / (stop_loss_distance *
#           entry_price)"; include example calculation in the output.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Create a risk_management_rule string that details maximum drawdown limit,
#   stop‑loss per trade, portfolio diversification (e.g., max 5 assets), and
#   any other constraints such as maximum daily loss.
#   Reason: Consolidating risk limits into a single rule facilitates enforcement by the
#           execution engine.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Format as: "Max_drawdown = 20% of equity; Stop_loss = 2% per trade;
#           Diversify across <=5 assets; Max_daily_loss = 5% of equity."
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Filter the assets_traded list from the parent node to include only those with
#   data_quality_score >= 0.8 and average daily volume above a set threshold,
#   ensuring the strategy trades only liquid and reliable instruments.
#   Reason: Trading illiquid or low‑quality data can lead to slippage and execution
#           issues.
#   Impact: LOW
#   Complexity: LOW
#   Method: Apply a boolean mask on the parent output lists; return the filtered list.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Assemble the final strategy dictionary mapping each required output key to
#   its corresponding value, ensuring correct data types (e.g., strings for
#   rules, list for assets).
#   Reason: Matches the node's output schema, allowing downstream nodes to parse the
#           result unambiguously.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use a Python dict: {"strategy_name":..., "entry_rules":...,
#           "exit_rules":..., "position_sizing_rule":...,
#           "risk_management_rule":..., "assets_traded":...} and serialize
#           to JSON if needed.
# -- END PRD --

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


class DefineTradingStrategyOutput(BaseModel):
    """Pydantic model for define_trading_strategy node outputs."""
    strategy_name: str = Field(..., description="Descriptive name of the trading strategy")
    entry_rules: str = Field(..., description="Textual description of the conditions that trigger a long or short position")
    exit_rules: str = Field(..., description="Textual description of the conditions that trigger the closure of a position")
    position_sizing_rule: str = Field(..., description="Rule or formula that determines how much capital or how many shares/contracts to trade")
    risk_management_rule: str = Field(..., description="Description of stop\u2011loss levels, max draw\u2011down limits, and portfolio diversification constraints")
    assets_traded: str = Field(..., description="List of asset symbols or identifiers that the strategy is designed to trade")


def define_trading_strategy(collect_historical_market_data_input: CollectHistoricalMarketDataOutput, **kwargs) -> DefineTradingStrategyOutput:
    """Develop a trading strategy based on analysis of historical data.

    Args:
        collect_historical_market_data_input: Input from the 'collect_historical_market_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineTradingStrategyOutput: Object containing outputs for this node.
    """
    # Validate and structure raw historical data into clean DataFrame
    clean_dataframe = validate_and_structure_data(
        assets=collect_historical_market_data_input.assets,
        timestamps=collect_historical_market_data_input.timestamps,
        price_values=collect_historical_market_data_input.price_values,
        timeframes=collect_historical_market_data_input.timeframes
    )
    
    # Compute descriptive statistics for each asset and timeframe
    statistical_metadata = compute_descriptive_statistics(dataframe=clean_dataframe)
    
    # Generate comprehensive set of technical indicators
    indicators_dataframe = generate_technical_indicators(
        dataframe=clean_dataframe,
        timeframes=collect_historical_market_data_input.timeframes
    )
    
    # Perform correlation and predictive power analysis
    signal_analysis_results = analyze_indicator_predictive_power(
        indicators_df=indicators_dataframe,
        statistical_data=statistical_metadata
    )
    
    # Formulate composite entry rule using top-performing indicators
    entry_rule_string: str = formulate_entry_rules(
        signal_results=signal_analysis_results,
        indicators_df=indicators_dataframe
    )
    
    # Design exit rules with time-based and price-based conditions
    exit_rule_string: str = design_exit_rules(
        indicators_df=indicators_dataframe,
        statistical_data=statistical_metadata
    )
    
    # Specify position sizing rule using fixed-fractional approach
    position_sizing_rule_string: str = create_position_sizing_rule(
        risk_tolerance=0.02,  # 2% risk per trade
        method="fixed_fractional"
    )
    
    # Create comprehensive risk management rule
    risk_management_rule_string: str = create_risk_management_rule(
        max_drawdown=0.20,
        max_assets=5,
        max_daily_loss=0.05
    )
    
    # Filter assets based on data quality and volume thresholds
    filtered_assets: str = filter_tradeable_assets(
        assets=collect_historical_market_data_input.assets,
        data_quality_score=collect_historical_market_data_input.data_quality_score,
        dataframe=clean_dataframe,
        min_quality_threshold=0.8
    )
    
    # Generate strategy name based on characteristics
    strategy_name: str = generate_strategy_name(
        entry_rules=entry_rule_string,
        timeframes=collect_historical_market_data_input.timeframes
    )
    
    # Assemble final strategy dictionary and return
    return DefineTradingStrategyOutput(
        strategy_name=strategy_name,
        entry_rules=entry_rule_string,
        exit_rules=exit_rule_string,
        position_sizing_rule=position_sizing_rule_string,
        risk_management_rule=risk_management_rule_string,
        assets_traded=filtered_assets
    )