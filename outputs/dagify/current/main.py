import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.align_and_clean_data import align_and_clean_data
from code.analyze_feature_importance import analyze_feature_importance
from code.assemble_feature_matrix import assemble_feature_matrix
from code.compile_strategy_documentation import compile_strategy_documentation
from code.compute_cross_asset_features import compute_cross_asset_features
from code.compute_price_action_features import compute_price_action_features
from code.compute_regime_features import compute_regime_features
from code.compute_volatility_features import compute_volatility_features
from code.create_monitoring_plan import create_monitoring_plan
from code.define_hyperparameter_grid import define_hyperparameter_grid
from code.define_strategy_objectives import define_strategy_objectives
from code.design_risk_controls import design_risk_controls
from code.draft_execution_logic import draft_execution_logic
from code.evaluate_models import evaluate_models
from code.fetch_cross_asset_data import fetch_cross_asset_data
from code.fetch_price_data import fetch_price_data
from code.fetch_regime_indicator_data import fetch_regime_indicator_data
from code.fetch_volatility_data import fetch_volatility_data
from code.final_deliverables_package import final_deliverables_package
from code.list_data_sources import list_data_sources
from code.run_backtest import run_backtest
from code.select_best_model import select_best_model
from code.setup_backtest_environment import setup_backtest_environment
from code.specify_model_architecture import specify_model_architecture
from code.split_dataset import split_dataset
from code.summarize_backtest_results import summarize_backtest_results
from code.train_models import train_models

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

