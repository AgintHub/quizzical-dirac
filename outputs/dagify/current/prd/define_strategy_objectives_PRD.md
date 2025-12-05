# define_strategy_objectives PRD

## Description
State the high‑level goals, asset universe, time horizon, and performance targets for the quant strategy.


## Implementation Plan

### 1. Collect the strategic brief from the user or upstream documentation and split it into five mandatory fields: primary asset, asset universe, target return, drawdown tolerance, and holding period.

| Category | Details |
| --- | --- |
| **Reason** | A deterministic extraction ensures every required output field is populated and prevents downstream null values. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a simple regex pattern (e.g., `Primary Asset: (\S+)`) for each bullet; fallback to a default placeholder if a field is missing. |

### 2. Validate `primary_tradable_asset` against a curated master ticker list (e.g., Bloomberg, Refinitiv) to guarantee the symbol exists and is tradable in the intended market.

| Category | Details |
| --- | --- |
| **Reason** | Invalid tickers cause data‑fetch failures later in the pipeline. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Load the master ticker CSV into a set; perform O(1) membership test; raise a clear error if not found. |

### 3. Normalize `asset_universe` by merging the primary asset with any secondary assets mentioned in the brief; de‑duplicate and sort alphabetically.

| Category | Details |
| --- | --- |
| **Reason** | A clean, ordered universe simplifies downstream feature generation and risk‑control loops. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Split the universe string on commas/semicolons, strip whitespace, add primary asset if absent, convert to set, then `sorted(list(set))`. |

### 4. Parse `desired_annual_return_pct` as a float, enforce a realistic range (1‑100 %), and round to two decimal places.

| Category | Details |
| --- | --- |
| **Reason** | Extreme return expectations break hyper‑parameter search and risk‑control calibration. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | float(value); if value < 1 or > 100 → clamp or raise warning; `round(value, 2)`. |

### 5. Parse `risk_tolerance_max_drawdown_pct` as a float, ensure it is positive and ≤ 100, and round to two decimals.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown limits drive the design of stop‑loss and VaR controls later in the workflow. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Same parsing logic as return; store as a positive percentage. |

### 6. Parse `holding_period_days` as an integer, enforce a sensible bound (1‑365 days), and default to 5 days if unspecified.

| Category | Details |
| --- | --- |
| **Reason** | Holding period directly influences feature lag windows and back‑test rebalance frequency. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | int(value); if out‑of‑range → set to default; log the adjustment. |

### 7. Extract `regulatory_constraints` by scanning the brief for known keywords (e.g., "short‑selling ban", "leverage limit", "region restriction"). Return a list; if none are found, return an empty list.

| Category | Details |
| --- | --- |
| **Reason** | Explicit constraints are needed for `design_risk_controls` and `create_monitoring_plan` nodes. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of regex → constraint string; iterate over patterns, append matches; deduplicate. |

### 8. Assemble the final output dictionary matching the `output_structure` schema and serialize it for downstream nodes.

| Category | Details |
| --- | --- |
| **Reason** | A single, well‑typed payload guarantees type‑safe consumption by all dependent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python dict with the six keys; validate types using a lightweight schema validator (e.g., `jsonschema`); raise if mismatch. |
