import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.define_world_context import define_world_context
from code.gather_geographical_data import gather_geographical_data
from code.collect_cultural_data import collect_cultural_data
from code.analyze_geographical_data import analyze_geographical_data
from code.analyze_cultural_data import analyze_cultural_data
from code.integrate_findings import integrate_findings
from code.generate_world_report import generate_world_report

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

define_world_context_async = make_async(define_world_context)
gather_geographical_data_async = make_async(gather_geographical_data)
collect_cultural_data_async = make_async(collect_cultural_data)
analyze_geographical_data_async = make_async(analyze_geographical_data)
analyze_cultural_data_async = make_async(analyze_cultural_data)
integrate_findings_async = make_async(integrate_findings)
generate_world_report_async = make_async(generate_world_report)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_world_context
    async def run_define_world_context():
        # Call the async version of define_world_context with results from dependencies
        return await define_world_context_async(user_input)

    # Run level 0 nodes in parallel
    results['define_world_context'] = await run_define_world_context()

    # Level 1: collect_cultural_data, gather_geographical_data
    async def run_collect_cultural_data():
        # Call the async version of collect_cultural_data with results from dependencies
        return await collect_cultural_data_async(results['define_world_context'])

    async def run_gather_geographical_data():
        # Call the async version of gather_geographical_data with results from dependencies
        return await gather_geographical_data_async(results['define_world_context'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_collect_cultural_data(), run_gather_geographical_data())
    results['collect_cultural_data'] = level_1_results[0]
    results['gather_geographical_data'] = level_1_results[1]

    # Level 2: analyze_cultural_data, analyze_geographical_data
    async def run_analyze_cultural_data():
        # Call the async version of analyze_cultural_data with results from dependencies
        return await analyze_cultural_data_async(results['collect_cultural_data'])

    async def run_analyze_geographical_data():
        # Call the async version of analyze_geographical_data with results from dependencies
        return await analyze_geographical_data_async(results['gather_geographical_data'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_analyze_cultural_data(), run_analyze_geographical_data())
    results['analyze_cultural_data'] = level_2_results[0]
    results['analyze_geographical_data'] = level_2_results[1]

    # Level 3: integrate_findings
    async def run_integrate_findings():
        # Call the async version of integrate_findings with results from dependencies
        return await integrate_findings_async(results['analyze_geographical_data'], results['analyze_cultural_data'])

    # Run level 3 nodes in parallel
    results['integrate_findings'] = await run_integrate_findings()

    # Level 4: generate_world_report
    async def run_generate_world_report():
        # Call the async version of generate_world_report with results from dependencies
        return await generate_world_report_async(results['integrate_findings'])

    # Run level 4 nodes in parallel
    results['generate_world_report'] = await run_generate_world_report()

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
