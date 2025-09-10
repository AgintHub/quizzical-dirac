import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.choose_trading_strategy import choose_trading_strategy
from code.compile_trading_dashboard_outline import compile_trading_dashboard_outline
from code.define_asset_universe import define_asset_universe
from code.define_trading_objectives import define_trading_objectives
from code.define_trading_performance_metrics import define_trading_performance_metrics
from code.design_risk_management_framework import design_risk_management_framework
from code.develop_trading_plan import develop_trading_plan
from code.produce_final_trading_report import produce_final_trading_report
from code.set_trading_parameters import set_trading_parameters

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

choose_trading_strategy_async = make_async(choose_trading_strategy)
compile_trading_dashboard_outline_async = make_async(compile_trading_dashboard_outline)
define_asset_universe_async = make_async(define_asset_universe)
define_trading_objectives_async = make_async(define_trading_objectives)
define_trading_performance_metrics_async = make_async(define_trading_performance_metrics)
design_risk_management_framework_async = make_async(design_risk_management_framework)
develop_trading_plan_async = make_async(develop_trading_plan)
produce_final_trading_report_async = make_async(produce_final_trading_report)
set_trading_parameters_async = make_async(set_trading_parameters)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_trading_objectives
    async def run_define_trading_objectives():
        # Call the async version of define_trading_objectives with results from dependencies
        return await define_trading_objectives_async(user_input)

    # Run level 0 nodes in parallel
    results['define_trading_objectives'] = await run_define_trading_objectives()

    # Level 1: choose_trading_strategy
    async def run_choose_trading_strategy():
        # Call the async version of choose_trading_strategy with results from dependencies
        return await choose_trading_strategy_async(results['define_trading_objectives'])

    # Run level 1 nodes in parallel
    results['choose_trading_strategy'] = await run_choose_trading_strategy()

    # Level 2: define_asset_universe, set_trading_parameters
    async def run_define_asset_universe():
        # Call the async version of define_asset_universe with results from dependencies
        return await define_asset_universe_async(results['choose_trading_strategy'])

    async def run_set_trading_parameters():
        # Call the async version of set_trading_parameters with results from dependencies
        return await set_trading_parameters_async(results['choose_trading_strategy'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_define_asset_universe(), run_set_trading_parameters())
    results['define_asset_universe'] = level_2_results[0]
    results['set_trading_parameters'] = level_2_results[1]

    # Level 3: design_risk_management_framework
    async def run_design_risk_management_framework():
        # Call the async version of design_risk_management_framework with results from dependencies
        return await design_risk_management_framework_async(results['set_trading_parameters'])

    # Run level 3 nodes in parallel
    results['design_risk_management_framework'] = await run_design_risk_management_framework()

    # Level 4: develop_trading_plan
    async def run_develop_trading_plan():
        # Call the async version of develop_trading_plan with results from dependencies
        return await develop_trading_plan_async(results['define_asset_universe'], results['set_trading_parameters'], results['design_risk_management_framework'])

    # Run level 4 nodes in parallel
    results['develop_trading_plan'] = await run_develop_trading_plan()

    # Level 5: define_trading_performance_metrics, compile_trading_dashboard_outline
    async def run_define_trading_performance_metrics():
        # Call the async version of define_trading_performance_metrics with results from dependencies
        return await define_trading_performance_metrics_async(results['develop_trading_plan'])

    async def run_compile_trading_dashboard_outline():
        # Call the async version of compile_trading_dashboard_outline with results from dependencies
        return await compile_trading_dashboard_outline_async(results['develop_trading_plan'])

    # Run level 5 nodes in parallel
    level_5_results = await asyncio.gather(run_define_trading_performance_metrics(), run_compile_trading_dashboard_outline())
    results['define_trading_performance_metrics'] = level_5_results[0]
    results['compile_trading_dashboard_outline'] = level_5_results[1]

    # Level 6: produce_final_trading_report
    async def run_produce_final_trading_report():
        # Call the async version of produce_final_trading_report with results from dependencies
        return await produce_final_trading_report_async(results['develop_trading_plan'], results['compile_trading_dashboard_outline'], results['define_trading_performance_metrics'])

    # Run level 6 nodes in parallel
    results['produce_final_trading_report'] = await run_produce_final_trading_report()

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
