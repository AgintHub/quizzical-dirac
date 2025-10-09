# -- PRD --
# 1. BULLET: Implement data validation against known cultural data standards and the
#   provided world context.
#   Reason: To ensure the accuracy and relevance of the cultural data collected.
#   Impact: Improves the reliability of cultural data used in subsequent workflow
#           steps.
#   Complexity: MEDIUM
#   Method: Use a combination of natural language processing (NLP) techniques and
#           knowledge graphs to validate cultural data against known
#           standards and the world context.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different types of cultural data (religions, languages, cultural
#   practices) using type-specific validation rules.
#   Reason: Different types of cultural data have different validation requirements.
#   Impact: Enhances the flexibility and applicability of the validation function
#           across various cultural data types.
#   Complexity: HIGH
#   Method: Develop modular validation rules for each data type, leveraging type-
#           specific knowledge bases and ontologies.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Provide a feedback mechanism to indicate the confidence level of the
#   validation result.
#   Reason: To give users an understanding of the reliability of the validated data.
#   Impact: Increases user trust in the validated cultural data by providing
#           transparency on the validation process.
#   Complexity: MEDIUM
#   Method: Implement a scoring system based on the validation process, considering
#           factors like data source reliability and matching accuracy.
# -- END PRD --

import re
from typing import List


def validate_cultural_data(data: str, data_type: str, world_context: str) -> List[str]:
    """
    Validates cultural data for accuracy and relevance within a defined world context.

    Args:
        data: Input parameter of type str
data_type: Input parameter of type str
world_context: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    # Initialize validation results list
    validation_results = []
    
    # Basic data quality checks
    if not data or not data.strip():
        validation_results.append("INVALID: Empty or whitespace-only data")
        return validation_results
    
    if not data_type or data_type not in ['religion', 'language', 'cultural_practice']:
        validation_results.append("INVALID: Unsupported or missing data_type")
        return validation_results
    
    # Clean and normalize input data
    cleaned_data = re.sub(r'[^\w\s-]', '', data.strip().lower())
    
    # Define validation rules based on data type
    if data_type == 'religion':
        # Known religions validation
        known_religions = {
            'christianity', 'islam', 'judaism', 'hinduism', 'buddhism', 'sikhism',
            'jainism', 'zoroastrianism', 'bahai', 'shintoism', 'taoism', 'confucianism',
            'animism', 'paganism', 'wicca', 'atheism', 'agnosticism'
        }
        
        # Check if religion is recognized
        found_match = False
        for religion in known_religions:
            if religion in cleaned_data or cleaned_data in religion:
                validation_results.append(f"VALID: Recognized religion - {religion}")
                found_match = True
                break
        
        if not found_match:
            validation_results.append("WARNING: Unrecognized religion - requires manual verification")
    
    elif data_type == 'language':
        # Known languages validation (ISO 639-1 common languages)
        known_languages = {
            'english', 'spanish', 'french', 'german', 'italian', 'portuguese',
            'russian', 'chinese', 'japanese', 'korean', 'arabic', 'hindi',
            'bengali', 'punjabi', 'tamil', 'telugu', 'marathi', 'gujarati',
            'urdu', 'persian', 'turkish', 'greek', 'hebrew', 'thai',
            'vietnamese', 'indonesian', 'malay', 'filipino', 'dutch', 'swedish',
            'norwegian', 'danish', 'polish', 'czech', 'hungarian', 'romanian'
        }
        
        # Check if language is recognized
        found_match = False
        for language in known_languages:
            if language in cleaned_data or cleaned_data in language:
                validation_results.append(f"VALID: Recognized language - {language}")
                found_match = True
                break
        
        if not found_match:
            validation_results.append("WARNING: Unrecognized language - requires manual verification")
    
    elif data_type == 'cultural_practice':
        # Cultural practice keywords validation
        practice_keywords = {
            'festival', 'ceremony', 'ritual', 'tradition', 'custom', 'celebration',
            'dance', 'music', 'art', 'cuisine', 'clothing', 'marriage', 'funeral',
            'birth', 'coming of age', 'harvest', 'religious', 'seasonal',
            'wedding', 'prayer', 'meditation', 'pilgrimage'
        }
        
        # Check if practice contains recognized keywords
        found_keywords = []
        for keyword in practice_keywords:
            if keyword in cleaned_data:
                found_keywords.append(keyword)
        
        if found_keywords:
            validation_results.append(f"VALID: Cultural practice with recognized elements - {', '.join(found_keywords)}")
        else:
            validation_results.append("WARNING: Cultural practice with no recognized keywords - requires manual verification")
    
    # World context validation
    if world_context and world_context.strip():
        context_lower = world_context.lower()
        
        # Check for geographical context
        continents = ['africa', 'asia', 'europe', 'north america', 'south america', 'australia', 'antarctica']
        regions = ['middle east', 'southeast asia', 'east asia', 'south asia', 'central asia',
                  'eastern europe', 'western europe', 'northern europe', 'southern europe',
                  'caribbean', 'central america', 'oceania']
        
        context_found = False
        for continent in continents:
            if continent in context_lower:
                validation_results.append(f"CONTEXT: Geographical context identified - {continent}")
                context_found = True
                break
        
        if not context_found:
            for region in regions:
                if region in context_lower:
                    validation_results.append(f"CONTEXT: Regional context identified - {region}")
                    context_found = True
                    break
        
        if not context_found:
            validation_results.append("CONTEXT: No recognized geographical context")
        
        # Check for temporal context
        time_periods = ['ancient', 'medieval', 'renaissance', 'modern', 'contemporary',
                       'traditional', 'historical', 'current', 'past', 'present']
        
        for period in time_periods:
            if period in context_lower:
                validation_results.append(f"CONTEXT: Temporal context identified - {period}")
                break
    else:
        validation_results.append("CONTEXT: No world context provided")
    
    # Add confidence assessment
    valid_count = len([r for r in validation_results if r.startswith('VALID')])
    warning_count = len([r for r in validation_results if r.startswith('WARNING')])
    total_checks = valid_count + warning_count
    
    if total_checks > 0:
        confidence = (valid_count / total_checks) * 100
        validation_results.append(f"CONFIDENCE: {confidence:.1f}% validation confidence")
    else:
        validation_results.append("CONFIDENCE: Unable to calculate confidence")
    
    return validation_results