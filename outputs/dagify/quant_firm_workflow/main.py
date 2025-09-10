import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.backtest_trading_strategy import backtest_trading_strategy
from code.build_alpha_models import build_alpha_models
from code.collect_market_data import collect_market_data
from code.deploy_trading_strategy import deploy_trading_strategy
from code.evaluate_alpha_models import evaluate_alpha_models
from code.feature_engineering import feature_engineering
from code.generate_trading_signals import generate_trading_signals
from code.preprocess_market_data import preprocess_market_data
from code.refine_trading_strategy import refine_trading_strategy
from code.select_alpha_factors import select_alpha_factors
from code.select_best_alpha_model import select_best_alpha_model

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

backtest_trading_strategy_async = make_async(backtest_trading_strategy)
build_alpha_models_async = make_async(build_alpha_models)
collect_market_data_async = make_async(collect_market_data)
deploy_trading_strategy_async = make_async(deploy_trading_strategy)
evaluate_alpha_models_async = make_async(evaluate_alpha_models)
feature_engineering_async = make_async(feature_engineering)
generate_trading_signals_async = make_async(generate_trading_signals)
preprocess_market_data_async = make_async(preprocess_market_data)
refine_trading_strategy_async = make_async(refine_trading_strategy)
select_alpha_factors_async = make_async(select_alpha_factors)
select_best_alpha_model_async = make_async(select_best_alpha_model)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: collect_market_data, select_alpha_factors
    async def run_collect_market_data():
        # Call the async version of collect_market_data with results from dependencies
        return await collect_market_data_async(user_input)

    async def run_select_alpha_factors():
        # Call the async version of select_alpha_factors with results from dependencies
        return await select_alpha_factors_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_collect_market_data(), run_select_alpha_factors())
    results['collect_market_data'] = level_0_results[0]
    results['select_alpha_factors'] = level_0_results[1]

    # Level 1: preprocess_market_data
    async def run_preprocess_market_data():
        # Call the async version of preprocess_market_data with results from dependencies
        return await preprocess_market_data_async(results['collect_market_data'])

    # Run level 1 nodes in parallel
    results['preprocess_market_data'] = await run_preprocess_market_data()

    # Level 2: feature_engineering
    async def run_feature_engineering():
        # Call the async version of feature_engineering with results from dependencies
        return await feature_engineering_async(results['preprocess_market_data'])

    # Run level 2 nodes in parallel
    results['feature_engineering'] = await run_feature_engineering()

    # Level 3: build_alpha_models
    async def run_build_alpha_models():
        # Call the async version of build_alpha_models with results from dependencies
        return await build_alpha_models_async(results['feature_engineering'], results['select_alpha_factors'])

    # Run level 3 nodes in parallel
    results['build_alpha_models'] = await run_build_alpha_models()

    # Level 4: evaluate_alpha_models
    async def run_evaluate_alpha_models():
        # Call the async version of evaluate_alpha_models with results from dependencies
        return await evaluate_alpha_models_async(results['build_alpha_models'])

    # Run level 4 nodes in parallel
    results['evaluate_alpha_models'] = await run_evaluate_alpha_models()

    # Level 5: select_best_alpha_model
    async def run_select_best_alpha_model():
        # Call the async version of select_best_alpha_model with results from dependencies
        return await select_best_alpha_model_async(results['evaluate_alpha_models'])

    # Run level 5 nodes in parallel
    results['select_best_alpha_model'] = await run_select_best_alpha_model()

    # Level 6: generate_trading_signals
    async def run_generate_trading_signals():
        # Call the async version of generate_trading_signals with results from dependencies
        return await generate_trading_signals_async(results['select_best_alpha_model'])

    # Run level 6 nodes in parallel
    results['generate_trading_signals'] = await run_generate_trading_signals()

    # Level 7: backtest_trading_strategy
    async def run_backtest_trading_strategy():
        # Call the async version of backtest_trading_strategy with results from dependencies
        return await backtest_trading_strategy_async(results['generate_trading_signals'])

    # Run level 7 nodes in parallel
    results['backtest_trading_strategy'] = await run_backtest_trading_strategy()

    # Level 8: refine_trading_strategy
    async def run_refine_trading_strategy():
        # Call the async version of refine_trading_strategy with results from dependencies
        return await refine_trading_strategy_async(results['backtest_trading_strategy'])

    # Run level 8 nodes in parallel
    results['refine_trading_strategy'] = await run_refine_trading_strategy()

    # Level 9: deploy_trading_strategy
    async def run_deploy_trading_strategy():
        # Call the async version of deploy_trading_strategy with results from dependencies
        return await deploy_trading_strategy_async(results['refine_trading_strategy'])

    # Run level 9 nodes in parallel
    results['deploy_trading_strategy'] = await run_deploy_trading_strategy()

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
