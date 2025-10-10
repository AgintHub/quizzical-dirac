# -- PRD --
# 1. BULLET: Implement a validation mechanism to check if secret management is properly
#   configured for the given containers and images
#   Reason: To ensure that sensitive information is handled securely
#   Impact: Improves the overall security posture of the containerized application
#   Complexity: MEDIUM
#   Method: Use a combination of configuration checks and potentially external secret
#           management tools to validate the setup
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle different types of secret management configurations (e.g., environment
#   variables, Kubernetes secrets)
#   Reason: To support various deployment scenarios and secret management strategies
#   Impact: Enhances the flexibility and adaptability of the validation process
#   Complexity: HIGH
#   Method: Implement modular checks for different secret management approaches,
#           allowing for easy extension and customization
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Provide clear output indicating whether secret management is valid or not
#   Reason: To enable downstream processes to react accordingly based on the validation
#           result
#   Impact: Facilitates informed decision-making and potential corrective actions
#   Complexity: LOW
#   Method: Return a boolean value indicating the validity of the secret management
#           configuration
# -- END PRD --

import re
import subprocess
import json


def validate_secret_management(container_names: str, image_names: str) -> bool:
    """
    Validates secret management configurations for containers and images

    Args:
        container_names: Input parameter of type str
image_names: Input parameter of type str

    Returns:
        bool: Output of type bool
    """
    
    # Parse container and image names from input strings
    container_list = [name.strip() for name in container_names.split(',') if name.strip()]
    image_list = [name.strip() for name in image_names.split(',') if name.strip()]
    
    # Validation flags
    all_valid = True
    
    # Check environment variables for secret management patterns
    secret_env_patterns = [
        r'.*_SECRET.*',
        r'.*_PASSWORD.*',
        r'.*_TOKEN.*',
        r'.*_KEY.*',
        r'.*_CREDENTIAL.*'
    ]
    
    # Validate containers
    for container_name in container_list:
        container_valid = False
        
        try:
            # Check if container has proper secret mounts or environment variables
            # Inspect container configuration
            inspect_cmd = ['docker', 'inspect', container_name]
            result = subprocess.run(inspect_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                container_config = json.loads(result.stdout)[0]
                
                # Check for mounted secrets
                mounts = container_config.get('Mounts', [])
                for mount in mounts:
                    mount_source = mount.get('Source', '').lower()
                    if 'secret' in mount_source or 'credential' in mount_source:
                        container_valid = True
                        break
                
                # Check environment variables for proper secret handling
                if not container_valid:
                    env_vars = container_config.get('Config', {}).get('Env', [])
                    for env_var in env_vars:
                        for pattern in secret_env_patterns:
                            if re.match(pattern, env_var.split('=')[0], re.IGNORECASE):
                                # Check if the value looks like a reference rather than hardcoded
                                env_value = env_var.split('=', 1)[1] if '=' in env_var else ''
                                if (env_value.startswith('/var/run/secrets/') or 
                                    env_value.startswith('${') or 
                                    len(env_value) == 0):
                                    container_valid = True
                                    break
                    
                # Check for Kubernetes secret volume mounts
                if not container_valid:
                    volumes = container_config.get('Config', {}).get('Volumes', {})
                    for volume_path in volumes.keys():
                        if '/var/run/secrets' in volume_path or '/etc/secrets' in volume_path:
                            container_valid = True
                            break
                            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError, KeyError, IndexError):
            # If container inspection fails, assume invalid secret management
            container_valid = False
        
        if not container_valid:
            all_valid = False
    
    # Validate images
    for image_name in image_list:
        image_valid = False
        
        try:
            # Inspect image configuration
            inspect_cmd = ['docker', 'inspect', image_name]
            result = subprocess.run(inspect_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                image_config = json.loads(result.stdout)[0]
                
                # Check image environment variables
                config = image_config.get('Config', {})
                env_vars = config.get('Env', [])
                
                # Image is valid if it doesn't contain hardcoded secrets
                image_valid = True  # Assume valid unless proven otherwise
                
                for env_var in env_vars:
                    for pattern in secret_env_patterns:
                        if re.match(pattern, env_var.split('=')[0], re.IGNORECASE):
                            env_value = env_var.split('=', 1)[1] if '=' in env_var else ''
                            # If secret-like env var has a hardcoded value, it's invalid
                            if (env_value and 
                                not env_value.startswith('/var/run/secrets/') and 
                                not env_value.startswith('${') and 
                                len(env_value) > 0):
                                image_valid = False
                                break
                    if not image_valid:
                        break
                        
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError, KeyError, IndexError):
            # If image inspection fails, assume invalid secret management
            image_valid = False
        
        if not image_valid:
            all_valid = False
    
    # Additional check for Kubernetes secrets if kubectl is available
    try:
        # Check if we're in a Kubernetes environment
        kubectl_cmd = ['kubectl', 'get', 'secrets', '--no-headers']
        result = subprocess.run(kubectl_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            # Kubernetes secrets are available, which is good for secret management
            pass  # This doesn't change validation but indicates good practice
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        # kubectl not available or not in K8s environment
        pass
    
    return all_valid