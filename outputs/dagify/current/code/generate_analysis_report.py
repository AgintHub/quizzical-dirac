from ._generate_analysis_report.analyze_resource_utilization_trends import analyze_resource_utilization_trends
from ._generate_analysis_report.evaluate_security_configurations import evaluate_security_configurations
from ._generate_analysis_report.generate_executive_summary import generate_executive_summary
from ._generate_analysis_report.compile_optimization_recommendations import compile_optimization_recommendations
from ._generate_analysis_report.compile_security_recommendations import compile_security_recommendations
from ._generate_analysis_report.calculate_weighted_report_score import calculate_weighted_report_score

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Extract analysis findings from parent nodes 'analyze_resource_utilization'
#   and 'check_security_configurations'
#   Reason: These nodes provide crucial data for generating the analysis report
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use the output from 'analyze_resource_utilization' and
#           'check_security_configurations' to gather necessary data
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Analyze resource utilization data to identify optimization opportunities
#   Reason: To provide actionable recommendations for optimizing container
#           configurations
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Analyze 'avg_cpu_utilization', 'avg_memory_utilization', and
#           'peak_utilization_times' from 'analyze_resource_utilization' to
#           identify trends and potential bottlenecks
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Evaluate security configurations to identify security hardening opportunities
#   Reason: To provide recommendations for improving container security
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Assess 'network_policy_status', 'secret_management_status', and
#           'vulnerabilities_found' from 'check_security_configurations' to
#           identify potential security risks
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Generate executive summary based on analysis findings
#   Reason: To provide a concise overview of key findings and recommendations
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Summarize key insights from resource utilization analysis and security
#           configuration evaluation
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Compile optimization recommendations
#   Reason: To provide actionable advice for optimizing container configurations
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Based on the analysis of resource utilization, generate recommendations for
#           optimizing container configurations
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Compile security recommendations
#   Reason: To provide actionable advice for improving container security
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Based on the evaluation of security configurations, generate
#           recommendations for security hardening
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Calculate report score
#   Reason: To provide an overall health and security score for container
#           configurations
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a weighted scoring system based on the findings from
#           'analyze_resource_utilization' and
#           'check_security_configurations' to calculate the report score
# -- END PRD --



class AnalyzeResourceUtilizationOutput(BaseModel):
    """Pydantic model for analyze_resource_utilization node outputs."""
    avg_cpu_utilization: float = Field(..., description="Average CPU utilization across containers")
    avg_memory_utilization: float = Field(..., description="Average memory utilization across containers")
    peak_utilization_times: str = Field(..., description="List of timestamps for peak resource utilization")


class CheckSecurityConfigurationsOutput(BaseModel):
    """Pydantic model for check_security_configurations node outputs."""
    network_policy_status: bool = Field(..., description="Whether network policies are properly configured")
    secret_management_status: bool = Field(..., description="Whether secret management is properly configured")
    vulnerabilities_found: List[str] = Field(..., description="List of identified vulnerabilities")


class GenerateAnalysisReportOutput(BaseModel):
    """Pydantic model for generate_analysis_report node outputs."""
    executive_summary: str = Field(..., description="Brief summary of key findings and recommendations")
    optimization_recommendations: str = Field(..., description="List of recommendations for optimizing container configurations")
    security_recommendations: str = Field(..., description="List of recommendations for improving container security")
    report_score: float = Field(..., description="Score indicating overall health and security of container configurations")


def generate_analysis_report(analyze_resource_utilization_input: AnalyzeResourceUtilizationOutput, check_security_configurations_input: CheckSecurityConfigurationsOutput, **kwargs) -> GenerateAnalysisReportOutput:
    """Generate a detailed analysis report based on collected data and analysis

    Args:
        analyze_resource_utilization_input: Input from the 'analyze_resource_utilization' node.
        check_security_configurations_input: Input from the 'check_security_configurations' node.
        **kwargs: Additional keyword arguments.

    Returns:
        GenerateAnalysisReportOutput: Object containing outputs for this node.
    """
    # Analyze resource utilization data to identify optimization opportunities
    optimization_insights: str = analyze_resource_utilization_trends(
        avg_cpu=analyze_resource_utilization_input.avg_cpu_utilization,
        avg_memory=analyze_resource_utilization_input.avg_memory_utilization,
        peak_times=analyze_resource_utilization_input.peak_utilization_times
    )
    
    # Evaluate security configurations to identify security hardening opportunities
    security_insights: str = evaluate_security_configurations(
        network_policy=check_security_configurations_input.network_policy_status,
        secret_management=check_security_configurations_input.secret_management_status,
        vulnerabilities=check_security_configurations_input.vulnerabilities_found
    )
    
    # Generate executive summary based on analysis findings
    executive_summary: str = generate_executive_summary(
        resource_insights=optimization_insights,
        security_insights=security_insights
    )
    
    # Compile optimization recommendations
    optimization_recommendations: str = compile_optimization_recommendations(
        resource_data=analyze_resource_utilization_input
    )
    
    # Compile security recommendations
    security_recommendations: str = compile_security_recommendations(
        security_data=check_security_configurations_input
    )
    
    # Calculate report score using weighted scoring system
    report_score: float = calculate_weighted_report_score(
        resource_data=analyze_resource_utilization_input,
        security_data=check_security_configurations_input
    )
    
    return GenerateAnalysisReportOutput(
        executive_summary=executive_summary,
        optimization_recommendations=optimization_recommendations,
        security_recommendations=security_recommendations,
        report_score=report_score
    )