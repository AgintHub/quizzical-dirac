# train_models PRD

## Description
Perform hyperparameter optimization on the training set and fit each candidate model.


## Implementation Plan

### 1. Load training and validation datasets from the 'split_dataset' node.

| Category | Details |
| --- | --- |
| **Reason** | These datasets are essential for training and evaluating the candidate models during hyperparameter optimization. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a CSV parsing library (e.g., pandas in Python) to load the 'train_csv' and 'validation_csv' strings from the 'split_dataset' node into dataframes. Ensure the Date column, if present, is parsed correctly as a datetime object. |

### 2. Load the hyperparameter grid from the 'define_hyperparameter_grid' node.

| Category | Details |
| --- | --- |
| **Reason** | The hyperparameter grid specifies the search space for hyperparameter optimization. It is crucial for determining the different hyperparameter combinations to test. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the 'hyperparameter_grid_json' string from the 'define_hyperparameter_grid' node using a JSON parsing library (e.g., json in Python). Store the hyperparameter grids for both Gradient Boosting and LSTM models separately in dictionaries. |

### 3. Implement a grid or random search algorithm.

| Category | Details |
| --- | --- |
| **Reason** | The prompt requests a hyperparameter search, and either grid search or random search will fulfill this requirement. Random search often performs better with high-dimensional hyperparameter spaces. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a random search.  For each model type (GB and LSTM), randomly sample hyperparameter combinations from the defined grid.  Use a fixed number of iterations (e.g., 50 for each model). Ensure sampled hyperparameters are within the specified ranges and are of the correct datatype (e.g., integer or float).  Store each hyperparameter combination in a list. |

### 4. Train each candidate model on the training set.

| Category | Details |
| --- | --- |
| **Reason** | Training is essential for model fitting. Each model needs to learn the relationship between features and target from the training data. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each sampled hyperparameter combination, instantiate a Gradient Boosting model (e.g., from scikit-learn) or an LSTM model (e.g., from TensorFlow/Keras) with the corresponding hyperparameters. Train the model using the training data and the 'fit' method. Use appropriate loss functions and optimizers for each model type (e.g., mean squared error for regression problems). Implement early stopping based on the validation set performance to prevent overfitting. |

### 5. Evaluate each trained model on the validation set.

| Category | Details |
| --- | --- |
| **Reason** | Evaluation on the validation set provides an unbiased estimate of the model's performance on unseen data. This is crucial for selecting the best hyperparameters. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each trained model, predict the target variable on the validation set. Calculate the Sharpe ratio and Root Mean Squared Error (RMSE) using the predicted values and the actual values from the validation set. Ensure proper calculation of Sharpe Ratio considering the risk-free rate (which may need to be a configurable parameter).  RMSE should be computed after scaling the predicted values back to the original scale of the target variable if scaling was applied during preprocessing. |

### 6. Store hyperparameters, Validation Sharpe Ratios, and Validation RMSE for each candidate model.

| Category | Details |
| --- | --- |
| **Reason** | This information is needed to compare the performance of different models and select the best one. This table will then be used by the 'evaluate_models' node to decide on the best overall model |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create three lists: 'hyperparameters', 'validation_sharpe', and 'validation_rmse'.  For each trained model, store the hyperparameter combination (as a string), the validation Sharpe ratio, and the validation RMSE in the respective lists.  Consider using a standardized string format for the hyperparameters using JSON serialization |

### 7. Return a table (represented as lists) containing Hyperparameters, ValidationSharpe, ValidationRMSE.

| Category | Details |
| --- | --- |
| **Reason** | This table is the final output, providing the summarized performance of all models. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return the created lists 'hyperparameters', 'validation_sharpe', and 'validation_rmse' as the output of this node. Confirm that that number of elements in each list are identical, failing if not. Use appropriate error handling if model training fails to prevent exiting on the first failure. Instead, move on to the next model, storing a NaN for the validation metrics. |
