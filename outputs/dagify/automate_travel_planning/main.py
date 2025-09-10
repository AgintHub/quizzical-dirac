import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.apply_for_visas import apply_for_visas
from code.book_cars import book_cars
from code.book_flights import book_flights
from code.book_hotels import book_hotels
from code.check_immigration_requirements import check_immigration_requirements
from code.create_itinerary import create_itinerary
from code.define_travel_objectives import define_travel_objectives
from code.finalize_travel_arrangements import finalize_travel_arrangements
from code.research_destination_options import research_destination_options
from code.search_cars import search_cars
from code.search_flights import search_flights
from code.search_hotels import search_hotels

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

apply_for_visas_async = make_async(apply_for_visas)
book_cars_async = make_async(book_cars)
book_flights_async = make_async(book_flights)
book_hotels_async = make_async(book_hotels)
check_immigration_requirements_async = make_async(check_immigration_requirements)
create_itinerary_async = make_async(create_itinerary)
define_travel_objectives_async = make_async(define_travel_objectives)
finalize_travel_arrangements_async = make_async(finalize_travel_arrangements)
research_destination_options_async = make_async(research_destination_options)
search_cars_async = make_async(search_cars)
search_flights_async = make_async(search_flights)
search_hotels_async = make_async(search_hotels)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_travel_objectives
    async def run_define_travel_objectives():
        # Call the async version of define_travel_objectives with results from dependencies
        return await define_travel_objectives_async(user_input)

    # Run level 0 nodes in parallel
    results['define_travel_objectives'] = await run_define_travel_objectives()

    # Level 1: research_destination_options
    async def run_research_destination_options():
        # Call the async version of research_destination_options with results from dependencies
        return await research_destination_options_async(results['define_travel_objectives'])

    # Run level 1 nodes in parallel
    results['research_destination_options'] = await run_research_destination_options()

    # Level 2: search_hotels, check_immigration_requirements, search_flights, search_cars
    async def run_search_hotels():
        # Call the async version of search_hotels with results from dependencies
        return await search_hotels_async(results['research_destination_options'])

    async def run_check_immigration_requirements():
        # Call the async version of check_immigration_requirements with results from dependencies
        return await check_immigration_requirements_async(results['research_destination_options'])

    async def run_search_flights():
        # Call the async version of search_flights with results from dependencies
        return await search_flights_async(results['research_destination_options'])

    async def run_search_cars():
        # Call the async version of search_cars with results from dependencies
        return await search_cars_async(results['research_destination_options'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_search_hotels(), run_check_immigration_requirements(), run_search_flights(), run_search_cars())
    results['search_hotels'] = level_2_results[0]
    results['check_immigration_requirements'] = level_2_results[1]
    results['search_flights'] = level_2_results[2]
    results['search_cars'] = level_2_results[3]

    # Level 3: create_itinerary
    async def run_create_itinerary():
        # Call the async version of create_itinerary with results from dependencies
        return await create_itinerary_async(results['search_flights'], results['search_hotels'], results['search_cars'], results['check_immigration_requirements'])

    # Run level 3 nodes in parallel
    results['create_itinerary'] = await run_create_itinerary()

    # Level 4: apply_for_visas, book_hotels, book_cars, book_flights
    async def run_apply_for_visas():
        # Call the async version of apply_for_visas with results from dependencies
        return await apply_for_visas_async(results['check_immigration_requirements'], results['create_itinerary'])

    async def run_book_hotels():
        # Call the async version of book_hotels with results from dependencies
        return await book_hotels_async(results['create_itinerary'])

    async def run_book_cars():
        # Call the async version of book_cars with results from dependencies
        return await book_cars_async(results['create_itinerary'])

    async def run_book_flights():
        # Call the async version of book_flights with results from dependencies
        return await book_flights_async(results['create_itinerary'])

    # Run level 4 nodes in parallel
    level_4_results = await asyncio.gather(run_apply_for_visas(), run_book_hotels(), run_book_cars(), run_book_flights())
    results['apply_for_visas'] = level_4_results[0]
    results['book_hotels'] = level_4_results[1]
    results['book_cars'] = level_4_results[2]
    results['book_flights'] = level_4_results[3]

    # Level 5: finalize_travel_arrangements
    async def run_finalize_travel_arrangements():
        # Call the async version of finalize_travel_arrangements with results from dependencies
        return await finalize_travel_arrangements_async(results['book_flights'], results['book_hotels'], results['book_cars'], results['apply_for_visas'])

    # Run level 5 nodes in parallel
    results['finalize_travel_arrangements'] = await run_finalize_travel_arrangements()

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
