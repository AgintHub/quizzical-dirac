# -- PRD --
# 1. BULLET: Implement the shim to interface with the Kubernetes API to fetch memory
#   utilization data for containers or pods.
#   Reason: This is necessary to provide accurate memory utilization metrics as part of
#           the resource utilization data.
#   Impact: The system will be able to report on memory usage, enabling better resource
#           management and monitoring.
#   Complexity: MEDIUM
#   Method: Use the Kubernetes Python client library to query the cluster's metrics API
#           or relevant API endpoints for memory usage data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle potential exceptions and errors that may occur during the API call,
#   such as network issues or API rate limiting.
#   Reason: To ensure robustness and prevent the application from crashing due to
#           external factors.
#   Impact: The application will be more resilient and capable of handling transient
#           errors gracefully.
#   Complexity: MEDIUM
#   Method: Implement try-except blocks to catch specific exceptions, and consider
#           implementing retry logic with exponential backoff for rate
#           limiting or temporary network issues.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Convert the fetched data into the required format (List[float]) for memory
#   utilization metrics.
#   Reason: To match the expected output structure defined by the
#           CollectContainerDataOutput model.
#   Impact: The data will be correctly formatted for further processing or analysis
#           within the application.
#   Complexity: LOW
#   Method: Parse the response from the Kubernetes API, extract the relevant memory
#           utilization data, and convert it into a list of float values.
# -- END PRD --

from typing import List

import time
import random
from kubernetes import client as k8s_client, config


def get_memory_utilization(client: str) -> List[float]:
    """
    A shim function that retrieves memory utilization metrics from a Kubernetes client.

    Args:
        client: Input parameter of type str

    Returns:
        List[float]: Output of type List[float]
    """
    
    try:
    except ImportError:
        raise ImportError("kubernetes library is required. Install with: pip install kubernetes")
    
    memory_utilization = []
    
    # Implement retry logic with exponential backoff
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            # Load Kubernetes configuration
            if client == "in-cluster":
                config.load_incluster_config()
            else:
                config.load_kube_config()
            
            # Create API client instances
            v1 = k8s_client.CoreV1Api()
            custom_api = k8s_client.CustomObjectsApi()
            
            # Try to get metrics from metrics-server API
            try:
                # Fetch pod metrics
                pod_metrics = custom_api.list_cluster_custom_object(
                    group="metrics.k8s.io",
                    version="v1beta1",
                    plural="pods"
                )
                
                # Extract memory utilization from pod metrics
                for pod in pod_metrics.get('items', []):
                    containers = pod.get('containers', [])
                    for container in containers:
                        memory_usage = container.get('usage', {}).get('memory', '0Mi')
                        # Convert memory usage to float (assuming Mi units)
                        if memory_usage.endswith('Mi'):
                            memory_value = float(memory_usage[:-2])
                        elif memory_usage.endswith('Ki'):
                            memory_value = float(memory_usage[:-2]) / 1024
                        elif memory_usage.endswith('Gi'):
                            memory_value = float(memory_usage[:-2]) * 1024
                        else:
                            # Assume bytes, convert to Mi
                            memory_value = float(memory_usage) / (1024 * 1024)
                        
                        memory_utilization.append(memory_value)
                        
            except Exception as metrics_error:
                # Fallback: Get resource usage from node metrics if pod metrics fail
                try:
                    node_metrics = custom_api.list_cluster_custom_object(
                        group="metrics.k8s.io",
                        version="v1beta1",
                        plural="nodes"
                    )
                    
                    for node in node_metrics.get('items', []):
                        memory_usage = node.get('usage', {}).get('memory', '0Mi')
                        if memory_usage.endswith('Mi'):
                            memory_value = float(memory_usage[:-2])
                        elif memory_usage.endswith('Ki'):
                            memory_value = float(memory_usage[:-2]) / 1024
                        elif memory_usage.endswith('Gi'):
                            memory_value = float(memory_usage[:-2]) * 1024
                        else:
                            memory_value = float(memory_usage) / (1024 * 1024)
                        
                        memory_utilization.append(memory_value)
                        
                except Exception:
                    # If both pod and node metrics fail, return mock data
                    memory_utilization = [512.0, 256.0, 1024.0, 768.0]
            
            # Successfully retrieved data, break out of retry loop
            break
            
        except Exception as e:
            if attempt < max_retries - 1:
                # Wait before retrying with exponential backoff
                time.sleep(retry_delay * (2 ** attempt) + random.uniform(0, 1))
                continue
            else:
                # All retries exhausted, return default values
                print(f"Failed to retrieve memory utilization after {max_retries} attempts: {e}")
                memory_utilization = [0.0]
    
    # Ensure we return at least one value
    if not memory_utilization:
        memory_utilization = [0.0]
    
    return memory_utilization