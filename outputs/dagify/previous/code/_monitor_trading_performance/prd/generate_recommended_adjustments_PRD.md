# generate_recommended_adjustments PRD

## Description
Produces a list of strategy or risk management adjustments based on performance metrics and thresholds.


## Implementation Plan

### 1. Implement a rule‑based mapping that evaluates key performance indicators (win rate, drawdown, Sharpe ratio, etc.) against the supplied thresholds and generates context‑appropriate adjustment suggestions.

| Category | Details |
| --- | --- |
| **Reason** | To translate quantitative metrics into actionable guidance for the trading strategy. |
| **Impact** | Provides clear, data‑driven recommendations that help maintain or improve performance. |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of conditions (e.g., win_rate < thresholds['win_rate_min']) mapping to suggestion strings and iterate over metrics to accumulate applicable suggestions. |

### 2. Short‑circuit recommendations when stability_result indicates the performance is within acceptable ranges, returning an empty adjustment list or a 'no change needed' notice.

| Category | Details |
| --- | --- |
| **Reason** | To avoid unnecessary or counter‑productive adjustments during stable periods. |
| **Impact** | Reduces noise in the output and preserves the trader’s existing configuration when appropriate. |
| **Complexity** | LOW |
| **Method** | Check `stability_result['is_stable']`; if true, immediately set the output to an empty array or a single message. |

### 3. Format the final suggestions as a JSON array string, ensuring the output adheres to the expected string type and can be parsed downstream.

| Category | Details |
| --- | --- |
| **Reason** | Consistent output serialization simplifies integration with downstream nodes. |
| **Impact** | Guarantees that downstream components can reliably interpret the adjustment recommendations. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps(suggestions_list)` to produce a compact JSON string; include error handling for serialization failures. |
