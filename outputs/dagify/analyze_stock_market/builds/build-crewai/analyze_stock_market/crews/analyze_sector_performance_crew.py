from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import analyze_sector_performance_output

@CrewBase
class analyze_sector_performance_crew:
    """Crew for analyze_sector_performance operations."""


    @agent
    def analyze_sector_performance_agent(self):
        return Agent(
            role="Analyze Sector Performance Specialist",
            goal="""Execute analyze_sector_performance task accurately.
PRD Requirements:
- Group stocks by sector using a dictionary where the keys are sector names and the values are lists of stock symbols.
- Calculate average returns for each sector using the daily returns of the stocks in that sector.
- Calculate volatility (standard deviation of returns) for each sector using the daily returns of the stocks in that sector.
- Count the number of stocks in each sector.
- Validate the sector performance data by checking for missing or invalid values.""",
            backstory="You are a specialized worker focused on Analyze the performance of different sectors in the stock market.",
            verbose=True
        )



    @task
    def analyze_sector_performance_task(self):
        """Task for analyze_sector_performance."""
        agent = self.analyze_sector_performance_agent()
        return Task(
            description="""Using {calculate_stock_metrics_output}, Analyze the performance of different sectors in the stock market.""",
            agent=agent,
            expected_output="""{
    sector_performance: list of strs  # List of sector names (e.g., technology, healthcare, finance)
    sector_average_returns: list of floats  # List of average returns for each sector
    sector_volatility: list of floats  # List of volatility (standard deviation of returns) for each sector
    sector_counts: list of ints  # List of stock counts for each sector
    is_valid: bool  # Whether the sector performance data is valid
}""",
            output_pydantic=analyze_sector_performance_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.analyze_sector_performance_agent()],
            tasks=[self.analyze_sector_performance_task()],
            verbose=True
        )
