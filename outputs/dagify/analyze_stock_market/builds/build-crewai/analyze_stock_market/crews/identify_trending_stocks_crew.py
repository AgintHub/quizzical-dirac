from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_trending_stocks_output

@CrewBase
class identify_trending_stocks_crew:
    """Crew for identify_trending_stocks operations."""


    @agent
    def identify_trending_stocks_agent(self):
        return Agent(
            role="Identify Trending Stocks Specialist",
            goal="""Execute identify_trending_stocks task accurately.
PRD Requirements:
- Retrieve the list of stock symbols and their calculated metrics from the output of the calculate_stock_metrics node.
- Calculate the short-term trend (50-day) for each stock by comparing the current price to the 50-day moving average.
- Calculate the long-term trend (200-day) for each stock by comparing the current price to the 200-day moving average.
- Determine the overall trend for each stock based on the short-term and long-term trends.
- Calculate the trend confidence score for each stock based on the strength of the trend.
- Output the list of stocks with their corresponding trends, trend confidence scores, short-term trends, and long-term trends.""",
            backstory="You are a specialized worker focused on Identify stocks that are trending upwards or downwards.",
            verbose=True
        )



    @task
    def identify_trending_stocks_task(self):
        """Task for identify_trending_stocks."""
        agent = self.identify_trending_stocks_agent()
        return Task(
            description="""Using {calculate_stock_metrics_output}, Identify stocks that are trending upwards or downwards.""",
            agent=agent,
            expected_output="""{
    stock_symbol: str  # The symbol of the stock (e.g., AAPL, GOOGL)
    trend: str  # The trend identifier (e.g., upward, downward)
    trend_confidence: float  # A confidence score for the trend (e.g., 0.8 for a strong upward trend)
    short_term_trend: str  # The short-term trend (50-day) identifier (e.g., upward, downward)
    long_term_trend: str  # The long-term trend (200-day) identifier (e.g., upward, downward)
}""",
            output_pydantic=identify_trending_stocks_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_trending_stocks_agent()],
            tasks=[self.identify_trending_stocks_task()],
            verbose=True
        )
