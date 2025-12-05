# select_best_model PRD

## Description
Pick the model with the highest risk‑adjusted performance according to a predefined criterion.


## Implementation Plan

### 1. Retrieve candidate model performance metrics from the 'evaluate_models' node output.

| Category | Details |
| --- | --- |
| **Reason** | The `evaluate_models` node provides the necessary performance metrics (Sharpe Ratio, Max Drawdown, and Annualized Return) for each candidate model to determine the best performing one. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Access the `candidate_models`, `sharpe_ratios`, `max_drawdowns`, and `annualized_returns` lists from the `evaluate_models` node's output. |

### 2. Implement a selection criterion based on Sharpe ratio and maximum drawdown, prioritizing Sharpe Ratio subject to a Max Drawdown threshold.

| Category | Details |
| --- | --- |
| **Reason** | The prompt specifies selecting the model with the 'best combination of Sharpe and low max drawdown'. A sensible approach is to maximize the Sharpe Ratio while ensuring the Max Drawdown is below a predefined risk tolerance threshold.  This reflects a risk-adjusted return perspective. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a `max_drawdown_threshold` (e.g., 0.15 for 15%). Iterate through the models. If a model's Max Drawdown is *less than or equal to* the `max_drawdown_threshold`, store it in a list of valid model candidates. From these valid model candidates, choose the model with the highest Sharpe Ratio. |

### 3. Handle the case where no model satisfies the risk tolerance threshold (max drawdown constraint).

| Category | Details |
| --- | --- |
| **Reason** | It's possible that none of the candidate models meets the Max Drawdown threshold, especially if the financial climate was particularly turbulent during backtesting.  The strategy should degrade gracefully if no model meets the hard constraints. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | If no model satisfies the `max_drawdown_threshold`, select the model with the absolute LOWEST max drawdown. If all the models have very high drawdowns, choose one that has a 'reasonable' Sharpe Ratio. If even that is not avaialble, return null/None for all outputs. Log a warning message to indicate this exceptional case. |

### 4. Extract the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and 'annualized_return' for selected best model.

| Category | Details |
| --- | --- |
| **Reason** | The output structure requires the model's identifier and its key metrics. This step formats the selected values into the defined output structure. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | After identifying the best model index, retrieve the corresponding values from the `candidate_models`, `sharpe_ratios`, `max_drawdowns`, and `annualized_returns` lists. Store the values into output variables named: `best_model_identifier`, `sharpe_ratio`, `max_drawdown`, and `annualized_return` |

### 5. Return the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and 'annualized_return'.

| Category | Details |
| --- | --- |
| **Reason** | Deliver required data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return the variables created above. The return types must be enforced with exception handling or type coercion to meet the requested output structure types. |
