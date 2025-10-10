# -- PRD --
# 1. BULLET: Define a weighted scoring system that combines resource utilization and
#   security configuration metrics.
#   Reason: To provide a comprehensive score that reflects both aspects of container
#           health and security.
#   Impact: Enables a holistic evaluation of container configurations, aiding in
#           decision-making for optimization and security hardening.
#   Complexity: MEDIUM
#   Method: Establish a formula that weights different metrics (e.g., CPU utilization,
#           memory usage, security vulnerabilities) appropriately, possibly
#           using a configurable weighting system.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement data processing to extract necessary metrics from input data
#   structures.
#   Reason: To feed the weighted scoring system with relevant data.
#   Impact: Allows the scoring system to accurately reflect the state of container
#           configurations based on the analysis of resource utilization
#           and security data.
#   Complexity: MEDIUM
#   Method: Use data parsing and processing techniques to extract key metrics from the
#           AnalyzeResourceUtilizationOutput and
#           CheckSecurityConfigurationsOutput structures.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle edge cases and missing data to ensure robustness of the scoring
#   system.
#   Reason: To prevent errors or inaccuracies in scoring due to incomplete or malformed
#           input data.
#   Impact: Ensures that the report score is reliable and usable even when some data is
#           missing or inconsistent.
#   Complexity: HIGH
#   Method: Implement data validation and default values for missing data, along with
#           logic to gracefully handle edge cases, such as extremely high
#           or low metric values.
# -- END PRD --

import json


def calculate_weighted_report_score(resource_data: str, security_data: str) -> float:
    """
    Calculates a weighted report score based on resource utilization and security configuration data.

    Args:
        resource_data: Input parameter of type str
security_data: Input parameter of type str

    Returns:
        float: Output of type float
    """
    
    # Define configurable weights for different metrics
    RESOURCE_WEIGHT = 0.6
    SECURITY_WEIGHT = 0.4
    
    # Initialize default scores
    resource_score = 0.0
    security_score = 0.0
    
    # Process resource utilization data
    try:
        if resource_data and resource_data.strip():
            # Try to parse as JSON first
            try:
                resource_json = json.loads(resource_data)
            except json.JSONDecodeError:
                # If not JSON, create a simple structure
                resource_json = {"raw_data": resource_data}
            
            # Extract CPU utilization (0-100%)
            cpu_usage = 0.0
            if isinstance(resource_json, dict):
                cpu_usage = float(resource_json.get('cpu_utilization', 
                                resource_json.get('cpu_usage', 
                                resource_json.get('cpu', 0))))
                # Handle percentage values > 1
                if cpu_usage > 1:
                    cpu_usage = cpu_usage / 100.0
            
            # Extract memory utilization (0-100%)
            memory_usage = 0.0
            if isinstance(resource_json, dict):
                memory_usage = float(resource_json.get('memory_utilization',
                                   resource_json.get('memory_usage',
                                   resource_json.get('memory', 0))))
                # Handle percentage values > 1
                if memory_usage > 1:
                    memory_usage = memory_usage / 100.0
            
            # Calculate resource score (inverse of utilization - lower usage = higher score)
            # Cap utilization at 1.0 to handle edge cases
            cpu_usage = min(max(cpu_usage, 0.0), 1.0)
            memory_usage = min(max(memory_usage, 0.0), 1.0)
            
            # Score calculation: higher utilization = lower score
            cpu_score = 1.0 - cpu_usage
            memory_score = 1.0 - memory_usage
            resource_score = (cpu_score + memory_score) / 2.0
            
    except (ValueError, TypeError, AttributeError) as e:
        # Handle malformed resource data with default score
        resource_score = 0.5  # Neutral score for missing/invalid data
    
    # Process security configuration data
    try:
        if security_data and security_data.strip():
            # Try to parse as JSON first
            try:
                security_json = json.loads(security_data)
            except json.JSONDecodeError:
                # If not JSON, analyze as text for security keywords
                security_json = {"raw_data": security_data}
            
            # Extract security vulnerabilities count
            vulnerabilities = 0
            if isinstance(security_json, dict):
                vulnerabilities = int(security_json.get('vulnerabilities',
                                    security_json.get('vuln_count',
                                    security_json.get('security_issues', 0))))
            
            # Extract security compliance score (0-100%)
            compliance_score = 1.0  # Default to perfect compliance
            if isinstance(security_json, dict):
                compliance = security_json.get('compliance_score',
                           security_json.get('compliance',
                           security_json.get('security_score', 100)))
                compliance_score = float(compliance)
                if compliance_score > 1:
                    compliance_score = compliance_score / 100.0
            
            # Calculate security score
            # Factor in vulnerabilities (each vulnerability reduces score)
            vuln_penalty = min(vulnerabilities * 0.1, 0.8)  # Cap penalty at 0.8
            compliance_score = min(max(compliance_score, 0.0), 1.0)
            
            security_score = max(compliance_score - vuln_penalty, 0.0)
            
    except (ValueError, TypeError, AttributeError) as e:
        # Handle malformed security data with default score
        security_score = 0.5  # Neutral score for missing/invalid data
    
    # Calculate weighted final score
    weighted_score = (resource_score * RESOURCE_WEIGHT) + (security_score * SECURITY_WEIGHT)
    
    # Ensure score is between 0.0 and 1.0
    final_score = min(max(weighted_score, 0.0), 1.0)
    
    return final_score