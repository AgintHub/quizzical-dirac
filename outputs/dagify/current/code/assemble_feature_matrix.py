from ._assemble_feature_matrix.load_price_action_csv import load_price_action_csv
from ._assemble_feature_matrix.load_cross_asset_csv import load_cross_asset_csv
from ._assemble_feature_matrix.load_regime_csv import load_regime_csv
from ._assemble_feature_matrix.load_volatility_csv import load_volatility_csv
from ._assemble_feature_matrix.standardize_date_index import standardize_date_index
from ._assemble_feature_matrix.inner_join_on_date import inner_join_on_date
from ._assemble_feature_matrix.resolve_duplicate_columns import resolve_duplicate_columns
from ._assemble_feature_matrix.compute_next_day_return_target import compute_next_day_return_target
from ._assemble_feature_matrix.sort_and_reset_index import sort_and_reset_index
from ._assemble_feature_matrix.validate_feature_matrix import validate_feature_matrix
from ._assemble_feature_matrix.serialize_to_csv_string import serialize_to_csv_string
from ._assemble_feature_matrix.log_feature_matrix_summary import log_feature_matrix_summary

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Load the CSV payloads from each parent node (price_action, cross_asset,
#   regime, volatility) into in‑memory data frames using a robust CSV parser
#   that respects ISO‑8601 dates and quoted fields.
#   Reason: Ensures that all feature tables are correctly interpreted before any join
#           operation; parsing errors are caught early.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use pandas.read_csv with `parse_dates=['Date']`, `dayfirst=False`, `dtype`
#           inference disabled; wrap in try/except to capture malformed
#           rows.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Standardize the Date column across all data frames to midnight UTC and set it
#   as the index to guarantee exact alignment during the merge.
#   Reason: Date inconsistencies (timezones, format variations) would cause mismatched
#           joins and missing rows.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Apply `df['Date'] = pd.to_datetime(df['Date']).dt.normalize()` and then
#           `df.set_index('Date', inplace=True)`.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Perform an inner join on the Date index across the four feature data frames
#   to keep only dates present in every source, thereby guaranteeing a
#   complete feature row for each observation.
#   Reason: Target computation requires a complete set of predictors; dropping dates
#           with missing features avoids NaNs later in modeling.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use `merged = price_df.join([cross_df, regime_df, vol_df], how='inner')`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Detect and resolve any duplicate column names that may arise from overlapping
#   feature names (e.g., both price and volatility tables containing a column
#   called `date`).
#   Reason: Duplicate columns cause CSV export failures and ambiguous feature
#           references in downstream models.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: After merging, inspect `merged.columns`. For any duplicates, rename using a
#           prefix based on source table (e.g., `price_`, `vol_`).
#           Implement a helper `unique_rename(columns, source_prefix)`.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compute the target variable – next‑day simple return – using the cleaned
#   primary asset closing price series that resides in the price_action
#   feature table (column `close`).
#   Reason: The model learns to predict this target; it must be aligned with the
#           feature row date (i.e., return from t to t+1 assigned to row at
#           date t).
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Create a series `next_day_return = price_df['close'].shift(-1) /
#           price_df['close'] - 1`. Append as a new column `Target` to the
#           merged data frame. Drop the final row where Target is NaN.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Re‑index the final merged data frame to ensure chronological order (oldest to
#   newest) and reset the index to a regular `Date` column for CSV export.
#   Reason: Ordered dates simplify downstream time‑series splits and improve
#           readability of the CSV output.
#   Impact: LOW
#   Complexity: LOW
#   Method: Execute `merged.sort_index(inplace=True);
#           merged.reset_index(inplace=True)`.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Validate the final matrix: ensure no missing values, confirm that the column
#   count equals sum of unique feature columns plus `Date` and `Target`, and
#   verify that row count matches the expected number of trading days
#   (original dates minus one for target lag).
#   Reason: A sanity check prevents propagation of corrupted data into model training
#           and backtesting stages.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Run assertions: `assert merged.isnull().sum().sum() == 0`, `assert 'Target'
#           in merged.columns`, `assert len(merged) == expected_rows`.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Serialize the validated data frame to a CSV‑formatted string with UTF‑8
#   encoding, ensuring the header line includes `Date` followed by all
#   feature names and finally `Target`.
#   Reason: The downstream nodes expect a plain string CSV; consistent encoding avoids
#           hidden character issues.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `feature_matrix_csv = merged.to_csv(index=False, line_terminator='\n')`
#           and store as a Python string.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Return the CSV string as the node output `feature_matrix_csv` and log a
#   concise summary (row count, column count, date range) for observability.
#   Reason: Provides transparency for pipeline monitoring and aids debugging if
#           downstream nodes fail.
#   Impact: LOW
#   Complexity: LOW
#   Method: Construct a log message: `logger.info(f'Feature matrix generated:
#           {len(merged)} rows, {len(merged.columns)} columns, dates
#           {merged["Date"].min()}–{merged["Date"].max()}')` then assign to
#           output.
# -- END PRD --



class ComputePriceActionFeaturesOutput(BaseModel):
    """Pydantic model for compute_price_action_features node outputs."""
    csv_data: str = Field(..., description="CSV\u2011formatted text containing the Date column followed by each computed feature column (log_return, ma_10, ma_30, rsi, macd, atr).")
    feature_names: List[str] = Field(..., description="List of feature column names in the order they appear in the CSV (excluding the Date column).")
    row_count: int = Field(..., description="Number of rows (dates) in the generated feature table.")


class ComputeCrossAssetFeaturesOutput(BaseModel):
    """Pydantic model for compute_cross_asset_features node outputs."""
    date: List[str] = Field(..., description="List of dates for the computed features (ISO\u20118601 strings, sorted ascending).")
    asset_pairs: List[str] = Field(..., description="List of cross\u2011asset pair identifiers used for correlation and spread calculation, formatted as "Primary-SecondaryTicker".")
    correlations: List[float] = Field(..., description="Flattened list of rolling 20\u2011day Pearson correlation values. Order is by date (earliest to latest) then by asset_pairs order.")
    price_spreads: List[float] = Field(..., description="Flattened list of daily price spread values (PrimaryClose - SecondaryClose). Order matches the correlations list.")


class ComputeRegimeFeaturesOutput(BaseModel):
    """Pydantic model for compute_regime_features node outputs."""
    dates: List[str] = Field(..., description="List of dates (ISO\u20118601 strings) for which regime signals are generated.")
    regime_labels: List[str] = Field(..., description="Corresponding regime label for each date: either "high_vol" or "low_vol".")
    pmi_flags: List[bool] = Field(..., description="Binary flag indicating PMI direction for each date: true for positive PMI, false for negative PMI.")


class ComputeVolatilityFeaturesOutput(BaseModel):
    """Pydantic model for compute_volatility_features node outputs."""
    dates: List[str] = Field(..., description="List of dates (ISO format) for which the forecasts are generated.")
    garch_forecasts: List[float] = Field(..., description="One\u2011step\u2011ahead volatility forecast from the GARCH(1,1) model for each corresponding date.")
    implied_vol_delta_5d: List[float] = Field(..., description="5\u2011day change in implied volatility (ImpliedVol[t] - ImpliedVol[t-5]) for each date.")


class AssembleFeatureMatrixOutput(BaseModel):
    """Pydantic model for assemble_feature_matrix node outputs."""
    feature_matrix_csv: str = Field(..., description="CSV\u2011formatted string containing the complete feature matrix with a Date column, all merged feature columns, and a Target column for the next\u2011day return.")


def assemble_feature_matrix(compute_price_action_features_input: ComputePriceActionFeaturesOutput, compute_cross_asset_features_input: ComputeCrossAssetFeaturesOutput, compute_regime_features_input: ComputeRegimeFeaturesOutput, compute_volatility_features_input: ComputeVolatilityFeaturesOutput, **kwargs) -> AssembleFeatureMatrixOutput:
    """Combine all individual feature tables into a single matrix aligned with the target variable.

    Args:
        compute_price_action_features_input: Input from the 'compute_price_action_features' node.
        compute_cross_asset_features_input: Input from the 'compute_cross_asset_features' node.
        compute_regime_features_input: Input from the 'compute_regime_features' node.
        compute_volatility_features_input: Input from the 'compute_volatility_features' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AssembleFeatureMatrixOutput: Object containing outputs for this node.
    """
    # Load CSV payloads from each parent node into DataFrames
    price_df = load_price_action_csv(csv_data=compute_price_action_features_input.csv_data)
    cross_df = load_cross_asset_csv(dates=compute_cross_asset_features_input.date, 
                                     asset_pairs=compute_cross_asset_features_input.asset_pairs,
                                     correlations=compute_cross_asset_features_input.correlations,
                                     price_spreads=compute_cross_asset_features_input.price_spreads)
    regime_df = load_regime_csv(dates=compute_regime_features_input.dates,
                                 regime_labels=compute_regime_features_input.regime_labels,
                                 pmi_flags=compute_regime_features_input.pmi_flags)
    vol_df = load_volatility_csv(dates=compute_volatility_features_input.dates,
                                  garch_forecasts=compute_volatility_features_input.garch_forecasts,
                                  implied_vol_delta_5d=compute_volatility_features_input.implied_vol_delta_5d)
    
    # Standardize Date columns and set as index
    price_df = standardize_date_index(df=price_df)
    cross_df = standardize_date_index(df=cross_df)
    regime_df = standardize_date_index(df=regime_df)
    vol_df = standardize_date_index(df=vol_df)
    
    # Perform inner join on Date index
    merged_df = inner_join_on_date(price_df=price_df, cross_df=cross_df, regime_df=regime_df, vol_df=vol_df)
    
    # Detect and resolve duplicate column names
    merged_df = resolve_duplicate_columns(df=merged_df, source_prefixes=['price_', 'cross_', 'regime_', 'vol_'])
    
    # Compute target variable (next-day simple return)
    merged_df = compute_next_day_return_target(df=merged_df, close_column='close')
    
    # Re-index to chronological order and reset index
    merged_df = sort_and_reset_index(df=merged_df)
    
    # Validate final matrix
    validate_feature_matrix(df=merged_df, expected_columns=['Date', 'Target'])
    
    # Serialize to CSV string
    feature_matrix_csv: str = serialize_to_csv_string(df=merged_df)
    
    # Log summary for observability
    log_feature_matrix_summary(df=merged_df)
    
    return AssembleFeatureMatrixOutput(
        feature_matrix_csv=feature_matrix_csv
    )