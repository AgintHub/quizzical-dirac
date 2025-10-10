# get_memory_utilization PRD

## Description
A shim function that retrieves memory utilization metrics from a Kubernetes client.


## Implementation Plan

### 1. Implement the shim to interface with the Kubernetes API to fetch memory utilization data for containers or pods.

| Category | Details |
| --- | --- |
| **Reason** | This is necessary to provide accurate memory utilization metrics as part of the resource utilization data. |
| **Impact** | The system will be able to report on memory usage, enabling better resource management and monitoring. |
| **Complexity** | MEDIUM |
| **Method** | Use the Kubernetes Python client library to query the cluster's metrics API or relevant API endpoints for memory usage data. |

### 2. Handle potential exceptions and errors that may occur during the API call, such as network issues or API rate limiting.

| Category | Details |
| --- | --- |
| **Reason** | To ensure robustness and prevent the application from crashing due to external factors. |
| **Impact** | The application will be more resilient and capable of handling transient errors gracefully. |
| **Complexity** | MEDIUM |
| **Method** | Implement try-except blocks to catch specific exceptions, and consider implementing retry logic with exponential backoff for rate limiting or temporary network issues. |

### 3. Convert the fetched data into the required format (List[float]) for memory utilization metrics.

| Category | Details |
| --- | --- |
| **Reason** | To match the expected output structure defined by the CollectContainerDataOutput model. |
| **Impact** | The data will be correctly formatted for further processing or analysis within the application. |
| **Complexity** | LOW |
| **Method** | Parse the response from the Kubernetes API, extract the relevant memory utilization data, and convert it into a list of float values. |
