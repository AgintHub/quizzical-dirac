# -- PRD --
# 1. BULLET: Develop an algorithm to identify significant features from the input
#   patterns.
#   Reason: The ability to extract significant features is crucial for generating a
#           comprehensive world report.
#   Impact: Enhances the quality and relevance of the report by focusing on key
#           aspects.
#   Complexity: MEDIUM
#   Method: Use natural language processing techniques to analyze the patterns and
#           identify significant features.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle diverse input patterns and adapt to different data formats.
#   Reason: The input patterns may vary in structure and content, requiring a flexible
#           extraction mechanism.
#   Impact: Ensures the shim can work with various data sources and formats, improving
#           its utility.
#   Complexity: HIGH
#   Method: Implement a modular parsing system that can be easily extended to support
#           new data formats.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Optimize the extraction process for performance and scalability.
#   Reason: Large volumes of data may need to be processed, requiring an efficient
#           extraction process.
#   Impact: Reduces processing time and improves overall system performance.
#   Complexity: MEDIUM
#   Method: Utilize parallel processing techniques or optimize algorithms to minimize
#           computational overhead.
# -- END PRD --

import re
import json
from collections import Counter


def extract_significant_features(patterns: str) -> str:
    """
    Extracts significant features from the given patterns.

    Args:
        patterns: Input parameter of type str

    Returns:
        str: Output of type list
    """
    
    # Handle empty or None input
    if not patterns or not patterns.strip():
        return json.dumps([])
    
    # Initialize list to store significant features
    significant_features = []
    
    # Split patterns into lines for processing
    lines = patterns.strip().split('\n')
    
    # Extract features from each line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract numerical patterns
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', line)
        if numbers:
            significant_features.extend([f"numeric_value_{num}" for num in numbers])
        
        # Extract email patterns
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
        if emails:
            significant_features.extend([f"email_domain_{email.split('@')[1]}" for email in emails])
        
        # Extract URL patterns
        urls = re.findall(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?', line)
        if urls:
            significant_features.extend([f"url_domain_{url.split('/')[2]}" for url in urls])
        
        # Extract capitalized words (potential proper nouns)
        capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', line)
        if capitalized_words:
            significant_features.extend([f"proper_noun_{word.lower()}" for word in capitalized_words])
        
        # Extract special characters patterns
        special_chars = re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', line)
        if special_chars:
            char_counts = Counter(special_chars)
            for char, count in char_counts.items():
                if count > 1:
                    significant_features.append(f"repeated_special_char_{char}_{count}")
        
        # Extract word patterns (words longer than 6 characters)
        long_words = re.findall(r'\b[a-zA-Z]{7,}\b', line)
        if long_words:
            significant_features.extend([f"long_word_{word.lower()}" for word in long_words])
        
        # Extract date patterns
        date_patterns = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b', line)
        if date_patterns:
            significant_features.extend([f"date_pattern_{pattern}" for pattern in date_patterns])
    
    # Remove duplicates while preserving order
    unique_features = list(dict.fromkeys(significant_features))
    
    # Limit to most significant features (top 20) for performance
    if len(unique_features) > 20:
        # Count frequency of feature types
        feature_types = {}
        for feature in unique_features:
            feature_type = feature.split('_')[0] + '_' + feature.split('_')[1]
            feature_types[feature_type] = feature_types.get(feature_type, 0) + 1
        
        # Prioritize features by type frequency
        sorted_features = sorted(unique_features, key=lambda x: (
            feature_types.get(x.split('_')[0] + '_' + x.split('_')[1], 0),
            x
        ), reverse=True)
        
        unique_features = sorted_features[:20]
    
    # Return as JSON string to maintain str return type
    return json.dumps(unique_features)