# calculate_performance_metrics PRD

## Description
Computes key trading performance statistics from closed trade data and an equity curve.


## Implementation Plan

### 1. Deserialize the `closed_trades` and `equity_curve` JSON strings into Python objects while validating schema consistency.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that downstream computations receive correctly structured data and helps catch malformed inputs early. |
| **Impact** | Prevents runtime errors during metric calculations and guarantees that all required fields are present. |
| **Complexity** | LOW |
| **Method** | Use `json.loads()` with try/except blocks and optionally leverage Pydantic models or schema validation to enforce field types. |

### 2. Iterate over the list of closed trades to compute trade‑level statistics (total, wins, losses, win rate, average return) and aggregate equity changes to calculate max drawdown and the Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | These metrics are the core outputs required by downstream performance monitoring nodes. |
| **Impact** | Provides a concise performance snapshot that informs risk management and strategy adjustments. |
| **Complexity** | MEDIUM |
| **Method** | Use plain Python loops or NumPy/Pandas for vectorized calculations; compute cumulative equity to derive drawdowns and use risk‑free rate = 0 to calculate Sharpe ratio. |

### 3. Serialize the computed metrics dictionary into a JSON string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | Matches the shim’s expected output type and allows callers to parse the results easily. |
| **Impact** | Ensures compatibility with downstream nodes that expect a string payload. |
| **Complexity** | LOW |
| **Method** | Use `json.dumps()` on the metrics dictionary and return the string. |
