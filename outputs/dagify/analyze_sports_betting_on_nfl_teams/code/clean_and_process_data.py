# -- PRD --
# 1. BULLET: Handle missing values in team names by replacing them with standardized names
#   Reason: Ensures consistency in team names across datasets
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use regular expressions to detect and replace missing team names
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Clean and process win-loss records by converting them to a standardized
#   format
#   Reason: Enables accurate calculation of team performance metrics
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use string manipulation to extract win-loss records and convert to a
#           standardized format
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle outliers in points scored by winsorizing the data
#   Reason: Prevents extreme values from skewing analysis results
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use statistical methods (e.g., winsorization) to handle outliers in points
#           scored
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Clean and process betting odds by converting them to a standardized format
#   Reason: Enables accurate analysis of betting odds
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use string manipulation to extract betting odds and convert to a
#           standardized format
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Validate the cleaned data to ensure it meets analysis requirements
#   Reason: Ensures accuracy and reliability of analysis results
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use data validation techniques (e.g., data profiling) to verify data
#           quality
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CollectNflTeamsDataOutput(BaseModel):
    """Pydantic model for collect_nfl_teams_data node outputs."""
    team_name: str = Field(..., description="Name of the NFL team")
    win_loss_record: str = Field(..., description="Win-loss record of the team (e.g., 10-5)")
    points_scored: int = Field(..., description="Total points scored by the team")
    standings: str = Field(..., description="Current standings of the team (e.g., 1st in division)")
    statistics: str = Field(..., description="List of additional statistics for the team (e.g., passing yards, rushing yards, etc.)")


class CollectBettingOddsDataOutput(BaseModel):
    """Pydantic model for collect_betting_odds_data node outputs."""
    teams: List[str] = Field(..., description="List of NFL team names")
    point_spreads: List[float] = Field(..., description="List of point spreads corresponding to each team")
    moneylines: List[float] = Field(..., description="List of moneyline odds corresponding to each team")
    over_unders: List[float] = Field(..., description="List of over/under odds corresponding to each team")


class CleanAndProcessDataOutput(BaseModel):
    """Pydantic model for clean_and_process_data node outputs."""
    cleaned_teams_data: List[str] = Field(..., description="List of cleaned team names")
    processed_win_loss_records: List[str] = Field(..., description="List of processed win-loss records")
    cleaned_points_scored: List[float] = Field(..., description="List of cleaned points scored")
    cleaned_odds: List[float] = Field(..., description="List of cleaned betting odds")
    processed_point_spreads: List[float] = Field(..., description="List of processed point spreads")
    cleaned_over_unders: List[float] = Field(..., description="List of cleaned over/unders")
    data_is_valid: bool = Field(..., description="Whether the cleaned data is valid")


def clean_and_process_data(collect_nfl_teams_data_input: CollectNflTeamsDataOutput, collect_betting_odds_data_input: CollectBettingOddsDataOutput, **kwargs) -> CleanAndProcessDataOutput:
    """Clean and process the collected data, including handling missing values and outliers.

    Args:
        collect_nfl_teams_data_input: Input from the 'collect_nfl_teams_data' node.
        collect_betting_odds_data_input: Input from the 'collect_betting_odds_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CleanAndProcessDataOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return CleanAndProcessDataOutput(
        cleaned_teams_data=[],
        processed_win_loss_records=[],
        cleaned_points_scored=[],
        cleaned_odds=[],
        processed_point_spreads=[],
        cleaned_over_unders=[],
        data_is_valid=False,
    )