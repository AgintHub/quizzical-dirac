# -- PRD --
# 1. BULLET: Implement a parsing mechanism to convert the input string into a dictionary.
#   Reason: The input string needs to be structured into a usable format for further
#           processing.
#   Impact: Enables the extraction of geographical, cultural, and significant patterns
#           from the integrated findings.
#   Complexity: MEDIUM
#   Method: Use a combination of natural language processing (NLP) techniques and
#           regular expressions to parse the input string.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle varying input formats and potential errors in the input string.
#   Reason: The input may not always be in the expected format, and the parsing
#           mechanism needs to be robust.
#   Impact: Ensures that the parsing function can handle different types of input and
#           provides meaningful error messages when necessary.
#   Complexity: HIGH
#   Method: Implement error handling mechanisms and input validation to ensure
#           robustness.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Optimize the parsing function for performance.
#   Reason: The parsing function will be a critical component in the data processing
#           pipeline.
#   Impact: Improves the overall efficiency of the data processing pipeline.
#   Complexity: LOW
#   Method: Use efficient data structures and algorithms to minimize processing time.
# -- END PRD --

import re
import json
from typing import Dict, Any, List


def parse_integrated_findings(findings: str) -> str:
    """
    Parses integrated findings into a structured dictionary format.

    Args:
        findings: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    
    # Initialize the result dictionary
    parsed_data: Dict[str, Any] = {
        "geographical_patterns": [],
        "cultural_patterns": [],
        "significant_findings": [],
        "metadata": {
            "total_entries": 0,
            "parsing_errors": []
        }
    }
    
    try:
        # Handle empty or None input
        if not findings or not isinstance(findings, str):
            parsed_data["metadata"]["parsing_errors"].append("Invalid or empty input provided")
            return json.dumps(parsed_data)
        
        # Clean and normalize the input string
        cleaned_findings = findings.strip()
        
        # Split findings into individual entries (assuming entries are separated by newlines or specific delimiters)
        entries = re.split(r'\n+|\r\n+|;+', cleaned_findings)
        entries = [entry.strip() for entry in entries if entry.strip()]
        
        parsed_data["metadata"]["total_entries"] = len(entries)
        
        # Define patterns for different types of findings
        geo_patterns = [
            r'\b(?:located|found|situated|positioned)\s+(?:in|at|near)\s+([^.\n]+)',
            r'\b(region|area|location|place|city|country|continent)\s*:?\s*([^.\n]+)',
            r'\b(north|south|east|west|northern|southern|eastern|western)\s+([^.\n]+)',
            r'\b(coordinates?|latitude|longitude|GPS)\s*:?\s*([^.\n]+)'
        ]
        
        cultural_patterns = [
            r'\b(culture|cultural|tradition|traditional|custom|ritual|belief)\s+([^.\n]+)',
            r'\b(language|dialect|ethnic|ethnicity|heritage)\s*:?\s*([^.\n]+)',
            r'\b(festival|ceremony|celebration|practice)\s+([^.\n]+)'
        ]
        
        significance_patterns = [
            r'\b(significant|important|notable|remarkable|key|critical)\s+([^.\n]+)',
            r'\b(finding|discovery|observation|result|conclusion)\s*:?\s*([^.\n]+)',
            r'\b(indicates?|suggests?|reveals?|shows?)\s+([^.\n]+)'
        ]
        
        # Process each entry
        for i, entry in enumerate(entries):
            try:
                entry_processed = False
                
                # Check for geographical patterns
                for pattern in geo_patterns:
                    matches = re.finditer(pattern, entry, re.IGNORECASE)
                    for match in matches:
                        parsed_data["geographical_patterns"].append({
                            "type": "geographical",
                            "content": match.group(0),
                            "extracted_value": match.group(1) if len(match.groups()) >= 1 else match.group(0),
                            "source_entry": i + 1
                        })
                        entry_processed = True
                
                # Check for cultural patterns
                for pattern in cultural_patterns:
                    matches = re.finditer(pattern, entry, re.IGNORECASE)
                    for match in matches:
                        parsed_data["cultural_patterns"].append({
                            "type": "cultural",
                            "content": match.group(0),
                            "extracted_value": match.group(1) if len(match.groups()) >= 1 else match.group(0),
                            "source_entry": i + 1
                        })
                        entry_processed = True
                
                # Check for significance patterns
                for pattern in significance_patterns:
                    matches = re.finditer(pattern, entry, re.IGNORECASE)
                    for match in matches:
                        parsed_data["significant_findings"].append({
                            "type": "significant",
                            "content": match.group(0),
                            "extracted_value": match.group(1) if len(match.groups()) >= 1 else match.group(0),
                            "source_entry": i + 1
                        })
                        entry_processed = True
                
                # If no patterns matched, add as general finding
                if not entry_processed and len(entry) > 10:  # Only add substantial entries
                    parsed_data["significant_findings"].append({
                        "type": "general",
                        "content": entry,
                        "extracted_value": entry,
                        "source_entry": i + 1
                    })
                    
            except Exception as entry_error:
                parsed_data["metadata"]["parsing_errors"].append(f"Error processing entry {i + 1}: {str(entry_error)}")
        
        # Remove duplicates while preserving order
        def remove_duplicates(pattern_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            seen = set()
            unique_list = []
            for item in pattern_list:
                content_key = item["content"].lower().strip()
                if content_key not in seen:
                    seen.add(content_key)
                    unique_list.append(item)
            return unique_list
        
        parsed_data["geographical_patterns"] = remove_duplicates(parsed_data["geographical_patterns"])
        parsed_data["cultural_patterns"] = remove_duplicates(parsed_data["cultural_patterns"])
        parsed_data["significant_findings"] = remove_duplicates(parsed_data["significant_findings"])
        
    except Exception as e:
        parsed_data["metadata"]["parsing_errors"].append(f"General parsing error: {str(e)}")
    
    # Convert dictionary to JSON string for return
    try:
        return json.dumps(parsed_data, ensure_ascii=False, indent=2)
    except Exception as json_error:
        # Fallback in case of JSON serialization issues
        fallback_result = {
            "error": f"Failed to serialize results: {str(json_error)}",
            "raw_findings_length": len(findings) if findings else 0
        }
        return json.dumps(fallback_result)