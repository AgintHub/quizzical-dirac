# refine_trading_strategy PRD

## Description
Refine the trading strategy based on analysis of trading results.


## Implementation Plan

### 1. Retrieve baseline strategy metadata from a configuration store or versioned strategy repository.

| Category | Details |
| --- | --- |
| **Reason** | The refinement process must preserve the original strategy context so that updates are applied incrementally rather than from scratch. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a key/value store (e.g., Redis, a JSON file, or a database table) indexed by strategy_name to fetch current entry_rule, exit_rule, position_size_rule, stop_loss_level, take_profit_level, max_drawdown_limit, risk_per_trade. Validate that all required fields exist; if not, abort refinement. |

### 2. Validate that `improvement_suggestions` from `analyze_trading_results` contains actionable items; if empty or null, set `is_strategy_updated` to False and terminate.

| Category | Details |
| --- | --- |
| **Reason** | Refinement should only occur when there are concrete improvement points. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Perform a simple list length check. If zero, construct a minimal output with original strategy values and `confidence_level` set to 0.5. |

### 3. Map each suggestion string to a rule category using a predefined keyword-to-category dictionary (e.g., 'entry timing' → 'entry', 'stop loss' → 'risk', 'position size' → 'position').

| Category | Details |
| --- | --- |
| **Reason** | Structured mapping enables systematic rule updates and prevents ambiguous interpretation of natural language suggestions. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use regex patterns and a lookup table. For each suggestion, identify the dominant keyword and assign it to a category. Store mapping results in a list of (category, suggestion) tuples. |

### 4. Generate updated textual rules for each mapped category by applying template-based transformations.

| Category | Details |
| --- | --- |
| **Reason** | Consistent rule language reduces ambiguity for downstream execution systems. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a set of rule templates: e.g., if category is 'entry', use "Enter long when {condition} and {indicator} crosses above {threshold}". Replace placeholders with values extracted from suggestions (e.g., threshold from numeric tokens). Concatenate multiple suggestions within the same category into a single rule string. |

### 5. Recalculate `stop_loss_level` by combining suggested risk adjustments with baseline values, ensuring it does not exceed 20% of equity or violate the `max_drawdown_limit`.

| Category | Details |
| --- | --- |
| **Reason** | Maintaining risk discipline is critical to prevent catastrophic losses. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | If any suggestion contains a numeric risk value (e.g., '2% stop loss'), parse it; otherwise, use baseline stop_loss_percentage. Then, enforce a hard cap: `stop_loss_level = min(parsed_value, 0.20)`. Convert to float percentage. |

### 6. Set `take_profit_level` as a multiple of the new `stop_loss_level` (e.g., 2:1 reward-to-risk ratio), or override with a numeric value from suggestions if present.

| Category | Details |
| --- | --- |
| **Reason** | Balanced reward-to-risk encourages sustainable profitability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If a suggestion contains 'take profit at X%', use that; otherwise, compute `take_profit_level = stop_loss_level * 2`. Ensure the value is a positive float. |

### 7. Update `max_drawdown_limit` by applying any suggested percentage or defaulting to baseline if no suggestion exists.

| Category | Details |
| --- | --- |
| **Reason** | Alignment with overall portfolio risk tolerance. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Search for numeric tokens followed by '%' in `improvement_suggestions` labeled as 'drawdown'; if found, use that; otherwise, keep baseline. |

### 8. Adjust `risk_per_trade` based on suggested changes to position sizing or stop loss, ensuring it stays within 1–3% of equity.

| Category | Details |
| --- | --- |
| **Reason** | Avoid overexposure while allowing flexibility to capitalize on identified opportunities. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | If a suggestion includes 'risk per trade', parse the percentage; else, calculate as `risk_per_trade = stop_loss_level * position_size_fraction` where `position_size_fraction` is derived from the baseline `position_size_rule` (e.g., fixed fractional). Clamp to 0.01–0.03. |

### 9. Estimate `expected_return` using `average_return_per_trade` and an annualization heuristic based on the number of trades per year inferred from `total_trades` over the monitoring period.

| Category | Details |
| --- | --- |
| **Reason** | Provides a realistic expectation for stakeholders. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Assume the monitoring period length is known (e.g., one month). Compute trades_per_year = total_trades / period_months * 12. Then `expected_return = average_return_per_trade * trades_per_year * 100`. Convert to a percentage. |

### 10. Compute `expected_sharpe_ratio` by applying a conservative multiplier (e.g., +10%) to the current `sharpe_ratio` if suggestions focus on volatility reduction; otherwise, keep the same.

| Category | Details |
| --- | --- |
| **Reason** | Reflects modest gains from the applied refinements without overpromising. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | If any suggestion contains words like 'reduce volatility' or 'improve Sharpe', multiply current sharpe_ratio by 1.10. Cap the result at a maximum of 3.0 to stay realistic. |

### 11. Determine `confidence_level` as a weighted score: 0.5 × `is_significant_change` + 0.3 × (number_of_suggestions / max_possible_suggestions) + 0.2 × (expected_sharpe_ratio / 3).

| Category | Details |
| --- | --- |
| **Reason** | Combines statistical significance, actionable density, and expected performance improvement into a single metric. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Normalize each component to [0,1] and compute the weighted sum. Ensure the final value is clipped to [0,1]. |

### 12. Construct `adjustments_summary` by concatenating human‑readable bullet points for each category that received an update, using the new rule text and parameter values.

| Category | Details |
| --- | --- |
| **Reason** | Provides transparency for auditors and traders. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Iterate over updated categories and append lines like '- Updated entry rule: {entry_rule}'. Join with newline separators. |

### 13. Set `is_strategy_updated` to True if any rule or parameter has changed compared to baseline; otherwise, set to False.

| Category | Details |
| --- | --- |
| **Reason** | Prevents unnecessary redeployment when no changes were made. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Compare each output field to its baseline value. If any differ, flag True. |
