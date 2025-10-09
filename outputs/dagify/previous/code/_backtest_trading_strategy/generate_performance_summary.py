# -- PRD --
# 1. BULLET: Parse the `metrics` JSON string into a dictionary and validate the presence
#   of required keys (`total_return`, `annualized_return`, `max_drawdown`,
#   `sharpe_ratio`, `number_of_trades`, `win_rate`).
#   Reason: Ensures that all necessary data points are available for summary generation
#           and prevents downstream errors.
#   Impact: Guarantees accurate and reliable summary creation, improving user trust and
#           reducing runtime failures.
#   Complexity: LOW
#   Method: Use `json.loads()` with a try/except block; check for key existence and
#           numeric types.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create a flexible natural‑language template using Jinja2 or f‑string
#   formatting to embed metric values into a readable summary.
#   Reason: Allows consistent, human‑friendly summaries while keeping the code
#           maintainable.
#   Impact: Provides clear, actionable insights to traders and stakeholders, enhancing
#           the interpretability of backtest results.
#   Complexity: MEDIUM
#   Method: Define a Jinja2 template string that references each metric; render with
#           the parsed dictionary.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle edge cases such as missing metrics, non‑numeric values, or extreme
#   values by providing fallback text or warnings in the summary.
#   Reason: Improves robustness and prevents the shim from crashing on malformed input.
#   Impact: Ensures graceful degradation, maintaining system stability and user
#           experience.
#   Complexity: LOW
#   Method: Implement validation checks and default values; if validation fails, insert
#           a standardized error message into the summary.
# -- END PRD --


def generate_performance_summary(strategy_name: str, metrics: str) -> str:
    """
    Generates a concise textual performance summary for a trading strategy based on provided performance metrics.

    Args:
        strategy_name: Input parameter of type str
metrics: Input parameter of type str

    Returns:
        str: Output of type str
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
