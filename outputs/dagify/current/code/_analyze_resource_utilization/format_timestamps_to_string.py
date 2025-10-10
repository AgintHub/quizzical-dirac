# -- PRD --
# 1. BULLET: Implement a function that accepts a list of timestamps as input and returns a
#   comma-separated string of these timestamps.
#   Reason: This is necessary to convert the list of peak utilization times into a
#           format that can be stored and displayed in the
#           AnalyzeResourceUtilizationOutput model.
#   Impact: The output will be used to populate the peak_utilization_times field in the
#           AnalyzeResourceUtilizationOutput model, providing a human-
#           readable representation of peak resource utilization times.
#   Complexity: LOW
#   Method: Use Python's built-in str.join() method to concatenate the list of
#           timestamps into a single comma-separated string.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle potential errors that may occur during the formatting process, such as
#   None or empty input lists.
#   Reason: To ensure the function is robust and can handle unexpected inputs.
#   Impact: The function will be able to gracefully handle edge cases, preventing
#           potential errors downstream.
#   Complexity: MEDIUM
#   Method: Implement input validation to check for None or empty lists and return an
#           appropriate default value or raise a meaningful exception.
# -- END PRD --


def format_timestamps_to_string(timestamps: str) -> str:
    """
    A shim function that formats a list of timestamps into a comma-separated string.

    Args:
        timestamps: Input parameter of type str

    Returns:
        str: Output of type str
    """
    # Handle None or empty input
    if timestamps is None:
        return ""
    
    # If input is already a string, return it as-is (assuming it's already formatted)
    if isinstance(timestamps, str):
        # Handle empty string case
        if not timestamps.strip():
            return ""
        return timestamps.strip()
    
    # If somehow we get a list (though signature says str), handle it
    try:
        if hasattr(timestamps, '__iter__') and not isinstance(timestamps, str):
            # Convert list-like object to comma-separated string
            return ", ".join(str(item) for item in timestamps if item is not None)
    except (TypeError, AttributeError):
        # Fallback: convert whatever we have to string
        return str(timestamps)
    
    # Default fallback
    return str(timestamps)