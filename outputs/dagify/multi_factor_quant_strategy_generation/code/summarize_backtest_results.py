# -- PRD --
# 1. BULLET: Parse the `equity_curve_csv` output from the `run_backtest` node into a
#   pandas DataFrame.
#   Reason: Pandas DataFrames are well-suited for time series analysis and calculation
#           of performance metrics.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `pandas.read_csv()` with the `Date` column as the index and parse the
#           'Date' column as datetime objects. Handle potential errors
#           (e.g., invalid date formats) gracefully using try-except blocks
#           and logging any issues.  The expected columns are 'Date' and
#           'Equity'.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Calculate daily returns from the equity curve.
#   Reason: Daily returns are needed to calculate the Sharpe ratio and generate the
#           histogram of returns.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `equity_curve['Equity'].pct_change()` to compute the daily returns.
#           Handle the first `NaN` value (resulting from the percentage
#           change) by filling it with zero or dropping it, depending if
#           the backtest start at equity zero or not.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate the annualized return.
#   Reason: Annualized return is a standard performance metric for evaluating trading
#           strategies.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Calculate the total return over the backtest period.  Then, annualize it
#           using the formula: `(1 + total_return)**(252 /
#           number_of_trading_days) - 1`. 252 is the average number of
#           trading days in a year. Use `len(equity_curve)` to accurately
#           count the trading days.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate the Sharpe ratio.
#   Reason: The Sharpe ratio measures risk-adjusted return.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Sharpe Ratio is calculated as: Annualized Return / Annualized Volatility.
#           Where Annualized Volatility is the standard deviation of the
#           returns multiplied by the square root of 252 (trading days in a
#           year).  Use `daily_returns.std() * np.sqrt(252)` to get the
#           annualized volatility.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Calculate the maximum drawdown.
#   Reason: Max drawdown indicates the largest peak-to-trough decline during the
#           backtest period and assesses risk.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Calculate the cumulative maximum equity value up to each point in time
#           using `equity_curve['Equity'].cummax()`.  Then, calculate the
#           drawdown as the percentage difference between the cumulative
#           maximum and the current equity value: `(equity_curve['Equity']
#           - cumulative_max) / cumulative_max`.  The maximum drawdown is
#           the minimum (most negative) value of the drawdown series.
#           Return the max drawdown as a negative number.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Parse the `trades_log_csv` output from the `run_backtest` node into a pandas
#   DataFrame.
#   Reason: The trades log is necessary to determine when to measure turnover. Also
#           need to extract trade direction for win/loss calculation.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Read the `trades_log_csv` string into a pandas DataFrame using
#           `pd.read_csv()`.  Ensure the 'Date' column is parsed as dates.
#           The expected columns are 'Date', 'Symbol', 'Quantity', 'Price',
#           and 'PnL'. Implement error handling in case the data is
#           malformed.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Calculate portfolio turnover. Assume a 1 month turnover period.
#   Reason: Turnover indicates how frequently the portfolio is rebalanced.
#   Impact: MEDIUM
#   Complexity: HIGH
#   Method: First, the total value traded each month must be computed. Then, divide
#           that by the average portfolio value for the month. Average
#           these monthly turnover values to get overall portfolio
#           turnover.  This requires calculating the portfolio value at the
#           end of each day from `equity_curve_csv`, finding the trade
#           values from `trades_log_csv`, and correctly aggregating
#           turnover for each monthly period. Use resample('M') to group
#           trades into monthly buckets. Implment handling for division by
#           zero (when the average portfolio value is zero). The `turnover`
#           output should represent the average monthly turnover, expressed
#           as a decimal. E.g., 0.30 for 30% turnover per month.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Calculate the win rate.
#   Reason: Win rate is calculated by checking how many trades had a positive return.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Extract the PnL and check how many values are positive using boolean
#           indexing into Pandas.  Calculate the win rate as the number of
#           winning trades divided by the total number of trades.
#           `trades_log['PnL'] > 0 `. Return as fraction from 0 to 1.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Generate a description of histogram for daily returns.
#   Reason: Used to visualize return distribution.
#   Impact: MEDIUM
#   Complexity: HIGH
#   Method: Generate a histogram of daily returns using `matplotlib.pyplot.hist()`.
#           Analyze the histogram to identify skewness, kurtosis, and the
#           presence of outliers.  Write a markdown description summarizing
#           these observations. The description should include: general
#           shape of the distribution (normal, skewed), location of the
#           mean return, presence of outliers. Store the generated string
#           in the `histogram_description` output.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Generate a description for the turnover time series chart.
#   Reason: Used to visualize trading activity.
#   Impact: MEDIUM
#   Complexity: HIGH
#   Method: The turnover has already been calculated on a monthly basis. Output the
#           turnover values on a time series (`turnover_ts`). Write a
#           markdown description highlighting any trends (increasing,
#           decreasing, stable), spikes, or seasonality in the turnover.
#           Analyze the relationship between turnover and strategy
#           performance. Store the generated markdown string in the
#           `turnover_chart_description` output.
# 
# -----------------------------------------------------------------------------
# 11. BULLET: Create a markdown report.
#   Reason: Consolidates the statistics and chart descriptions for easy readability and
#           integration with downstream nodes.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Combine the calculated statistics (annualized return, Sharpe ratio, max
#           drawdown, turnover, win rate) and the chart descriptions
#           (`histogram_description`, `turnover_chart_description`) into a
#           markdown report. Use markdown headings and bullet points for
#           clear formatting.  Include a title for the report: 'Backtest
#           Performance Summary'. Store the complete markdown report in the
#           `markdown_report` output.
# -- END PRD --

