# -- PRD --
# 1. BULLET: Define the initial capital for the backtest. A reasonable starting point is
#   1,000,000.00, but this can be adjusted based on the desired scale and
#   risk profile of the strategy.
#   Reason: The initial capital is a fundamental parameter that determines the trading
#           size and affects performance metrics like Sharpe ratio and
#           drawdown.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Set the `initial_capital` to 1000000.00. Consider making this configurable
#           via a parameter.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement a slippage model. A simple model representing the execution cost is
#   to assume a fixed slippage of 0.5 basis points (0.005%).
#   Reason: Slippage accounts for the difference between the expected and actual
#           execution price, especially for large orders or illiquid
#           assets. It provides a more realistic backtest environment.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Set `slippage_bps` to 0.005. Model slippage linearly proportional to trade
#           size for increased realism within the backtesting engine.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Implement a commission model. A standard commission rate is 0.1% per trade
#   (0.001).
#   Reason: Commissions are trading costs charged by brokers, which need to be
#           accounted for in the backtest. This impacts the overall
#           profitability.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Set the `commission_pct` to 0.001.  Model this as a percentage of the trade
#           value incurred at both entry and exit.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Define the rebalancing frequency. Common choices are 'daily', 'weekly', or
#   'monthly'. Choose based on the strategy's typical holding period and
#   desired turnover.
#   Reason: Rebalancing ensures that the portfolio maintains its desired asset
#           allocation and risk profile. The frequency affects transaction
#           costs and tracking error.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Set `rebalance_frequency` to 'daily'. Add input validation to ensure
#           allowed values are only 'daily', 'weekly', or 'monthly'.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Extract the list of risk control rules from the `design_risk_controls` node
#   output. The `risk_control_names`, `risk_control_thresholds`, and
#   `risk_control_formulas` are mapped to a human-readable string and stored
#   in `risk_controls_summary` list.
#   Reason: This step prepares the risk control information for reporting and
#           integration into the backtesting engine.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Iterate through risk controls from the dependency node
#           `design_risk_controls`. Format each control info a string.
#           Example: `max_gross_exposure 20%`. Construct the output list
#           `risk_controls_summary`.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Define the risk control enforcement method. Choose a method such as 'pre-
#   trade check' or 'post-trade check'.
#   Reason: The enforcement method determines how risk controls are applied during the
#           simulation. 'Pre-trade check' aborts trades that violate risk
#           limits, while 'post-trade check' may trigger corrective
#           actions.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Set `risk_control_enforcement_method` to 'pre-trade check that aborts
#           orders violating any rule'. If post-trade, provide method to
#           reduce position size if any risk limit is breached post order
#           execution.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Integrate the cleaned data from the `align_and_clean_data` node. The cleaned
#   data will be used as the price feed for the backtesting engine. CSV
#   format is available in `cleaned_data_csv`.
#   Reason: This ensures the backtest uses a consistent and reliable data source, free
#           of missing values and properly aligned for accurate simulation.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Parse data in `cleaned_data_csv` and feed into backtest. Handle potential
#           parse errors.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Integrate the selected best model from the `select_best_model` node. The
#   `best_model_identifier` specifies the identifier of the model to load and
#   use during backtesting.
#   Reason: This step ensures the backtest reflects the expected performance of the
#           selected model.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use `best_model_identifier` to load the persisted model and use it when
#           generating trading signals in the backtesting engine. This
#           assumes a model persistence/loading mechanism is available
#           external to the backtest function.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Implement the chosen risk controls within the backtesting engine. The risk
#   control parameters are from the `design_risk_controls` node.
#   Reason: Enforcing risk controls accurately during backtesting is critical to
#           estimating the strategy's risk-adjusted performance.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: For each risk control extracted in previous step from node
#           `design_risk_controls`, implement the corresponding
#           `risk_control_formulas` with the respective
#           `risk_control_thresholds`. Implement checks specified in the
#           `risk_control_enforcement_method`.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class AlignAndCleanDataOutput(BaseModel):
    """Pydantic model for align_and_clean_data node outputs."""
    cleaned_data_csv: str = Field(..., description="CSV\u2011formatted text of the cleaned master DataFrame after merging and imputation.")
    row_count: int = Field(..., description="Number of rows (dates) present in the cleaned DataFrame.")
    column_names: List[str] = Field(..., description="List of column names in the cleaned DataFrame, including the primary asset fields and all feature columns.")
    missing_values_filled: bool = Field(..., description="Indicates whether any missing values were forward\u2011filled during the cleaning process (true if any fill occurred, false if none were needed).")


class SelectBestModelOutput(BaseModel):
    """Pydantic model for select_best_model node outputs."""
    best_model_identifier: str = Field(..., description="Identifier of the selected best model.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected model.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the selected model.")
    annualized_return: float = Field(..., description="Annualized return of the selected model.")


class DesignRiskControlsOutput(BaseModel):
    """Pydantic model for design_risk_controls node outputs."""
    risk_control_names: List[str] = Field(..., description="Identifier for each risk control (e.g., max_gross_exposure, var_99, max_asset_weight, daily_stop_loss, monthly_turnover).")
    risk_control_thresholds: List[float] = Field(..., description="Numeric threshold for each risk control in the same order as risk_control_names (e.g., 0.20 for 20% gross exposure, 0.02 for 2% VaR).")
    risk_control_formulas: List[str] = Field(..., description="Short implementation formula or rule for each risk control (e.g., "GrossExposure <= 0.20", "VaR_99 <= 0.02").")


class SetupBacktestEnvironmentOutput(BaseModel):
    """Pydantic model for setup_backtest_environment node outputs."""
    initial_capital: float = Field(..., description="Starting capital for the backtest (e.g., 1_000_000).")
    slippage_bps: float = Field(..., description="Slippage applied per trade expressed in basis points.")
    commission_pct: float = Field(..., description="Commission charged per trade as a percentage of trade value.")
    rebalance_frequency: str = Field(..., description="How often the portfolio is rebalanced (e.g., "daily", "weekly", "monthly").")
    risk_controls_summary: str = Field(..., description="List of risk\u2011control rules that will be enforced during the simulation (e.g., "max_gross_exposure 20%", "VaR 99% \u2264 2%", "per_asset_weight \u2264 5%", "daily_stop_loss 2%", "turnover \u2264 30%/month").")
    risk_control_enforcement_method: str = Field(..., description="Brief description of how risk controls are applied in the backtest engine (e.g., "pre\u2011trade check that aborts orders violating any rule").")


def setup_backtest_environment(align_and_clean_data_input: AlignAndCleanDataOutput, select_best_model_input: SelectBestModelOutput, design_risk_controls_input: DesignRiskControlsOutput, **kwargs) -> SetupBacktestEnvironmentOutput:
    """Configure a backtesting engine with data, model, risk controls, and transaction cost assumptions.

    Args:
        align_and_clean_data_input: Input from the 'align_and_clean_data' node.
        select_best_model_input: Input from the 'select_best_model' node.
        design_risk_controls_input: Input from the 'design_risk_controls' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SetupBacktestEnvironmentOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SetupBacktestEnvironmentOutput(
        initial_capital=0.0,
        slippage_bps=0.0,
        commission_pct=0.0,
        rebalance_frequency="",
        risk_controls_summary="",
        risk_control_enforcement_method="",
    )