from ._evaluate_models.parse_csv_to_dataframe import parse_csv_to_dataframe
from ._evaluate_models.validate_test_dataframe_columns import validate_test_dataframe_columns
from ._evaluate_models.extract_model_identifiers_and_hyperparams import extract_model_identifiers_and_hyperparams
from ._evaluate_models.load_trained_models import load_trained_models
from ._evaluate_models.generate_test_predictions import generate_test_predictions
from ._evaluate_models.convert_predictions_to_positions import convert_predictions_to_positions
from ._evaluate_models.compute_portfolio_returns import compute_portfolio_returns
from ._evaluate_models.calculate_sharpe_ratios import calculate_sharpe_ratios
from ._evaluate_models.calculate_annualized_returns import calculate_annualized_returns
from ._evaluate_models.calculate_max_drawdowns import calculate_max_drawdowns
from ._evaluate_models.calculate_turnovers import calculate_turnovers
from ._evaluate_models.calculate_hit_rates import calculate_hit_rates
from ._evaluate_models.calculate_composite_rankings import calculate_composite_rankings
from ._evaluate_models.validate_output_consistency import validate_output_consistency
from ._evaluate_models.log_evaluation_summary import log_evaluation_summary

from pydantic import BaseModel, Field
from typing import List
from typing import Dict
from typing import Any


