# compute_portfolio_returns PRD

## Description
Calculates daily portfolio returns for each model by applying position signals to the test set price movements.


## Implementation Plan

### 1. Parse the string inputs into usable Python objects (positions dict and pandas DataFrame).

| Category | Details |
| --- | --- |
| **Reason** | The shim receives JSON‑encoded strings; they must be converted before any numeric calculations can occur. |
| **Impact** | Enables downstream vectorized operations and prevents type errors during return computation. |
| **Complexity** | LOW |
| **Method** | Use json.loads for the positions string and pandas.read_csv (via StringIO) for the test_df string to obtain a DataFrame with proper dtypes. |

### 2. Align position signals with asset price changes and compute weighted daily returns for each model.

| Category | Details |
| --- | --- |
| **Reason** | Accurate portfolio returns require matching each model's position schedule to the corresponding asset returns on the same dates. |
| **Impact** | Produces a dictionary mapping model identifiers to pandas Series of daily returns, which feed all subsequent performance metrics. |
| **Complexity** | MEDIUM |
| **Method** | Calculate asset daily returns with DataFrame.pct_change(), then for each model multiply the position array (aligned via index.join) by the asset returns and sum across assets, handling NaNs with fillna(0). |

### 3. Serialize the resulting returns dictionary back to a JSON string for downstream nodes.

| Category | Details |
| --- | --- |
| **Reason** | The rest of the pipeline expects string outputs consistent with other shim interfaces. |
| **Impact** | Ensures seamless integration with EvaluateModelsOutput generation and maintains a uniform data contract. |
| **Complexity** | LOW |
| **Method** | Convert each pandas Series to a list of floats, build a plain dict, then json.dumps the dict and assign to the 'output' field. |
