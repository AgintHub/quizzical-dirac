# -- PRD --
# 1. BULLET: Implement a filtering mechanism that assesses the significance of cultural
#   patterns based on the provided analysis.
#   Reason: This is necessary to identify and isolate patterns that are deemed
#           significant according to the threshold.
#   Impact: The system will be able to distinguish between significant and
#           insignificant cultural patterns, enhancing the quality of the
#           analysis.
#   Complexity: MEDIUM
#   Method: Develop an algorithm that parses the pattern analysis and compares it
#           against the threshold to filter significant patterns.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different data formats for pattern analysis to ensure compatibility
#   and flexibility.
#   Reason: The input data format may vary, and the shim needs to be adaptable to these
#           variations.
#   Impact: The shim will be robust and capable of processing different types of input
#           data, making it versatile for various applications.
#   Complexity: HIGH
#   Method: Implement data parsing and normalization techniques to handle diverse input
#           formats and convert them into a standard format for analysis.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Optimize the filtering process for performance to handle large datasets
#   efficiently.
#   Reason: Large datasets are common, and inefficient processing can lead to
#           significant delays.
#   Impact: The system will be able to process large datasets quickly, improving
#           overall system responsiveness and user experience.
#   Complexity: MEDIUM
#   Method: Utilize efficient data structures and algorithms, such as binary search or
#           hash tables, to optimize the filtering process.
# -- END PRD --

from typing import List

import json
import re


def filter_significant_patterns(pattern_analysis: str, threshold: str) -> List[str]:
    """
    Filters significant cultural patterns based on their analysis and a given threshold.

    Args:
        pattern_analysis: Input parameter of type str
threshold: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Parse the threshold value
    try:
        threshold_value = float(threshold)
    except ValueError:
        # Try to extract numeric value from threshold string
        threshold_match = re.search(r'\d+\.?\d*', threshold)
        if threshold_match:
            threshold_value = float(threshold_match.group())
        else:
            threshold_value = 0.5  # Default threshold
    
    # Parse pattern analysis - handle different data formats
    patterns_data = []
    
    # Try to parse as JSON first
    try:
        patterns_data = json.loads(pattern_analysis)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to parse as structured text
        # Look for patterns like "Pattern: X, Significance: Y" or similar
        pattern_lines = pattern_analysis.strip().split('\n')
        for line in pattern_lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract pattern name and significance score
            # Handle various formats like "Pattern: X, Score: Y" or "X: Y" etc.
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    pattern_name = parts[0].strip()
                    score_part = parts[1].strip()
                    
                    # Extract numeric score from the score part
                    score_match = re.search(r'\d+\.?\d*', score_part)
                    if score_match:
                        score = float(score_match.group())
                        patterns_data.append({
                            'pattern': pattern_name,
                            'significance': score
                        })
    
    # Filter significant patterns based on threshold
    significant_patterns = []
    
    if isinstance(patterns_data, list):
        for item in patterns_data:
            if isinstance(item, dict):
                # Handle dictionary format
                pattern_name = item.get('pattern', item.get('name', str(item)))
                significance = item.get('significance', item.get('score', item.get('value', 0)))
                
                try:
                    significance_value = float(significance)
                    if significance_value >= threshold_value:
                        significant_patterns.append(str(pattern_name))
                except (ValueError, TypeError):
                    continue
            elif isinstance(item, str):
                # Handle string format - assume it's already significant if listed
                significant_patterns.append(item)
    elif isinstance(patterns_data, dict):
        # Handle single dictionary or nested dictionary format
        for key, value in patterns_data.items():
            try:
                if isinstance(value, (int, float)) and float(value) >= threshold_value:
                    significant_patterns.append(str(key))
                elif isinstance(value, dict):
                    significance = value.get('significance', value.get('score', 0))
                    if float(significance) >= threshold_value:
                        significant_patterns.append(str(key))
            except (ValueError, TypeError):
                continue
    
    # Remove duplicates while preserving order
    seen = set()
    filtered_patterns = []
    for pattern in significant_patterns:
        if pattern not in seen:
            seen.add(pattern)
            filtered_patterns.append(pattern)
    
    return filtered_patterns