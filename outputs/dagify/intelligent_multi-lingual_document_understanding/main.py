import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.document_preprocessing import document_preprocessing
from code.language_detection import language_detection
from code.text_extraction import text_extraction
from code.handwritten_text_recognition import handwritten_text_recognition
from code.component_localization import component_localization
from code.component_conversion import component_conversion
from code.output_generation import output_generation

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

document_preprocessing_async = make_async(document_preprocessing)
language_detection_async = make_async(language_detection)
text_extraction_async = make_async(text_extraction)
handwritten_text_recognition_async = make_async(handwritten_text_recognition)
component_localization_async = make_async(component_localization)
component_conversion_async = make_async(component_conversion)
output_generation_async = make_async(output_generation)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: document_preprocessing
    async def run_document_preprocessing():
        # Call the async version of document_preprocessing with results from dependencies
        return await document_preprocessing_async(user_input)

    # Run level 0 nodes in parallel
    results['document_preprocessing'] = await run_document_preprocessing()

    # Level 1: language_detection, text_extraction, handwritten_text_recognition
    async def run_language_detection():
        # Call the async version of language_detection with results from dependencies
        return await language_detection_async(results['document_preprocessing'])

    async def run_text_extraction():
        # Call the async version of text_extraction with results from dependencies
        return await text_extraction_async(results['document_preprocessing'])

    async def run_handwritten_text_recognition():
        # Call the async version of handwritten_text_recognition with results from dependencies
        return await handwritten_text_recognition_async(results['document_preprocessing'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_language_detection(), run_text_extraction(), run_handwritten_text_recognition())
    results['language_detection'] = level_1_results[0]
    results['text_extraction'] = level_1_results[1]
    results['handwritten_text_recognition'] = level_1_results[2]

    # Level 2: component_localization
    async def run_component_localization():
        # Call the async version of component_localization with results from dependencies
        return await component_localization_async(results['text_extraction'], results['handwritten_text_recognition'])

    # Run level 2 nodes in parallel
    results['component_localization'] = await run_component_localization()

    # Level 3: component_conversion
    async def run_component_conversion():
        # Call the async version of component_conversion with results from dependencies
        return await component_conversion_async(results['component_localization'])

    # Run level 3 nodes in parallel
    results['component_conversion'] = await run_component_conversion()

    # Level 4: output_generation
    async def run_output_generation():
        # Call the async version of output_generation with results from dependencies
        return await output_generation_async(results['text_extraction'], results['handwritten_text_recognition'], results['component_conversion'])

    # Run level 4 nodes in parallel
    results['output_generation'] = await run_output_generation()

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
