# -- PRD --
# 1. BULLET: Define the structure of the report sections dictionary
#   Reason: To ensure consistency in the output format
#   Impact: Enables seamless integration with subsequent report drafting functions
#   Complexity: LOW
#   Method: Specify the keys and value types for the report sections dictionary
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement logic to categorize patterns into appropriate sections
#   Reason: To organize the extracted information in a meaningful way
#   Impact: Facilitates the creation of a coherent and well-structured report
#   Complexity: MEDIUM
#   Method: Use conditional logic to determine the appropriate section for each pattern
#           based on its type
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle edge cases such as empty or missing input patterns
#   Reason: To ensure the function is robust and can handle various input scenarios
#   Impact: Prevents potential errors or inconsistencies in the report
#   Complexity: MEDIUM
#   Method: Implement input validation and default values for missing patterns
# -- END PRD --

import json


def organize_report_sections(geographical: str, cultural: str, features: str) -> str:
    """
    Organizes geographical, cultural, and feature patterns into a structured dictionary for report generation

    Args:
        geographical: Input parameter of type str
cultural: Input parameter of type str
features: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Initialize the report sections dictionary structure
    report_sections = {
        "geographical_analysis": [],
        "cultural_analysis": [],
        "feature_analysis": [],
        "summary": ""
    }
    
    # Handle edge cases - validate and provide defaults for empty/missing inputs
    geographical = geographical if geographical and geographical.strip() else ""
    cultural = cultural if cultural and cultural.strip() else ""
    features = features if features and features.strip() else ""
    
    # Categorize geographical patterns into appropriate sections
    if geographical:
        geographical_items = [item.strip() for item in geographical.split(',') if item.strip()]
        report_sections["geographical_analysis"] = geographical_items
    
    # Categorize cultural patterns into appropriate sections
    if cultural:
        cultural_items = [item.strip() for item in cultural.split(',') if item.strip()]
        report_sections["cultural_analysis"] = cultural_items
    
    # Categorize feature patterns into appropriate sections
    if features:
        feature_items = [item.strip() for item in features.split(',') if item.strip()]
        report_sections["feature_analysis"] = feature_items
    
    # Generate summary based on available sections
    summary_parts = []
    if report_sections["geographical_analysis"]:
        summary_parts.append(f"Geographical analysis covers {len(report_sections['geographical_analysis'])} key areas")
    if report_sections["cultural_analysis"]:
        summary_parts.append(f"Cultural analysis includes {len(report_sections['cultural_analysis'])} aspects")
    if report_sections["feature_analysis"]:
        summary_parts.append(f"Feature analysis examines {len(report_sections['feature_analysis'])} elements")
    
    report_sections["summary"] = ". ".join(summary_parts) if summary_parts else "No patterns available for analysis"
    
    # Return as JSON string (note: return type annotation says str but docstring says dict)
    return json.dumps(report_sections, indent=2)