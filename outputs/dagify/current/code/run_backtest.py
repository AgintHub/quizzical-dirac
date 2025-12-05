# -- PRD --
# 1. BULLET: Instantiate the backtesting engine using settings from
#   `setup_backtest_environment`.
#   Reason: This step initializes the backtesting framework with crucial parameters
#           like initial capital, commission, slippage, rebalance
#           frequency, and risk controls, enabling realistic simulations.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Create a BacktestingEngine class. Read the `initial_capital` (float),
#           `slippage_bps` (float), `commission_pct` (float),
#           `rebalance_frequency` (str), `risk_controls_summary` (List of
#           str), and `risk_control_enforcement_method` (str) from the
#           `setup_backtest_environment` output. Pass them as arguments to
#           the BacktestingEngine's constructor.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Load the cleaned data from `align_and_clean_data` to feed the backtesting
#   engine as a DataFrame.
#   Reason: The cleaned data provides the historical price data and features to
#           simulate the trading strategy over time.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Access the `cleaned_data_csv` output of the `align_and_clean_data` node.
#           Convert the CSV formatted data into a Pandas DataFrame using
#           `pd.read_csv()`. The `Date` column should become the index of
#           data frame.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Load best model saved in previous step `select_best_model`
#   Reason: We need the best model found previously in order to simulate it in the
#           backtest. So we load the model and use it later.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: The `best_model_identifier` from the output of node `select_best_model`
#           indicates which model to load and use for backtesting.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Implement the core backtesting loop: Iterate through each day in the test set
#   of cleaned data obtained from `split_dataset`.
#   Reason: This loop simulates the trading strategy's decision-making process on each
#           day, allowing us to observe its performance over time.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: For each day: (1) Fetch the current feature vector. (2) Generate a trading
#           signal using the loaded model and the current feature vector.
#           (3) Enforce risk controls as defined in
#           `setup_backtest_environment`, using `risk_controls_summary` and
#           `risk_control_enforcement_method` to guide the enforcement. (4)
#           Calculate the order size. (5) Execute the trade, accounting for
#           slippage and commission. (6) Update portfolio positions and
#           capital. (7) Implement rebalancing according to
#           `rebalance_frequency` from `setup_backtest_environment.`
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Record the daily equity and executed trades within the backtesting loop so
#   that they can be persisted later
#   Reason: This record keeps track of all trades and daily changes in equity, which
#           are key elements for the evaluation of backtest performance.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Daily store the current ‘equity’ value after the execution of each trade.
#           Keep track of the ‘Date’, ‘Symbol’, ‘Quantity’, ‘Price’ and
#           ‘PnL’ of each trade executed.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Format the daily equity curve as a CSV string.
#   Reason: The CSV format provides a standard and easily accessible representation of
#           the equity curve for further analysis and visualization.
#   Impact: LOW
#   Complexity: LOW
#   Method: Convert the recorded daily equity data (Date and Equity) into a Pandas
#           DataFrame. Then, use the `to_csv()` method to generate a CSV
#           formatted string and store in the equity_curve_csv output
#           field.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Format the trades log as a CSV string.
#   Reason: The CSV format allows for simple sharing and processing of trade
#           information.
#   Impact: LOW
#   Complexity: LOW
#   Method: Create a Pandas DataFrame using the `Date`, `Symbol`, `Quantity`, `Price`,
#           and `PnL` data that was tracked within the backtesting loop.
#           Finally, use the DataFrame's `to_csv()` method to create a CSV
#           formatted string. This CSV string needs to be placed into the
#           `trades_log_csv` output field.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Generate textual summary of backtest execution.
#   Reason: This summary provides a quick overview of the backtest, including key
#           metrics and any warnings encountered.
#   Impact: LOW
#   Complexity: LOW
#   Method: Record the runtime of the backtest. Also log any warnings encountered
#           during the backtesting process (e.g., risk control violations,
#           data issues). Construct a string containing the runtime and any
#           warnings, and assign it to the `summary_message` output field.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Set `backtest_success` to True if the backtest completed without runtime
#   errors, otherwise set it to False.
#   Reason: This boolean flag indicates the overall success of the backtest execution.
#   Impact: LOW
#   Complexity: LOW
#   Method: By default, set the `backtest_success` to True. If any exception is raised
#           during the backtesting loop (e.g., due to data issues or risk
#           control violations), catch it and set `backtest_success` to
#           False. Also, store the error message to the `summary_message`.
# -- END PRD --

from pydantic import BaseModel, Field


class SetupBacktestEnvironmentOutput(BaseModel):
    """Pydantic model for setup_backtest_environment node outputs."""
    initial_capital: float = Field(..., description="Starting capital for the backtest (e.g., 1_000_000).")
    slippage_bps: float = Field(..., description="Slippage applied per trade expressed in basis points.")
    commission_pct: float = Field(..., description="Commission charged per trade as a percentage of trade value.")
    rebalance_frequency: str = Field(..., description="How often the portfolio is rebalanced (e.g., \"daily\", \"weekly\", \"monthly\").")
    risk_controls_summary: str = Field(..., description="List of risk\u2011control rules that will be enforced during the simulation (e.g., \"max_gross_exposure 20%\", \"VaR 99% \u2264 2%\", \"per_asset_weight \u2264 5%\", \"daily_stop_loss 2%\", \"turnover \u2264 30%/month\").")
    risk_control_enforcement_method: str = Field(..., description="Brief description of how risk controls are applied in the backtest engine (e.g., \"pre\u2011trade check that aborts orders violating any rule\").")


class RunBacktestOutput(BaseModel):
    """Pydantic model for run_backtest node outputs."""
    backtest_success: bool = Field(..., description="True if the backtest completed without runtime errors, otherwise False.")
    equity_curve_csv: str = Field(..., description="CSV\u2011formatted string of the daily equity curve. Columns: Date, Equity.")
    trades_log_csv: str = Field(..., description="CSV\u2011formatted string of all executed trades. Columns: Date, Symbol, Quantity, Price, PnL.")
    summary_message: str = Field(..., description="Brief textual summary of backtest execution (e.g., runtime, any warnings).")


def run_backtest(setup_backtest_environment_input: SetupBacktestEnvironmentOutput, **kwargs) -> RunBacktestOutput:
    """Execute the backtest over the test period and record performance timeseries.

    Args:
        setup_backtest_environment_input: Input from the 'setup_backtest_environment' node.
        **kwargs: Additional keyword arguments.

    Returns:
        RunBacktestOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return RunBacktestOutput(
        backtest_success=False,
        equity_curve_csv="",
        trades_log_csv="",
        summary_message="",
    )