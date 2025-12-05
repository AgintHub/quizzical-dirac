# evaluate_models PRD

## Description
Assess all trained candidates on the test set and compute performance metrics.


## Implementation Plan

### 1. Parse `split_dataset` output CSV strings (`train_csv`, `validation_csv`, `test_csv`) into three Pandas DataFrames with proper dtypes (Date → datetime, numeric columns → float). Validate that the Test DataFrame contains the columns required for model inference (features + Target).

| Category | Details |
| --- | --- |
| **Reason** | Reliable DataFrames are the foundation for generating predictions; parsing errors would cascade into incorrect metric calculations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` + `pd.read_csv`; enforce `parse_dates=['Date']`; assert required feature columns exist; raise descriptive error if mismatch. |

### 2. Extract the list of model identifiers from `train_models` output (`hyperparameters`). For each hyperparameter string, generate a deterministic model identifier (e.g., `model_001`, `model_002`, …) and store the corresponding hyperparameter dict by parsing the string back into a Python dict (e.g., using `ast.literal_eval`).

| Category | Details |
| --- | --- |
| **Reason** | The identifiers link the trained models to the evaluation step; parsing keeps the provenance of each candidate. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `hyperparameters`; apply `enumerate` for stable IDs; `ast.literal_eval` to convert string representation to dict; build a dict `model_id -> hyperparams`. |

### 3. For each candidate model, reconstruct the trained estimator object from persisted storage. Assume a convention where each model is serialized to `models/{model_id}.pkl` using `joblib.dump` during `train_models`. Load with `joblib.load`. If file missing, log a warning and skip the candidate.

| Category | Details |
| --- | --- |
| **Reason** | Evaluation must use the exact parameters learned during training; re‑training would invalidate the validation metrics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Import `joblib`; loop over identifiers; try‑except `FileNotFoundError`; maintain `valid_models` list. |

### 4. Generate predictions on the Test DataFrame for each valid model. Use the model's `predict` method on the feature matrix (exclude `Target` and `Date`). Store predictions as a NumPy array aligned with the Test dates.

| Category | Details |
| --- | --- |
| **Reason** | Predictions are needed to construct daily position signals and subsequent performance series. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Extract feature columns via `test_df.drop(columns=['Date','Target'])`; ensure same column order as used in training; call `model.predict(X_test)`; cache in dict `model_id -> predictions`. |

### 5. Convert raw predictions into daily position signals. Adopt a simple long‑short rule: `position = np.sign(prediction)`. Optionally, apply a volatility‑scaled position size using the `GARCHForecast` from `compute_volatility_features` if available; otherwise use unit exposure.

| Category | Details |
| --- | --- |
| **Reason** | A deterministic signal generation rule enables reproducible performance metrics across all candidates. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `positions = np.sign(predictions)`; ensure positions are -1, 0, or +1; store as `model_id -> positions`. |

### 6. Compute daily portfolio returns for each model: `return_t = position_t * test_df['Target'].values`. This assumes the Target column is the next‑day excess return of the primary asset.

| Category | Details |
| --- | --- |
| **Reason** | Portfolio returns are the direct input for Sharpe, drawdown, turnover and hit‑rate calculations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Element‑wise multiplication; produce a Series `daily_ret` indexed by Date. |

### 7. Calculate performance metrics per model:
- **Sharpe ratio**: mean(daily_ret) / std(daily_ret) * sqrt(252).
- **Annualized return**: (1 + mean(daily_ret))^252 - 1, expressed in percent.
- **Max drawdown**: use the cumulative product of (1+daily_ret) to build equity curve, then compute peak‑to‑trough decline.
- **Turnover**: average absolute change in position per day (`|Δposition|`) expressed as a percent of the notional (since position values are -1/0/1, turnover = mean(|Δposition|) * 100).
- **Hit‑rate**: proportion of days where `daily_ret > 0`.
Store each metric in its respective list.

| Category | Details |
| --- | --- |
| **Reason** | These metrics directly answer the node's prompt and provide a basis for ranking. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement helper functions: `calc_sharpe`, `calc_ann_return`, `calc_max_dd`, `calc_turnover`, `calc_hit_rate`. Use `numpy` for vectorised operations; guard against zero‑variance (std=0) by returning Sharpe=0. |

### 8. Assemble a composite ranking score. Define the score as a weighted sum: `score = Sharpe * 0.5 - MaxDrawdown * 0.3 + AnnualizedReturn * 0.2`. Higher scores are better. Compute scores for all candidates and obtain ranks via `np.argsort(-score) + 1` (1 = best).

| Category | Details |
| --- | --- |
| **Reason** | A single numeric ranking enables clear ordering while respecting risk‑adjusted performance. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create NumPy arrays for each metric; apply weights; use `np.argsort` to produce rank list aligned with `candidate_models`. |

### 9. Populate the output fields in the order of the original candidate list:
- `candidate_models` = list of identifiers.
- `sharpe_ratios`, `annualized_returns`, `max_drawdowns`, `turnovers`, `hit_rates`, `ranks` = corresponding metric lists.
Convert percentages to float (e.g., 12.5 for 12.5%).

| Category | Details |
| --- | --- |
| **Reason** | Ensures the output conforms exactly to the declared schema for downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Iterate over stored metric dicts; cast to Python `float`; build final dict matching `output_structure`. |

### 10. Validate the final output: confirm all lists have identical length, no `None` values, and ranks form a permutation of 1..N. If any check fails, raise an exception with a clear message.

| Category | Details |
| --- | --- |
| **Reason** | Pre‑empt downstream failures (e.g., `select_best_model`) caused by malformed output. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `assert len(set(ranks)) == N and max(ranks) == N` etc.; use Python `assert` with custom error text. |

### 11. Log a concise summary to stdout or a logger: number of evaluated models, best model identifier, its Sharpe and max drawdown. This aids debugging and audit trails.

| Category | Details |
| --- | --- |
| **Reason** | Transparency for users and for automated pipelines that capture logs. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use Python `logging` module at INFO level; format string with f‑interpolation. |
