# -- PRD --
# 1. BULLET: Parse the `daily_returns` string into a structured list of numeric daily
#   return series for each model.
#   Reason: The function receives raw text; it must be converted to a usable numeric
#           format before any calculations.
#   Impact: Ensures downstream calculations receive correctly typed data and prevents
#           parsing errors that would break the evaluation pipeline.
#   Complexity: LOW
#   Method: Detect common delimiters (commas, newlines, semicolons), split the string
#           accordingly, and convert each token to float using Python's
#           `float()` within a try/except block; raise a clear
#           ValidationError if conversion fails.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement the annualized return formula: ((1 + r̄) ^ N) - 1, where r̄ is the
#   average daily return and N is the number of trading days in a year (e.g.,
#   252).
#   Reason: Annualized return provides a comparable performance metric across models
#           regardless of the test period length.
#   Impact: Produces the primary output metric required by the `evaluate_models` node,
#           enabling ranking and reporting of model performance.
#   Complexity: MEDIUM
#   Method: For each daily return series, compute the geometric mean using
#           `numpy.prod(1 + returns) ** (252 / len(returns)) - 1`; multiply
#           by 100 to express as a percentage and store in the output list.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Add robust edge‑case handling (empty series, non‑finite values, zero‑length
#   input).
#   Reason: Real‑world data can contain gaps or NaNs; the shim must fail gracefully to
#           keep the pipeline stable.
#   Impact: Prevents runtime crashes, provides meaningful error messages, and ensures
#           that downstream nodes receive consistent list lengths.
#   Complexity: MEDIUM
#   Method: Validate each series length > 0; replace NaN or infinite values with
#           `numpy.nanmean` or skip them; if a series becomes empty after
#           cleaning, append `float('nan')` to the result and log a
#           warning.
# -- END PRD --

from typing import List


def calculate_annualized_returns(daily_returns: str) -> List[float]:
    """
    Computes the annualized return (in percent) for each model from a string containing daily returns.

    Args:
        daily_returns: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
