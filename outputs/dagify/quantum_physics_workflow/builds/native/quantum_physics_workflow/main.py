import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_simulation_results import analyze_simulation_results
from code.define_quantum_system import define_quantum_system
from code.generate_quantum_circuit import generate_quantum_circuit
from code.select_quantum_algorithm import select_quantum_algorithm
from code.simulate_quantum_circuit import simulate_quantum_circuit
from code.visualize_results import visualize_results

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

analyze_simulation_results_async = make_async(analyze_simulation_results)
define_quantum_system_async = make_async(define_quantum_system)
generate_quantum_circuit_async = make_async(generate_quantum_circuit)
select_quantum_algorithm_async = make_async(select_quantum_algorithm)
simulate_quantum_circuit_async = make_async(simulate_quantum_circuit)
visualize_results_async = make_async(visualize_results)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_quantum_system
    async def run_define_quantum_system():
        # Call the async version of define_quantum_system with results from dependencies
        return await define_quantum_system_async(user_input)

    # Run level 0 nodes in parallel
    results['define_quantum_system'] = await run_define_quantum_system()

    # Level 1: select_quantum_algorithm
    async def run_select_quantum_algorithm():
        # Call the async version of select_quantum_algorithm with results from dependencies
        return await select_quantum_algorithm_async(results['define_quantum_system'])

    # Run level 1 nodes in parallel
    results['select_quantum_algorithm'] = await run_select_quantum_algorithm()

    # Level 2: generate_quantum_circuit
    async def run_generate_quantum_circuit():
        # Call the async version of generate_quantum_circuit with results from dependencies
        return await generate_quantum_circuit_async(results['select_quantum_algorithm'])

    # Run level 2 nodes in parallel
    results['generate_quantum_circuit'] = await run_generate_quantum_circuit()

    # Level 3: simulate_quantum_circuit
    async def run_simulate_quantum_circuit():
        # Call the async version of simulate_quantum_circuit with results from dependencies
        return await simulate_quantum_circuit_async(results['generate_quantum_circuit'])

    # Run level 3 nodes in parallel
    results['simulate_quantum_circuit'] = await run_simulate_quantum_circuit()

    # Level 4: analyze_simulation_results
    async def run_analyze_simulation_results():
        # Call the async version of analyze_simulation_results with results from dependencies
        return await analyze_simulation_results_async(results['simulate_quantum_circuit'])

    # Run level 4 nodes in parallel
    results['analyze_simulation_results'] = await run_analyze_simulation_results()

    # Level 5: visualize_results
    async def run_visualize_results():
        # Call the async version of visualize_results with results from dependencies
        return await visualize_results_async(results['analyze_simulation_results'])

    # Run level 5 nodes in parallel
    results['visualize_results'] = await run_visualize_results()

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
