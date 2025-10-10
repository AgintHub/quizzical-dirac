from ._collect_container_data.initialize_k8s_client import initialize_k8s_client
from ._collect_container_data.get_container_configs import get_container_configs
from ._collect_container_data.serialize_configs_to_yaml import serialize_configs_to_yaml
from ._collect_container_data.get_cpu_utilization import get_cpu_utilization
from ._collect_container_data.get_memory_utilization import get_memory_utilization
from ._collect_container_data.combine_resource_metrics import combine_resource_metrics
from ._collect_container_data.get_active_pods import get_active_pods
from ._collect_container_data.fetch_pod_logs import fetch_pod_logs

from pydantic import BaseModel, Field
from typing import List


class CollectContainerDataOutput(BaseModel):
    """Pydantic model for collect_container_data node outputs."""
    container_configs: List[str] = Field(..., description="List of container configuration manifests")
    resource_utilization: List[float] = Field(..., description="List of resource utilization metrics (e.g., CPU, memory)")
    container_logs: List[str] = Field(..., description="List of container logs")


def collect_container_data(general_input: str, **kwargs) -> CollectContainerDataOutput:
    """Gather relevant container data from Kubernetes cluster

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        CollectContainerDataOutput: Object containing outputs for this node.
    """
    # Initialize Kubernetes client connection
    k8s_client = initialize_k8s_client()
    
    # Collect container configuration manifests
    raw_configs: List[dict] = get_container_configs(client=k8s_client)
    container_configs: List[str] = serialize_configs_to_yaml(configs=raw_configs)
    
    # Collect resource utilization metrics
    cpu_metrics: List[float] = get_cpu_utilization(client=k8s_client)
    memory_metrics: List[float] = get_memory_utilization(client=k8s_client)
    resource_utilization: List[float] = combine_resource_metrics(cpu=cpu_metrics, memory=memory_metrics)
    
    # Collect container logs
    container_pods: List[str] = get_active_pods(client=k8s_client)
    container_logs: List[str] = fetch_pod_logs(client=k8s_client, pods=container_pods)
    
    return CollectContainerDataOutput(
        container_configs=container_configs,
        resource_utilization=resource_utilization,
        container_logs=container_logs,
    )