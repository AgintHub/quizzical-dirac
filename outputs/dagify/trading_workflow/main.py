import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.fetch_market_data import fetch_market_data
from code.analyze_market_trends import analyze_market_trends
from code.calculate_trading_indicators import calculate_trading_indicators
from code.generate_trading_signals import generate_trading_signals
from code.execute_trades import execute_trades

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

fetch_market_data_async = make_async(fetch_market_data)
analyze_market_trends_async = make_async(analyze_market_trends)
calculate_trading_indicators_async = make_async(calculate_trading_indicators)
generate_trading_signals_async = make_async(generate_trading_signals)
execute_trades_async = make_async(execute_trades)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: fetch_market_data
    async def run_fetch_market_data():
        # Call the async version of fetch_market_data with results from dependencies
        return await fetch_market_data_async(user_input)

    # Run level 0 nodes in parallel
    results['fetch_market_data'] = await run_fetch_market_data()

    # Level 1: analyze_market_trends, calculate_trading_indicators
    async def run_analyze_market_trends():
        # Call the async version of analyze_market_trends with results from dependencies
        return await analyze_market_trends_async(results['fetch_market_data'])

    async def run_calculate_trading_indicators():
        # Call the async version of calculate_trading_indicators with results from dependencies
        return await calculate_trading_indicators_async(results['fetch_market_data'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_analyze_market_trends(), run_calculate_trading_indicators())
    results['analyze_market_trends'] = level_1_results[0]
    results['calculate_trading_indicators'] = level_1_results[1]

    # Level 2: generate_trading_signals
    async def run_generate_trading_signals():
        # Call the async version of generate_trading_signals with results from dependencies
        return await generate_trading_signals_async(results['analyze_market_trends'], results['calculate_trading_indicators'])

    # Run level 2 nodes in parallel
    results['generate_trading_signals'] = await run_generate_trading_signals()

    # Level 3: execute_trades
    async def run_execute_trades():
        # Call the async version of execute_trades with results from dependencies
        return await execute_trades_async(results['generate_trading_signals'])

    # Run level 3 nodes in parallel
    results['execute_trades'] = await run_execute_trades()

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
