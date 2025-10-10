import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.gather_market_data import gather_market_data
from code.analyze_market_trends import analyze_market_trends
from code.evaluate_risk_factors import evaluate_risk_factors
from code.formulate_trading_strategy import formulate_trading_strategy
from code.execute_trades import execute_trades
from code.monitor_and_adjust import monitor_and_adjust

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

gather_market_data_async = make_async(gather_market_data)
analyze_market_trends_async = make_async(analyze_market_trends)
evaluate_risk_factors_async = make_async(evaluate_risk_factors)
formulate_trading_strategy_async = make_async(formulate_trading_strategy)
execute_trades_async = make_async(execute_trades)
monitor_and_adjust_async = make_async(monitor_and_adjust)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: gather_market_data
    async def run_gather_market_data():
        # Call the async version of gather_market_data with results from dependencies
        return await gather_market_data_async(user_input)

    # Run level 0 nodes in parallel
    results['gather_market_data'] = await run_gather_market_data()

    # Level 1: analyze_market_trends, evaluate_risk_factors
    async def run_analyze_market_trends():
        # Call the async version of analyze_market_trends with results from dependencies
        return await analyze_market_trends_async(results['gather_market_data'])

    async def run_evaluate_risk_factors():
        # Call the async version of evaluate_risk_factors with results from dependencies
        return await evaluate_risk_factors_async(results['gather_market_data'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_analyze_market_trends(), run_evaluate_risk_factors())
    results['analyze_market_trends'] = level_1_results[0]
    results['evaluate_risk_factors'] = level_1_results[1]

    # Level 2: formulate_trading_strategy
    async def run_formulate_trading_strategy():
        # Call the async version of formulate_trading_strategy with results from dependencies
        return await formulate_trading_strategy_async(results['analyze_market_trends'], results['evaluate_risk_factors'])

    # Run level 2 nodes in parallel
    results['formulate_trading_strategy'] = await run_formulate_trading_strategy()

    # Level 3: execute_trades
    async def run_execute_trades():
        # Call the async version of execute_trades with results from dependencies
        return await execute_trades_async(results['formulate_trading_strategy'])

    # Run level 3 nodes in parallel
    results['execute_trades'] = await run_execute_trades()

    # Level 4: monitor_and_adjust
    async def run_monitor_and_adjust():
        # Call the async version of monitor_and_adjust with results from dependencies
        return await monitor_and_adjust_async(results['execute_trades'])

    # Run level 4 nodes in parallel
    results['monitor_and_adjust'] = await run_monitor_and_adjust()

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
