# -- PRD --
# 1. BULLET: Parse input strings into lists of patterns and correlations.
#   Reason: The inputs are provided as strings and need to be converted into a usable
#           format.
#   Impact: Allows the function to process the inputs correctly.
#   Complexity: LOW
#   Method: Use JSON parsing or string splitting techniques to convert input strings
#           into lists.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Merge and compile the parsed patterns and correlations into a single list.
#   Reason: The function's primary purpose is to combine the various inputs into a
#           cohesive output.
#   Impact: Produces the required output format for further analysis or processing.
#   Complexity: MEDIUM
#   Method: Implement a merging algorithm that removes duplicates and organizes the
#           patterns logically.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Validate the compiled list for consistency and completeness.
#   Reason: Ensures the output is reliable and usable for downstream processes.
#   Impact: Prevents potential errors or inconsistencies in subsequent analyses.
#   Complexity: HIGH
#   Method: Implement checks for data consistency, handle edge cases, and test
#           thoroughly.
# -- END PRD --

from typing import List

import json
import re


def compile_geographical_patterns(spatial_patterns: str, distribution_patterns: str, correlations: str) -> List[str]:
    """
    Compiles geographical patterns, distribution patterns, and correlations into a final list of geographical patterns.

    Args:
        spatial_patterns: Input parameter of type str
distribution_patterns: Input parameter of type str
correlations: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse input strings into lists of patterns and correlations
    parsed_spatial = []
    parsed_distribution = []
    parsed_correlations = []
    
    # Try JSON parsing first, fallback to string splitting
    for input_str, target_list in [(spatial_patterns, parsed_spatial), 
                                   (distribution_patterns, parsed_distribution), 
                                   (correlations, parsed_correlations)]:
        if not input_str or input_str.strip() == "":
            continue
            
        try:
            # Try JSON parsing
            parsed_data = json.loads(input_str)
            if isinstance(parsed_data, list):
                target_list.extend([str(item) for item in parsed_data])
            else:
                target_list.append(str(parsed_data))
        except (json.JSONDecodeError, TypeError):
            # Fallback to string splitting on common delimiters
            delimiters = [',', ';', '\n', '|']
            items = [input_str]
            for delimiter in delimiters:
                new_items = []
                for item in items:
                    new_items.extend(item.split(delimiter))
                items = new_items
            
            # Clean and filter items
            cleaned_items = [item.strip() for item in items if item.strip()]
            target_list.extend(cleaned_items)
    
    # Merge and compile the parsed patterns and correlations into a single list
    compiled_patterns = []
    
    # Add spatial patterns with prefix for organization
    for pattern in parsed_spatial:
        if pattern not in compiled_patterns:
            compiled_patterns.append(f"spatial: {pattern}")
    
    # Add distribution patterns with prefix
    for pattern in parsed_distribution:
        if pattern not in compiled_patterns:
            compiled_patterns.append(f"distribution: {pattern}")
    
    # Add correlations with prefix
    for correlation in parsed_correlations:
        if correlation not in compiled_patterns:
            compiled_patterns.append(f"correlation: {correlation}")
    
    # Validate the compiled list for consistency and completeness
    validated_patterns = []
    
    for pattern in compiled_patterns:
        # Basic validation checks
        if not pattern or len(pattern.strip()) == 0:
            continue
            
        # Remove excessive whitespace
        cleaned_pattern = re.sub(r'\s+', ' ', pattern.strip())
        
        # Check for minimum length (avoid single character patterns)
        if len(cleaned_pattern) < 3:
            continue
            
        # Check for duplicates (case-insensitive)
        is_duplicate = False
        for existing_pattern in validated_patterns:
            if existing_pattern.lower() == cleaned_pattern.lower():
                is_duplicate = True
                break
        
        if not is_duplicate:
            validated_patterns.append(cleaned_pattern)
    
    # Sort patterns for consistency
    validated_patterns.sort()
    
    return validated_patterns