from pydantic import BaseModel, Field


class RunBacktestOutput(BaseModel):
    """Pydantic model for run_backtest node outputs."""
    backtest_success: bool = Field(..., description="True if the backtest completed without runtime errors, otherwise False.")
    equity_curve_csv: str = Field(..., description="CSV\u2011formatted string of the daily equity curve. Columns: Date, Equity.")
    trades_log_csv: str = Field(..., description="CSV\u2011formatted string of all executed trades. Columns: Date, Symbol, Quantity, Price, PnL.")
    summary_message: str = Field(..., description="Brief textual summary of backtest execution (e.g., runtime, any warnings).")


class SummarizeBacktestResultsOutput(BaseModel):
    """Pydantic model for summarize_backtest_results node outputs."""
    annualized_return: float = Field(..., description="Annualized return of the strategy expressed as a decimal (e.g., 0.12 for 12%).")
    sharpe_ratio: float = Field(..., description="Annualized Sharpe ratio of the strategy.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the equity curve expressed as a decimal (e.g., -0.25 for -25%).")
    turnover: float = Field(..., description="Average portfolio turnover per period (e.g., monthly turnover as a decimal).")
    win_rate: float = Field(..., description="Proportion of winning trades (range 0\u20111).")
    histogram_description: str = Field(..., description="Markdown description of the histogram chart for daily returns, including key observations.")
    turnover_chart_description: str = Field(..., description="Markdown description of the turnover time\u2011series chart, highlighting trends or spikes.")
    markdown_report: str = Field(..., description="Full markdown report containing the statistics and chart descriptions.")


def summarize_backtest_results(run_backtest_input: RunBacktestOutput, **kwargs) -> SummarizeBacktestResultsOutput:
    """Produce a concise performance summary with key statistics and charts description.

    Args:
        run_backtest_input: Input from the 'run_backtest' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SummarizeBacktestResultsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SummarizeBacktestResultsOutput(
        annualized_return=0.0,
        sharpe_ratio=0.0,
        max_drawdown=0.0,
        turnover=0.0,
        win_rate=0.0,
        histogram_description="",
        turnover_chart_description="",
        markdown_report="",
    )