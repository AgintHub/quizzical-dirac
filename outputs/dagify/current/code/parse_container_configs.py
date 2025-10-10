from ._parse_container_configs.extract_container_names import extract_container_names
from ._parse_container_configs.extract_image_names import extract_image_names
from ._parse_container_configs.extract_port_configurations import extract_port_configurations
from ._parse_container_configs.extract_resource_limits import extract_resource_limits

from pydantic import BaseModel, Field
from typing import List


class CollectContainerDataOutput(BaseModel):
    """Pydantic model for collect_container_data node outputs."""
    container_configs: List[str] = Field(..., description="List of container configuration manifests")
    resource_utilization: List[float] = Field(..., description="List of resource utilization metrics (e.g., CPU, memory)")
    container_logs: List[str] = Field(..., description="List of container logs")


class ParseContainerConfigsOutput(BaseModel):
    """Pydantic model for parse_container_configs node outputs."""
    container_names: List[str] = Field(..., description="List of container names")
    image_names: List[str] = Field(..., description="List of container image names")
    port_configurations: List[int] = Field(..., description="List of exposed port numbers")
    resource_limits: List[float] = Field(..., description="List of resource limits (e.g., CPU, memory)")


def parse_container_configs(collect_container_data_input: CollectContainerDataOutput, **kwargs) -> ParseContainerConfigsOutput:
    """Extract relevant configuration settings from container manifests

    Args:
        collect_container_data_input: Input from the 'collect_container_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ParseContainerConfigsOutput: Object containing outputs for this node.
    """
    # Parse container configuration manifests to extract container names
    container_names: List[str] = extract_container_names(configs=collect_container_data_input.container_configs)
    
    # Extract image names from container configurations
    image_names: List[str] = extract_image_names(configs=collect_container_data_input.container_configs)
    
    # Parse port configurations from container manifests
    port_configurations: List[int] = extract_port_configurations(configs=collect_container_data_input.container_configs)
    
    # Extract resource limits from container configurations
    resource_limits: List[float] = extract_resource_limits(configs=collect_container_data_input.container_configs)
    
    return ParseContainerConfigsOutput(
        container_names=container_names,
        image_names=image_names,
        port_configurations=port_configurations,
        resource_limits=resource_limits,
    )