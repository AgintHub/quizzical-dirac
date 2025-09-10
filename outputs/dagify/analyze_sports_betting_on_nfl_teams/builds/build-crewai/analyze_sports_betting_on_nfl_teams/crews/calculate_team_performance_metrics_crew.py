from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import calculate_team_performance_metrics_output

@CrewBase
class calculate_team_performance_metrics_crew:
    """Crew for calculate_team_performance_metrics operations."""


    @agent
    def calculate_team_performance_metrics_agent(self):
        return Agent(
            role="Calculate Team Performance Metrics Specialist",
            goal="""Execute calculate_team_performance_metrics task accurately.
PRD Requirements:
- Retrieve cleaned team data from the output of the clean_and_process_data node
- Calculate win rates for each team using their win-loss records
- Calculate points scored and allowed for each team
- Calculate yards gained for each team
- Compile the calculated metrics into a list of teams with their corresponding metrics""",
            backstory="You are a specialized worker focused on Calculate performance metrics for NFL teams, including their win rates, points scored, and other relevant statistics.",
            verbose=True
        )



    @task
    def calculate_team_performance_metrics_task(self):
        """Task for calculate_team_performance_metrics."""
        agent = self.calculate_team_performance_metrics_agent()
        return Task(
            description="""Using {clean_and_process_data_output}, Calculate performance metrics for NFL teams, including their win rates, points scored, and other relevant statistics.""",
            agent=agent,
            expected_output="""{
    team_names: list of strs  # List of NFL team names
    win_rates: list of floats  # List of win rates for each team, ranging from 0 to 1
    points_scored: list of ints  # List of points scored by each team
    points_allowed: list of ints  # List of points allowed by each team
    yards_gained: list of ints  # List of yards gained by each team
}""",
            output_pydantic=calculate_team_performance_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.calculate_team_performance_metrics_agent()],
            tasks=[self.calculate_team_performance_metrics_task()],
            verbose=True
        )