# -- PRD --
# 1. BULLET: Parse `split_dataset` output CSV strings (`train_csv`, `validation_csv`,
#   `test_csv`) into three Pandas DataFrames with proper dtypes (Date →
#   datetime, numeric columns → float). Validate that the Test DataFrame
#   contains the columns required for model inference (features + Target).
#   Reason: Reliable DataFrames are the foundation for generating predictions; parsing
#           errors would cascade into incorrect metric calculations.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `io.StringIO` + `pd.read_csv`; enforce `parse_dates=['Date']`; assert
#           required feature columns exist; raise descriptive error if
#           mismatch.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Extract the list of model identifiers from `train_models` output
#   (`hyperparameters`). For each hyperparameter string, generate a
#   deterministic model identifier (e.g., `model_001`, `model_002`, …) and
#   store the corresponding hyperparameter dict by parsing the string back
#   into a Python dict (e.g., using `ast.literal_eval`).
#   Reason: The identifiers link the trained models to the evaluation step; parsing
#           keeps the provenance of each candidate.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Iterate over `hyperparameters`; apply `enumerate` for stable IDs;
#           `ast.literal_eval` to convert string representation to dict;
#           build a dict `model_id -> hyperparams`.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: For each candidate model, reconstruct the trained estimator object from
#   persisted storage. Assume a convention where each model is serialized to
#   `models/{model_id}.pkl` using `joblib.dump` during `train_models`. Load
#   with `joblib.load`. If file missing, log a warning and skip the
#   candidate.
#   Reason: Evaluation must use the exact parameters learned during training;
#           re‑training would invalidate the validation metrics.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Import `joblib`; loop over identifiers; try‑except `FileNotFoundError`;
#           maintain `valid_models` list.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Generate predictions on the Test DataFrame for each valid model. Use the
#   model's `predict` method on the feature matrix (exclude `Target` and
#   `Date`). Store predictions as a NumPy array aligned with the Test dates.
#   Reason: Predictions are needed to construct daily position signals and subsequent
#           performance series.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Extract feature columns via `test_df.drop(columns=['Date','Target'])`;
#           ensure same column order as used in training; call
#           `model.predict(X_test)`; cache in dict `model_id ->
#           predictions`.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Convert raw predictions into daily position signals. Adopt a simple
#   long‑short rule: `position = np.sign(prediction)`. Optionally, apply a
#   volatility‑scaled position size using the `GARCHForecast` from
#   `compute_volatility_features` if available; otherwise use unit exposure.
#   Reason: A deterministic signal generation rule enables reproducible performance
#           metrics across all candidates.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: `positions = np.sign(predictions)`; ensure positions are -1, 0, or +1;
#           store as `model_id -> positions`.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Compute daily portfolio returns for each model: `return_t = position_t *
#   test_df['Target'].values`. This assumes the Target column is the next‑day
#   excess return of the primary asset.
#   Reason: Portfolio returns are the direct input for Sharpe, drawdown, turnover and
#           hit‑rate calculations.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Element‑wise multiplication; produce a Series `daily_ret` indexed by Date.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Calculate performance metrics per model: - **Sharpe ratio**: mean(daily_ret)
#   / std(daily_ret) * sqrt(252). - **Annualized return**: (1 +
#   mean(daily_ret))^252 - 1, expressed in percent. - **Max drawdown**: use
#   the cumulative product of (1+daily_ret) to build equity curve, then
#   compute peak‑to‑trough decline. - **Turnover**: average absolute change
#   in position per day (`|Δposition|`) expressed as a percent of the
#   notional (since position values are -1/0/1, turnover = mean(|Δposition|)
#   * 100). - **Hit‑rate**: proportion of days where `daily_ret > 0`. Store
#   each metric in its respective list.
#   Reason: These metrics directly answer the node's prompt and provide a basis for
#           ranking.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Implement helper functions: `calc_sharpe`, `calc_ann_return`,
#           `calc_max_dd`, `calc_turnover`, `calc_hit_rate`. Use `numpy`
#           for vectorised operations; guard against zero‑variance (std=0)
#           by returning Sharpe=0.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Assemble a composite ranking score. Define the score as a weighted sum:
#   `score = Sharpe * 0.5 - MaxDrawdown * 0.3 + AnnualizedReturn * 0.2`.
#   Higher scores are better. Compute scores for all candidates and obtain
#   ranks via `np.argsort(-score) + 1` (1 = best).
#   Reason: A single numeric ranking enables clear ordering while respecting
#           risk‑adjusted performance.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Create NumPy arrays for each metric; apply weights; use `np.argsort` to
#           produce rank list aligned with `candidate_models`.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Populate the output fields in the order of the original candidate list: -
#   `candidate_models` = list of identifiers. - `sharpe_ratios`,
#   `annualized_returns`, `max_drawdowns`, `turnovers`, `hit_rates`, `ranks`
#   = corresponding metric lists. Convert percentages to float (e.g., 12.5
#   for 12.5%).
#   Reason: Ensures the output conforms exactly to the declared schema for downstream
#           nodes.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Iterate over stored metric dicts; cast to Python `float`; build final dict
#           matching `output_structure`.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Validate the final output: confirm all lists have identical length, no `None`
#   values, and ranks form a permutation of 1..N. If any check fails, raise
#   an exception with a clear message.
#   Reason: Pre‑empt downstream failures (e.g., `select_best_model`) caused by
#           malformed output.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: `assert len(set(ranks)) == N and max(ranks) == N` etc.; use Python `assert`
#           with custom error text.
# 
# -----------------------------------------------------------------------------
# 11. BULLET: Log a concise summary to stdout or a logger: number of evaluated models, best
#   model identifier, its Sharpe and max drawdown. This aids debugging and
#   audit trails.
#   Reason: Transparency for users and for automated pipelines that capture logs.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use Python `logging` module at INFO level; format string with
#           f‑interpolation.
# -- END PRD --



class TrainModelsOutput(BaseModel):
    """Pydantic model for train_models node outputs."""
    hyperparameters: List[str] = Field(..., description="List of hyperparameter combinations for each trained model.")
    validation_sharpe: List[float] = Field(..., description="List of Sharpe ratios calculated on the validation set for each trained model.")
    validation_rmse: List[float] = Field(..., description="List of Root Mean Squared Errors calculated on the validation set for each trained model.")


class SplitDatasetOutput(BaseModel):
    """Pydantic model for split_dataset node outputs."""
    train_csv: str = Field(..., description="CSV formatted text containing the training subset of the feature matrix.")
    validation_csv: str = Field(..., description="CSV formatted text containing the validation subset of the feature matrix.")
    test_csv: str = Field(..., description="CSV formatted text containing the test subset of the feature matrix.")


