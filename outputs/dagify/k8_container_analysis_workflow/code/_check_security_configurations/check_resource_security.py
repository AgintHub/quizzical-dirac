# -- PRD --
# 1. BULLET: Parse input strings into usable data structures for analysis.
#   Reason: The input parameters (resource_limits and container_names) are strings that
#           need to be converted into appropriate data structures (e.g.,
#           lists or dictionaries) to facilitate checking for resource-
#           based security issues.
#   Impact: Successful parsing enables accurate identification of security
#           vulnerabilities.
#   Complexity: MEDIUM
#   Method: Use JSON parsing or string manipulation techniques to convert input strings
#           into required data structures.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Implement logic to check for resource-based security vulnerabilities.
#   Reason: The core functionality of this shim is to identify potential security
#           issues based on the provided resource limits and container
#           names.
#   Impact: Effective vulnerability checking enhances the overall security assessment
#           of container configurations.
#   Complexity: HIGH
#   Method: Develop algorithms that analyze resource limits against known security
#           thresholds or best practices, and identify container names that
#           may be associated with risky configurations.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Format the output as a list of strings representing identified
#   vulnerabilities.
#   Reason: The output needs to be in a format that can be easily consumed by
#           subsequent processes or nodes in the workflow.
#   Impact: Proper output formatting ensures seamless integration with other components
#           of the system.
#   Complexity: LOW
#   Method: Use string formatting or serialization techniques to convert the identified
#           vulnerabilities into a list of strings.
# -- END PRD --

from typing import List

import json
import re


def check_resource_security(resource_limits: str, container_names: str) -> List[str]:
    """
    Checks for resource-based security issues given container names and resource limits.

    Args:
        resource_limits: Input parameter of type str
container_names: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    vulnerabilities = []
    
    # Parse resource_limits string into usable data structure
    try:
        if resource_limits.strip():
            # Try to parse as JSON first
            try:
                limits_data = json.loads(resource_limits)
            except json.JSONDecodeError:
                # If not JSON, try to parse as key=value pairs
                limits_data = {}
                pairs = resource_limits.split(',')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        limits_data[key.strip()] = value.strip()
        else:
            limits_data = {}
    except Exception:
        limits_data = {}
    
    # Parse container_names string into list
    try:
        if container_names.strip():
            # Try to parse as JSON first
            try:
                names_list = json.loads(container_names)
                if not isinstance(names_list, list):
                    names_list = [str(names_list)]
            except json.JSONDecodeError:
                # If not JSON, split by comma
                names_list = [name.strip() for name in container_names.split(',') if name.strip()]
        else:
            names_list = []
    except Exception:
        names_list = []
    
    # Check for resource-based security vulnerabilities
    
    # Check memory limits
    if isinstance(limits_data, dict):
        memory_limit = limits_data.get('memory', limits_data.get('Memory', ''))
        if memory_limit:
            # Extract numeric value from memory limit
            memory_match = re.search(r'(\d+)', str(memory_limit))
            if memory_match:
                memory_value = int(memory_match.group(1))
                # Check if memory limit is too high (potential DoS) or too low (potential instability)
                if memory_value > 8192:  # > 8GB
                    vulnerabilities.append(f"High memory limit detected: {memory_limit} - potential resource exhaustion")
                elif memory_value < 64:  # < 64MB
                    vulnerabilities.append(f"Very low memory limit detected: {memory_limit} - potential instability")
        
        # Check CPU limits
        cpu_limit = limits_data.get('cpu', limits_data.get('CPU', limits_data.get('cpus', '')))
        if cpu_limit:
            cpu_match = re.search(r'(\d+(?:\.\d+)?)', str(cpu_limit))
            if cpu_match:
                cpu_value = float(cpu_match.group(1))
                if cpu_value > 4.0:  # > 4 CPUs
                    vulnerabilities.append(f"High CPU limit detected: {cpu_limit} - potential resource monopolization")
                elif cpu_value < 0.1:  # < 0.1 CPU
                    vulnerabilities.append(f"Very low CPU limit detected: {cpu_limit} - potential performance issues")
        
        # Check for missing resource limits
        if not memory_limit and not cpu_limit:
            vulnerabilities.append("No resource limits specified - containers can consume unlimited resources")
    
    # Check container names for security issues
    for name in names_list:
        if name:
            # Check for privileged or risky container names
            risky_patterns = ['root', 'admin', 'privileged', 'system', 'kube-system', 'docker']
            for pattern in risky_patterns:
                if pattern.lower() in name.lower():
                    vulnerabilities.append(f"Potentially risky container name detected: {name} - contains '{pattern}'")
            
            # Check for containers running as root or with elevated privileges
            if re.search(r'(root|uid.*0|gid.*0)', name.lower()):
                vulnerabilities.append(f"Container name suggests root privileges: {name} - security risk")
            
            # Check for development/debug containers in production-like names
            debug_patterns = ['debug', 'test', 'dev', 'tmp', 'temp']
            prod_patterns = ['prod', 'production', 'live']
            name_lower = name.lower()
            has_debug = any(pattern in name_lower for pattern in debug_patterns)
            has_prod = any(pattern in name_lower for pattern in prod_patterns)
            if has_debug and has_prod:
                vulnerabilities.append(f"Container name suggests debug/test in production: {name} - potential security exposure")
    
    return vulnerabilities