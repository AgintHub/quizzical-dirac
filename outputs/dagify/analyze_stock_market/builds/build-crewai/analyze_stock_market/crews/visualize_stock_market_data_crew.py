from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import visualize_stock_market_data_output

@CrewBase
class visualize_stock_market_data_crew:
    """Crew for visualize_stock_market_data operations."""


    @agent
    def visualize_stock_market_data_agent(self):
        return Agent(
            role="Visualize Stock Market Data Specialist",
            goal="""Execute visualize_stock_market_data task accurately.
PRD Requirements:
- Use matplotlib and seaborn libraries to create visualizations
- Create stock price charts using daily returns data from calculate_stock_metrics
- Create sector performance plots using sector-level metrics from analyze_sector_performance
- Create stock returns histogram using daily returns data from calculate_stock_metrics
- Create volatility heatmap using volatility data from calculate_stock_metrics""",
            backstory="You are a specialized worker focused on Visualize key stock market data and insights.",
            verbose=True
        )



    @task
    def visualize_stock_market_data_task(self):
        """Task for visualize_stock_market_data."""
        agent = self.visualize_stock_market_data_agent()
        return Task(
            description="""Using {calculate_stock_metrics_output}, {analyze_sector_performance_output}, Visualize key stock market data and insights.""",
            agent=agent,
            expected_output="""{
    stock_price_charts: list of strs  # List of file paths or URLs to stock price charts
    sector_performance_plots: list of strs  # List of file paths or URLs to sector performance plots
    stock_returns_histogram: str  # File path or URL to stock returns histogram
    volatility_heatmap: str  # File path or URL to volatility heatmap
    sector_average_returns: list of floats  # List of average returns for each sector
    sector_volatility: list of floats  # List of volatility measures for each sector
}""",
            output_pydantic=visualize_stock_market_data_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.visualize_stock_market_data_agent()],
            tasks=[self.visualize_stock_market_data_task()],
            verbose=True
        )
