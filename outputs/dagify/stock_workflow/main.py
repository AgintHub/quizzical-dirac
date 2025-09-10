import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.calculate_stock_valuation import calculate_stock_valuation
from code.define_stock_requirements import define_stock_requirements
from code.define_stock_structure import define_stock_structure
from code.determine_stock_type import determine_stock_type
from code.draft_stock_offering import draft_stock_offering
from code.finalize_stock_workflow import finalize_stock_workflow
from code.research_stock_market import research_stock_market
from code.review_stock_offering import review_stock_offering

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

calculate_stock_valuation_async = make_async(calculate_stock_valuation)
define_stock_requirements_async = make_async(define_stock_requirements)
define_stock_structure_async = make_async(define_stock_structure)
determine_stock_type_async = make_async(determine_stock_type)
draft_stock_offering_async = make_async(draft_stock_offering)
finalize_stock_workflow_async = make_async(finalize_stock_workflow)
research_stock_market_async = make_async(research_stock_market)
review_stock_offering_async = make_async(review_stock_offering)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: research_stock_market, define_stock_requirements
    async def run_research_stock_market():
        # Call the async version of research_stock_market with results from dependencies
        return await research_stock_market_async(user_input)

    async def run_define_stock_requirements():
        # Call the async version of define_stock_requirements with results from dependencies
        return await define_stock_requirements_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_research_stock_market(), run_define_stock_requirements())
    results['research_stock_market'] = level_0_results[0]
    results['define_stock_requirements'] = level_0_results[1]

    # Level 1: determine_stock_type
    async def run_determine_stock_type():
        # Call the async version of determine_stock_type with results from dependencies
        return await determine_stock_type_async(results['define_stock_requirements'], results['research_stock_market'])

    # Run level 1 nodes in parallel
    results['determine_stock_type'] = await run_determine_stock_type()

    # Level 2: calculate_stock_valuation
    async def run_calculate_stock_valuation():
        # Call the async version of calculate_stock_valuation with results from dependencies
        return await calculate_stock_valuation_async(results['determine_stock_type'])

    # Run level 2 nodes in parallel
    results['calculate_stock_valuation'] = await run_calculate_stock_valuation()

    # Level 3: define_stock_structure
    async def run_define_stock_structure():
        # Call the async version of define_stock_structure with results from dependencies
        return await define_stock_structure_async(results['calculate_stock_valuation'])

    # Run level 3 nodes in parallel
    results['define_stock_structure'] = await run_define_stock_structure()

    # Level 4: draft_stock_offering
    async def run_draft_stock_offering():
        # Call the async version of draft_stock_offering with results from dependencies
        return await draft_stock_offering_async(results['define_stock_structure'])

    # Run level 4 nodes in parallel
    results['draft_stock_offering'] = await run_draft_stock_offering()

    # Level 5: review_stock_offering
    async def run_review_stock_offering():
        # Call the async version of review_stock_offering with results from dependencies
        return await review_stock_offering_async(results['draft_stock_offering'])

    # Run level 5 nodes in parallel
    results['review_stock_offering'] = await run_review_stock_offering()

    # Level 6: finalize_stock_workflow
    async def run_finalize_stock_workflow():
        # Call the async version of finalize_stock_workflow with results from dependencies
        return await finalize_stock_workflow_async(results['review_stock_offering'])

    # Run level 6 nodes in parallel
    results['finalize_stock_workflow'] = await run_finalize_stock_workflow()

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
