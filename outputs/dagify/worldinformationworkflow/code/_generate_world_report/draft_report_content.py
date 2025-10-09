# -- PRD --
# 1. BULLET: Implement a function to iterate through the report sections and summarize the
#   findings.
#   Reason: To generate a coherent and comprehensive report, the function needs to
#           process each section's content.
#   Impact: The drafted report will provide a clear summary of the findings, making it
#           easier to review and refine.
#   Complexity: MEDIUM
#   Method: Use a template engine like Jinja2 to create a report template, and then
#           populate it with the section data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different types of report sections (e.g., geographical, cultural,
#   significant features).
#   Reason: The report sections may contain different types of information that need to
#           be handled appropriately.
#   Impact: The report will be more comprehensive and accurate, covering all necessary
#           aspects.
#   Complexity: HIGH
#   Method: Implement a modular design where each section type is handled by a separate
#           module or function, allowing for easy extension and
#           modification.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Ensure the drafted report is well-structured and easy to read.
#   Reason: A well-structured report is crucial for effective communication of the
#           findings.
#   Impact: The report will be more readable and understandable, facilitating its use
#           by stakeholders.
#   Complexity: LOW
#   Method: Use standard formatting techniques such as headings, bullet points, and
#           clear section demarcations.
# -- END PRD --

import json
import re


def draft_report_content(sections: str) -> str:
    """
    Drafts a report by summarizing findings in each section based on the provided report sections.

    Args:
        sections: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse the sections input - assume it's JSON string or structured text
    try:
        # Try to parse as JSON first
        if sections.strip().startswith('{') or sections.strip().startswith('['):
            section_data = json.loads(sections)
        else:
            # If not JSON, treat as plain text and create basic structure
            section_data = {'content': sections}
    except (json.JSONDecodeError, ValueError):
        # Fallback to treating as plain text
        section_data = {'content': sections}
    
    # Initialize report structure
    report_lines = []
    report_lines.append("# RESEARCH FINDINGS REPORT")
    report_lines.append("="*50)
    report_lines.append("")
    
    # Handle different types of report sections
    if isinstance(section_data, dict):
        # Process dictionary-based sections
        for section_type, content in section_data.items():
            # Format section headers
            formatted_header = section_type.replace('_', ' ').title()
            report_lines.append(f"## {formatted_header}")
            report_lines.append("-" * (len(formatted_header) + 3))
            
            # Handle different section types with specific formatting
            if 'geographical' in section_type.lower() or 'location' in section_type.lower():
                report_lines.append("### Geographic Analysis:")
                if isinstance(content, str):
                    report_lines.append(f"• Location findings: {content}")
                elif isinstance(content, list):
                    for item in content:
                        report_lines.append(f"• {item}")
                        
            elif 'cultural' in section_type.lower() or 'culture' in section_type.lower():
                report_lines.append("### Cultural Observations:")
                if isinstance(content, str):
                    report_lines.append(f"• Cultural insights: {content}")
                elif isinstance(content, list):
                    for item in content:
                        report_lines.append(f"• {item}")
                        
            elif 'significant' in section_type.lower() or 'feature' in section_type.lower():
                report_lines.append("### Significant Features:")
                if isinstance(content, str):
                    report_lines.append(f"• Key findings: {content}")
                elif isinstance(content, list):
                    for item in content:
                        report_lines.append(f"• {item}")
            else:
                # Generic section handling
                if isinstance(content, str):
                    # Split long content into paragraphs
                    paragraphs = content.split('\n')
                    for para in paragraphs:
                        if para.strip():
                            report_lines.append(f"• {para.strip()}")
                elif isinstance(content, list):
                    for item in content:
                        report_lines.append(f"• {str(item)}")
                elif isinstance(content, dict):
                    for key, value in content.items():
                        report_lines.append(f"• {key}: {value}")
            
            report_lines.append("")  # Add spacing between sections
            
    elif isinstance(section_data, list):
        # Process list-based sections
        report_lines.append("## Research Findings")
        report_lines.append("-" * 20)
        for i, item in enumerate(section_data, 1):
            report_lines.append(f"### Finding {i}:")
            report_lines.append(f"• {str(item)}")
            report_lines.append("")
    else:
        # Handle plain text input
        report_lines.append("## Summary")
        report_lines.append("-" * 10)
        
        # Split text into logical sections
        text_content = str(section_data)
        sentences = re.split(r'[.!?]+', text_content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                report_lines.append(f"• {sentence}")
        report_lines.append("")
    
    # Add summary section
    report_lines.append("## Executive Summary")
    report_lines.append("-" * 20)
    report_lines.append("This report summarizes the key findings from the research analysis.")
    report_lines.append("The sections above provide detailed insights into various aspects")
    report_lines.append("of the subject matter, organized for clear comprehension and review.")
    report_lines.append("")
    
    # Add conclusion
    report_lines.append("## Conclusion")
    report_lines.append("-" * 13)
    report_lines.append("The analysis provides comprehensive coverage of the research area,")
    report_lines.append("with structured findings that support further investigation and")
    report_lines.append("decision-making processes.")
    
    # Join all lines into final report
    final_report = "\n".join(report_lines)
    
    return final_report