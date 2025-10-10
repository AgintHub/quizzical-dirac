# -- PRD --
# 1. BULLET: Implement Kubernetes API call to fetch active pods
#   Reason: To retrieve the list of currently active pods in the cluster
#   Impact: Enables collection of container logs and monitoring of active containers
#   Complexity: MEDIUM
#   Method: Use Kubernetes Python client library to list pods with status 'Running'
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle Kubernetes client connection initialization and validation
#   Reason: To ensure the client is properly configured and authenticated
#   Impact: Ensures that the function can successfully interact with the Kubernetes
#           cluster
#   Complexity: LOW
#   Method: Validate client connection object and handle potential exceptions
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Process and filter pod list to extract relevant information
#   Reason: To provide a clean and relevant list of active pods
#   Impact: Simplifies downstream processing by providing a standardized output
#   Complexity: LOW
#   Method: Extract pod names from the Kubernetes API response and return as a list of
#           strings
# -- END PRD --

from typing import List

from kubernetes import client as k8s_client, config


def get_active_pods(client: str) -> List[str]:
    """
    Retrieves a list of active pods from a Kubernetes cluster using a provided client connection.

    Args:
        client: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    try:
        # Load Kubernetes configuration
        config.load_incluster_config()
    except:
        try:
            config.load_kube_config()
        except Exception as e:
            raise ValueError(f"Failed to load Kubernetes configuration: {e}")
    
    # Initialize the Kubernetes API client
    v1 = k8s_client.CoreV1Api()
    
    try:
        # Fetch all pods across all namespaces
        pods = v1.list_pod_for_all_namespaces()
        
        # Filter for active/running pods and extract names
        active_pod_names = []
        for pod in pods.items:
            if pod.status.phase == 'Running':
                active_pod_names.append(pod.metadata.name)
        
        return active_pod_names
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve pods from Kubernetes cluster: {e}")