class EvaluateModelsOutput(BaseModel):
    """Pydantic model for evaluate_models node outputs."""
    candidate_models: List[str] = Field(..., description="Identifier or name of each evaluated model candidate.")
    sharpe_ratios: List[float] = Field(..., description="Sharpe ratio for each model on the test set.")
    annualized_returns: List[float] = Field(..., description="Annualized return (in percent) for each model on the test set.")
    max_drawdowns: List[float] = Field(..., description="Maximum drawdown (in percent) observed for each model on the test set.")
    turnovers: List[float] = Field(..., description="Average portfolio turnover (as a percent of portfolio per period) for each model.")
    hit_rates: List[float] = Field(..., description="Proportion of trades with positive return (hit\u2011rate) for each model.")
    ranks: List[int] = Field(..., description="Rank of each model based on the chosen composite performance criterion (1 = best).")


def evaluate_models(train_models_input: TrainModelsOutput, split_dataset_input: SplitDatasetOutput, **kwargs) -> EvaluateModelsOutput:
    """Assess all trained candidates on the test set and compute performance metrics.

    Args:
        train_models_input: Input from the 'train_models' node.
        split_dataset_input: Input from the 'split_dataset' node.
        **kwargs: Additional keyword arguments.

    Returns:
        EvaluateModelsOutput: Object containing outputs for this node.
    """
    # Parse CSV strings into DataFrames with proper dtypes
    train_df = parse_csv_to_dataframe(csv_string=split_dataset_input.train_csv)
    validation_df = parse_csv_to_dataframe(csv_string=split_dataset_input.validation_csv)
    test_df = parse_csv_to_dataframe(csv_string=split_dataset_input.test_csv)
    
    # Validate test DataFrame has required columns
    validate_test_dataframe_columns(test_df=test_df)
    
    # Extract model identifiers and parse hyperparameters
    model_mapping: Dict[str, Dict] = extract_model_identifiers_and_hyperparams(hyperparameters=train_models_input.hyperparameters)
    
    # Load trained models from storage
    loaded_models: Dict[str, Any] = load_trained_models(model_ids=list(model_mapping.keys()))
    
    # Generate predictions for each valid model
    predictions: Dict[str, Any] = generate_test_predictions(models=loaded_models, test_df=test_df)
    
    # Convert predictions to position signals
    positions: Dict[str, Any] = convert_predictions_to_positions(predictions=predictions)
    
    # Compute daily portfolio returns for each model
    daily_returns: Dict[str, Any] = compute_portfolio_returns(positions=positions, test_df=test_df)
    
    # Calculate performance metrics for each model
    sharpe_ratios: List[float] = calculate_sharpe_ratios(daily_returns=daily_returns)
    annualized_returns: List[float] = calculate_annualized_returns(daily_returns=daily_returns)
    max_drawdowns: List[float] = calculate_max_drawdowns(daily_returns=daily_returns)
    turnovers: List[float] = calculate_turnovers(positions=positions)
    hit_rates: List[float] = calculate_hit_rates(daily_returns=daily_returns)
    
    # Calculate composite ranking scores
    ranks: List[int] = calculate_composite_rankings(
        sharpe_ratios=sharpe_ratios,
        max_drawdowns=max_drawdowns,
        annualized_returns=annualized_returns
    )
    
    # Get candidate model identifiers in order
    candidate_models: List[str] = list(loaded_models.keys())
    
    # Validate final output
    validate_output_consistency(
        candidate_models=candidate_models,
        sharpe_ratios=sharpe_ratios,
        annualized_returns=annualized_returns,
        max_drawdowns=max_drawdowns,
        turnovers=turnovers,
        hit_rates=hit_rates,
        ranks=ranks
    )
    
    # Log evaluation summary
    log_evaluation_summary(
        candidate_models=candidate_models,
        sharpe_ratios=sharpe_ratios,
        max_drawdowns=max_drawdowns,
        ranks=ranks
    )
    
    return EvaluateModelsOutput(
        candidate_models=candidate_models,
        sharpe_ratios=sharpe_ratios,
        annualized_returns=annualized_returns,
        max_drawdowns=max_drawdowns,
        turnovers=turnovers,
        hit_rates=hit_rates,
        ranks=ranks
    )