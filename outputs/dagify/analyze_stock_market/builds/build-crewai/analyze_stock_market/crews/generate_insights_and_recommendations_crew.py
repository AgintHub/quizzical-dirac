from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import generate_insights_and_recommendations_output

@CrewBase
class generate_insights_and_recommendations_crew:
    """Crew for generate_insights_and_recommendations operations."""


    @agent
    def generate_insights_and_recommendations_agent(self):
        return Agent(
            role="Generate Insights And Recommendations Specialist",
            goal="""Execute generate_insights_and_recommendations task accurately.
PRD Requirements:
- Integrate sector performance data from analyze_sector_performance node
- Integrate trending stock data from identify_trending_stocks node
- Analyze sector performance data to identify potential investment opportunities
- Generate recommendations for portfolio adjustments based on analysis results
- Summarize analysis results and insights into a comprehensive report""",
            backstory="You are a specialized worker focused on Generate insights and recommendations based on the analysis.",
            verbose=True
        )



    @task
    def generate_insights_and_recommendations_task(self):
        """Task for generate_insights_and_recommendations."""
        agent = self.generate_insights_and_recommendations_agent()
        return Task(
            description="""Using {analyze_sector_performance_output}, {identify_trending_stocks_output}, Generate insights and recommendations based on the analysis.""",
            agent=agent,
            expected_output="""{
    sector_performance_insights: str  # Summary of sector performance insights
    trending_stocks: list of strs  # List of trending stocks with their direction (up or down)
    investment_opportunities: list of strs  # List of potential investment opportunities
    portfolio_adjustment_recommendations: list of strs  # List of recommendations for portfolio adjustments
    analysis_summary: str  # Summary of the analysis
}""",
            output_pydantic=generate_insights_and_recommendations_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.generate_insights_and_recommendations_agent()],
            tasks=[self.generate_insights_and_recommendations_task()],
            verbose=True
        )
