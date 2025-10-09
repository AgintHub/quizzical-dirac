# analyze_trading_results PRD

## Description
Analyze the results of trading activities to identify areas for improvement.


## Implementation Plan

### 1. Retrieve the monitoring snapshot data from the parent node "monitor_trading_performance" and deserialize it into a structured dictionary using the predefined JSON schema.

| Category | Details |
| --- | --- |
| **Reason** | Ensures type safety and consistency with downstream processing. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a JSON parsing library (e.g., Python's json module) and validate against the schema; handle missing keys with default values. |

### 2. Compute "total_trades" by summing the provided "total_trades" from the parent snapshot; if missing, calculate as winning_trades + losing_trades.

| Category | Details |
| --- | --- |
| **Reason** | Accurate trade count is essential for all subsequent metrics. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Apply integer addition; include a sanity check that the resulting count matches the length of any trade ID list if available. |

### 3. Derive "win_rate" by dividing the number of winning trades by the total trades, ensuring a division‑by‑zero guard that returns 0.0 when total_trades is zero.

| Category | Details |
| --- | --- |
| **Reason** | Provides a normalized performance indicator. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use float division; encapsulate in a try/except block for ZeroDivisionError. |

### 4. Calculate "average_return_per_trade" by taking the parent snapshot’s "average_return_per_trade"; if not available, compute using the cumulative profit/loss over all trades divided by total_trades.

| Category | Details |
| --- | --- |
| **Reason** | Standardized metric for trade profitability. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | If cumulative return is provided, divide by total_trades; otherwise, parse individual trade returns from the parent data if available. |

### 5. Determine "max_drawdown" by retrieving the parent snapshot’s "max_drawdown" value; if absent, compute it by scanning the equity curve provided in the snapshot (e.g., using peak‑to‑trough algorithm).

| Category | Details |
| --- | --- |
| **Reason** | Max drawdown is a critical risk metric. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a one‑pass algorithm that tracks running maximum equity and calculates drawdowns; handle missing equity data gracefully. |

### 6. Compute "sharpe_ratio" by retrieving the parent snapshot’s "sharpe_ratio"; if absent, compute it using the formula (mean return - risk‑free rate) / std deviation of returns, assuming a risk‑free rate of 0.01 (1%).

| Category | Details |
| --- | --- |
| **Reason** | Sharpe ratio contextualizes return relative to volatility. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use NumPy or Pandas to calculate mean and std; apply the Sharpe formula; round to four decimals. |

### 7. Generate "improvement_suggestions" by performing a rule‑based analysis: compare computed metrics against target thresholds (e.g., win_rate > 0.55, max_drawdown < 0.15, Sharpe > 1.0). For any metric that falls below its target, add a concise suggestion.

| Category | Details |
| --- | --- |
| **Reason** | Provides actionable insights without requiring deep statistical modeling. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of thresholds; iterate over metrics; append strings like "Improve stop‑loss granularity" or "Increase position sizing discipline" based on the shortfall. |

### 8. Translate each suggestion in "improvement_suggestions" into a concrete "action_item" by mapping common suggestions to specific tasks (e.g., "Adjust stop‑loss to 1.5% of entry price").

| Category | Details |
| --- | --- |
| **Reason** | Transforms high‑level ideas into implementable actions. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a mapping table or simple templating; if a suggestion is already actionable, reuse it verbatim. |

### 9. Assess "is_significant_change" by conducting a simple statistical test: if the difference between observed win_rate and expected win_rate (e.g., 0.6) is greater than 2 standard deviations of win_rate across historical periods, flag as true.

| Category | Details |
| --- | --- |
| **Reason** | Provides a quantitative check for anomalous performance. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Fetch historical win_rate distribution from a persisted dataset; compute mean and std; apply z‑score threshold (e.g., |z| > 2). |

### 10. Validate the final output dictionary against the defined schema, ensuring all fields are present and correctly typed before serializing to JSON.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees compatibility with downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Implement a schema validator (e.g., jsonschema) that checks data types and required fields. |
