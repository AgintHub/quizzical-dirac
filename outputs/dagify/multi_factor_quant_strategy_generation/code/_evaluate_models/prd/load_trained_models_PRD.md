# load_trained_models PRD

## Description
This shim function loads trained models from a storage location based on provided model identifiers, returning them as a dictionary.


## Implementation Plan

### 1. Implement the retrieval of trained models based on the provided `model_ids`.

| Category | Details |
| --- | --- |
| **Reason** | The core functionality of the function relies on fetching the correct models. |
| **Impact** | Successful retrieval enables subsequent steps like performance metric calculation which are essential for model assessment. |
| **Complexity** | MEDIUM |
| **Method** | Utilize a persistent storage solution like cloud storage (AWS S3, Google Cloud Storage) or a local file system. Implement a function which takes the `model_ids` as input, searches for the corresponding model files in the storage, loads them into memory using a suitable model loading function (e.g., from the `pickle` or `joblib` library), and returns them as a dictionary. |

### 2. Add error handling for cases where models do not exist or cannot be loaded.

| Category | Details |
| --- | --- |
| **Reason** | Handles unexpected scenarios during loading, improving robustness. |
| **Impact** | Prevents the program from crashing and provides meaningful error messages, ensuring the system can handle incomplete datasets gracefully. |
| **Complexity** | LOW |
| **Method** | Implement try-except blocks to catch potential `FileNotFoundError` or loading errors. Log the error with a meaningful message and return an empty dictionary or a default model as appropriate. Consider raising a custom exception to indicate model loading failure explicitly. |

### 3. Ensure compatibility between the serialization/deserialization format with training stage.

| Category | Details |
| --- | --- |
| **Reason** | Avoids mismatches due to version or library conflicts. |
| **Impact** | Garbage-In-Garbage-Out problem during inference stage. |
| **Complexity** | HIGH |
| **Method** | Implement version control of the training and loading process via hashing, checking model structure is correct during inference, etc. |
