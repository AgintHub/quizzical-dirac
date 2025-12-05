# -- PRD --
# 1. BULLET: Parse the daily_returns string into a dictionary mapping model identifiers to
#   ordered lists of float daily returns.
#   Reason: The shim receives raw string data; converting it to a structured Python
#           object is required before any calculations.
#   Impact: Provides a reliable, typed data structure for downstream drawdown
#           calculations and ensures consistency with other metrics.
#   Complexity: MEDIUM
#   Method: Attempt JSON decoding with `json.loads`; if that fails, fall back to CSV
#           parsing using `pandas.read_csv` with `StringIO`, then convert
#           columns to floats.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: For each model's return series, compute the running maximum and derive the
#   drawdown series, then extract the maximum drawdown value.
#   Reason: Maximum drawdown is defined as the largest peak‑to‑trough decline, which
#           requires tracking the highest cumulative value up to each
#           point.
#   Impact: Generates the core performance metric required by the evaluation pipeline
#           and feeds directly into model ranking.
#   Complexity: LOW
#   Method: Use NumPy: `cummax = np.maximum.accumulate(returns)`, `drawdowns = (cummax
#           - returns) / cummax`, then `max_drawdown =
#           np.nanmax(drawdowns)`; handle empty or all‑NaN series by
#           returning 0.0.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Assemble the max drawdown values into a list ordered identically to the input
#   model identifiers, handling edge cases and validating output length.
#   Reason: Downstream components expect the list order to align with other metric
#           lists (sharpe, returns, etc.).
#   Impact: Ensures that each max drawdown correctly corresponds to its model,
#           preventing mis‑ranking or mismatched reporting.
#   Complexity: MEDIUM
#   Method: Iterate over the ordered keys from the parsed dictionary, collect each
#           computed max drawdown into a list, verify that the list length
#           matches the number of models, and raise a descriptive
#           `ValueError` if mismatched or if any value is NaN.
# -- END PRD --

from typing import List


def calculate_max_drawdowns(daily_returns: str) -> List[float]:
    """
    Computes the maximum drawdown (in percent) for each model from a string-encoded collection of daily returns.

    Args:
        daily_returns: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
