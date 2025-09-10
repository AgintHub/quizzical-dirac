import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_softness_levels import analyze_softness_levels
from code.gather_toilet_paper_data import gather_toilet_paper_data
from code.purchase_selected_toilet_paper import purchase_selected_toilet_paper
from code.research_toilet_paper_brands import research_toilet_paper_brands
from code.select_softest_toilet_paper import select_softest_toilet_paper
from code.verify_purchase import verify_purchase

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

analyze_softness_levels_async = make_async(analyze_softness_levels)
gather_toilet_paper_data_async = make_async(gather_toilet_paper_data)
purchase_selected_toilet_paper_async = make_async(purchase_selected_toilet_paper)
research_toilet_paper_brands_async = make_async(research_toilet_paper_brands)
select_softest_toilet_paper_async = make_async(select_softest_toilet_paper)
verify_purchase_async = make_async(verify_purchase)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: research_toilet_paper_brands
    async def run_research_toilet_paper_brands():
        # Call the async version of research_toilet_paper_brands with results from dependencies
        return await research_toilet_paper_brands_async(user_input)

    # Run level 0 nodes in parallel
    results['research_toilet_paper_brands'] = await run_research_toilet_paper_brands()

    # Level 1: gather_toilet_paper_data
    async def run_gather_toilet_paper_data():
        # Call the async version of gather_toilet_paper_data with results from dependencies
        return await gather_toilet_paper_data_async(results['research_toilet_paper_brands'])

    # Run level 1 nodes in parallel
    results['gather_toilet_paper_data'] = await run_gather_toilet_paper_data()

    # Level 2: analyze_softness_levels
    async def run_analyze_softness_levels():
        # Call the async version of analyze_softness_levels with results from dependencies
        return await analyze_softness_levels_async(results['gather_toilet_paper_data'])

    # Run level 2 nodes in parallel
    results['analyze_softness_levels'] = await run_analyze_softness_levels()

    # Level 3: select_softest_toilet_paper
    async def run_select_softest_toilet_paper():
        # Call the async version of select_softest_toilet_paper with results from dependencies
        return await select_softest_toilet_paper_async(results['analyze_softness_levels'])

    # Run level 3 nodes in parallel
    results['select_softest_toilet_paper'] = await run_select_softest_toilet_paper()

    # Level 4: purchase_selected_toilet_paper
    async def run_purchase_selected_toilet_paper():
        # Call the async version of purchase_selected_toilet_paper with results from dependencies
        return await purchase_selected_toilet_paper_async(results['select_softest_toilet_paper'])

    # Run level 4 nodes in parallel
    results['purchase_selected_toilet_paper'] = await run_purchase_selected_toilet_paper()

    # Level 5: verify_purchase
    async def run_verify_purchase():
        # Call the async version of verify_purchase with results from dependencies
        return await verify_purchase_async(results['purchase_selected_toilet_paper'])

    # Run level 5 nodes in parallel
    results['verify_purchase'] = await run_verify_purchase()

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
