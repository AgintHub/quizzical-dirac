# -- PRD --
# 1. BULLET: Implement a function that takes the integrated narrative as input and formats
#   it into a readable string.
#   Reason: To ensure the final output is human-readable and well-structured.
#   Impact: Improves the usability of the integrated findings output.
#   Complexity: LOW
#   Method: Use Python's built-in string formatting capabilities to clean and structure
#           the narrative.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle edge cases such as empty or null input narratives.
#   Reason: To prevent errors and ensure robustness.
#   Impact: Enhances the reliability of the function.
#   Complexity: MEDIUM
#   Method: Implement input validation and error handling mechanisms.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Consider configurable formatting options to cater to different output
#   requirements.
#   Reason: To increase the function's versatility.
#   Impact: Allows for more flexible usage across different contexts.
#   Complexity: HIGH
#   Method: Introduce optional parameters for customizing the output format.
# -- END PRD --

import re


def format_narrative_output(narrative: str) -> str:
    """
    Formats the integrated narrative into a well-structured string output.

    Args:
        narrative: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Handle edge cases - empty or null input narratives
    if not narrative or narrative.strip() == "":
        return "No narrative content available."
    
    # Clean and structure the narrative using string formatting
    # Remove excessive whitespace and normalize line breaks
    cleaned_narrative = re.sub(r'\s+', ' ', narrative.strip())
    
    # Split into sentences for better formatting
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_narrative)
    
    # Filter out empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    if not sentences:
        return "No valid content found in narrative."
    
    # Format the narrative with proper structure
    formatted_output = "\n\n".join(sentences)
    
    # Add a header and ensure proper capitalization
    if formatted_output:
        # Ensure first character is capitalized
        formatted_output = formatted_output[0].upper() + formatted_output[1:] if len(formatted_output) > 1 else formatted_output.upper()
        
        # Add structured formatting
        final_output = f"NARRATIVE SUMMARY:\n\n{formatted_output}"
        
        # Ensure proper ending punctuation
        if not final_output.endswith(('.', '!', '?')):
            final_output += "."
            
        return final_output
    
    return "Unable to format narrative content."