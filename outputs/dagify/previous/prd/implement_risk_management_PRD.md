# implement_risk_management PRD

## Description
Develop and implement risk management rules to control exposure.


## Implementation Plan

### 1. Parse the `risk_management_rule` text from the parent `define_trading_strategy` output to extract explicit numeric risk thresholds using a combination of regular expressions and a lightweight NLP parser.

| Category | Details |
| --- | --- |
| **Reason** | The strategy definition contains human‑readable risk constraints that need to be programmatically interpreted to populate numeric fields. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use regex patterns such as `risk per trade[:=]\s*(\d+%|\d*\.?\d+)`, `stop‑loss[:=]\s*(\d+%|\d*\.?\d+)`, `max drawdown[:=]\s*(\d+%|\d*\.?\d+)`, and `diversification[:=]\s*(\d+)` to capture numbers; if percentages are present, convert to decimal; otherwise default to 0.01 for risk per trade. |

### 2. Validate the extracted numeric values and apply default fallbacks where necessary (e.g., 1% risk per trade, 2% stop‑loss, 20% max drawdown, 10 diversification assets).

| Category | Details |
| --- | --- |
| **Reason** | Ensures the risk management configuration is robust even if the strategy text omits some parameters. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If a key is missing or cannot be parsed, assign hard‑coded defaults; log a warning for auditability. |

### 3. Determine the `position_sizing_strategy` by mapping the parsed risk parameters to a chosen sizing model (default to "fixed fractional").

| Category | Details |
| --- | --- |
| **Reason** | A clear strategy name is required for downstream systems to interpret how position sizes are calculated. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If the strategy text contains keywords like "Kelly" or "equity curve", set `position_sizing_strategy` accordingly; otherwise default to "fixed fractional". |

### 4. Compute the `stop_loss_levels` list for each asset in `assets_traded` by applying the parsed `stop_loss_percentage` to a placeholder or expected entry price.

| Category | Details |
| --- | --- |
| **Reason** | Stop‑loss price levels must be concrete for the execution engine to enforce. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each asset symbol, retrieve the most recent closing price from a cached data source; compute stop price = entry_price * (1 - stop_loss_percentage). If entry price is unavailable, flag the asset for manual review. |

### 5. Apply the `max_drawdown` and `diversification_assets` values to create an internal portfolio constraint model that will be passed to the execution layer.

| Category | Details |
| --- | --- |
| **Reason** | These constraints limit overall exposure and enforce diversification, which are critical for risk control. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Instantiate a `PortfolioRiskConstraint` object with attributes `max_drawdown_pct` and `min_asset_count`; expose its API to the execution engine via a shared configuration store (e.g., Redis or a JSON file). |

### 6. Set `diversification_strategy` by inferring the strategy type from the strategy name or by checking if the assets span multiple sectors.

| Category | Details |
| --- | --- |
| **Reason** | The diversification approach should align with the intended portfolio structure. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | If the strategy name contains "sector" or the asset list includes at least 3 distinct sectors, set to "sector‑based"; otherwise set to "beta‑neutral". |

### 7. Persist all computed risk parameters to a secure configuration repository and return `is_implemented = true` if no errors occur during persistence.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the risk rules are applied before any trade execution takes place. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a transactional write to a configuration database; on success set `is_implemented` to true; on failure log the error and set `is_implemented` to false. |

### 8. Expose a validation endpoint that `execute_trades` can call to confirm that risk rules are in place before placing orders.

| Category | Details |
| --- | --- |
| **Reason** | Prevents trades from being executed without the associated risk controls. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Implement a lightweight REST or gRPC service that returns the current risk configuration and an `is_valid` flag; integrate this call into the trade‑ordering workflow. |
