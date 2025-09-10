import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.defineworkflowobjective import defineworkflowobjective
from code.decomposeworkflowobjective import decomposeworkflowobjective
from code.identifyinputrequirements import identifyinputrequirements
from code.defineprojectscope import defineprojectscope
from code.createworkflowdesign import createworkflowdesign
from code.refineworkflowdesign import refineworkflowdesign
from code.executeworkflow import executeworkflow
from code.evaluateworkflowperformance import evaluateworkflowperformance
from code.iterateonworkflowimprovements import iterateonworkflowimprovements

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

defineworkflowobjective_async = make_async(defineworkflowobjective)
decomposeworkflowobjective_async = make_async(decomposeworkflowobjective)
identifyinputrequirements_async = make_async(identifyinputrequirements)
defineprojectscope_async = make_async(defineprojectscope)
createworkflowdesign_async = make_async(createworkflowdesign)
refineworkflowdesign_async = make_async(refineworkflowdesign)
executeworkflow_async = make_async(executeworkflow)
evaluateworkflowperformance_async = make_async(evaluateworkflowperformance)
iterateonworkflowimprovements_async = make_async(iterateonworkflowimprovements)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: defineworkflowobjective
    async def run_defineworkflowobjective():
        # Call the async version of defineworkflowobjective with results from dependencies
        return await defineworkflowobjective_async(user_input)

    # Run level 0 nodes in parallel
    results['defineworkflowobjective'] = await run_defineworkflowobjective()

    # Level 1: decomposeworkflowobjective
    async def run_decomposeworkflowobjective():
        # Call the async version of decomposeworkflowobjective with results from dependencies
        return await decomposeworkflowobjective_async(results['defineworkflowobjective'])

    # Run level 1 nodes in parallel
    results['decomposeworkflowobjective'] = await run_decomposeworkflowobjective()

    # Level 2: identifyinputrequirements
    async def run_identifyinputrequirements():
        # Call the async version of identifyinputrequirements with results from dependencies
        return await identifyinputrequirements_async(results['decomposeworkflowobjective'])

    # Run level 2 nodes in parallel
    results['identifyinputrequirements'] = await run_identifyinputrequirements()

    # Level 3: defineprojectscope
    async def run_defineprojectscope():
        # Call the async version of defineprojectscope with results from dependencies
        return await defineprojectscope_async(results['identifyinputrequirements'])

    # Run level 3 nodes in parallel
    results['defineprojectscope'] = await run_defineprojectscope()

    # Level 4: createworkflowdesign
    async def run_createworkflowdesign():
        # Call the async version of createworkflowdesign with results from dependencies
        return await createworkflowdesign_async(results['defineprojectscope'])

    # Run level 4 nodes in parallel
    results['createworkflowdesign'] = await run_createworkflowdesign()

    # Level 5: refineworkflowdesign
    async def run_refineworkflowdesign():
        # Call the async version of refineworkflowdesign with results from dependencies
        return await refineworkflowdesign_async(results['createworkflowdesign'])

    # Run level 5 nodes in parallel
    results['refineworkflowdesign'] = await run_refineworkflowdesign()

    # Level 6: executeworkflow
    async def run_executeworkflow():
        # Call the async version of executeworkflow with results from dependencies
        return await executeworkflow_async(results['refineworkflowdesign'])

    # Run level 6 nodes in parallel
    results['executeworkflow'] = await run_executeworkflow()

    # Level 7: evaluateworkflowperformance
    async def run_evaluateworkflowperformance():
        # Call the async version of evaluateworkflowperformance with results from dependencies
        return await evaluateworkflowperformance_async(results['executeworkflow'])

    # Run level 7 nodes in parallel
    results['evaluateworkflowperformance'] = await run_evaluateworkflowperformance()

    # Level 8: iterateonworkflowimprovements
    async def run_iterateonworkflowimprovements():
        # Call the async version of iterateonworkflowimprovements with results from dependencies
        return await iterateonworkflowimprovements_async(results['evaluateworkflowperformance'])

    # Run level 8 nodes in parallel
    results['iterateonworkflowimprovements'] = await run_iterateonworkflowimprovements()

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
