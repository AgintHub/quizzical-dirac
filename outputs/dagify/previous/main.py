import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.collect_order_book_data import collect_order_book_data
from code.generate_trading_signals import generate_trading_signals
from code.send_buy_orders import send_buy_orders
from code.send_sell_orders import send_sell_orders
from code.record_trade_performance import record_trade_performance
from code.analyze_trading_performance import analyze_trading_performance

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

collect_order_book_data_async = make_async(collect_order_book_data)
generate_trading_signals_async = make_async(generate_trading_signals)
send_buy_orders_async = make_async(send_buy_orders)
send_sell_orders_async = make_async(send_sell_orders)
record_trade_performance_async = make_async(record_trade_performance)
analyze_trading_performance_async = make_async(analyze_trading_performance)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: collect_order_book_data
    async def run_collect_order_book_data():
        # Call the async version of collect_order_book_data with results from dependencies
        return await collect_order_book_data_async(user_input)

    # Run level 0 nodes in parallel
    results['collect_order_book_data'] = await run_collect_order_book_data()

    # Level 1: generate_trading_signals
    async def run_generate_trading_signals():
        # Call the async version of generate_trading_signals with results from dependencies
        return await generate_trading_signals_async(results['collect_order_book_data'])

    # Run level 1 nodes in parallel
    results['generate_trading_signals'] = await run_generate_trading_signals()

    # Level 2: send_buy_orders, send_sell_orders
    async def run_send_buy_orders():
        # Call the async version of send_buy_orders with results from dependencies
        return await send_buy_orders_async(results['generate_trading_signals'])

    async def run_send_sell_orders():
        # Call the async version of send_sell_orders with results from dependencies
        return await send_sell_orders_async(results['generate_trading_signals'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_send_buy_orders(), run_send_sell_orders())
    results['send_buy_orders'] = level_2_results[0]
    results['send_sell_orders'] = level_2_results[1]

    # Level 3: record_trade_performance
    async def run_record_trade_performance():
        # Call the async version of record_trade_performance with results from dependencies
        return await record_trade_performance_async(results['send_buy_orders'], results['send_sell_orders'])

    # Run level 3 nodes in parallel
    results['record_trade_performance'] = await run_record_trade_performance()

    # Level 4: analyze_trading_performance
    async def run_analyze_trading_performance():
        # Call the async version of analyze_trading_performance with results from dependencies
        return await analyze_trading_performance_async(results['record_trade_performance'])

    # Run level 4 nodes in parallel
    results['analyze_trading_performance'] = await run_analyze_trading_performance()

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
