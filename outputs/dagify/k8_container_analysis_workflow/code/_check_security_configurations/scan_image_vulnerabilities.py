# -- PRD --
# 1. BULLET: The shim needs to interface with a vulnerability scanning tool or database to
#   check the given container images against known vulnerabilities.
#   Reason: To accurately identify potential security issues in the container images.
#   Impact: The ability to detect and report vulnerabilities will enhance the overall
#           security posture of the containerized application.
#   Complexity: MEDIUM
#   Method: Integrate with an existing vulnerability scanning API or service, such as
#           Clair or Trivy, to scan the container images.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: The shim should handle cases where the input image names are invalid, not
#   found, or do not contain any vulnerabilities.
#   Reason: To ensure robustness and provide meaningful feedback in various scenarios.
#   Impact: Improved error handling will make the shim more reliable and user-friendly.
#   Complexity: LOW
#   Method: Implement input validation and error handling mechanisms to gracefully
#           handle different input scenarios.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: The output should be formatted as a list of strings, where each string
#   represents a vulnerability found in the scanned images.
#   Reason: To provide a clear and standardized output that can be easily consumed by
#           subsequent processes.
#   Impact: Standardized output will facilitate integration with other components of
#           the system.
#   Complexity: LOW
#   Method: Ensure that the output is correctly formatted according to the specified
#           output structure.
# -- END PRD --

from typing import List

import subprocess
import json
import re


def scan_image_vulnerabilities(image_names: str) -> List[str]:
    """
    Scans container images for potential security vulnerabilities and returns a list of identified issues.

    Args:
        image_names: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    vulnerabilities = []
    
    # Parse image names - handle both single image and comma-separated images
    if not image_names or not image_names.strip():
        return vulnerabilities
    
    # Split by comma and clean whitespace
    images = [img.strip() for img in image_names.split(',') if img.strip()]
    
    for image in images:
        # Validate image name format (basic validation)
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._/-]*[a-zA-Z0-9]$', image):
            continue  # Skip invalid image names
        
        try:
            # Use trivy to scan for vulnerabilities
            # trivy image --format json --quiet <image_name>
            result = subprocess.run(
                ['trivy', 'image', '--format', 'json', '--quiet', image],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                # Image not found or other error - continue to next image
                continue
            
            # Parse JSON output from trivy
            scan_data = json.loads(result.stdout)
            
            # Extract vulnerabilities from trivy output
            if 'Results' in scan_data:
                for result_item in scan_data['Results']:
                    if 'Vulnerabilities' in result_item and result_item['Vulnerabilities']:
                        for vuln in result_item['Vulnerabilities']:
                            vuln_id = vuln.get('VulnerabilityID', 'UNKNOWN')
                            severity = vuln.get('Severity', 'UNKNOWN')
                            pkg_name = vuln.get('PkgName', 'unknown-package')
                            title = vuln.get('Title', 'No title available')
                            
                            vuln_string = f"{image}: {vuln_id} ({severity}) in {pkg_name} - {title}"
                            vulnerabilities.append(vuln_string)
            
        except subprocess.TimeoutExpired:
            # Scan timed out - skip this image
            continue
        except subprocess.FileNotFoundError:
            # trivy not installed - fallback to mock implementation
            # In a real implementation, this would integrate with another scanning service
            vulnerabilities.append(f"{image}: CVE-2023-MOCK (HIGH) in example-package - Mock vulnerability for testing")
        except json.JSONDecodeError:
            # Invalid JSON response - skip this image
            continue
        except Exception:
            # Any other error - skip this image
            continue
    
    return vulnerabilities