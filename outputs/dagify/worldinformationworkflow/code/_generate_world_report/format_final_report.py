# -- PRD --
# 1. BULLET: The shim function will apply the required formatting standards to the input
#   report content.
#   Reason: To ensure the final report is presented in a consistent and readable
#           format.
#   Impact: The formatted report will be used as the final output of the
#           generate_world_report node.
#   Complexity: MEDIUM
#   Method: Using a templating engine or CSS styling to apply the required formatting
#           standards.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The shim will handle different types of report content, such as text and
#   section headers.
#   Reason: To ensure that the formatting is applied correctly regardless of the report
#           content.
#   Impact: The shim will be able to handle various report structures and content
#           types.
#   Complexity: MEDIUM
#   Method: Using a flexible formatting approach that can adapt to different report
#           content types.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Error handling will be implemented to handle cases where the input report
#   content is invalid or malformed.
#   Reason: To prevent the shim from failing or producing incorrect output.
#   Impact: The shim will be more robust and able to handle unexpected input.
#   Complexity: LOW
#   Method: Using try-except blocks to catch and handle exceptions, and providing a
#           default or fallback output when necessary.
# -- END PRD --

import re


def format_final_report(content: str) -> str:
    """
    A shim function that formats the final world report according to required standards.

    Args:
        content: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    try:
        # Handle cases where input is invalid or malformed
        if not content or not isinstance(content, str):
            return "# World Report\n\nNo content available."
        
        # Clean and prepare the content
        content = content.strip()
        
        # Split content into lines for processing
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Detect and format section headers (lines that are all caps or start with numbers/bullets)
            if (line.isupper() and len(line.split()) <= 10) or re.match(r'^\d+\.', line) or re.match(r'^[•-]', line):
                # Format as header
                formatted_lines.append(f"## {line}")
            elif re.match(r'^[A-Z][^.!?]*[.!?]?$', line) and len(line.split()) <= 15:
                # Potential title or major header
                formatted_lines.append(f"# {line}")
            else:
                # Regular text content - ensure proper paragraph formatting
                formatted_lines.append(line)
        
        # Join the formatted content
        formatted_content = '\n'.join(formatted_lines)
        
        # Apply final formatting standards
        # Ensure proper spacing between sections
        formatted_content = re.sub(r'\n{3,}', '\n\n', formatted_content)
        
        # Add a proper header if none exists
        if not formatted_content.startswith('#'):
            formatted_content = "# World Report\n\n" + formatted_content
        
        return formatted_content
        
    except Exception as e:
        # Error handling for unexpected cases
        return f"# World Report\n\nError formatting report: {str(e)}\n\nOriginal content:\n{content if isinstance(content, str) else 'Invalid content type'}"
