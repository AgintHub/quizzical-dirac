import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_betting_odds import analyze_betting_odds
from code.calculate_team_performance_metrics import calculate_team_performance_metrics
from code.clean_and_process_data import clean_and_process_data
from code.collect_betting_odds_data import collect_betting_odds_data
from code.collect_nfl_teams_data import collect_nfl_teams_data
from code.generate_insights import generate_insights
from code.visualize_results import visualize_results

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

analyze_betting_odds_async = make_async(analyze_betting_odds)
calculate_team_performance_metrics_async = make_async(calculate_team_performance_metrics)
clean_and_process_data_async = make_async(clean_and_process_data)
collect_betting_odds_data_async = make_async(collect_betting_odds_data)
collect_nfl_teams_data_async = make_async(collect_nfl_teams_data)
generate_insights_async = make_async(generate_insights)
visualize_results_async = make_async(visualize_results)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: collect_betting_odds_data, collect_nfl_teams_data
    async def run_collect_betting_odds_data():
        # Call the async version of collect_betting_odds_data with results from dependencies
        return await collect_betting_odds_data_async(user_input)

    async def run_collect_nfl_teams_data():
        # Call the async version of collect_nfl_teams_data with results from dependencies
        return await collect_nfl_teams_data_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_collect_betting_odds_data(), run_collect_nfl_teams_data())
    results['collect_betting_odds_data'] = level_0_results[0]
    results['collect_nfl_teams_data'] = level_0_results[1]

    # Level 1: clean_and_process_data
    async def run_clean_and_process_data():
        # Call the async version of clean_and_process_data with results from dependencies
        return await clean_and_process_data_async(results['collect_nfl_teams_data'], results['collect_betting_odds_data'])

    # Run level 1 nodes in parallel
    results['clean_and_process_data'] = await run_clean_and_process_data()

    # Level 2: calculate_team_performance_metrics, analyze_betting_odds
    async def run_calculate_team_performance_metrics():
        # Call the async version of calculate_team_performance_metrics with results from dependencies
        return await calculate_team_performance_metrics_async(results['clean_and_process_data'])

    async def run_analyze_betting_odds():
        # Call the async version of analyze_betting_odds with results from dependencies
        return await analyze_betting_odds_async(results['clean_and_process_data'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_calculate_team_performance_metrics(), run_analyze_betting_odds())
    results['calculate_team_performance_metrics'] = level_2_results[0]
    results['analyze_betting_odds'] = level_2_results[1]

    # Level 3: generate_insights
    async def run_generate_insights():
        # Call the async version of generate_insights with results from dependencies
        return await generate_insights_async(results['calculate_team_performance_metrics'], results['analyze_betting_odds'])

    # Run level 3 nodes in parallel
    results['generate_insights'] = await run_generate_insights()

    # Level 4: visualize_results
    async def run_visualize_results():
        # Call the async version of visualize_results with results from dependencies
        return await visualize_results_async(results['generate_insights'])

    # Run level 4 nodes in parallel
    results['visualize_results'] = await run_visualize_results()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
