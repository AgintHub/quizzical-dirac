from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import generate_insights_output

@CrewBase
class generate_insights_crew:
    """Crew for generate_insights operations."""


    @agent
    def generate_insights_agent(self):
        return Agent(
            role="Generate Insights Specialist",
            goal="""Execute generate_insights task accurately.
PRD Requirements:
- Integrate team performance metrics from calculate_team_performance_metrics node
- Analyze betting odds data from analyze_betting_odds node
- Determine recommended teams to bet on and avoid
- Generate summary of trends and patterns in betting odds
- Create insights on over/under rates and point spread distributions""",
            backstory="You are a specialized worker focused on Generate insights on NFL teams based on their performance metrics and betting odds analysis.",
            verbose=True
        )



    @task
    def generate_insights_task(self):
        """Task for generate_insights."""
        agent = self.generate_insights_agent()
        return Task(
            description="""Using {calculate_team_performance_metrics_output}, {analyze_betting_odds_output}, Generate insights on NFL teams based on their performance metrics and betting odds analysis.""",
            agent=agent,
            expected_output="""{
    recommended_teams_to_bet_on: list of strs  # List of team names recommended to bet on
    recommended_teams_to_avoid: list of strs  # List of team names recommended to avoid betting on
    top_performing_teams: list of strs  # List of top performing team names based on metrics
    worst_performing_teams: list of strs  # List of worst performing team names based on metrics
    betting_odds_trends: str  # Summary of trends and patterns in betting odds
    over_under_insights: str  # Insights on over/under rates
    point_spread_distribution: str  # Distribution of point spreads
}""",
            output_pydantic=generate_insights_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.generate_insights_agent()],
            tasks=[self.generate_insights_task()],
            verbose=True
        )
