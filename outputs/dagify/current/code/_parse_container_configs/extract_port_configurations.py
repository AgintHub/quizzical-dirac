# -- PRD --
# 1. BULLET: Parse container configuration manifests to identify port configurations.
#   Reason: To extract the specific port numbers that are exposed by the containers.
#   Impact: This will enable the system to understand which ports are used by the
#           containers, crucial for network configuration and security.
#   Complexity: MEDIUM
#   Method: Use a parsing library (e.g., YAML or JSON parser depending on the manifest
#           format) to read the container configuration manifests and
#           identify sections related to port configurations.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Convert identified port configurations into a list of integers.
#   Reason: To standardize the output format for further processing or analysis.
#   Impact: This will allow for consistent handling of port configuration data across
#           the system.
#   Complexity: LOW
#   Method: Implement a simple data type conversion, ensuring that the port numbers are
#           correctly represented as integers.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle potential errors or inconsistencies in the container configuration
#   manifests.
#   Reason: To ensure the robustness and reliability of the shim function.
#   Impact: This will prevent errors in the port configuration extraction process from
#           propagating to other parts of the system.
#   Complexity: MEDIUM
#   Method: Implement error handling mechanisms, such as try-except blocks, to catch
#           and manage parsing errors or data inconsistencies.
# -- END PRD --

from typing import List

import json
import yaml
import re


def extract_port_configurations(configs: str) -> List[int]:
    """
    Extracts port configurations from container manifests and returns them as a list of integers.

    Args:
        configs: Input parameter of type str

    Returns:
        List[int]: Output of type List[int]
    """
    
    ports = []
    
    try:
        # Try to parse as JSON first
        try:
            data = json.loads(configs)
        except json.JSONDecodeError:
            # If JSON parsing fails, try YAML
            try:
                data = yaml.safe_load(configs)
            except yaml.YAMLError:
                # If both fail, try to extract port numbers using regex
                port_pattern = r'(?:port|expose|ports?)\s*[:\-=]?\s*(\d+)'
                matches = re.findall(port_pattern, configs, re.IGNORECASE)
                for match in matches:
                    try:
                        port = int(match)
                        if 1 <= port <= 65535:  # Valid port range
                            ports.append(port)
                    except ValueError:
                        continue
                return sorted(list(set(ports)))
        
        # Extract ports from parsed data structure
        def extract_ports_recursive(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_lower = str(key).lower()
                    if any(port_key in key_lower for port_key in ['port', 'expose', 'containerport', 'hostport']):
                        if isinstance(value, (int, str)):
                            try:
                                port = int(value)
                                if 1 <= port <= 65535:
                                    ports.append(port)
                            except (ValueError, TypeError):
                                pass
                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, (int, str)):
                                    try:
                                        port = int(item)
                                        if 1 <= port <= 65535:
                                            ports.append(port)
                                    except (ValueError, TypeError):
                                        pass
                                elif isinstance(item, dict) and 'containerPort' in item:
                                    try:
                                        port = int(item['containerPort'])
                                        if 1 <= port <= 65535:
                                            ports.append(port)
                                    except (ValueError, TypeError, KeyError):
                                        pass
                    else:
                        extract_ports_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_ports_recursive(item)
        
        extract_ports_recursive(data)
        
    except Exception as e:
        # Fallback: try regex extraction on the original string
        port_pattern = r'(?:port|expose|ports?)\s*[:\-=]?\s*(\d+)'
        matches = re.findall(port_pattern, configs, re.IGNORECASE)
        for match in matches:
            try:
                port = int(match)
                if 1 <= port <= 65535:
                    ports.append(port)
            except ValueError:
                continue
    
    # Remove duplicates and sort
    return sorted(list(set(ports)))