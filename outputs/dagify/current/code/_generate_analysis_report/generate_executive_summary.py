# -- PRD --
# 1. BULLET: The shim will process the resource insights and security insights to identify
#   key findings and recommendations.
#   Reason: This is necessary to provide a concise summary that captures the essence of
#           the analysis.
#   Impact: The executive summary will be used to inform stakeholders about the overall
#           health and security of container configurations.
#   Complexity: MEDIUM
#   Method: Natural Language Processing (NLP) techniques can be employed to analyze the
#           insights and generate a coherent summary.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The shim will need to integrate with the analysis report generation pipeline
#   to receive the necessary insights.
#   Reason: This integration is required to ensure that the shim has access to the
#           relevant data for generating the executive summary.
#   Impact: The integration will enable the shim to produce a summary that is
#           consistent with the overall analysis report.
#   Complexity: MEDIUM
#   Method: API-based integration can be used to connect the shim with the analysis
#           report generation pipeline.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The shim should be designed to be flexible and adaptable to different types
#   of insights and analysis reports.
#   Reason: This flexibility is necessary to ensure that the shim can be reused in
#           different contexts and with varying analysis report structures.
#   Impact: The shim's flexibility will enhance its reusability and reduce maintenance
#           efforts.
#   Complexity: HIGH
#   Method: Modular design principles can be applied to develop a flexible and
#           adaptable shim.
# -- END PRD --


def generate_executive_summary(resource_insights: str, security_insights: str) -> str:
    """
    Generates a concise executive summary based on resource utilization and security insights.

    Args:
        resource_insights: Input parameter of type str
security_insights: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse and analyze resource insights
    resource_findings = []
    if resource_insights:
        # Extract key resource metrics and issues
        lines = resource_insights.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and ('high' in line.lower() or 'critical' in line.lower() or 'warning' in line.lower()):
                resource_findings.append(line)
    
    # Parse and analyze security insights
    security_findings = []
    if security_insights:
        # Extract key security issues and vulnerabilities
        lines = security_insights.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and ('vulnerability' in line.lower() or 'security' in line.lower() or 'risk' in line.lower() or 'threat' in line.lower()):
                security_findings.append(line)
    
    # Generate executive summary
    summary_parts = []
    
    # Add header
    summary_parts.append("EXECUTIVE SUMMARY - Container Configuration Analysis")
    summary_parts.append("=" * 60)
    
    # Resource insights summary
    if resource_findings:
        summary_parts.append("\nRESOURCE UTILIZATION FINDINGS:")
        summary_parts.append(f"- {len(resource_findings)} critical resource issues identified")
        for finding in resource_findings[:3]:  # Limit to top 3 findings
            summary_parts.append(f"- {finding}")
        if len(resource_findings) > 3:
            summary_parts.append(f"- ... and {len(resource_findings) - 3} additional issues")
    else:
        summary_parts.append("\nRESOURCE UTILIZATION: No critical issues identified")
    
    # Security insights summary
    if security_findings:
        summary_parts.append("\nSECURITY FINDINGS:")
        summary_parts.append(f"- {len(security_findings)} security concerns identified")
        for finding in security_findings[:3]:  # Limit to top 3 findings
            summary_parts.append(f"- {finding}")
        if len(security_findings) > 3:
            summary_parts.append(f"- ... and {len(security_findings) - 3} additional concerns")
    else:
        summary_parts.append("\nSECURITY: No critical security issues identified")
    
    # Overall assessment
    total_issues = len(resource_findings) + len(security_findings)
    summary_parts.append("\nOVERALL ASSESSMENT:")
    if total_issues == 0:
        summary_parts.append("- Container configurations appear to be healthy with no critical issues")
        summary_parts.append("- Recommended action: Continue monitoring")
    elif total_issues <= 3:
        summary_parts.append("- Minor issues identified that should be addressed")
        summary_parts.append("- Recommended action: Schedule maintenance window for remediation")
    else:
        summary_parts.append("- Multiple critical issues require immediate attention")
        summary_parts.append("- Recommended action: Prioritize remediation efforts based on security and resource impact")
    
    # Recommendations
    summary_parts.append("\nRECOMMENDATIONS:")
    if security_findings:
        summary_parts.append("- Address security vulnerabilities as highest priority")
    if resource_findings:
        summary_parts.append("- Optimize resource allocation to improve efficiency")
    summary_parts.append("- Implement continuous monitoring for early detection")
    summary_parts.append("- Schedule regular configuration reviews")
    
    return "\n".join(summary_parts)