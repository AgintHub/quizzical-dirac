# -- PRD --
# 1. BULLET: Process security configuration data to identify potential security risks and
#   vulnerabilities.
#   Reason: To provide actionable security recommendations, the shim needs to analyze
#           the security data.
#   Impact: The quality of the security recommendations depends on the accuracy of this
#           analysis.
#   Complexity: MEDIUM
#   Method: Implement a parsing mechanism to extract relevant information from the
#           security data, and then apply a set of predefined rules or
#           heuristics to identify potential security issues.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Generate clear and actionable security recommendations based on the analysis.
#   Reason: The purpose of this shim is to provide useful security recommendations.
#   Impact: The effectiveness of the security recommendations will directly impact the
#           user's ability to secure their container configurations.
#   Complexity: HIGH
#   Method: Use a template-based approach to generate recommendations, leveraging the
#           insights gained from the analysis of security data. Consider
#           integrating with a knowledge base or expert system for more
#           sophisticated recommendations.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the security recommendations into a user-friendly output.
#   Reason: To ensure the recommendations are easily understood and implemented by the
#           user.
#   Impact: Improves the usability of the security recommendations.
#   Complexity: LOW
#   Method: Use a standardized formatting template to present the recommendations in a
#           clear and concise manner, possibly using markdown or a similar
#           lightweight markup language.
# -- END PRD --

import json
import re


def compile_security_recommendations(security_data: str) -> str:
    """
    This shim compiles security recommendations based on the security data provided by the check_security_configurations node.

    Args:
        security_data: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse security data to extract relevant information
    security_issues = []
    recommendations = []
    
    try:
        # Try to parse as JSON first
        parsed_data = json.loads(security_data)
        
        # Analyze for common security vulnerabilities
        if isinstance(parsed_data, dict):
            # Check for exposed ports
            if 'ports' in parsed_data:
                exposed_ports = parsed_data.get('ports', [])
                for port in exposed_ports:
                    if port in [22, 23, 80, 443, 3389]:
                        security_issues.append(f"Potentially risky port {port} exposed")
                        recommendations.append(f"Consider restricting access to port {port} or using secure alternatives")
            
            # Check for root user usage
            if 'user' in parsed_data and parsed_data.get('user') == 'root':
                security_issues.append("Container running as root user")
                recommendations.append("Use a non-root user to run container processes")
            
            # Check for privileged mode
            if parsed_data.get('privileged', False):
                security_issues.append("Container running in privileged mode")
                recommendations.append("Avoid using privileged mode unless absolutely necessary")
            
            # Check for missing security contexts
            if 'securityContext' not in parsed_data:
                security_issues.append("No security context defined")
                recommendations.append("Define appropriate security context with runAsNonRoot and readOnlyRootFilesystem")
                
    except json.JSONDecodeError:
        # If not JSON, treat as plain text and look for patterns
        
        # Check for exposed sensitive information
        if re.search(r'(password|secret|key|token)\s*[:=]\s*\S+', security_data, re.IGNORECASE):
            security_issues.append("Potential secrets exposed in configuration")
            recommendations.append("Use environment variables or secret management systems for sensitive data")
        
        # Check for insecure protocols
        if re.search(r'http://', security_data, re.IGNORECASE):
            security_issues.append("Insecure HTTP protocol detected")
            recommendations.append("Use HTTPS instead of HTTP for secure communication")
        
        # Check for default credentials
        if re.search(r'(admin|administrator|root).*password', security_data, re.IGNORECASE):
            security_issues.append("Potential default credentials found")
            recommendations.append("Change default usernames and passwords")
    
    # Generate formatted output
    output_lines = []
    output_lines.append("# Security Analysis Report")
    output_lines.append("")
    
    if security_issues:
        output_lines.append("## Security Issues Identified:")
        for i, issue in enumerate(security_issues, 1):
            output_lines.append(f"{i}. {issue}")
        output_lines.append("")
        
        output_lines.append("## Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            output_lines.append(f"{i}. {rec}")
        output_lines.append("")
    else:
        output_lines.append("## No immediate security issues detected")
        output_lines.append("")
        output_lines.append("### General Recommendations:")
        output_lines.append("1. Regularly update container images and dependencies")
        output_lines.append("2. Implement proper access controls and authentication")
        output_lines.append("3. Use security scanning tools for continuous monitoring")
        output_lines.append("4. Follow the principle of least privilege")
    
    output_lines.append("")
    output_lines.append("*This analysis is based on common security best practices and patterns.*")
    
    return "\n".join(output_lines)