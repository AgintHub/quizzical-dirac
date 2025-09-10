# -- PRD --
# 1. BULLET: Retrieve cleaned team data from the output of the 'clean_and_process_data'
#   node
#   Reason: The 'clean_and_process_data' node provides the necessary cleaned team data
#           for calculating performance metrics
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the 'cleaned_teams_data' output field from the 'clean_and_process_data'
#           node
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Calculate win rates for each team using their win-loss records
#   Reason: Win rates are a crucial performance metric for NFL teams
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the 'processed_win_loss_records' output field from the
#           'clean_and_process_data' node and apply a formula to calculate
#           win rates
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate points scored and allowed for each team
#   Reason: Points scored and allowed are essential performance metrics for NFL teams
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the 'cleaned_points_scored' output field from the
#           'clean_and_process_data' node
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Calculate yards gained for each team
#   Reason: Yards gained is a relevant performance metric for NFL teams
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use the 'processed_win_loss_records' output field from the
#           'clean_and_process_data' node and apply a formula to calculate
#           yards gained
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compile the calculated metrics into a list of teams with their corresponding
#   metrics
#   Reason: The output should be a comprehensive list of teams with their performance
#           metrics
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use a data structure such as a Pandas DataFrame to compile the metrics
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CleanAndProcessDataOutput(BaseModel):
    """Pydantic model for clean_and_process_data node outputs."""
    cleaned_teams_data: List[str] = Field(..., description="List of cleaned team names")
    processed_win_loss_records: List[str] = Field(..., description="List of processed win-loss records")
    cleaned_points_scored: List[float] = Field(..., description="List of cleaned points scored")
    cleaned_odds: List[float] = Field(..., description="List of cleaned betting odds")
    processed_point_spreads: List[float] = Field(..., description="List of processed point spreads")
    cleaned_over_unders: List[float] = Field(..., description="List of cleaned over/unders")
    data_is_valid: bool = Field(..., description="Whether the cleaned data is valid")


class CalculateTeamPerformanceMetricsOutput(BaseModel):
    """Pydantic model for calculate_team_performance_metrics node outputs."""
    team_names: List[str] = Field(..., description="List of NFL team names")
    win_rates: List[float] = Field(..., description="List of win rates for each team, ranging from 0 to 1")
    points_scored: List[int] = Field(..., description="List of points scored by each team")
    points_allowed: List[int] = Field(..., description="List of points allowed by each team")
    yards_gained: List[int] = Field(..., description="List of yards gained by each team")


def calculate_team_performance_metrics(clean_and_process_data_input: CleanAndProcessDataOutput, **kwargs) -> CalculateTeamPerformanceMetricsOutput:
    """Calculate performance metrics for NFL teams, including their win rates, points scored, and other relevant statistics.

    Args:
        clean_and_process_data_input: Input from the 'clean_and_process_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CalculateTeamPerformanceMetricsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return CalculateTeamPerformanceMetricsOutput(
        team_names=[],
        win_rates=[],
        points_scored=[],
        points_allowed=[],
        yards_gained=[],
    )