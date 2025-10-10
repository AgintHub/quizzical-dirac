# -- PRD --
# 1. BULLET: Analyze the input resource utilization data to identify optimization
#   opportunities.
#   Reason: To provide relevant optimization recommendations, the function needs to
#           understand the current resource utilization trends.
#   Impact: The quality of the optimization recommendations depends on the accuracy of
#           the analysis.
#   Complexity: MEDIUM
#   Method: Implement a data analysis algorithm to process the resource utilization
#           data and identify patterns or trends that suggest optimization
#           opportunities.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Generate optimization recommendations based on the analysis.
#   Reason: The primary purpose of this shim is to provide actionable recommendations
#           for optimizing resource utilization.
#   Impact: The output of this function will be used to inform decisions about resource
#           allocation and optimization.
#   Complexity: HIGH
#   Method: Develop a rules-based system or utilize machine learning models to generate
#           optimization recommendations based on the insights gained from
#           the analysis.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the recommendations into a user-friendly output string.
#   Reason: The output needs to be easily understandable by the users.
#   Impact: The usability of the output affects the overall user experience.
#   Complexity: LOW
#   Method: Use natural language processing techniques to format the recommendations
#           into a clear and concise string.
# -- END PRD --

import json
import re
from statistics import mean, stdev


def compile_optimization_recommendations(resource_data: str) -> str:
    """
    Compiles optimization recommendations based on the provided resource utilization data.

    Args:
        resource_data: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse the resource data
    try:
        if resource_data.strip().startswith('{') or resource_data.strip().startswith('['):
            # JSON format
            data = json.loads(resource_data)
        else:
            # Assume CSV-like format, parse manually
            lines = resource_data.strip().split('\n')
            data = []
            for line in lines[1:]:  # Skip header
                values = line.split(',')
                if len(values) >= 3:
                    try:
                        data.append({
                            'resource': values[0].strip(),
                            'utilization': float(values[1].strip()),
                            'timestamp': values[2].strip() if len(values) > 2 else ''
                        })
                    except ValueError:
                        continue
    except (json.JSONDecodeError, ValueError):
        # Fallback: extract numbers from text
        numbers = re.findall(r'\d+\.?\d*', resource_data)
        data = [{'resource': f'resource_{i}', 'utilization': float(num)} for i, num in enumerate(numbers) if float(num) <= 100]
    
    if not data:
        return "Unable to parse resource data. Please provide valid resource utilization information."
    
    # Analyze the data to identify optimization opportunities
    recommendations = []
    
    # Extract utilization values
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            utilizations = [item.get('utilization', 0) for item in data if 'utilization' in item]
        else:
            utilizations = [float(x) for x in data if isinstance(x, (int, float)) or str(x).replace('.', '').isdigit()]
    else:
        utilizations = []
    
    if not utilizations:
        return "No valid utilization data found for analysis."
    
    # Calculate statistics
    avg_utilization = mean(utilizations)
    max_utilization = max(utilizations)
    min_utilization = min(utilizations)
    
    # Generate recommendations based on analysis
    
    # High utilization analysis
    if max_utilization > 90:
        recommendations.append("Critical: Peak resource utilization exceeds 90%. Consider immediate capacity scaling or load balancing.")
    elif max_utilization > 80:
        recommendations.append("Warning: Peak resource utilization is above 80%. Monitor closely and prepare for scaling.")
    
    # Average utilization analysis
    if avg_utilization > 75:
        recommendations.append("High average utilization detected. Consider adding resources or optimizing workload distribution.")
    elif avg_utilization < 30:
        recommendations.append("Low average utilization detected. Consider resource consolidation or rightsizing to reduce costs.")
    
    # Variability analysis
    if len(utilizations) > 1:
        try:
            std_dev = stdev(utilizations)
            if std_dev > 25:
                recommendations.append("High variability in resource usage detected. Consider implementing auto-scaling or workload scheduling.")
        except:
            pass
    
    # Specific threshold recommendations
    high_util_count = sum(1 for u in utilizations if u > 80)
    low_util_count = sum(1 for u in utilizations if u < 20)
    
    if high_util_count > len(utilizations) * 0.3:
        recommendations.append("Frequent high utilization spikes detected. Implement proactive monitoring and alerting.")
    
    if low_util_count > len(utilizations) * 0.4:
        recommendations.append("Significant periods of low utilization found. Evaluate resource allocation efficiency.")
    
    # Additional optimization strategies
    if avg_utilization > 50 and max_utilization > 85:
        recommendations.append("Consider implementing caching mechanisms or optimizing resource-intensive operations.")
    
    # Format recommendations into user-friendly output
    if not recommendations:
        recommendations.append("Resource utilization appears optimal. Continue monitoring for any changes in usage patterns.")
    
    # Create formatted output string
    output_lines = [
        "=== Resource Optimization Recommendations ===",
        f"Analysis Summary: Avg: {avg_utilization:.1f}%, Max: {max_utilization:.1f}%, Min: {min_utilization:.1f}%",
        "",
        "Recommendations:"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        output_lines.append(f"{i}. {rec}")
    
    output_lines.extend([
        "",
        "Note: Implement changes gradually and monitor impact on system performance."
    ])
    
    return "\n".join(output_lines)