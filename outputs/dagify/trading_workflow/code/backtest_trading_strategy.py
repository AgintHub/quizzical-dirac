from ._backtest_trading_strategy.validate_strategy_definition import validate_strategy_definition
from ._backtest_trading_strategy.retrieve_historical_price_data import retrieve_historical_price_data
from ._backtest_trading_strategy.simulate_trade_execution import simulate_trade_execution
from ._backtest_trading_strategy.calculate_performance_metrics import calculate_performance_metrics
from ._backtest_trading_strategy.calculate_max_drawdown import calculate_max_drawdown
from ._backtest_trading_strategy.calculate_annualized_return import calculate_annualized_return
from ._backtest_trading_strategy.calculate_sharpe_ratio import calculate_sharpe_ratio
from ._backtest_trading_strategy.generate_performance_summary import generate_performance_summary

from pydantic import BaseModel, Field


# -- PRD --
# 1. BULLET: Extract strategy definition from the parent node's output, ensuring all
#   fields (strategy_name, entry_rules, exit_rules, position_sizing_rule,
#   risk_management_rule, assets_traded) are available for use.
#   Reason: The backtest logic relies on the precise trading rules and asset universe
#           specified by the strategy; missing data would cause incorrect
#           simulation.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Validate presence of each field; use JSON schema validation to assert data
#           types before proceeding.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Retrieve clean historical price data for each asset in assets_traded from the
#   data repository or by invoking collect_historical_market_data, filtering
#   by the timeframes required by the strategy.
#   Reason: Accurate backtesting demands high‑quality, time‑aligned price series; the
#           strategy may depend on specific timeframes.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a data access layer to query the database by ticker and timeframe;
#           apply resampling or interpolation if needed; verify is_clean
#           flag and data_quality_score > 0.8.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Simulate trade execution for the entire historical period by iterating over
#   each time step, applying entry_rules to generate buy or sell signals, and
#   exit_rules to close positions, while respecting position_sizing_rule and
#   risk_management_rule.
#   Reason: This step creates the chronological sequence of trades that will be used to
#           compute performance metrics.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Implement an event‑driven simulator: for each bar, evaluate boolean
#           expressions in entry_rules/exits using the bar's OHLCV data;
#           compute position size using a risk‑based formula; apply
#           stop‑loss and take‑profit logic from risk_management_rule;
#           maintain a list of open positions and update PnL on each step.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate cumulative returns per trade, aggregate them to compute
#   total_return, number_of_trades, win_rate, avg_profit_per_trade,
#   avg_loss_per_trade, and win_loss_ratio.
#   Reason: These core metrics directly reflect the strategy’s profitability and trade
#           quality.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: For each closed trade, compute PnL = (exit_price - entry_price) * quantity;
#           classify as win/loss; use numpy or pandas to aggregate
#           statistics; ensure rounding to 6 decimal places for
#           consistency.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Determine max_drawdown by constructing the equity curve over time, computing
#   rolling peaks, and measuring the largest drop from a peak to a trough.
#   Reason: Drawdown is a key risk metric that captures the worst equity loss
#           experienced during the period.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use cumulative returns to build equity_curve; apply pandas .cummax() to
#           track peaks; compute drawdown = (equity_curve - peaks)/peaks;
#           take the minimum value.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Compute the annualized_return by annualizing the cumulative return based on
#   the number of trading days in the backtesting period and the typical
#   market calendar.
#   Reason: Annualized return allows comparison across strategies with different time
#           horizons.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Annualized = (1 + total_return) ** (252 / total_trading_days) - 1, assuming
#           252 trading days per year.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Calculate Sharpe ratio using the daily excess returns (return minus risk‑free
#   rate) divided by the standard deviation of daily returns, then annualize
#   the result.
#   Reason: Sharpe ratio is a standard risk‑adjusted performance metric.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Set risk_free_rate = 0.0 (or fetch from treasury data); compute
#           daily_excess = daily_return - risk_free_rate; sharpe_daily =
#           mean(daily_excess)/std(daily_excess); annualized_sharpe =
#           sharpe_daily * sqrt(252).
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Generate a concise performance_summary string summarizing the key metrics,
#   formatted for human readability and future reporting.
#   Reason: The summary provides a quick snapshot for stakeholders and is required by
#           the output structure.
#   Impact: LOW
#   Complexity: LOW
#   Method: Template: "{strategy_name} achieved a total return of
#           {total_return*100:.2f}%, an annualized return of
#           {annualized_return*100:.2f}%, max drawdown
#           {max_drawdown*100:.2f}%, Sharpe ratio {sharpe_ratio:.2f}.
#           {number_of_trades} trades were executed with a win rate of
#           {win_rate:.2%}."
# -- END PRD --



