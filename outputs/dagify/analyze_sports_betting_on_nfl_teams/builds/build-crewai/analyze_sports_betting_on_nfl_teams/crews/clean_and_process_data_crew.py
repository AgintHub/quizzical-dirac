from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import clean_and_process_data_output

@CrewBase
class clean_and_process_data_crew:
    """Crew for clean_and_process_data operations."""


    @agent
    def clean_and_process_data_agent(self):
        return Agent(
            role="Clean And Process Data Specialist",
            goal="""Execute clean_and_process_data task accurately.
PRD Requirements:
- Handle missing values in team names by replacing them with standardized names
- Clean and process win-loss records by converting them to a standardized format
- Handle outliers in points scored by winsorizing the data
- Clean and process betting odds by converting them to a standardized format
- Validate the cleaned data to ensure it meets analysis requirements""",
            backstory="You are a specialized worker focused on Clean and process the collected data, including handling missing values and outliers.",
            verbose=True
        )



    @task
    def clean_and_process_data_task(self):
        """Task for clean_and_process_data."""
        agent = self.clean_and_process_data_agent()
        return Task(
            description="""Using {collect_nfl_teams_data_output}, {collect_betting_odds_data_output}, Clean and process the collected data, including handling missing values and outliers.""",
            agent=agent,
            expected_output="""{
    cleaned_teams_data: list of strs  # List of cleaned team names
    processed_win_loss_records: list of strs  # List of processed win-loss records
    cleaned_points_scored: list of floats  # List of cleaned points scored
    cleaned_odds: list of floats  # List of cleaned betting odds
    processed_point_spreads: list of floats  # List of processed point spreads
    cleaned_over_unders: list of floats  # List of cleaned over/unders
    data_is_valid: bool  # Whether the cleaned data is valid
}""",
            output_pydantic=clean_and_process_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.clean_and_process_data_agent()],
            tasks=[self.clean_and_process_data_task()],
            verbose=True
        )
