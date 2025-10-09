# -- PRD --
# 1. BULLET: Implement natural language processing (NLP) techniques to analyze the input
#   data and extract the workflow's purpose.
#   Reason: To understand the context and objectives of the workflow.
#   Impact: Enables the system to determine the appropriate context for 'world' in the
#           workflow.
#   Complexity: MEDIUM
#   Method: Use NLP libraries such as spaCy or NLTK to process the input data and
#           identify key elements that define the workflow's purpose.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Integrate the analysis of additional keyword arguments (kwargs) to refine the
#   understanding of the workflow's purpose.
#   Reason: To incorporate any additional context or constraints provided through
#           kwargs.
#   Impact: Enhances the accuracy of the workflow purpose analysis by considering all
#           available information.
#   Complexity: LOW
#   Method: Parse kwargs and use their values to adjust the NLP analysis or directly
#           incorporate relevant information.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Ensure the output is a clear and concise string representation of the
#   workflow's purpose.
#   Reason: To facilitate easy consumption by subsequent nodes in the workflow.
#   Impact: Simplifies the integration with downstream processes that rely on the
#           analyzed workflow purpose.
#   Complexity: LOW
#   Method: Use string formatting techniques to generate a clear and concise output
#           string.
# -- END PRD --

import re
import json


def analyze_workflow_purpose(input_data: str, kwargs: str) -> str:
    """
    Analyzes the workflow's purpose based on the input data and additional parameters.

    Args:
        input_data: Input parameter of type str
kwargs: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse kwargs if it's JSON-formatted
    additional_context = {}
    try:
        if kwargs and kwargs.strip():
            additional_context = json.loads(kwargs)
    except (json.JSONDecodeError, ValueError):
        # If kwargs is not valid JSON, treat as plain text
        additional_context = {'additional_info': kwargs}
    
    # Clean and normalize input data for NLP analysis
    cleaned_input = re.sub(r'[^\w\s]', ' ', input_data.lower())
    cleaned_input = re.sub(r'\s+', ' ', cleaned_input).strip()
    
    # Extract key purpose-indicating words and phrases
    purpose_keywords = {
        'data_processing': ['process', 'transform', 'convert', 'parse', 'extract', 'clean'],
        'analysis': ['analyze', 'examine', 'evaluate', 'assess', 'study', 'investigate'],
        'automation': ['automate', 'schedule', 'trigger', 'execute', 'run', 'perform'],
        'integration': ['integrate', 'connect', 'sync', 'merge', 'combine', 'link'],
        'monitoring': ['monitor', 'track', 'watch', 'observe', 'alert', 'notify'],
        'reporting': ['report', 'generate', 'create', 'produce', 'compile', 'summarize']
    }
    
    # Identify workflow purpose based on keyword matching
    detected_purposes = []
    words = cleaned_input.split()
    
    for category, keywords in purpose_keywords.items():
        for keyword in keywords:
            if keyword in words:
                detected_purposes.append(category)
                break
    
    # Extract action verbs and objects from input
    action_pattern = r'\b(to|will|shall|should|must)\s+(\w+(?:\s+\w+)*?)\b'
    actions = re.findall(action_pattern, cleaned_input, re.IGNORECASE)
    
    # Incorporate kwargs context
    if additional_context:
        for key, value in additional_context.items():
            if isinstance(value, str):
                value_words = re.sub(r'[^\w\s]', ' ', value.lower()).split()
                for category, keywords in purpose_keywords.items():
                    for keyword in keywords:
                        if keyword in value_words and category not in detected_purposes:
                            detected_purposes.append(category)
    
    # Generate purpose description
    if detected_purposes:
        main_purpose = detected_purposes[0]  # Primary purpose
        purpose_description = f"This workflow is designed for {main_purpose.replace('_', ' ')}"
        
        if len(detected_purposes) > 1:
            secondary_purposes = ', '.join([p.replace('_', ' ') for p in detected_purposes[1:]])
            purpose_description += f" with additional focus on {secondary_purposes}"
    else:
        # Fallback: extract general intent from input
        if any(word in cleaned_input for word in ['workflow', 'process', 'task']):
            purpose_description = "This workflow is designed to execute a series of automated tasks"
        else:
            purpose_description = "This workflow is designed to process and handle the provided input data"
    
    # Add action context if found
    if actions:
        action_verbs = [action[1] for action in actions]
        unique_actions = list(set(action_verbs))
        if unique_actions:
            purpose_description += f" by performing actions such as {', '.join(unique_actions[:3])}"
    
    # Include kwargs context in output if relevant
    if additional_context and any(key in ['goal', 'objective', 'purpose', 'intent'] for key in additional_context.keys()):
        relevant_context = [str(v) for k, v in additional_context.items() if k in ['goal', 'objective', 'purpose', 'intent']]
        if relevant_context:
            purpose_description += f" with the specific objective of {relevant_context[0]}"
    
    # Ensure proper sentence structure
    purpose_description = purpose_description.strip()
    if not purpose_description.endswith('.'):
        purpose_description += '.'
    
    return purpose_description