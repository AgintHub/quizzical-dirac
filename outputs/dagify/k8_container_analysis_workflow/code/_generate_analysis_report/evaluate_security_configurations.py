# -- PRD --
# 1. BULLET: Analyze the network policy status to determine its effectiveness in securing
#   the container configurations.
#   Reason: Understanding the network policy is crucial for identifying potential
#           security risks and hardening opportunities.
#   Impact: This analysis will directly influence the security insights and
#           recommendations provided in the final report.
#   Complexity: MEDIUM
#   Method: Implement a policy evaluation engine that assesses the network policy
#           against a set of predefined security benchmarks.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Assess the secret management status to ensure it adheres to best practices
#   for securing sensitive information.
#   Reason: Proper secret management is critical for preventing unauthorized access to
#           sensitive data.
#   Impact: The assessment will contribute to the overall security posture and
#           recommendations for improvement.
#   Complexity: HIGH
#   Method: Develop a module that evaluates secret management practices against
#           industry standards and best practices.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Evaluate the identified vulnerabilities to prioritize remediation efforts
#   based on risk severity.
#   Reason: Understanding the vulnerabilities is essential for focusing remediation
#           efforts on the most critical issues.
#   Impact: This evaluation will inform the security recommendations and prioritization
#           in the final report.
#   Complexity: MEDIUM
#   Method: Utilize a vulnerability scoring system (e.g., CVSS) to assess and
#           prioritize identified vulnerabilities.
# -- END PRD --


