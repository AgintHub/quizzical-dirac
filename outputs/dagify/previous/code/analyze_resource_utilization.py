from ._analyze_resource_utilization.parse_resource_metrics import parse_resource_metrics
from ._analyze_resource_utilization.extract_cpu_metrics import extract_cpu_metrics
from ._analyze_resource_utilization.calculate_average_utilization import calculate_average_utilization
from ._analyze_resource_utilization.extract_memory_metrics import extract_memory_metrics
from ._analyze_resource_utilization.identify_peak_utilization_times import identify_peak_utilization_times
from ._analyze_resource_utilization.format_timestamps_to_string import format_timestamps_to_string

from pydantic import BaseModel, Field
from typing import List


class CollectContainerDataOutput(BaseModel):
    """Pydantic model for collect_container_data node outputs."""
    container_configs: List[str] = Field(..., description="List of container configuration manifests")
    resource_utilization: List[float] = Field(..., description="List of resource utilization metrics (e.g., CPU, memory)")
    container_logs: List[str] = Field(..., description="List of container logs")


class AnalyzeResourceUtilizationOutput(BaseModel):
    """Pydantic model for analyze_resource_utilization node outputs."""
    avg_cpu_utilization: float = Field(..., description="Average CPU utilization across containers")
    avg_memory_utilization: float = Field(..., description="Average memory utilization across containers")
    peak_utilization_times: str = Field(..., description="List of timestamps for peak resource utilization")


def analyze_resource_utilization(collect_container_data_input: CollectContainerDataOutput, **kwargs) -> AnalyzeResourceUtilizationOutput:
    """Analyze container resource utilization patterns

    Args:
        collect_container_data_input: Input from the 'collect_container_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AnalyzeResourceUtilizationOutput: Object containing outputs for this node.
    """
    # Parse and extract resource metrics from utilization data
    parsed_metrics: List[dict] = parse_resource_metrics(utilization_data=collect_container_data_input.resource_utilization)
    
    # Calculate CPU utilization statistics
    cpu_metrics: List[float] = extract_cpu_metrics(parsed_metrics=parsed_metrics)
    avg_cpu: float = calculate_average_utilization(metrics=cpu_metrics)
    
    # Calculate memory utilization statistics
    memory_metrics: List[float] = extract_memory_metrics(parsed_metrics=parsed_metrics)
    avg_memory: float = calculate_average_utilization(metrics=memory_metrics)
    
    # Identify peak utilization periods from logs and metrics
    peak_timestamps: List[str] = identify_peak_utilization_times(
        cpu_metrics=cpu_metrics,
        memory_metrics=memory_metrics,
        container_logs=collect_container_data_input.container_logs
    )
    
    # Format peak times as comma-separated string
    formatted_peak_times: str = format_timestamps_to_string(timestamps=peak_timestamps)
    
    return AnalyzeResourceUtilizationOutput(
        avg_cpu_utilization=avg_cpu,
        avg_memory_utilization=avg_memory,
        peak_utilization_times=formatted_peak_times
    )