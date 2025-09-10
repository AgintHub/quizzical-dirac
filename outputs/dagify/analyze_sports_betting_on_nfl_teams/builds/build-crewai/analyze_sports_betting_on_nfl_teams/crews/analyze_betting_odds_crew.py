from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import analyze_betting_odds_output

@CrewBase
class analyze_betting_odds_crew:
    """Crew for analyze_betting_odds operations."""


    @agent
    def analyze_betting_odds_agent(self):
        return Agent(
            role="Analyze Betting Odds Specialist",
            goal="""Execute analyze_betting_odds task accurately.
PRD Requirements:
- Load and validate the cleaned and processed data from the clean_and_process_data node
- Calculate the over/under rates for each team using the cleaned and processed data
- Calculate the point spread distributions for each team using the cleaned and processed data
- Identify trends and patterns in the betting odds data using statistical methods and data visualization techniques
- Generate insights on the betting odds, including recommendations""",
            backstory="You are a specialized worker focused on Analyze the sports betting odds data to identify trends and patterns, and provide insights on the odds.",
            verbose=True
        )



    @task
    def analyze_betting_odds_task(self):
        """Task for analyze_betting_odds."""
        agent = self.analyze_betting_odds_agent()
        return Task(
            description="""Using {clean_and_process_data_output}, Analyze the sports betting odds data to identify trends and patterns, and provide insights on the odds.""",
            agent=agent,
            expected_output="""{
    over_under_rates: list of floats  # List of over/under rates for each team
    point_spread_distributions: list of floats  # List of point spread distributions for each team
    trends_and_patterns: str  # Description of trends and patterns identified in the betting odds data
    insights: str  # Insights on the betting odds, including recommendations
    is_data_valid: bool  # Whether the data is valid for analysis
}""",
            output_pydantic=analyze_betting_odds_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.analyze_betting_odds_agent()],
            tasks=[self.analyze_betting_odds_task()],
            verbose=True
        )
