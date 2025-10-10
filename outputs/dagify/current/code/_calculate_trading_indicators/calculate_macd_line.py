# -- PRD --
# 1. BULLET: Parse the input EMA strings into lists of floats to perform calculations
#   Reason: The input EMAs are provided as strings and need to be converted to
#           numerical values for the MACD calculation
#   Impact: Enables the correct calculation of the MACD line
#   Complexity: LOW
#   Method: Use a parsing library or a simple string splitting and conversion method
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Perform element-wise subtraction of the 26-period EMA from the 12-period EMA
#   Reason: The MACD line is defined as the difference between the 12-period and
#           26-period EMAs
#   Impact: Produces the MACD line values necessary for further analysis
#   Complexity: MEDIUM
#   Method: Use a library like NumPy for efficient element-wise operations on lists of
#           numbers
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the calculated MACD line as a list of floats
#   Reason: The output needs to be in a format that can be easily consumed by
#           subsequent nodes or analysis
#   Impact: Provides the MACD line in a usable format
#   Complexity: LOW
#   Method: Simply return the result of the subtraction as a list
# -- END PRD --

from typing import List


def calculate_macd_line(ema_12: str, ema_26: str) -> List[float]:
    """
    Calculates the MACD line by subtracting the 26-period EMA from the 12-period EMA

    Args:
        ema_12: Input parameter of type str
ema_26: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
