from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import retrieve_historical_stock_data_output

@CrewBase
class retrieve_historical_stock_data_crew:
    """Crew for retrieve_historical_stock_data operations."""


    @agent
    def retrieve_historical_stock_data_agent(self):
        return Agent(
            role="Retrieve Historical Stock Data Specialist",
            goal="""Execute retrieve_historical_stock_data task accurately.
PRD Requirements:
- Use the Yahoo Finance API to retrieve historical stock prices for the specified stocks and indices.
- Handle API request errors and exceptions.
- Validate the retrieved data to ensure it conforms to the expected format.
- Store the retrieved data in a suitable data structure for further processing.""",
            backstory="You are a specialized worker focused on Retrieve historical stock prices for major indices and stocks.",
            verbose=True
        )



    @task
    def retrieve_historical_stock_data_task(self):
        """Task for retrieve_historical_stock_data."""
        agent = self.retrieve_historical_stock_data_agent()
        return Task(
            description="""Using {input}, Retrieve historical stock prices for major indices and stocks.""",
            agent=agent,
            expected_output="""{
    stock_symbol: str  # Stock symbol (e.g., AAPL, GOOG, SP500)
    historical_prices: list of floats  # List of daily closing prices over the past year
    date: str  # Date in 'YYYY-MM-DD' format
    is_valid: bool  # Whether the retrieved data is valid
}""",
            output_pydantic=retrieve_historical_stock_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.retrieve_historical_stock_data_agent()],
            tasks=[self.retrieve_historical_stock_data_task()],
            verbose=True
        )
