from ._check_security_configurations.validate_network_policies import validate_network_policies
from ._check_security_configurations.validate_secret_management import validate_secret_management
from ._check_security_configurations.scan_image_vulnerabilities import scan_image_vulnerabilities
from ._check_security_configurations.check_resource_security import check_resource_security
from ._check_security_configurations.check_port_security import check_port_security
from ._check_security_configurations.consolidate_vulnerabilities import consolidate_vulnerabilities

from pydantic import BaseModel, Field
from typing import List


class ParseContainerConfigsOutput(BaseModel):
    """Pydantic model for parse_container_configs node outputs."""
    container_names: List[str] = Field(..., description="List of container names")
    image_names: List[str] = Field(..., description="List of container image names")
    port_configurations: List[int] = Field(..., description="List of exposed port numbers")
    resource_limits: List[float] = Field(..., description="List of resource limits (e.g., CPU, memory)")


class CheckSecurityConfigurationsOutput(BaseModel):
    """Pydantic model for check_security_configurations node outputs."""
    network_policy_status: bool = Field(..., description="Whether network policies are properly configured")
    secret_management_status: bool = Field(..., description="Whether secret management is properly configured")
    vulnerabilities_found: List[str] = Field(..., description="List of identified vulnerabilities")


def check_security_configurations(parse_container_configs_input: ParseContainerConfigsOutput, **kwargs) -> CheckSecurityConfigurationsOutput:
    """Assess container security configurations and identify potential vulnerabilities

    Args:
        parse_container_configs_input: Input from the 'parse_container_configs' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CheckSecurityConfigurationsOutput: Object containing outputs for this node.
    """
    # Check network policy configurations
    network_policy_valid: bool = validate_network_policies(
        container_names=parse_container_configs_input.container_names,
        port_configs=parse_container_configs_input.port_configurations
    )
    
    # Check secret management configurations
    secret_mgmt_valid: bool = validate_secret_management(
        container_names=parse_container_configs_input.container_names,
        image_names=parse_container_configs_input.image_names
    )
    
    # Scan for vulnerabilities in container images
    image_vulnerabilities: List[str] = scan_image_vulnerabilities(
        image_names=parse_container_configs_input.image_names
    )
    
    # Check for resource-based security issues
    resource_vulnerabilities: List[str] = check_resource_security(
        resource_limits=parse_container_configs_input.resource_limits,
        container_names=parse_container_configs_input.container_names
    )
    
    # Check for port-based security issues
    port_vulnerabilities: List[str] = check_port_security(
        port_configurations=parse_container_configs_input.port_configurations
    )
    
    # Combine all vulnerability findings
    all_vulnerabilities: List[str] = consolidate_vulnerabilities(
        image_vulns=image_vulnerabilities,
        resource_vulns=resource_vulnerabilities,
        port_vulns=port_vulnerabilities
    )
    
    return CheckSecurityConfigurationsOutput(
        network_policy_status=network_policy_valid,
        secret_management_status=secret_mgmt_valid,
        vulnerabilities_found=all_vulnerabilities
    )