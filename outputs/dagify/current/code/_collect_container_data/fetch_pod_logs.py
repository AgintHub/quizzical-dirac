# -- PRD --
# 1. BULLET: Implement Kubernetes API client to fetch pod logs
#   Reason: To interact with the Kubernetes cluster and retrieve logs from specified
#           pods.
#   Impact: Enables the collection of container logs from the Kubernetes cluster.
#   Complexity: MEDIUM
#   Method: Use the Kubernetes Python client library to establish a connection to the
#           cluster and fetch logs.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle errors and exceptions during log retrieval
#   Reason: To ensure robustness and handle potential issues such as network errors or
#           pod not found.
#   Impact: Prevents the node from failing unexpectedly and provides useful error
#           messages instead.
#   Complexity: MEDIUM
#   Method: Implement try-except blocks to catch and handle exceptions, logging
#           relevant error messages.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Process and format the retrieved logs into a list of strings
#   Reason: To match the expected output format of the node.
#   Impact: Ensures that the output is consistent and usable by subsequent nodes.
#   Complexity: LOW
#   Method: Split the retrieved logs into individual log messages and store them in a
#           list.
# -- END PRD --

from typing import List

from kubernetes import client as k8s_client, config
import json


def fetch_pod_logs(client: str, pods: str) -> List[str]:
    """
    Fetches logs from specified pods in a Kubernetes cluster and returns them as a list of strings.

    Args:
        client: Input parameter of type str
pods: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    try:
        # Load Kubernetes configuration
        # Try in-cluster config first, then fall back to kubeconfig
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        
        # Create API client
        v1 = k8s_client.CoreV1Api()
        
        # Parse pods parameter (assuming it's a JSON string with pod names and namespaces)
        try:
            pods_data = json.loads(pods)
        except json.JSONDecodeError:
            # If not JSON, treat as a single pod name in default namespace
            pods_data = [{"name": pods, "namespace": "default"}]
        
        all_logs = []
        
        # Fetch logs for each pod
        for pod_info in pods_data:
            pod_name = pod_info.get("name", pod_info) if isinstance(pod_info, dict) else pod_info
            namespace = pod_info.get("namespace", "default") if isinstance(pod_info, dict) else "default"
            
            try:
                # Fetch pod logs
                logs = v1.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace,
                    pretty=True
                )
                
                # Process and format logs into list of strings
                if logs:
                    log_lines = logs.strip().split('\n')
                    # Filter out empty lines
                    log_lines = [line for line in log_lines if line.strip()]
                    all_logs.extend(log_lines)
                
            except k8s_client.exceptions.ApiException as e:
                error_msg = f"Error fetching logs for pod {pod_name} in namespace {namespace}: {e.reason}"
                print(error_msg)
                all_logs.append(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error fetching logs for pod {pod_name}: {str(e)}"
                print(error_msg)
                all_logs.append(error_msg)
        
        return all_logs
        
    except Exception as e:
        error_msg = f"Failed to initialize Kubernetes client or fetch logs: {str(e)}"
        print(error_msg)
        return [error_msg]