class DefineTradingStrategyOutput(BaseModel):
    """Pydantic model for define_trading_strategy node outputs."""
    strategy_name: str = Field(..., description="Descriptive name of the trading strategy")
    entry_rules: str = Field(..., description="Textual description of the conditions that trigger a long or short position")
    exit_rules: str = Field(..., description="Textual description of the conditions that trigger the closure of a position")
    position_sizing_rule: str = Field(..., description="Rule or formula that determines how much capital or how many shares/contracts to trade")
    risk_management_rule: str = Field(..., description="Description of stop\u2011loss levels, max draw\u2011down limits, and portfolio diversification constraints")
    assets_traded: str = Field(..., description="List of asset symbols or identifiers that the strategy is designed to trade")


class BacktestTradingStrategyOutput(BaseModel):
    """Pydantic model for backtest_trading_strategy node outputs."""
    total_return: float = Field(..., description="Total cumulative return of the strategy over the backtesting period.")
    annualized_return: float = Field(..., description="Annualized return of the strategy.")
    max_drawdown: float = Field(..., description="Maximum drawdown observed during backtesting.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the strategy.")
    number_of_trades: int = Field(..., description="Total number of trades executed during backtesting.")
    win_rate: float = Field(..., description="Fraction of profitable trades (value between 0 and 1).")
    avg_profit_per_trade: float = Field(..., description="Average profit per winning trade.")
    avg_loss_per_trade: float = Field(..., description="Average loss per losing trade.")
    win_loss_ratio: float = Field(..., description="Ratio of average profit to average loss.")
    performance_summary: str = Field(..., description="Concise textual summary of backtest results.")


def backtest_trading_strategy(define_trading_strategy_input: DefineTradingStrategyOutput, **kwargs) -> BacktestTradingStrategyOutput:
    """Test the trading strategy on historical data to evaluate performance.

    Args:
        define_trading_strategy_input: Input from the 'define_trading_strategy' node.
        **kwargs: Additional keyword arguments.

    Returns:
        BacktestTradingStrategyOutput: Object containing outputs for this node.
    """
    # Extract and validate strategy definition
    validated_strategy: dict = validate_strategy_definition(
        strategy_input=define_trading_strategy_input
    )
    
    # Retrieve historical price data for all assets
    historical_data: dict = retrieve_historical_price_data(
        assets=validated_strategy['assets_traded'],
        timeframes=validated_strategy['required_timeframes']
    )
    
    # Simulate trade execution over historical period
    trade_results: list = simulate_trade_execution(
        historical_data=historical_data,
        entry_rules=validated_strategy['entry_rules'],
        exit_rules=validated_strategy['exit_rules'],
        position_sizing=validated_strategy['position_sizing_rule'],
        risk_management=validated_strategy['risk_management_rule']
    )
    
    # Calculate performance metrics from trade results
    performance_metrics: dict = calculate_performance_metrics(
        trade_results=trade_results
    )
    
    # Calculate maximum drawdown from equity curve
    max_drawdown: float = calculate_max_drawdown(
        equity_curve=performance_metrics['equity_curve']
    )
    
    # Calculate annualized return
    annualized_return: float = calculate_annualized_return(
        total_return=performance_metrics['total_return'],
        trading_days=performance_metrics['total_trading_days']
    )
    
    # Calculate Sharpe ratio
    sharpe_ratio: float = calculate_sharpe_ratio(
        daily_returns=performance_metrics['daily_returns'],
        risk_free_rate=0.0
    )
    
    # Generate performance summary
    summary: str = generate_performance_summary(
        strategy_name=validated_strategy['strategy_name'],
        metrics={
            'total_return': performance_metrics['total_return'],
            'annualized_return': annualized_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'number_of_trades': performance_metrics['number_of_trades'],
            'win_rate': performance_metrics['win_rate']
        }
    )
    
    return BacktestTradingStrategyOutput(
        total_return=performance_metrics['total_return'],
        annualized_return=annualized_return,
        max_drawdown=max_drawdown,
        sharpe_ratio=sharpe_ratio,
        number_of_trades=performance_metrics['number_of_trades'],
        win_rate=performance_metrics['win_rate'],
        avg_profit_per_trade=performance_metrics['avg_profit_per_trade'],
        avg_loss_per_trade=performance_metrics['avg_loss_per_trade'],
        win_loss_ratio=performance_metrics['win_loss_ratio'],
        performance_summary=summary
    )