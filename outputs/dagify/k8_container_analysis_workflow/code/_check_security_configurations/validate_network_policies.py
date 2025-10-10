# -- PRD --
# 1. BULLET: Implement a validation mechanism to check if network policies are properly
#   configured for the given container names and port configurations
#   Reason: To ensure that the network policies are correctly applied and do not expose
#           the containers to unnecessary risks
#   Impact: Improper network policy validation could lead to security vulnerabilities
#           or misconfigured containers
#   Complexity: MEDIUM
#   Method: Use a combination of rule-based validation and possibly machine learning
#           models to assess the network policies against the container
#           configurations
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle edge cases such as empty container names or port configurations
#   Reason: To prevent the validation function from failing or producing incorrect
#           results when faced with incomplete or missing data
#   Impact: Failure to handle edge cases could result in the function crashing or
#           returning incorrect validation results
#   Complexity: LOW
#   Method: Implement input validation to check for empty or null values and return
#           appropriate error messages or default values
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Integrate with existing security frameworks or tools to leverage their
#   network policy validation capabilities
#   Reason: To benefit from established security best practices and reduce the
#           development effort required for implementing a robust
#           validation mechanism
#   Impact: Successful integration could enhance the accuracy and reliability of the
#           network policy validation
#   Complexity: HIGH
#   Method: Research and identify suitable security frameworks or tools that provide
#           network policy validation APIs or interfaces, and integrate
#           them into the shim function
# -- END PRD --

import json
import re


def validate_network_policies(container_names: str, port_configs: str) -> bool:
    """
    Validates network policies for a list of container names and their corresponding port configurations

    Args:
        container_names: Input parameter of type str
port_configs: Input parameter of type str

    Returns:
        bool: Output of type bool
    """
    
    # Handle edge cases - empty or invalid inputs
    if not container_names or not container_names.strip():
        return False
    
    if not port_configs or not port_configs.strip():
        return False
    
    try:
        # Parse container names (assuming comma-separated string)
        container_list = [name.strip() for name in container_names.split(',') if name.strip()]
        
        # Parse port configurations (assuming JSON string format)
        try:
            port_config_dict = json.loads(port_configs)
        except json.JSONDecodeError:
            # If not JSON, try to parse as comma-separated port numbers
            port_list = [port.strip() for port in port_configs.split(',') if port.strip()]
            port_config_dict = {}
            for i, container in enumerate(container_list):
                if i < len(port_list):
                    port_config_dict[container] = port_list[i]
        
        # Validate container names format
        container_name_pattern = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$')
        for container in container_list:
            if not container_name_pattern.match(container):
                return False
        
        # Validate port configurations
        for container, port_info in port_config_dict.items():
            if isinstance(port_info, str):
                try:
                    port_num = int(port_info)
                except ValueError:
                    return False
            elif isinstance(port_info, int):
                port_num = port_info
            else:
                return False
            
            # Check if port is in valid range
            if port_num < 1 or port_num > 65535:
                return False
            
            # Check for common security risks
            # Privileged ports (1-1023) should be carefully validated
            if port_num < 1024:
                # Only allow common secure services on privileged ports
                allowed_privileged_ports = [22, 80, 443, 993, 995]
                if port_num not in allowed_privileged_ports:
                    return False
        
        # Basic network policy validation rules
        # Check that each container has at least one port configured
        for container in container_list:
            if container not in port_config_dict:
                return False
        
        # Additional security checks
        # Ensure no duplicate port assignments across containers
        used_ports = set()
        for port_info in port_config_dict.values():
            port_num = int(port_info) if isinstance(port_info, str) else port_info
            if port_num in used_ports:
                return False
            used_ports.add(port_num)
        
        # All validations passed
        return True
        
    except Exception as e:
        # Handle any unexpected errors during validation
        return False