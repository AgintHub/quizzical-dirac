# -- PRD --
# 1. BULLET: Extract strategy‑level parameters from the `define_strategy_objectives`
#   output: desired annual return, max drawdown tolerance, holding period,
#   and any regulatory constraints.
#   Reason: These parameters set the high‑level risk appetite and legal limits that
#           drive quantitative risk control thresholds.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Parse the `define_strategy_objectives` JSON fields; store values in local
#           variables (e.g., `max_drawdown_tol =
#           risk_tolerance_max_drawdown_pct / 100`).
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Extract model‑specific performance metrics from `select_best_model`: Sharpe
#   ratio, max drawdown, and annualized return.
#   Reason: Model volatility and drawdown behavior inform appropriate VaR limits,
#           stop‑loss levels, and turnover caps that are realistic for the
#           selected model.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Read the fields `sharpe_ratio`, `max_drawdown`, and `annualized_return`
#           from the best model output; convert percentages to decimals
#           where needed.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Define a canonical list of five core quantitative risk controls:
#   `max_gross_exposure`, `var_99`, `max_asset_weight`, `daily_stop_loss`,
#   `monthly_turnover`.
#   Reason: A fixed, well‑known set of controls provides consistency across downstream
#           nodes (documentation, execution, back‑test).
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Create an ordered Python list: `["max_gross_exposure", "var_99",
#           "max_asset_weight", "daily_stop_loss", "monthly_turnover"]`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Compute the numeric thresholds for each control using a blend of strategy
#   objectives and model metrics: - `max_gross_exposure` = 0.20 (hard‑coded
#   policy or derived from capital allocation guidelines). - `var_99` =
#   max(0.02, model_max_drawdown * 0.5) to ensure VaR is stricter than
#   historical drawdown. - `max_asset_weight` = min(0.05,
#   desired_annual_return / 250) – cap at 5% per‑asset. - `daily_stop_loss` =
#   max(0.02, model_max_drawdown / 10) – a conservative 2% floor. -
#   `monthly_turnover` = min(0.30, 1 / holding_period_days) – caps turnover
#   proportionally to holding period.
#   Reason: Formulas explicitly tie risk limits to both business objectives and
#           empirical model behavior, guaranteeing that controls are
#           neither too lax nor infeasible.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement each formula as a Python expression; ensure all percentages are
#           expressed as decimals. Use `max()`/`min()` to enforce policy
#           caps.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Generate human‑readable implementation strings for each control, preserving
#   the same order as the names list: - `"GrossExposure <= 0.20"` - `"VaR_99
#   <= {var_99:.4f}"` - `"Weight_per_asset <= {max_asset_weight:.4f}"` -
#   `"DailyStopLoss <= {daily_stop_loss:.4f}"` - `"Turnover_monthly <=
#   {monthly_turnover:.4f}"`.
#   Reason: Explicit formula strings are required by downstream nodes (e.g., execution
#           pseudocode, back‑test configuration) for direct embedding.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use Python f‑strings to interpolate the computed thresholds; round to 4
#           decimal places for clarity.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Validate that each threshold respects regulatory constraints (e.g., if
#   `short‑selling ban` is present, enforce `max_asset_weight` ≤ 0 for short
#   positions) and raise an error if any rule violates policy.
#   Reason: Ensuring compliance early prevents downstream failures and aligns with the
#           `regulatory_constraints` output.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Iterate over `regulatory_constraints`; if a constraint mentions
#           short‑selling, adjust `max_asset_weight` or add an additional
#           control such as `short_exposure <= 0`. Use assertions to fail
#           fast.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Assemble the three parallel output lists (`risk_control_names`,
#   `risk_control_thresholds`, `risk_control_formulas`) and return them in
#   the exact order defined by the schema.
#   Reason: Correct ordering guarantees that consuming nodes can zip the three lists
#           without ambiguity.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Return a JSON object with keys matching the output_structure; each list is
#           built from the earlier steps and verified for equal length.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class SelectBestModelOutput(BaseModel):
    """Pydantic model for select_best_model node outputs."""
    best_model_identifier: str = Field(..., description="Identifier of the selected best model.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected model.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the selected model.")
    annualized_return: float = Field(..., description="Annualized return of the selected model.")


class DefineStrategyObjectivesOutput(BaseModel):
    """Pydantic model for define_strategy_objectives node outputs."""
    primary_tradable_asset: str = Field(..., description="Ticker or identifier of the main asset the strategy will trade")
    asset_universe: List[str] = Field(..., description="List of all assets (tickers or identifiers) considered in the strategy")
    desired_annual_return_pct: float = Field(..., description="Target annualized return expressed as a percentage (e.g., 12.5 for 12.5%)")
    risk_tolerance_max_drawdown_pct: float = Field(..., description="Maximum acceptable drawdown expressed as a percentage of capital")
    holding_period_days: int = Field(..., description="Typical holding period for positions in days")
    regulatory_constraints: List[str] = Field(..., description="List of regulatory or compliance constraints affecting the strategy (e.g., short\u2011selling bans, leverage limits)")


class DesignRiskControlsOutput(BaseModel):
    """Pydantic model for design_risk_controls node outputs."""
    risk_control_names: List[str] = Field(..., description="Identifier for each risk control (e.g., max_gross_exposure, var_99, max_asset_weight, daily_stop_loss, monthly_turnover).")
    risk_control_thresholds: List[float] = Field(..., description="Numeric threshold for each risk control in the same order as risk_control_names (e.g., 0.20 for 20% gross exposure, 0.02 for 2% VaR).")
    risk_control_formulas: List[str] = Field(..., description="Short implementation formula or rule for each risk control (e.g., \"GrossExposure <= 0.20\", \"VaR_99 <= 0.02\").")


def design_risk_controls(select_best_model_input: SelectBestModelOutput, define_strategy_objectives_input: DefineStrategyObjectivesOutput, **kwargs) -> DesignRiskControlsOutput:
    """Define portfolio‑level and position‑level risk limits, stop‑loss rules, and turnover caps.

    Args:
        select_best_model_input: Input from the 'select_best_model' node.
        define_strategy_objectives_input: Input from the 'define_strategy_objectives' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DesignRiskControlsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DesignRiskControlsOutput(
        risk_control_names=[],
        risk_control_thresholds=[],
        risk_control_formulas=[],
    )