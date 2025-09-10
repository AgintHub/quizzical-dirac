from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import collect_betting_odds_data_output

@CrewBase
class collect_betting_odds_data_crew:
    """Crew for collect_betting_odds_data operations."""


    @agent
    def collect_betting_odds_data_agent(self):
        return Agent(
            role="Collect Betting Odds Data Specialist",
            goal="""Execute collect_betting_odds_data task accurately.
PRD Requirements:
- Use a web scraping library such as BeautifulSoup or Scrapy to collect data on sports betting odds from a reliable online sportsbook.
- Identify and extract relevant data points including team names, point spreads, moneyline odds, and over/under odds.
- Store the collected data in a structured format such as a pandas DataFrame or a SQL database.
- Implement data validation to ensure that the collected data is accurate and consistent.""",
            backstory="You are a specialized worker focused on Collect data on sports betting odds for NFL teams, including point spreads, moneylines, and over/unders.",
            verbose=True
        )



    @task
    def collect_betting_odds_data_task(self):
        """Task for collect_betting_odds_data."""
        agent = self.collect_betting_odds_data_agent()
        return Task(
            description="""Using {input}, Collect data on sports betting odds for NFL teams, including point spreads, moneylines, and over/unders.""",
            agent=agent,
            expected_output="""{
    teams: list of strs  # List of NFL team names
    point_spreads: list of floats  # List of point spreads corresponding to each team
    moneylines: list of floats  # List of moneyline odds corresponding to each team
    over_unders: list of floats  # List of over/under odds corresponding to each team
}""",
            output_pydantic=collect_betting_odds_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.collect_betting_odds_data_agent()],
            tasks=[self.collect_betting_odds_data_task()],
            verbose=True
        )