def evaluate_security_configurations(network_policy: str, secret_management: str, vulnerabilities: str) -> str:
    """
    Evaluates security configurations based on network policy, secret management, and identified vulnerabilities to provide security insights.

    Args:
        network_policy: Input parameter of type str
secret_management: Input parameter of type str
vulnerabilities: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # --- Network Policy Analysis ---
    network_score = 0
    network_issues = []
    
    # Check for basic network policy configurations
    if "NetworkPolicy" in network_policy:
        network_score += 30
    else:
        network_issues.append("No NetworkPolicy resources found")
    
    # Check for ingress/egress rules
    if "ingress" in network_policy.lower():
        network_score += 20
    else:
        network_issues.append("No ingress rules defined")
        
    if "egress" in network_policy.lower():
        network_score += 20
    else:
        network_issues.append("No egress rules defined")
    
    # Check for pod selectors
    if "podSelector" in network_policy:
        network_score += 15
    else:
        network_issues.append("No pod selectors configured")
        
    # Check for namespace selectors
    if "namespaceSelector" in network_policy:
        network_score += 15
    else:
        network_issues.append("No namespace selectors configured")
    
    # --- Secret Management Assessment ---
    secret_score = 0
    secret_issues = []
    
    # Check for encrypted secrets
    if "encryption" in secret_management.lower() or "encrypted" in secret_management.lower():
        secret_score += 25
    else:
        secret_issues.append("Secrets are not encrypted at rest")
    
    # Check for RBAC on secrets
    if "rbac" in secret_management.lower() or "role" in secret_management.lower():
        secret_score += 25
    else:
        secret_issues.append("No RBAC controls found for secret access")
    
    # Check for secret rotation
    if "rotation" in secret_management.lower() or "rotate" in secret_management.lower():
        secret_score += 20
    else:
        secret_issues.append("No secret rotation policy found")
    
    # Check for external secret management
    if any(provider in secret_management.lower() for provider in ["vault", "aws", "azure", "gcp", "external"]):
        secret_score += 20
    else:
        secret_issues.append("No external secret management system detected")
    
    # Check for secret scanning
    if "scan" in secret_management.lower() or "detect" in secret_management.lower():
        secret_score += 10
    else:
        secret_issues.append("No secret scanning mechanisms found")
    
    # --- Vulnerability Assessment ---
    vuln_score = 0
    vuln_issues = []
    critical_vulns = 0
    high_vulns = 0
    medium_vulns = 0
    
    # Parse vulnerabilities and assign CVSS-like scoring
    vuln_lines = vulnerabilities.split('\n')
    for line in vuln_lines:
        line_lower = line.lower()
        if any(critical_term in line_lower for critical_term in ["critical", "rce", "remote code", "privilege escalation", "cvss:9", "cvss:10"]):
            critical_vulns += 1
        elif any(high_term in line_lower for high_term in ["high", "injection", "xss", "csrf", "cvss:7", "cvss:8"]):
            high_vulns += 1
        elif any(medium_term in line_lower for medium_term in ["medium", "disclosure", "dos", "cvss:4", "cvss:5", "cvss:6"]):
            medium_vulns += 1
    
    # Score based on vulnerability count and severity
    total_vulns = critical_vulns + high_vulns + medium_vulns
    
    if total_vulns == 0:
        vuln_score = 100
    else:
        # Penalty system based on severity
        penalty = (critical_vulns * 40) + (high_vulns * 20) + (medium_vulns * 10)
        vuln_score = max(0, 100 - penalty)
    
    if critical_vulns > 0:
        vuln_issues.append(f"{critical_vulns} critical vulnerabilities require immediate attention")
    if high_vulns > 0:
        vuln_issues.append(f"{high_vulns} high severity vulnerabilities need prompt remediation")
    if medium_vulns > 0:
        vuln_issues.append(f"{medium_vulns} medium severity vulnerabilities should be addressed")
    
    # --- Calculate Overall Security Score ---
    overall_score = (network_score + secret_score + vuln_score) / 3
    
    # --- Generate Security Insights Report ---
    if overall_score >= 80:
        security_level = "EXCELLENT"
        summary = "Security configurations are well-implemented with minimal risks."
    elif overall_score >= 60:
        security_level = "GOOD"
        summary = "Security configurations are adequate but have room for improvement."
    elif overall_score >= 40:
        security_level = "MODERATE"
        summary = "Security configurations have significant gaps that should be addressed."
    else:
        security_level = "POOR"
        summary = "Security configurations have critical issues requiring immediate attention."
    
    # --- Compile Recommendations ---
    recommendations = []
    
    if network_score < 70:
        recommendations.append("Implement comprehensive NetworkPolicy resources with proper ingress/egress rules")
        recommendations.append("Configure pod and namespace selectors for network segmentation")
    
    if secret_score < 70:
        recommendations.append("Enable encryption at rest for all secrets")
        recommendations.append("Implement RBAC controls for secret access")
        recommendations.append("Establish secret rotation policies")
        recommendations.append("Consider external secret management solutions")
    
    if critical_vulns > 0:
        recommendations.append("URGENT: Address all critical vulnerabilities immediately")
    if high_vulns > 0:
        recommendations.append("HIGH PRIORITY: Remediate high severity vulnerabilities within 7 days")
    
    # --- Format Final Report ---
    report = f"""SECURITY CONFIGURATION ANALYSIS REPORT
===============================================

OVERALL SECURITY LEVEL: {security_level}
OVERALL SCORE: {overall_score:.1f}/100

SUMMARY:
{summary}

DETAILED SCORES:
- Network Policy Security: {network_score}/100
- Secret Management Security: {secret_score}/100
- Vulnerability Assessment: {vuln_score}/100

IDENTIFIED ISSUES:

Network Policy Issues:
{chr(10).join('- ' + issue for issue in network_issues) if network_issues else '- No significant issues found'}

Secret Management Issues:
{chr(10).join('- ' + issue for issue in secret_issues) if secret_issues else '- No significant issues found'}

Vulnerability Issues:
{chr(10).join('- ' + issue for issue in vuln_issues) if vuln_issues else '- No vulnerabilities detected'}

RECOMMENDATIONS:
{chr(10).join('- ' + rec for rec in recommendations) if recommendations else '- Continue maintaining current security practices'}

VULNERABILITY SUMMARY:
- Critical: {critical_vulns}
- High: {high_vulns}
- Medium: {medium_vulns}
- Total: {total_vulns}
"""
    
    return report