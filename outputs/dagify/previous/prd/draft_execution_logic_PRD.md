# draft_execution_logic PRD

## Description
Create pseudo‑code describing order sizing, routing, and real‑time signal handling.


## Implementation Plan

### 1. Load parent node outputs: retrieve `best_model_identifier` and its performance metrics from `select_best_model`; retrieve `risk_control_names`, `risk_control_thresholds`, and `risk_control_formulas` from `design_risk_controls`.

| Category | Details |
| --- | --- |
| **Reason** | The execution logic must be aware of which model to call and the exact numeric limits to enforce; pulling them up front avoids repeated look‑ups during runtime. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the JSON/structured output of the parent nodes; store values in in‑memory variables `model_id`, `risk_names[]`, `risk_limits[]`, `risk_formulas[]`. |

### 2. Define a function `fetch_latest_feature_vector()` that reads the most recent row from the persisted feature matrix (produced by `assemble_feature_matrix`). The function returns a dictionary mapping feature names to numeric values.

| Category | Details |
| --- | --- |
| **Reason** | Real‑time inference requires the freshest feature snapshot; encapsulating this in a function isolates I/O and allows unit testing. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement file I/O (e.g., pandas.read_csv with `skiprows=-1`) or query a feature store; ensure datatype conversion to float; include error handling for missing or NaN values. |

### 3. Create a wrapper `generate_position_signal(feature_vector)` that loads the serialized model identified by `model_id` (e.g., via joblib or torch) and computes a raw signal (e.g., probability or expected return). Normalize the signal to a signed magnitude in [-1, 1].

| Category | Details |
| --- | --- |
| **Reason** | The raw model output may be on an arbitrary scale; normalizing ensures downstream sizing logic remains consistent across models. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Load model with appropriate library; apply `model.predict(feature_vector)`; if output >0.5 map to +1, else -1; optionally scale by (output - 0.5)*2. |

### 4. Implement `apply_risk_controls(signal, current_exposure, portfolio_state)` that iterates over `risk_names` and evaluates each `risk_formulas` using the current portfolio metrics (gross exposure, VaR, per‑asset weight, daily P&L, turnover). If any rule would be violated, clamp or nullify the signal accordingly and log the adjustment.

| Category | Details |
| --- | --- |
| **Reason** | Risk compliance must be enforced before any order is sent; a systematic loop makes the logic extensible when new controls are added. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | For each control: parse the formula string (e.g., "GrossExposure <= 0.20") into a Python lambda; evaluate with real‑time numbers; if `signal` would cause breach, set `signal = 0` or reduce magnitude; record a string “Control X applied: signal capped to Y” into `risk_control_implementation_details` list. |

### 5. Define the order sizing formula as a string `order_sizing_formula = "size = min( capital * signal * leverage, risk_limit * capital )"` and also compute the numeric size in a helper `compute_order_size(signal, capital, risk_limits)` following that formula.

| Category | Details |
| --- | --- |
| **Reason** | Both a human‑readable formula (for documentation) and an executable calculation (for the pseudocode) are required by the output spec. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use variables: `capital` (available cash), `leverage` (model‑defined, e.g., 2x), `max_position = risk_limits['max_gross_exposure'] * capital`; final size = min(|signal| * capital * leverage, max_position); preserve sign from `signal`. |

### 6. Write the final pseudocode block (`execution_logic_pseudocode`) that strings together the above functions in logical order, with explicit comment lines for each major step:
```
# 1. Load latest features
features = fetch_latest_feature_vector()
# 2. Generate raw model signal
raw_signal = generate_position_signal(features)
# 3. Apply risk controls (may adjust signal)
adjusted_signal, rc_details = apply_risk_controls(raw_signal, current_exposure, portfolio_state)
# 4. Compute order size
order_qty = compute_order_size(adjusted_signal, capital, risk_limits)
# 5. Submit limit order
submit_limit_order(symbol, order_qty, limit_price)
```

| Category | Details |
| --- | --- |
| **Reason** | The prompt explicitly asks for concise pseudocode with clear step comments; the block satisfies readability and documentation needs. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Concatenate comment strings and code lines into a single multi‑line string; ensure variable names match those defined earlier; wrap in markdown triple backticks for clarity. |

### 7. Populate `risk_control_implementation_details` list with the textual logs generated in step 4 (e.g., "Applied max_gross_exposure: signal reduced from 0.8 to 0.4") so that the output documents exactly how each control altered the signal.

| Category | Details |
| --- | --- |
| **Reason** | The output requires a list of implementation details; capturing them during risk‑control evaluation provides traceability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Within `apply_risk_controls`, whenever a control modifies the signal, append a formatted string to a list; return that list to the caller. |

### 8. Validate the assembled outputs: ensure `execution_logic_pseudocode` is non‑empty string, `risk_control_implementation_details` contains at least one entry (or an empty list if no limits triggered), and `order_sizing_formula` matches the documented expression.

| Category | Details |
| --- | --- |
| **Reason** | Simple sanity checks prevent downstream failures when the compiled strategy document consumes these fields. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Add assert statements or conditional checks; raise descriptive exceptions if any check fails. |
