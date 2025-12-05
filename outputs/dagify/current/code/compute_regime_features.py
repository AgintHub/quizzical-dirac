from ._compute_regime_features.parse_csv_to_dataframe import parse_csv_to_dataframe
from ._compute_regime_features.validate_required_columns import validate_required_columns
from ._compute_regime_features.compute_vix_threshold import compute_vix_threshold
from ._compute_regime_features.create_regime_labels import create_regime_labels
from ._compute_regime_features.create_pmi_flags import create_pmi_flags
from ._compute_regime_features.extract_date_list import extract_date_list
from ._compute_regime_features.extract_regime_labels_list import extract_regime_labels_list
from ._compute_regime_features.extract_pmi_flags_list import extract_pmi_flags_list

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Load the `cleaned_data_csv` string from the `align_and_clean_data` node,
#   parse it into a pandas DataFrame preserving the original chronological
#   order.
#   Reason: The regime classifier needs numeric VIX and PMI series aligned to dates;
#           parsing ensures we work with structured data.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use `io.StringIO` to feed the CSV string into `pd.read_csv`, set
#           `parse_dates=['Date']`, and sort by the Date column if not
#           already sorted.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate that the DataFrame contains the required macro columns `VIX` and
#   `PMI`; raise a clear error if either is missing.
#   Reason: Early validation prevents downstream logic failures and makes debugging
#           data‑pipeline issues straightforward.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Check `{'VIX', 'PMI'}.issubset(df.columns)`; if false, construct an
#           informative Exception listing missing columns.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Compute the 75th percentile of the entire VIX series using
#   `numpy.percentile(df['VIX'].dropna(), 75)` and store it as
#   `vix_threshold`.
#   Reason: A fixed percentile threshold implements the rule‑based high/low volatility
#           regime definition described in the prompt.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Import `numpy as np`; ensure NaNs are excluded from the percentile
#           calculation.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Create a new column `RegimeLabel` where each row receives `'high_vol'` if its
#   VIX value exceeds `vix_threshold`, otherwise `'low_vol'`.
#   Reason: Translates the numeric VIX observation into a categorical regime label
#           required by downstream models.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use vectorised pandas logic: `df['RegimeLabel'] = np.where(df['VIX'] >
#           vix_threshold, 'high_vol', 'low_vol')`.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Create a binary column `PMIFlag` set to `True` when the PMI value is greater
#   than 0 (positive PMI) and `False` otherwise.
#   Reason: Provides a simple directional macro signal that can be used as a feature in
#           the assembled matrix.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: `df['PMIFlag'] = df['PMI'] > 0` (pandas will produce a boolean series).
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Extract three parallel Python lists preserving date order: `dates =
#   df['Date'].dt.strftime('%Y-%m-%d').tolist()`, `regime_labels =
#   df['RegimeLabel'].tolist()`, and `pmi_flags = df['PMIFlag'].tolist()`.
#   Reason: The node's output specification demands plain Python lists (primitive
#           types), not pandas objects.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Leverage pandas `.tolist()` after ensuring the DataFrame is sorted by Date.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Return a JSON‑compatible dictionary containing the three lists under the keys
#   `dates`, `regime_labels`, and `pmi_flags` as defined in the output
#   structure.
#   Reason: Conforms to the typed node contract, enabling downstream nodes (e.g.,
#           `assemble_feature_matrix`) to consume the data without further
#           transformation.
#   Impact: HIGH
#   Complexity: LOW
#   Method: `return {"dates": dates, "regime_labels": regime_labels, "pmi_flags":
#           pmi_flags}`.
# -- END PRD --



class AlignAndCleanDataOutput(BaseModel):
    """Pydantic model for align_and_clean_data node outputs."""
    cleaned_data_csv: str = Field(..., description="CSV\u2011formatted text of the cleaned master DataFrame after merging and imputation.")
    row_count: int = Field(..., description="Number of rows (dates) present in the cleaned DataFrame.")
    column_names: List[str] = Field(..., description="List of column names in the cleaned DataFrame, including the primary asset fields and all feature columns.")
    missing_values_filled: bool = Field(..., description="Indicates whether any missing values were forward\u2011filled during the cleaning process (true if any fill occurred, false if none were needed).")


class ComputeRegimeFeaturesOutput(BaseModel):
    """Pydantic model for compute_regime_features node outputs."""
    dates: List[str] = Field(..., description="List of dates (ISO\u20118601 strings) for which regime signals are generated.")
    regime_labels: List[str] = Field(..., description="Corresponding regime label for each date: either "high_vol" or "low_vol".")
    pmi_flags: List[bool] = Field(..., description="Binary flag indicating PMI direction for each date: true for positive PMI, false for negative PMI.")


def compute_regime_features(align_and_clean_data_input: AlignAndCleanDataOutput, **kwargs) -> ComputeRegimeFeaturesOutput:
    """Derive regime classification signals from macro indicators (e.g., high‑/low‑vol regimes).

    Args:
        align_and_clean_data_input: Input from the 'align_and_clean_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ComputeRegimeFeaturesOutput: Object containing outputs for this node.
    """
    # Load and parse the CSV data into a DataFrame
    df = parse_csv_to_dataframe(csv_string=align_and_clean_data_input.cleaned_data_csv)
    
    # Validate required columns are present
    validate_required_columns(dataframe=df, required_columns=["VIX", "PMI"])
    
    # Compute the 75th percentile threshold for VIX
    vix_threshold: float = compute_vix_threshold(vix_series=df["VIX"])
    
    # Create regime labels based on VIX threshold
    df = create_regime_labels(dataframe=df, vix_threshold=vix_threshold)
    
    # Create PMI flags based on positive/negative PMI values
    df = create_pmi_flags(dataframe=df)
    
    # Extract ordered lists for output
    dates: List[str] = extract_date_list(dataframe=df)
    regime_labels: List[str] = extract_regime_labels_list(dataframe=df)
    pmi_flags: List[bool] = extract_pmi_flags_list(dataframe=df)
    
    return ComputeRegimeFeaturesOutput(
        dates=dates,
        regime_labels=regime_labels,
        pmi_flags=pmi_flags
    )