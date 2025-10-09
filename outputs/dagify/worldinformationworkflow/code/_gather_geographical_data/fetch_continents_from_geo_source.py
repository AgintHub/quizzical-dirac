# -- PRD --
# 1. BULLET: Implement a data source connector to fetch geographical data.
#   Reason: To provide the required functionality, we need to connect to a reliable
#           geographical data source.
#   Impact: Enables the node to retrieve accurate geographical data.
#   Complexity: MEDIUM
#   Method: Utilize an existing geographical data API or database, such as GeoNames or
#           Natural Earth, to fetch the required data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Parse the geographical scope to determine the relevant continents.
#   Reason: The scope will dictate which continents are relevant, requiring parsing to
#           identify the correct data.
#   Impact: Ensures that the node returns the correct continents based on the provided
#           scope.
#   Complexity: LOW
#   Method: Use a simple string comparison or a more complex parsing logic depending on
#           the scope's format.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle errors and exceptions from the data source connection.
#   Reason: To ensure robustness, the node must handle potential errors from the data
#           source.
#   Impact: Prevents the node from failing unexpectedly due to external data source
#           issues.
#   Complexity: MEDIUM
#   Method: Implement try-except blocks to catch and handle exceptions, potentially
#           retrying the connection or returning a default value.
# -- END PRD --

from typing import List


def fetch_continents_from_geo_source(scope: str) -> List[str]:
    """
    Fetches a list of continents based on the geographical scope provided.

    Args:
        scope: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
