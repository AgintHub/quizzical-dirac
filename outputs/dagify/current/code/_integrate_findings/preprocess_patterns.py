# -- PRD --
# 1. BULLET: Implement data cleaning to remove irrelevant information from the input
#   patterns.
#   Reason: To ensure the quality and relevance of the patterns for further analysis.
#   Impact: Improved accuracy in downstream tasks such as theme identification and
#           narrative crafting.
#   Complexity: MEDIUM
#   Method: Use natural language processing techniques or regular expressions to filter
#           out irrelevant data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Remove duplicates from the input patterns.
#   Reason: To prevent duplication of effort and ensure uniqueness of patterns.
#   Impact: Reduces redundancy and improves efficiency in subsequent processing steps.
#   Complexity: LOW
#   Method: Utilize data structures like sets to automatically eliminate duplicate
#           entries.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle different pattern types (e.g., geographical, cultural) appropriately.
#   Reason: To tailor the preprocessing according to the specific requirements of each
#           pattern type.
#   Impact: Enhances the flexibility and applicability of the preprocessing function
#           across various domains.
#   Complexity: HIGH
#   Method: Implement type-specific preprocessing logic or utilize modular design to
#           accommodate different pattern types.
# -- END PRD --

from typing import List

import re


def preprocess_patterns(patterns: str, pattern_type: str) -> List[str]:
    """
    Preprocesses and cleans input patterns to remove duplicates and irrelevant information based on the pattern type.

    Args:
        patterns: Input parameter of type str
pattern_type: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Split patterns into individual items (assuming newline or comma separated)
    if '\n' in patterns:
        pattern_list = patterns.split('\n')
    elif ',' in patterns:
        pattern_list = patterns.split(',')
    else:
        pattern_list = [patterns]
    
    # Clean each pattern to remove irrelevant information
    cleaned_patterns = []
    for pattern in pattern_list:
        # Strip whitespace
        cleaned_pattern = pattern.strip()
        
        # Skip empty patterns
        if not cleaned_pattern:
            continue
            
        # Remove special characters and extra whitespace based on pattern type
        if pattern_type.lower() == 'geographical':
            # Keep alphanumeric, spaces, hyphens, and common geographical punctuation
            cleaned_pattern = re.sub(r'[^a-zA-Z0-9\s\-.,()]', '', cleaned_pattern)
        elif pattern_type.lower() == 'cultural':
            # Keep alphanumeric, spaces, and common cultural text characters
            cleaned_pattern = re.sub(r'[^a-zA-Z0-9\s\-.,():\'"&]', '', cleaned_pattern)
        else:
            # Default cleaning: remove non-alphanumeric except spaces and basic punctuation
            cleaned_pattern = re.sub(r'[^a-zA-Z0-9\s\-.,]', '', cleaned_pattern)
        
        # Normalize whitespace
        cleaned_pattern = re.sub(r'\s+', ' ', cleaned_pattern).strip()
        
        # Only keep non-empty patterns with meaningful content (at least 2 characters)
        if len(cleaned_pattern) >= 2:
            cleaned_patterns.append(cleaned_pattern)
    
    # Remove duplicates while preserving order
    seen = set()
    deduplicated_patterns = []
    for pattern in cleaned_patterns:
        # Case-insensitive duplicate removal
        pattern_lower = pattern.lower()
        if pattern_lower not in seen:
            seen.add(pattern_lower)
            deduplicated_patterns.append(pattern)
    
    return deduplicated_patterns