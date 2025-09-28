import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_trading_results import analyze_trading_results
from code.backtest_trading_strategy import backtest_trading_strategy
from code.collect_historical_market_data import collect_historical_market_data
from code.configure_trading_infrastructure import configure_trading_infrastructure
from code.define_trading_strategy import define_trading_strategy
from code.execute_trades import execute_trades
from code.implement_risk_management import implement_risk_management
from code.monitor_trading_performance import monitor_trading_performance
from code.refine_trading_strategy import refine_trading_strategy

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

analyze_trading_results_async = make_async(analyze_trading_results)
backtest_trading_strategy_async = make_async(backtest_trading_strategy)
collect_historical_market_data_async = make_async(collect_historical_market_data)
configure_trading_infrastructure_async = make_async(configure_trading_infrastructure)
define_trading_strategy_async = make_async(define_trading_strategy)
execute_trades_async = make_async(execute_trades)
implement_risk_management_async = make_async(implement_risk_management)
monitor_trading_performance_async = make_async(monitor_trading_performance)
refine_trading_strategy_async = make_async(refine_trading_strategy)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: configure_trading_infrastructure, collect_historical_market_data
    async def run_configure_trading_infrastructure():
        # Call the async version of configure_trading_infrastructure with results from dependencies
        return await configure_trading_infrastructure_async(user_input)

    async def run_collect_historical_market_data():
        # Call the async version of collect_historical_market_data with results from dependencies
        return await collect_historical_market_data_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_configure_trading_infrastructure(), run_collect_historical_market_data())
    results['configure_trading_infrastructure'] = level_0_results[0]
    results['collect_historical_market_data'] = level_0_results[1]

    # Level 1: define_trading_strategy
    async def run_define_trading_strategy():
        # Call the async version of define_trading_strategy with results from dependencies
        return await define_trading_strategy_async(results['collect_historical_market_data'])

    # Run level 1 nodes in parallel
    results['define_trading_strategy'] = await run_define_trading_strategy()

    # Level 2: implement_risk_management, backtest_trading_strategy
    async def run_implement_risk_management():
        # Call the async version of implement_risk_management with results from dependencies
        return await implement_risk_management_async(results['define_trading_strategy'])

    async def run_backtest_trading_strategy():
        # Call the async version of backtest_trading_strategy with results from dependencies
        return await backtest_trading_strategy_async(results['define_trading_strategy'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_implement_risk_management(), run_backtest_trading_strategy())
    results['implement_risk_management'] = level_2_results[0]
    results['backtest_trading_strategy'] = level_2_results[1]

    # Level 3: execute_trades
    async def run_execute_trades():
        # Call the async version of execute_trades with results from dependencies
        return await execute_trades_async(results['backtest_trading_strategy'], results['configure_trading_infrastructure'], results['implement_risk_management'])

    # Run level 3 nodes in parallel
    results['execute_trades'] = await run_execute_trades()

    # Level 4: monitor_trading_performance
    async def run_monitor_trading_performance():
        # Call the async version of monitor_trading_performance with results from dependencies
        return await monitor_trading_performance_async(results['execute_trades'])

    # Run level 4 nodes in parallel
    results['monitor_trading_performance'] = await run_monitor_trading_performance()

    # Level 5: analyze_trading_results
    async def run_analyze_trading_results():
        # Call the async version of analyze_trading_results with results from dependencies
        return await analyze_trading_results_async(results['monitor_trading_performance'])

    # Run level 5 nodes in parallel
    results['analyze_trading_results'] = await run_analyze_trading_results()

    # Level 6: refine_trading_strategy
    async def run_refine_trading_strategy():
        # Call the async version of refine_trading_strategy with results from dependencies
        return await refine_trading_strategy_async(results['analyze_trading_results'])

    # Run level 6 nodes in parallel
    results['refine_trading_strategy'] = await run_refine_trading_strategy()

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
