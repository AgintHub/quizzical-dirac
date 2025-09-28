# analyze_indicator_predictive_power PRD

## Description
Analyzes the predictive power of a set of technical indicators by correlating them with statistical metadata and identifying the most informative indicators for generating trading signals.


## Implementation Plan

### 1. Calculate the correlation matrix between all technical indicators and the target price returns to identify linear relationships.

| Category | Details |
| --- | --- |
| **Reason** | Linear correlations provide an initial filter for indicators that have direct influence on price movements. |
| **Impact** | Creates a ranking that helps downstream nodes prioritize indicators for rule generation. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas DataFrame correlation functions to compute Pearson coefficients and sort by absolute value. |

### 2. Train a lightweight machine‑learning model (e.g., RandomForestRegressor) on lagged returns to quantify non‑linear predictive importance of each indicator.

| Category | Details |
| --- | --- |
| **Reason** | Captures complex interactions that simple correlations miss, giving a more accurate importance score. |
| **Impact** | Produces a feature importance list that can be directly used to craft entry/exit rules. |
| **Complexity** | HIGH |
| **Method** | Prepare a training set with future return labels, fit the model using scikit‑learn, extract feature_importances_ and normalize for reporting. |

### 3. Aggregate correlation and ML importance results into a formatted string summary highlighting the top‑performing indicators.

| Category | Details |
| --- | --- |
| **Reason** | Provides a human‑readable, machine‑processable output that downstream nodes can consume. |
| **Impact** | Ensures consistency and clarity in strategy definition, facilitating automation and debugging. |
| **Complexity** | LOW |
| **Method** | Merge ranked lists, format as JSON or plain text, and return as the 'output' field. |
