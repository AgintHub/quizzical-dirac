# -- PRD --
# 1. BULLET: Validate and safely parse the `datetime_index` string into a pandas
#   DatetimeIndex object.
#   Reason: The input may be malformed, empty, or not represent a DatetimeIndex, which
#           would cause runtime errors downstream.
#   Impact: Prevents crashes and provides clear error messages, improving robustness of
#           the pipeline.
#   Complexity: MEDIUM
#   Method: Use `ast.literal_eval` or `pd.read_json` to deserialize the string, then
#           wrap with `pd.DatetimeIndex`; catch `ValueError` and raise a
#           custom exception with context.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Convert each timestamp in the parsed DatetimeIndex to an ISO‑8601 string.
#   Reason: Downstream nodes expect dates in a standardized string format for
#           consistency across datasets.
#   Impact: Ensures uniform date representation, enabling correct alignment of
#           time‑series data.
#   Complexity: LOW
#   Method: Call `datetime_index.strftime('%Y-%m-%d')` (or `%Y-%m-%dT%H:%M:%S%z` if
#           time components are needed) and collect the results into a
#           Python list.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the list of date strings as the `output` field while preserving the
#   original `datetime_index` input for logging/debugging.
#   Reason: The shim’s contract requires both the derived list and the raw input to be
#           part of the output structure.
#   Impact: Facilitates downstream tracing and debugging without needing to recompute
#           the parsing step.
#   Complexity: LOW
#   Method: Construct and return a dictionary `{ "output": date_list, "datetime_index":
#           original_string }` that conforms to the defined output schema.
# -- END PRD --

from typing import List


def extract_date_strings(datetime_index: str) -> List[str]:
    """
    Extracts a list of ISO‑format date strings from a pandas DatetimeIndex supplied as a string representation.

    Args:
        datetime_index: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
