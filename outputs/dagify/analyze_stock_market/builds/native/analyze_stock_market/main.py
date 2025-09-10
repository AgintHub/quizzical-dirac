import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_sector_performance import analyze_sector_performance
from code.calculate_stock_metrics import calculate_stock_metrics
from code.clean_and_process_stock_data import clean_and_process_stock_data
from code.generate_insights_and_recommendations import generate_insights_and_recommendations
from code.identify_trending_stocks import identify_trending_stocks
from code.retrieve_historical_stock_data import retrieve_historical_stock_data
from code.summarize_analysis_results import summarize_analysis_results
from code.visualize_stock_market_data import visualize_stock_market_data

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

analyze_sector_performance_async = make_async(analyze_sector_performance)
calculate_stock_metrics_async = make_async(calculate_stock_metrics)
clean_and_process_stock_data_async = make_async(clean_and_process_stock_data)
generate_insights_and_recommendations_async = make_async(generate_insights_and_recommendations)
identify_trending_stocks_async = make_async(identify_trending_stocks)
retrieve_historical_stock_data_async = make_async(retrieve_historical_stock_data)
summarize_analysis_results_async = make_async(summarize_analysis_results)
visualize_stock_market_data_async = make_async(visualize_stock_market_data)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: retrieve_historical_stock_data
    async def run_retrieve_historical_stock_data():
        # Call the async version of retrieve_historical_stock_data with results from dependencies
        return await retrieve_historical_stock_data_async(user_input)

    # Run level 0 nodes in parallel
    results['retrieve_historical_stock_data'] = await run_retrieve_historical_stock_data()

    # Level 1: clean_and_process_stock_data
    async def run_clean_and_process_stock_data():
        # Call the async version of clean_and_process_stock_data with results from dependencies
        return await clean_and_process_stock_data_async(results['retrieve_historical_stock_data'])

    # Run level 1 nodes in parallel
    results['clean_and_process_stock_data'] = await run_clean_and_process_stock_data()

    # Level 2: calculate_stock_metrics
    async def run_calculate_stock_metrics():
        # Call the async version of calculate_stock_metrics with results from dependencies
        return await calculate_stock_metrics_async(results['clean_and_process_stock_data'])

    # Run level 2 nodes in parallel
    results['calculate_stock_metrics'] = await run_calculate_stock_metrics()

    # Level 3: identify_trending_stocks, analyze_sector_performance
    async def run_identify_trending_stocks():
        # Call the async version of identify_trending_stocks with results from dependencies
        return await identify_trending_stocks_async(results['calculate_stock_metrics'])

    async def run_analyze_sector_performance():
        # Call the async version of analyze_sector_performance with results from dependencies
        return await analyze_sector_performance_async(results['calculate_stock_metrics'])

    # Run level 3 nodes in parallel
    level_3_results = await asyncio.gather(run_identify_trending_stocks(), run_analyze_sector_performance())
    results['identify_trending_stocks'] = level_3_results[0]
    results['analyze_sector_performance'] = level_3_results[1]

    # Level 4: generate_insights_and_recommendations, visualize_stock_market_data
    async def run_generate_insights_and_recommendations():
        # Call the async version of generate_insights_and_recommendations with results from dependencies
        return await generate_insights_and_recommendations_async(results['analyze_sector_performance'], results['identify_trending_stocks'])

    async def run_visualize_stock_market_data():
        # Call the async version of visualize_stock_market_data with results from dependencies
        return await visualize_stock_market_data_async(results['calculate_stock_metrics'], results['analyze_sector_performance'])

    # Run level 4 nodes in parallel
    level_4_results = await asyncio.gather(run_generate_insights_and_recommendations(), run_visualize_stock_market_data())
    results['generate_insights_and_recommendations'] = level_4_results[0]
    results['visualize_stock_market_data'] = level_4_results[1]

    # Level 5: summarize_analysis_results
    async def run_summarize_analysis_results():
        # Call the async version of summarize_analysis_results with results from dependencies
        return await summarize_analysis_results_async(results['generate_insights_and_recommendations'], results['visualize_stock_market_data'])

    # Run level 5 nodes in parallel
    results['summarize_analysis_results'] = await run_summarize_analysis_results()

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
