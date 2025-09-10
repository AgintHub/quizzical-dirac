# /// script
# dependencies = ["crewai==0.105.0"]
# ///
import sys
import logging
from crewai import Crew
from crews import *

class FilteredStream:
    # @traceable
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.filtered_messages = [
            "File not found:",
            "agents.yaml",
            "tasks.yaml"
        ]
        self.buffer = ""

    # @traceable
    def write(self, text):
        # Add to buffer
        self.buffer += text

        # If we have a complete line (ends with newline)
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            # Process all complete lines
            for line in lines[:-1]:
                if not any(msg in line for msg in self.filtered_messages):
                    self.original_stream.write(line + '\n')
            # Keep the last incomplete line in buffer
            self.buffer = lines[-1]

    # @traceable
    def flush(self):
        # Process any remaining buffer content
        if self.buffer and not any(msg in self.buffer for msg in self.filtered_messages):
            self.original_stream.write(self.buffer)
        self.buffer = ""
        self.original_stream.flush()

# Redirect stdout to our filtered stream
sys.stdout = FilteredStream(sys.stdout)

# Suppress CrewAI configuration warnings
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)
import os
import asyncio
from typing import Dict
from crewai import Crew

from crews.analyze_betting_odds_crew import analyze_betting_odds_crew
from crews.calculate_team_performance_metrics_crew import calculate_team_performance_metrics_crew
from crews.clean_and_process_data_crew import clean_and_process_data_crew
from crews.collect_betting_odds_data_crew import collect_betting_odds_data_crew
from crews.collect_nfl_teams_data_crew import collect_nfl_teams_data_crew
from crews.generate_insights_crew import generate_insights_crew
from crews.visualize_results_crew import visualize_results_crew


# @traceable
async def run_workflow(inputs: Dict = None, openai_api_key: str = None):
    """Execute the full workflow."""
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    elif not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key must be provided")

    if inputs is None:
        inputs = {}

    results = {}
    crews = {}
    crews["analyze_betting_odds"] = analyze_betting_odds_crew().crew()
    crews["calculate_team_performance_metrics"] = calculate_team_performance_metrics_crew().crew()
    crews["clean_and_process_data"] = clean_and_process_data_crew().crew()
    crews["collect_betting_odds_data"] = collect_betting_odds_data_crew().crew()
    crews["collect_nfl_teams_data"] = collect_nfl_teams_data_crew().crew()
    crews["generate_insights"] = generate_insights_crew().crew()
    crews["visualize_results"] = visualize_results_crew().crew()

    # Level 0 execution
    results["collect_betting_odds_data"] = await crews["collect_betting_odds_data"].kickoff_async(inputs=inputs)
    results["collect_nfl_teams_data"] = await crews["collect_nfl_teams_data"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["clean_and_process_data"].kickoff_async(inputs={"collect_nfl_teams_data_output": results["collect_nfl_teams_data"].raw, "collect_betting_odds_data_output": results["collect_betting_odds_data"].raw}))
    for node_name, result in zip(['clean_and_process_data'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["analyze_betting_odds"].kickoff_async(inputs={"clean_and_process_data_output": results["clean_and_process_data"].raw}), crews["calculate_team_performance_metrics"].kickoff_async(inputs={"clean_and_process_data_output": results["clean_and_process_data"].raw}))
    for node_name, result in zip(['analyze_betting_odds', 'calculate_team_performance_metrics'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["generate_insights"].kickoff_async(inputs={"calculate_team_performance_metrics_output": results["calculate_team_performance_metrics"].raw, "analyze_betting_odds_output": results["analyze_betting_odds"].raw}))
    for node_name, result in zip(['generate_insights'], level_results):
        results[node_name] = result

    # Level 4 execution
    level_results = await asyncio.gather(crews["visualize_results"].kickoff_async(inputs={"generate_insights_output": results["generate_insights"].raw}))
    for node_name, result in zip(['visualize_results'], level_results):
        results[node_name] = result

    return results

# @traceable
def run_workflow_sync(inputs: Dict = None, openai_api_key: str = None):
    """Synchronous version of run_workflow."""
    return asyncio.run(run_workflow(inputs, openai_api_key))

if __name__ == "__main__":
    import sys
    import json

    api_key = os.getenv("OPENAI_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not api_key:
        print("Please provide OpenAI API key")
        sys.exit(1)

    print("Provide any runtime inputs/params/args/context in raw text or JSON format (press Enter for empty input):")
    user_input = input().strip()

    inputs = {"input": user_input} if user_input else {}

    try:
        if user_input:
            # Try to parse as JSON if provided
            json_input = json.loads(user_input)
            inputs = {"input": json_input}
    except json.JSONDecodeError:
        # If not valid JSON, use the raw string
        pass

    results = run_workflow_sync(inputs, openai_api_key=api_key)
