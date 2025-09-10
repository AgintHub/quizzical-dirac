from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import summarize_analysis_results_output

@CrewBase
class summarize_analysis_results_crew:
    """Crew for summarize_analysis_results operations."""


    @agent
    def summarize_analysis_results_agent(self):
        return Agent(
            role="Summarize Analysis Results Specialist",
            goal="""Execute summarize_analysis_results task accurately.
PRD Requirements:
- Receive and aggregate output data from the generate_insights_and_recommendations node, including sector performance insights, trending stocks, investment opportunities, and portfolio adjustment recommendations.
- Receive and aggregate output data from the visualize_stock_market_data node, including stock price charts, sector performance plots, stock returns histogram, and volatility heatmap.
- Synthesize the aggregated data from both nodes to create an overall summary of the stock market analysis.
- Extract key findings from the analysis and present them in a list.
- Compile a list of insights gained from the analysis.
- Develop a list of recommendations for investors based on the analysis.
- Validate the analysis by checking for data consistency and accuracy.""",
            backstory="You are a specialized worker focused on Summarize the results of the stock market analysis.",
            verbose=True
        )



    @task
    def summarize_analysis_results_task(self):
        """Task for summarize_analysis_results."""
        agent = self.summarize_analysis_results_agent()
        return Task(
            description="""Using {generate_insights_and_recommendations_output}, {visualize_stock_market_data_output}, Summarize the results of the stock market analysis.""",
            agent=agent,
            expected_output="""{
    summary: str  # Overall summary of the stock market analysis
    key_findings: list of strs  # List of key findings from the analysis
    insights: list of strs  # List of insights gained from the analysis
    recommendations: list of strs  # List of recommendations for investors
    analysis_validity: bool  # Whether the analysis is valid and reliable
}""",
            output_pydantic=summarize_analysis_results_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.summarize_analysis_results_agent()],
            tasks=[self.summarize_analysis_results_task()],
            verbose=True
        )
