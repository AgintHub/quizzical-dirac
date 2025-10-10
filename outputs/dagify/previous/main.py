import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.collect_container_data import collect_container_data
from code.parse_container_configs import parse_container_configs
from code.analyze_resource_utilization import analyze_resource_utilization
from code.check_security_configurations import check_security_configurations
from code.generate_analysis_report import generate_analysis_report

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

collect_container_data_async = make_async(collect_container_data)
parse_container_configs_async = make_async(parse_container_configs)
analyze_resource_utilization_async = make_async(analyze_resource_utilization)
check_security_configurations_async = make_async(check_security_configurations)
generate_analysis_report_async = make_async(generate_analysis_report)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: collect_container_data
    async def run_collect_container_data():
        # Call the async version of collect_container_data with results from dependencies
        return await collect_container_data_async(user_input)

    # Run level 0 nodes in parallel
    results['collect_container_data'] = await run_collect_container_data()

    # Level 1: parse_container_configs, analyze_resource_utilization
    async def run_parse_container_configs():
        # Call the async version of parse_container_configs with results from dependencies
        return await parse_container_configs_async(results['collect_container_data'])

    async def run_analyze_resource_utilization():
        # Call the async version of analyze_resource_utilization with results from dependencies
        return await analyze_resource_utilization_async(results['collect_container_data'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_parse_container_configs(), run_analyze_resource_utilization())
    results['parse_container_configs'] = level_1_results[0]
    results['analyze_resource_utilization'] = level_1_results[1]

    # Level 2: check_security_configurations
    async def run_check_security_configurations():
        # Call the async version of check_security_configurations with results from dependencies
        return await check_security_configurations_async(results['parse_container_configs'])

    # Run level 2 nodes in parallel
    results['check_security_configurations'] = await run_check_security_configurations()

    # Level 3: generate_analysis_report
    async def run_generate_analysis_report():
        # Call the async version of generate_analysis_report with results from dependencies
        return await generate_analysis_report_async(results['analyze_resource_utilization'], results['check_security_configurations'])

    # Run level 3 nodes in parallel
    results['generate_analysis_report'] = await run_generate_analysis_report()

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
