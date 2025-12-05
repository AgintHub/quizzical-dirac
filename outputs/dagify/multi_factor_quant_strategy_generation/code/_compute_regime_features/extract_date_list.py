# -- PRD --
# 1. BULLET: Parse the input CSV string into a pandas DataFrame and verify a date column
#   or index exists.
#   Reason: The shim must operate on a concrete DataFrame; parsing ensures the raw
#           string is usable and validation prevents downstream errors.
#   Impact: Guarantees that subsequent date extraction works on a correctly structured
#           DataFrame, avoiding crashes in dependent nodes.
#   Complexity: LOW
#   Method: Use `pandas.read_csv` with `StringIO`; if the DataFrame has a DateTimeIndex
#           use `df.index`, otherwise look for a column named 'date'
#           (case‑insensitive) and convert it with `pd.to_datetime`.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Sort the DataFrame chronologically and convert the date values to ISO‑8601
#   strings.
#   Reason: Regime‑feature generation expects dates in ascending order and in a
#           standardized string format.
#   Impact: Ensures deterministic ordering of outputs and compatibility with downstream
#           models that consume ISO‑8601 dates.
#   Complexity: MEDIUM
#   Method: If dates are in a column, set it as the index with `df.set_index('date',
#           inplace=True)`. Then call `df.sort_index(inplace=True)`.
#           Extract the index with `df.index.strftime('%Y-%m-%d')` to
#           produce a list of strings.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return the list of formatted dates as the `output` field while preserving the
#   original CSV string as `dataframe`.
#   Reason: The shim’s contract requires both the derived list and the unchanged input
#           for possible re‑use.
#   Impact: Provides the necessary output for the `ComputeRegimeFeatures` node and
#           retains input provenance for debugging or caching.
#   Complexity: LOW
#   Method: Assign the list to a variable `dates_list` and construct the return
#           dictionary `{ 'output': dates_list, 'dataframe': dataframe }`
#           (or the appropriate Pydantic model wrapper).
# -- END PRD --

from typing import List


def extract_date_list(dataframe: str) -> List[str]:
    """
    Extracts an ordered list of ISO‑8601 date strings from the provided DataFrame.

    Args:
        dataframe: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
