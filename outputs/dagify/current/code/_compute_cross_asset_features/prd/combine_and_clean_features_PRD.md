# combine_and_clean_features PRD

## Description
Merges the rolling correlation DataFrame and price spread DataFrame, aligns their indices, fills or drops NaN values, and returns the cleaned combined features as a CSV‑formatted string.


## Implementation Plan

### 1. Parse the input CSV strings into pandas DataFrames with a DateTime index.

| Category | Details |
| --- | --- |
| **Reason** | Subsequent operations require DataFrames to align on dates for accurate merging. |
| **Impact** | Enables correct temporal alignment and subsequent feature engineering steps. |
| **Complexity** | LOW |
| **Method** | Use pandas.read_csv with StringIO, parse dates column, and set it as the index. |

### 2. Align the two DataFrames on their index, perform an inner join, and handle missing values by forward‑filling then back‑filling.

| Category | Details |
| --- | --- |
| **Reason** | Correlation and spread series may have different start dates or NaNs; consistent rows are needed for modeling. |
| **Impact** | Produces a clean combined feature set without gaps, improving downstream model performance. |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.DataFrame.join with 'inner' mode, then apply df.ffill().bfill() to fill remaining NaNs. |

### 3. Serialize the cleaned combined DataFrame back to a CSV string for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | The pipeline expects string outputs to be passed between nodes without persisting to disk. |
| **Impact** | Provides a portable, text‑based representation compatible with the rest of the workflow. |
| **Complexity** | LOW |
| **Method** | Use DataFrame.to_csv with StringIO, ensuring ISO‑8601 date formatting. |
