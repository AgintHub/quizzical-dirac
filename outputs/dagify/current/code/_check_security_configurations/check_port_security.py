# -- PRD --
# 1. BULLET: Analyze the input port configurations to identify potentially vulnerable
#   ports
#   Reason: To detect ports that are commonly associated with security risks or are not
#           properly secured
#   Impact: Enhances the security posture by identifying potential entry points for
#           attackers
#   Complexity: MEDIUM
#   Method: Implement a port scanning or analysis algorithm that checks against known
#           vulnerable ports or configurations
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the input port configurations against a set of predefined security
#   rules or guidelines
#   Reason: To ensure compliance with organizational security policies and best
#           practices
#   Impact: Ensures that container configurations adhere to security standards,
#           reducing the risk of breaches
#   Complexity: LOW
#   Method: Develop a rules engine or validation mechanism that checks port
#           configurations against a configurable set of security rules
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Return a list of identified vulnerabilities or security issues related to the
#   port configurations
#   Reason: To provide actionable insights for securing the container configurations
#   Impact: Enables administrators to take corrective actions to mitigate identified
#           security risks
#   Complexity: LOW
#   Method: Format the results of the analysis into a list of vulnerabilities,
#           including details such as the port number, vulnerability type,
#           and recommended mitigation steps
# -- END PRD --

from typing import List

import re
import json


def check_port_security(port_configurations: str) -> List[str]:
    """
    Checks for port-based security issues in container configurations.

    Args:
        port_configurations: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    vulnerabilities = []
    
    # Define commonly vulnerable ports and their associated risks
    vulnerable_ports = {
        21: "FTP - Unencrypted file transfer protocol",
        22: "SSH - Ensure proper key management and disable password auth",
        23: "Telnet - Unencrypted remote access protocol",
        25: "SMTP - Mail server, potential for relay attacks",
        53: "DNS - Potential for DNS amplification attacks",
        80: "HTTP - Unencrypted web traffic",
        110: "POP3 - Unencrypted email retrieval",
        135: "RPC - Windows RPC endpoint mapper",
        139: "NetBIOS - Windows file sharing",
        143: "IMAP - Unencrypted email access",
        161: "SNMP - Simple Network Management Protocol",
        389: "LDAP - Unencrypted directory access",
        445: "SMB - Windows file sharing",
        993: "IMAPS - Check certificate configuration",
        995: "POP3S - Check certificate configuration",
        1433: "MSSQL - Database server exposure",
        1521: "Oracle - Database server exposure",
        3306: "MySQL - Database server exposure",
        3389: "RDP - Remote Desktop Protocol",
        5432: "PostgreSQL - Database server exposure",
        5984: "CouchDB - NoSQL database exposure",
        6379: "Redis - In-memory database exposure",
        8080: "HTTP-Alt - Alternative HTTP port",
        9200: "Elasticsearch - Search engine exposure",
        27017: "MongoDB - NoSQL database exposure"
    }
    
    # Security rules for port configurations
    security_rules = {
        "no_privileged_ports": "Avoid binding to privileged ports (< 1024) unless necessary",
        "no_wildcard_binding": "Avoid binding to 0.0.0.0 (all interfaces)",
        "use_specific_interfaces": "Bind to specific network interfaces when possible",
        "limit_port_range": "Minimize the number of exposed ports"
    }
    
    try:
        # Parse port configurations - handle various formats
        ports_to_check = []
        
        # Try to parse as JSON first
        try:
            config_data = json.loads(port_configurations)
            if isinstance(config_data, list):
                ports_to_check = config_data
            elif isinstance(config_data, dict):
                # Extract ports from various possible keys
                for key in ['ports', 'expose', 'ExposedPorts']:
                    if key in config_data:
                        ports_to_check.extend(config_data[key])
        except json.JSONDecodeError:
            # Parse as string format (e.g., "80:8080, 443:4433, 22")
            port_patterns = re.findall(r'\b(\d+)(?::(\d+))?\b', port_configurations)
            for match in port_patterns:
                # Use external port if specified, otherwise internal port
                port = int(match[1]) if match[1] else int(match[0])
                ports_to_check.append(port)
    
    except Exception as e:
        vulnerabilities.append(f"Configuration parsing error: {str(e)}")
        return vulnerabilities
    
    # Analyze ports against vulnerable ports database
    for port in ports_to_check:
        try:
            port_num = int(str(port).split('/')[0].split(':')[0])  # Handle formats like "80/tcp" or "80:8080"
            
            if port_num in vulnerable_ports:
                vulnerability_desc = vulnerable_ports[port_num]
                vulnerabilities.append(f"Port {port_num}: {vulnerability_desc}")
            
            # Check for privileged ports
            if port_num < 1024:
                vulnerabilities.append(f"Port {port_num}: Privileged port detected - requires elevated permissions")
            
            # Check for commonly targeted high ports
            if port_num in [8080, 8443, 8888, 9000, 9090]:
                vulnerabilities.append(f"Port {port_num}: Commonly targeted alternative port - ensure proper security measures")
                
        except ValueError:
            vulnerabilities.append(f"Invalid port format: {port}")
    
    # Validate against security rules
    config_lower = port_configurations.lower()
    
    # Check for wildcard binding
    if '0.0.0.0' in port_configurations:
        vulnerabilities.append("Security Rule Violation: Wildcard binding (0.0.0.0) detected - binds to all network interfaces")
    
    # Check for excessive port exposure
    if len(ports_to_check) > 10:
        vulnerabilities.append(f"Security Rule Violation: High number of exposed ports ({len(ports_to_check)}) - minimize attack surface")
    
    # Check for port ranges
    if '-' in port_configurations and ':' in port_configurations:
        vulnerabilities.append("Security Rule Violation: Port range detected - specify individual ports when possible")
    
    # If no vulnerabilities found, add a positive message
    if not vulnerabilities:
        vulnerabilities.append("No immediate security vulnerabilities detected in port configuration")
    
    return vulnerabilities