# design_risk_controls PRD

## Description
Define portfolio‑level and position‑level risk limits, stop‑loss rules, and turnover caps.


## Implementation Plan

### 1. Extract strategy‑level parameters from the `define_strategy_objectives` output: desired annual return, max drawdown tolerance, holding period, and any regulatory constraints.

| Category | Details |
| --- | --- |
| **Reason** | These parameters set the high‑level risk appetite and legal limits that drive quantitative risk control thresholds. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the `define_strategy_objectives` JSON fields; store values in local variables (e.g., `max_drawdown_tol = risk_tolerance_max_drawdown_pct / 100`). |

### 2. Extract model‑specific performance metrics from `select_best_model`: Sharpe ratio, max drawdown, and annualized return.

| Category | Details |
| --- | --- |
| **Reason** | Model volatility and drawdown behavior inform appropriate VaR limits, stop‑loss levels, and turnover caps that are realistic for the selected model. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the fields `sharpe_ratio`, `max_drawdown`, and `annualized_return` from the best model output; convert percentages to decimals where needed. |

### 3. Define a canonical list of five core quantitative risk controls: `max_gross_exposure`, `var_99`, `max_asset_weight`, `daily_stop_loss`, `monthly_turnover`.

| Category | Details |
| --- | --- |
| **Reason** | A fixed, well‑known set of controls provides consistency across downstream nodes (documentation, execution, back‑test). |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create an ordered Python list: `["max_gross_exposure", "var_99", "max_asset_weight", "daily_stop_loss", "monthly_turnover"]`. |

### 4. Compute the numeric thresholds for each control using a blend of strategy objectives and model metrics:
- `max_gross_exposure` = 0.20 (hard‑coded policy or derived from capital allocation guidelines).
- `var_99` = max(0.02, model_max_drawdown * 0.5) to ensure VaR is stricter than historical drawdown.
- `max_asset_weight` = min(0.05, desired_annual_return / 250) – cap at 5% per‑asset.
- `daily_stop_loss` = max(0.02, model_max_drawdown / 10) – a conservative 2% floor.
- `monthly_turnover` = min(0.30, 1 / holding_period_days) – caps turnover proportionally to holding period.

| Category | Details |
| --- | --- |
| **Reason** | Formulas explicitly tie risk limits to both business objectives and empirical model behavior, guaranteeing that controls are neither too lax nor infeasible. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement each formula as a Python expression; ensure all percentages are expressed as decimals. Use `max()`/`min()` to enforce policy caps. |

### 5. Generate human‑readable implementation strings for each control, preserving the same order as the names list:
- `"GrossExposure <= 0.20"`
- `"VaR_99 <= {var_99:.4f}"`
- `"Weight_per_asset <= {max_asset_weight:.4f}"`
- `"DailyStopLoss <= {daily_stop_loss:.4f}"`
- `"Turnover_monthly <= {monthly_turnover:.4f}"`.

| Category | Details |
| --- | --- |
| **Reason** | Explicit formula strings are required by downstream nodes (e.g., execution pseudocode, back‑test configuration) for direct embedding. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use Python f‑strings to interpolate the computed thresholds; round to 4 decimal places for clarity. |

### 6. Validate that each threshold respects regulatory constraints (e.g., if `short‑selling ban` is present, enforce `max_asset_weight` ≤ 0 for short positions) and raise an error if any rule violates policy.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring compliance early prevents downstream failures and aligns with the `regulatory_constraints` output. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `regulatory_constraints`; if a constraint mentions short‑selling, adjust `max_asset_weight` or add an additional control such as `short_exposure <= 0`. Use assertions to fail fast. |

### 7. Assemble the three parallel output lists (`risk_control_names`, `risk_control_thresholds`, `risk_control_formulas`) and return them in the exact order defined by the schema.

| Category | Details |
| --- | --- |
| **Reason** | Correct ordering guarantees that consuming nodes can zip the three lists without ambiguity. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return a JSON object with keys matching the output_structure; each list is built from the earlier steps and verified for equal length. |
