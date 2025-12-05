# -- PRD --
# 1. BULLET: Parse the `features_df` CSV string into a pandas DataFrame and verify that
#   each identifier in `asset_pairs` maps to a corresponding spread column.
#   Reason: The shim receives data as a string; converting it to a DataFrame is
#           required to perform column‑wise extraction and to catch
#           mismatches early.
#   Impact: Ensures downstream processing works on a structured DataFrame and provides
#           clear errors if expected columns are missing.
#   Complexity: MEDIUM
#   Method: Use `io.StringIO` with `pd.read_csv`, split `asset_pairs` on commas, and
#           assert that for each pair a column named `<pair>_Spread` (or
#           the naming convention used) exists in the DataFrame.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Iterate over the ordered `asset_pairs` list and, for each pair, collect the
#   column values row‑by‑row, preserving the chronological order of the
#   index.
#   Reason: The required output ordering is first by date (oldest to newest) then by
#           asset‑pair, matching the specification for the `price_spreads`
#           field.
#   Impact: Produces a correctly ordered flat list that aligns with the flattened
#           correlation list, enabling downstream models to pair spreads
#           with their correlations.
#   Complexity: MEDIUM
#   Method: For each asset pair, retrieve the spread column (`df[col]`), convert to a
#           NumPy array, and extend a master list; optionally use
#           `df[[col1, col2, ...]].to_numpy().ravel('F')` for vectorized
#           flattening.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle missing or NaN spread values by forward‑filling, backward‑filling, or
#   substituting a sentinel (e.g., 0.0) before flattening.
#   Reason: NaNs would break numeric downstream pipelines and could distort statistical
#           calculations.
#   Impact: Produces a clean, numeric‑only list that can be safely consumed by
#           downstream nodes without additional sanitisation.
#   Complexity: LOW
#   Method: Apply `df.fillna(method='ffill').fillna(method='bfill').fillna(0.0)` on the
#           selected spread columns before extraction.
# -- END PRD --

from typing import List


def flatten_price_spreads(features_df: str, asset_pairs: str) -> List[float]:
    """
    Flattens daily price spread values from a features DataFrame into a single ordered list of floats.

    Args:
        features_df: Input parameter of type str
asset_pairs: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
