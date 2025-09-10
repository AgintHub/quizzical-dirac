from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import clean_and_process_stock_data_output

@CrewBase
class clean_and_process_stock_data_crew:
    """Crew for clean_and_process_stock_data operations."""


    @agent
    def clean_and_process_stock_data_agent(self):
        return Agent(
            role="Clean And Process Stock Data Specialist",
            goal="""Execute clean_and_process_stock_data task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Clean and process the retrieved stock data.",
            verbose=True
        )



    @task
    def clean_and_process_stock_data_task(self):
        """Task for clean_and_process_stock_data."""
        agent = self.clean_and_process_stock_data_agent()
        return Task(
            description="""Using {retrieve_historical_stock_data_output}, Clean and process the retrieved stock data.""",
            agent=agent,
            expected_output="""{
    cleaned_data: list of floats  # List of cleaned stock prices
    processed_data: list of floats  # List of processed stock prices with normalized values
    date_formats: str  # List of date formats used for conversion
    missing_value_handling_status: bool  # Whether missing values were handled successfully
}""",
            output_pydantic=clean_and_process_stock_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.clean_and_process_stock_data_agent()],
            tasks=[self.clean_and_process_stock_data_task()],
            verbose=True
        )
