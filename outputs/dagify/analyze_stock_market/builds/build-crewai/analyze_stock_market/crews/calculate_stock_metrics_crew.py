from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import calculate_stock_metrics_output

@CrewBase
class calculate_stock_metrics_crew:
    """Crew for calculate_stock_metrics operations."""


    @agent
    def calculate_stock_metrics_agent(self):
        return Agent(
            role="Calculate Stock Metrics Specialist",
            goal="""Execute calculate_stock_metrics task accurately.
PRD Requirements:
- Retrieve cleaned and processed stock data from the output of the clean_and_process_stock_data node.
- Calculate daily returns for each stock using the formula: (current_price - previous_price) / previous_price.
- Calculate volatility (standard deviation of returns) for each stock using a 30-day window.
- Calculate 50-day and 200-day moving averages for each stock using the formula: moving_average = (sum(prices) / number_of_days).
- Store the calculated metrics in the output structure.""",
            backstory="You are a specialized worker focused on Calculate key metrics for each stock, such as daily returns and volatility.",
            verbose=True
        )



    @task
    def calculate_stock_metrics_task(self):
        """Task for calculate_stock_metrics."""
        agent = self.calculate_stock_metrics_agent()
        return Task(
            description="""Using {clean_and_process_stock_data_output}, Calculate key metrics for each stock, such as daily returns and volatility.""",
            agent=agent,
            expected_output="""{
    stock_metrics: list of strs  # List of stock symbols with calculated metrics
    daily_returns: list of floats  # List of daily returns for each stock
    volatility: list of floats  # List of volatility (standard deviation of returns) for each stock
    moving_averages_50_day: list of floats  # List of 50-day moving averages for each stock
    moving_averages_200_day: list of floats  # List of 200-day moving averages for each stock
}""",
            output_pydantic=calculate_stock_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.calculate_stock_metrics_agent()],
            tasks=[self.calculate_stock_metrics_task()],
            verbose=True
        )
