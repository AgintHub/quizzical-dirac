import re
import json


def analyze_resource_utilization_trends(avg_cpu: str, avg_memory: str, peak_times: str) -> str:
    """
    This shim analyzes resource utilization trends to provide insights for optimization

    Args:
        avg_cpu: Input parameter of type str
avg_memory: Input parameter of type str
peak_times: Input parameter of type str

    Returns:
        str: Output of type str
    """
    
    # Parse CPU utilization
    try:
        cpu_value = float(re.findall(r'\d+\.?\d*', avg_cpu)[0])
    except (IndexError, ValueError):
        cpu_value = 0.0
    
    # Parse memory utilization
    try:
        memory_value = float(re.findall(r'\d+\.?\d*', avg_memory)[0])
    except (IndexError, ValueError):
        memory_value = 0.0
    
    # Analyze trends and generate insights
    insights = []
    
    # CPU analysis
    if cpu_value > 80:
        insights.append("High CPU utilization detected - consider scaling up or optimizing CPU-intensive processes")
    elif cpu_value > 60:
        insights.append("Moderate CPU utilization - monitor for potential bottlenecks")
    else:
        insights.append("CPU utilization is within acceptable range")
    
    # Memory analysis
    if memory_value > 85:
        insights.append("High memory utilization detected - consider increasing memory or optimizing memory usage")
    elif memory_value > 70:
        insights.append("Moderate memory utilization - monitor for memory leaks")
    else:
        insights.append("Memory utilization is within acceptable range")
    
    # Peak times analysis
    peak_analysis = f"Peak usage times identified: {peak_times}"
    if "morning" in peak_times.lower() or "9" in peak_times or "10" in peak_times:
        peak_analysis += " - Consider pre-scaling resources before morning hours"
    if "evening" in peak_times.lower() or "17" in peak_times or "18" in peak_times:
        peak_analysis += " - Consider implementing auto-scaling for evening traffic"
    
    insights.append(peak_analysis)
    
    # Generate recommendations
    recommendations = []
    if cpu_value > 70 or memory_value > 70:
        recommendations.append("Implement auto-scaling policies")
        recommendations.append("Review and optimize resource-intensive operations")
    
    if cpu_value < 30 and memory_value < 30:
        recommendations.append("Consider downsizing resources to optimize costs")
    
    # Compile final analysis
    analysis_result = {
        "summary": f"Average CPU: {cpu_value}%, Average Memory: {memory_value}%",
        "insights": insights,
        "recommendations": recommendations,
        "optimization_priority": "High" if (cpu_value > 80 or memory_value > 85) else "Medium" if (cpu_value > 60 or memory_value > 70) else "Low"
    }
    
    return json.dumps(analysis_result, indent=2)