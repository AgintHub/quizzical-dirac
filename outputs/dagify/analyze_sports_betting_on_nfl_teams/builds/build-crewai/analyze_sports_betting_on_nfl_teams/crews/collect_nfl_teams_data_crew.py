from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import collect_nfl_teams_data_output

@CrewBase
class collect_nfl_teams_data_crew:
    """Crew for collect_nfl_teams_data operations."""


    @agent
    def collect_nfl_teams_data_agent(self):
        return Agent(
            role="Collect Nfl Teams Data Specialist",
            goal="""Execute collect_nfl_teams_data task accurately.
PRD Requirements:
- Collect NFL teams data from a reliable source such as the official NFL website or a sports data API
- Extract relevant data points for each team, including team name, win-loss record, points scored, and standings
- Clean and preprocess the data to handle missing values and outliers
- Organize the data into a structured format, including a list of teams with their corresponding data""",
            backstory="You are a specialized worker focused on Collect data on NFL teams, including their performance, standings, and statistics.",
            verbose=True
        )



    @task
    def collect_nfl_teams_data_task(self):
        """Task for collect_nfl_teams_data."""
        agent = self.collect_nfl_teams_data_agent()
        return Task(
            description="""Using {input}, Collect data on NFL teams, including their performance, standings, and statistics.""",
            agent=agent,
            expected_output="""{
    team_name: str  # Name of the NFL team
    win_loss_record: str  # Win-loss record of the team (e.g., 10-5)
    points_scored: int  # Total points scored by the team
    standings: str  # Current standings of the team (e.g., 1st in division)
    statistics: str  # List of additional statistics for the team (e.g., passing yards, rushing yards, etc.)
}""",
            output_pydantic=collect_nfl_teams_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.collect_nfl_teams_data_agent()],
            tasks=[self.collect_nfl_teams_data_task()],
            verbose=True
        )
