# -- PRD --
# 1. BULLET: Authenticate with the Kubernetes cluster using a suitable authentication
#   method (e.g., token, certificate).
#   Reason: To securely connect to the Kubernetes cluster, proper authentication is
#           required.
#   Impact: Successful authentication enables the collection of container data from the
#           cluster.
#   Complexity: MEDIUM
#   Method: Use the Kubernetes Python client library to handle authentication and
#           client initialization.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Configure the Kubernetes client with the appropriate cluster configuration
#   (e.g., context, namespace).
#   Reason: To interact with the correct cluster and resources, the client needs to be
#           configured accordingly.
#   Impact: Proper configuration ensures that data is collected from the intended
#           cluster resources.
#   Complexity: LOW
#   Method: Utilize the Kubernetes configuration files or environment variables to
#           configure the client.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Handle potential exceptions and errors during client initialization (e.g.,
#   connection failures, authentication errors).
#   Reason: To ensure robustness, the initialization process should be able to handle
#           and recover from errors.
#   Impact: Proper error handling prevents the application from crashing and provides
#           useful feedback instead.
#   Complexity: HIGH
#   Method: Implement try-except blocks to catch and handle specific Kubernetes client
#           exceptions, providing meaningful error messages.
# -- END PRD --

from kubernetes import client, config


def initialize_k8s_client() -> str:
    """
    Initializes a Kubernetes client connection for interacting with a Kubernetes cluster.

    Args:
        

    Returns:
        str: Output of type Any
    """
    try:
        
        # Try to load configuration in order of preference
        try:
            # First, try to load in-cluster configuration (for pods running in cluster)
            config.load_incluster_config()
            config_source = "in-cluster"
        except config.ConfigException:
            try:
                # Fall back to loading from kubeconfig file
                config.load_kube_config()
                config_source = "kubeconfig"
            except config.ConfigException as e:
                return f"Failed to load Kubernetes configuration: {str(e)}"
        
        # Create API client instance
        v1 = client.CoreV1Api()
        
        # Test the connection by making a simple API call
        try:
            # List namespaces as a connectivity test
            namespaces = v1.list_namespace()
            namespace_count = len(namespaces.items)
            
            return f"Successfully initialized Kubernetes client using {config_source} configuration. Connected to cluster with {namespace_count} namespaces."
            
        except client.exceptions.ApiException as api_err:
            return f"Authentication failed: {api_err.status} - {api_err.reason}"
        except Exception as conn_err:
            return f"Connection test failed: {str(conn_err)}"
            
    except ImportError:
        return "Failed to initialize: kubernetes Python client library is not installed. Please install with 'pip install kubernetes'"
    except Exception as e:
        return f"Unexpected error during Kubernetes client initialization: {str(e)}"