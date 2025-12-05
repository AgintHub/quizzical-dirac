# create_monitoring_plan PRD

## Description
Define real‑time monitoring metrics, alert thresholds, and model retraining schedule.


## Implementation Plan

### 1. Extract strategy‑level parameters from `define_strategy_objectives` (primary_tradable_asset, desired_annual_return_pct, risk_tolerance_max_drawdown_pct, holding_period_days, regulatory_constraints) and model performance metrics from `select_best_model` (sharpe_ratio, max_drawdown, annualized_return).

| Category | Details |
| --- | --- |
| **Reason** | These values provide the business context needed to select appropriate monitoring metrics and realistic alert thresholds. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the JSON output of the two parent nodes; store values in a temporary dictionary for later reference. |

### 2. Define a canonical set of daily live metrics that directly reflect the strategy’s risk‑adjusted performance and operational health. Include at minimum: (1) Realized volatility (30‑day rolling), (2) Forecast volatility (model GARCH forecast), (3) Prediction error (abs(predicted‑return – actual‑return)), (4) Position exposure (gross % of capital), (5) Daily P&L, (6) Cumulative Sharpe ratio, (7) Current drawdown, (8) Turnover rate, (9) Compliance flag (e.g., short‑sell allowed).

| Category | Details |
| --- | --- |
| **Reason** | These metrics cover market risk, model risk, execution risk, and regulatory compliance, matching the objectives and constraints defined earlier. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a static list of metric names; ensure each name is concise and matches downstream naming conventions used in monitoring dashboards. |

### 3. Populate `daily_live_metrics` output field with the ordered list of metric names defined above, ensuring the list type is `LIST_STR`.

| Category | Details |
| --- | --- |
| **Reason** | The output must conform exactly to the schema expected by downstream nodes and by the final deliverables package. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Assign the list directly to the output variable; no computation required. |

### 4. Select which of the daily metrics will have active alert thresholds. Prioritize metrics that, if breached, indicate imminent risk: Sharpe ratio, max drawdown, exposure limit, turnover, and compliance flag.

| Category | Details |
| --- | --- |
| **Reason** | Limiting alerts to high‑impact metrics reduces noise and ensures rapid operator response. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create `alert_thresholds_metrics` list containing the subset: ["Sharpe ratio", "Current drawdown", "Gross exposure", "Turnover rate", "Compliance flag"]. |

### 5. Derive numeric alert thresholds (`alert_thresholds_values`) using both strategy objectives and model performance:  
- Sharpe ratio threshold = max(0.5, 0.8 × model_sharpe_ratio)  
- Drawdown threshold = risk_tolerance_max_drawdown_pct (e.g., 0.15 for 15 %)  
- Gross exposure threshold = 0.20 (20 % of capital)  
- Turnover rate threshold = 0.30 (30 % per month)  
- Compliance flag threshold = 0 (0 = violation).

| Category | Details |
| --- | --- |
| **Reason** | Thresholds are anchored to the model’s historical performance and the strategy’s risk appetite, providing objective triggers. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Compute the Sharpe threshold dynamically using the best model’s sharpe_ratio; other thresholds are static constants derived from `define_strategy_objectives`. Cast all values to float and store in the same order as `alert_thresholds_metrics`. |

### 6. Validate that the lengths of `alert_thresholds_metrics` and `alert_thresholds_values` match; raise an exception if mismatched.

| Category | Details |
| --- | --- |
| **Reason** | Ensures data integrity before downstream consumption; mismatched arrays would cause runtime errors in monitoring pipelines. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If len(list1) != len(list2): throw ValueError with explanatory message. |

### 7. Draft a detailed quarterly retraining schedule and assign it to `retraining_schedule`. Include: (a) data window (most recent 2‑years), (b) feature engineering freeze date, (c) hyper‑parameter search period (first week of quarter), (d) back‑test validation (second week), (e) model selection criteria (Sharpe > 0.5 and drawdown < risk_tolerance), (f) production rollout (third week), (g) monitoring hand‑off (fourth week).

| Category | Details |
| --- | --- |
| **Reason** | A clear, repeatable process guarantees that model drift is addressed regularly and that stakeholders know exact timelines. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Compose a multi‑paragraph markdown string outlining each step, dates relative to quarter start, and responsible owners. |

### 8. Return the four output fields (`daily_live_metrics`, `alert_thresholds_metrics`, `alert_thresholds_values`, `retraining_schedule`) as a JSON object matching the defined `output_structure`.

| Category | Details |
| --- | --- |
| **Reason** | Final step to satisfy the node contract and enable downstream nodes (e.g., `final_deliverables_package`) to consume the monitoring plan. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Serialize the prepared variables into the response payload; ensure correct PrimitiveType mapping (list of strings, list of floats, string). |
