# -- PRD --
# 1. BULLET: Implement Kubernetes API client functionality to fetch container
#   configurations
#   Reason: To gather container configuration manifests, we need to interact with the
#           Kubernetes API
#   Impact: Enables the collection of container configuration data necessary for
#           further processing
#   Complexity: MEDIUM
#   Method: Use the Kubernetes Python client library to create a client instance that
#           can list and retrieve container configurations from the cluster
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Handle authentication and connection to the Kubernetes cluster
#   Reason: To access the Kubernetes API, proper authentication and connection handling
#           are required
#   Impact: Ensures that the function can securely and reliably connect to the
#           Kubernetes cluster
#   Complexity: MEDIUM
#   Method: Utilize Kubernetes client library's built-in authentication mechanisms,
#           such as using kubeconfig files or service account tokens
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Process and return container configuration data in the required format
#   Reason: The function needs to output the container configurations in a specific
#           format
#   Impact: Provides the necessary data for downstream processing and analysis
#   Complexity: LOW
#   Method: Convert the retrieved container configuration data into a list of
#           dictionaries, where each dictionary represents a container's
#           configuration manifest
# -- END PRD --

from typing import List
from kubernetes import config

import json


def get_container_configs(client: str) -> List[str]:
    """
    Retrieves container configuration manifests from a Kubernetes cluster using a provided client connection.

    Args:
        client: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    
    # Load Kubernetes configuration
    try:
        # Try to load in-cluster config first, then fall back to kubeconfig
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
    except Exception as e:
        raise ConnectionError(f"Failed to load Kubernetes configuration: {e}")
    
    # Create Kubernetes API client
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    
    container_configs = []
    
    try:
        # Get all namespaces
        namespaces = v1.list_namespace()
        
        for namespace in namespaces.items:
            namespace_name = namespace.metadata.name
            
            # Get pods in the namespace
            pods = v1.list_namespaced_pod(namespace=namespace_name)
            for pod in pods.items:
                pod_config = {
                    'kind': 'Pod',
                    'apiVersion': 'v1',
                    'metadata': {
                        'name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'labels': pod.metadata.labels or {}
                    },
                    'spec': {
                        'containers': []
                    }
                }
                
                # Process containers in the pod
                if pod.spec.containers:
                    for container in pod.spec.containers:
                        container_spec = {
                            'name': container.name,
                            'image': container.image,
                            'ports': [{'containerPort': port.container_port, 'protocol': port.protocol} for port in (container.ports or [])],
                            'env': [{'name': env.name, 'value': env.value} for env in (container.env or [])],
                            'resources': {}
                        }
                        
                        if container.resources:
                            if container.resources.limits:
                                container_spec['resources']['limits'] = dict(container.resources.limits)
                            if container.resources.requests:
                                container_spec['resources']['requests'] = dict(container.resources.requests)
                        
                        pod_config['spec']['containers'].append(container_spec)
                
                container_configs.append(json.dumps(pod_config))
            
            # Get deployments in the namespace
            deployments = apps_v1.list_namespaced_deployment(namespace=namespace_name)
            for deployment in deployments.items:
                deployment_config = {
                    'kind': 'Deployment',
                    'apiVersion': 'apps/v1',
                    'metadata': {
                        'name': deployment.metadata.name,
                        'namespace': deployment.metadata.namespace,
                        'labels': deployment.metadata.labels or {}
                    },
                    'spec': {
                        'replicas': deployment.spec.replicas,
                        'template': {
                            'spec': {
                                'containers': []
                            }
                        }
                    }
                }
                
                # Process containers in the deployment template
                if deployment.spec.template.spec.containers:
                    for container in deployment.spec.template.spec.containers:
                        container_spec = {
                            'name': container.name,
                            'image': container.image,
                            'ports': [{'containerPort': port.container_port, 'protocol': port.protocol} for port in (container.ports or [])],
                            'env': [{'name': env.name, 'value': env.value} for env in (container.env or [])],
                            'resources': {}
                        }
                        
                        if container.resources:
                            if container.resources.limits:
                                container_spec['resources']['limits'] = dict(container.resources.limits)
                            if container.resources.requests:
                                container_spec['resources']['requests'] = dict(container.resources.requests)
                        
                        deployment_config['spec']['template']['spec']['containers'].append(container_spec)
                
                container_configs.append(json.dumps(deployment_config))
    
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve container configurations: {e}")
    
    return container_configs