align_and_clean_data_async = make_async(align_and_clean_data)
analyze_feature_importance_async = make_async(analyze_feature_importance)
assemble_feature_matrix_async = make_async(assemble_feature_matrix)
compile_strategy_documentation_async = make_async(compile_strategy_documentation)
compute_cross_asset_features_async = make_async(compute_cross_asset_features)
compute_price_action_features_async = make_async(compute_price_action_features)
compute_regime_features_async = make_async(compute_regime_features)
compute_volatility_features_async = make_async(compute_volatility_features)
create_monitoring_plan_async = make_async(create_monitoring_plan)
define_hyperparameter_grid_async = make_async(define_hyperparameter_grid)
define_strategy_objectives_async = make_async(define_strategy_objectives)
design_risk_controls_async = make_async(design_risk_controls)
draft_execution_logic_async = make_async(draft_execution_logic)
evaluate_models_async = make_async(evaluate_models)
fetch_cross_asset_data_async = make_async(fetch_cross_asset_data)
fetch_price_data_async = make_async(fetch_price_data)
fetch_regime_indicator_data_async = make_async(fetch_regime_indicator_data)
fetch_volatility_data_async = make_async(fetch_volatility_data)
final_deliverables_package_async = make_async(final_deliverables_package)
list_data_sources_async = make_async(list_data_sources)
run_backtest_async = make_async(run_backtest)
select_best_model_async = make_async(select_best_model)
setup_backtest_environment_async = make_async(setup_backtest_environment)
specify_model_architecture_async = make_async(specify_model_architecture)
split_dataset_async = make_async(split_dataset)
summarize_backtest_results_async = make_async(summarize_backtest_results)
train_models_async = make_async(train_models)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_strategy_objectives
    async def run_define_strategy_objectives():
        # Call the async version of define_strategy_objectives with results from dependencies
        return await define_strategy_objectives_async(user_input)

    # Run level 0 nodes in parallel
    results['define_strategy_objectives'] = await run_define_strategy_objectives()

    # Level 1: list_data_sources, specify_model_architecture
    async def run_list_data_sources():
        # Call the async version of list_data_sources with results from dependencies
        return await list_data_sources_async(results['define_strategy_objectives'])

    async def run_specify_model_architecture():
        # Call the async version of specify_model_architecture with results from dependencies
        return await specify_model_architecture_async(results['define_strategy_objectives'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_list_data_sources(), run_specify_model_architecture())
    results['list_data_sources'] = level_1_results[0]
    results['specify_model_architecture'] = level_1_results[1]

    # Level 2: fetch_volatility_data, fetch_cross_asset_data, fetch_price_data, define_hyperparameter_grid, fetch_regime_indicator_data
    async def run_fetch_volatility_data():
        # Call the async version of fetch_volatility_data with results from dependencies
        return await fetch_volatility_data_async(results['list_data_sources'])

    async def run_fetch_cross_asset_data():
        # Call the async version of fetch_cross_asset_data with results from dependencies
        return await fetch_cross_asset_data_async(results['list_data_sources'])

    async def run_fetch_price_data():
        # Call the async version of fetch_price_data with results from dependencies
        return await fetch_price_data_async(results['list_data_sources'])

    async def run_define_hyperparameter_grid():
        # Call the async version of define_hyperparameter_grid with results from dependencies
        return await define_hyperparameter_grid_async(results['specify_model_architecture'])

    async def run_fetch_regime_indicator_data():
        # Call the async version of fetch_regime_indicator_data with results from dependencies
        return await fetch_regime_indicator_data_async(results['list_data_sources'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_fetch_volatility_data(), run_fetch_cross_asset_data(), run_fetch_price_data(), run_define_hyperparameter_grid(), run_fetch_regime_indicator_data())
    results['fetch_volatility_data'] = level_2_results[0]
    results['fetch_cross_asset_data'] = level_2_results[1]
    results['fetch_price_data'] = level_2_results[2]
    results['define_hyperparameter_grid'] = level_2_results[3]
    results['fetch_regime_indicator_data'] = level_2_results[4]

    # Level 3: align_and_clean_data
    async def run_align_and_clean_data():
        # Call the async version of align_and_clean_data with results from dependencies
        return await align_and_clean_data_async(results['fetch_price_data'], results['fetch_cross_asset_data'], results['fetch_regime_indicator_data'], results['fetch_volatility_data'])

    # Run level 3 nodes in parallel
    results['align_and_clean_data'] = await run_align_and_clean_data()

    # Level 4: compute_volatility_features, compute_price_action_features, compute_cross_asset_features, compute_regime_features
    async def run_compute_volatility_features():
        # Call the async version of compute_volatility_features with results from dependencies
        return await compute_volatility_features_async(results['align_and_clean_data'])

    async def run_compute_price_action_features():
        # Call the async version of compute_price_action_features with results from dependencies
        return await compute_price_action_features_async(results['align_and_clean_data'])

    async def run_compute_cross_asset_features():
        # Call the async version of compute_cross_asset_features with results from dependencies
        return await compute_cross_asset_features_async(results['align_and_clean_data'])

    async def run_compute_regime_features():
        # Call the async version of compute_regime_features with results from dependencies
        return await compute_regime_features_async(results['align_and_clean_data'])

    # Run level 4 nodes in parallel
    level_4_results = await asyncio.gather(run_compute_volatility_features(), run_compute_price_action_features(), run_compute_cross_asset_features(), run_compute_regime_features())
    results['compute_volatility_features'] = level_4_results[0]
    results['compute_price_action_features'] = level_4_results[1]
    results['compute_cross_asset_features'] = level_4_results[2]
    results['compute_regime_features'] = level_4_results[3]

    # Level 5: assemble_feature_matrix
    async def run_assemble_feature_matrix():
        # Call the async version of assemble_feature_matrix with results from dependencies
        return await assemble_feature_matrix_async(results['compute_price_action_features'], results['compute_cross_asset_features'], results['compute_regime_features'], results['compute_volatility_features'])

    # Run level 5 nodes in parallel
    results['assemble_feature_matrix'] = await run_assemble_feature_matrix()

    # Level 6: split_dataset
    async def run_split_dataset():
        # Call the async version of split_dataset with results from dependencies
        return await split_dataset_async(results['assemble_feature_matrix'])

    # Run level 6 nodes in parallel
    results['split_dataset'] = await run_split_dataset()

    # Level 7: train_models
    async def run_train_models():
        # Call the async version of train_models with results from dependencies
        return await train_models_async(results['split_dataset'], results['define_hyperparameter_grid'])

    # Run level 7 nodes in parallel
    results['train_models'] = await run_train_models()

    # Level 8: evaluate_models
    async def run_evaluate_models():
        # Call the async version of evaluate_models with results from dependencies
        return await evaluate_models_async(results['train_models'], results['split_dataset'])

    # Run level 8 nodes in parallel
    results['evaluate_models'] = await run_evaluate_models()

    # Level 9: select_best_model
    async def run_select_best_model():
        # Call the async version of select_best_model with results from dependencies
        return await select_best_model_async(results['evaluate_models'])

    # Run level 9 nodes in parallel
    results['select_best_model'] = await run_select_best_model()

    # Level 10: create_monitoring_plan, design_risk_controls, analyze_feature_importance
    async def run_create_monitoring_plan():
        # Call the async version of create_monitoring_plan with results from dependencies
        return await create_monitoring_plan_async(results['define_strategy_objectives'], results['select_best_model'])

    async def run_design_risk_controls():
        # Call the async version of design_risk_controls with results from dependencies
        return await design_risk_controls_async(results['select_best_model'], results['define_strategy_objectives'])

    async def run_analyze_feature_importance():
        # Call the async version of analyze_feature_importance with results from dependencies
        return await analyze_feature_importance_async(results['select_best_model'], results['assemble_feature_matrix'])

    # Run level 10 nodes in parallel
    level_10_results = await asyncio.gather(run_create_monitoring_plan(), run_design_risk_controls(), run_analyze_feature_importance())
    results['create_monitoring_plan'] = level_10_results[0]
    results['design_risk_controls'] = level_10_results[1]
    results['analyze_feature_importance'] = level_10_results[2]

    # Level 11: draft_execution_logic, setup_backtest_environment
    async def run_draft_execution_logic():
        # Call the async version of draft_execution_logic with results from dependencies
        return await draft_execution_logic_async(results['select_best_model'], results['design_risk_controls'])

    async def run_setup_backtest_environment():
        # Call the async version of setup_backtest_environment with results from dependencies
        return await setup_backtest_environment_async(results['align_and_clean_data'], results['select_best_model'], results['design_risk_controls'])

    # Run level 11 nodes in parallel
    level_11_results = await asyncio.gather(run_draft_execution_logic(), run_setup_backtest_environment())
    results['draft_execution_logic'] = level_11_results[0]
    results['setup_backtest_environment'] = level_11_results[1]

    # Level 12: run_backtest
    async def run_run_backtest():
        # Call the async version of run_backtest with results from dependencies
        return await run_backtest_async(results['setup_backtest_environment'])

    # Run level 12 nodes in parallel
    results['run_backtest'] = await run_run_backtest()

    # Level 13: summarize_backtest_results
    async def run_summarize_backtest_results():
        # Call the async version of summarize_backtest_results with results from dependencies
        return await summarize_backtest_results_async(results['run_backtest'])

    # Run level 13 nodes in parallel
    results['summarize_backtest_results'] = await run_summarize_backtest_results()

    # Level 14: compile_strategy_documentation
    async def run_compile_strategy_documentation():
        # Call the async version of compile_strategy_documentation with results from dependencies
        return await compile_strategy_documentation_async(results['select_best_model'], results['design_risk_controls'], results['draft_execution_logic'], results['summarize_backtest_results'])

    # Run level 14 nodes in parallel
    results['compile_strategy_documentation'] = await run_compile_strategy_documentation()

    # Level 15: final_deliverables_package
    async def run_final_deliverables_package():
        # Call the async version of final_deliverables_package with results from dependencies
        return await final_deliverables_package_async(results['compile_strategy_documentation'], results['create_monitoring_plan'])

    # Run level 15 nodes in parallel
    results['final_deliverables_package'] = await run_final_deliverables_package()

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
