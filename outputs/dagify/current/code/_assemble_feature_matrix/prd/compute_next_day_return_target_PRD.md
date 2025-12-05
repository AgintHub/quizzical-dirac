# compute_next_day_return_target PRD

## Description
Computes a next‑day simple return target column for the provided DataFrame and returns the updated CSV string.


## Implementation Plan

### 1. Parse the input CSV string into a pandas DataFrame and ensure the Date column is sorted chronologically.

| Category | Details |
| --- | --- |
| **Reason** | Accurate calculations depend on correct ordering and proper data types for numeric operations. |
| **Impact** | Guarantees that subsequent calculations operate on a clean, correctly indexed DataFrame. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(df))`, convert the Date column to datetime with `pd.to_datetime`, and sort by Date. |

### 2. Create the `Target` column by shifting the specified close price column one row forward and applying the simple return formula.

| Category | Details |
| --- | --- |
| **Reason** | The core business requirement is to provide the next‑day return as the model's target variable. |
| **Impact** | Adds a predictive target that aligns with feature rows, enabling supervised learning downstream. |
| **Complexity** | MEDIUM |
| **Method** | Compute `df['Target'] = df[close_column].shift(-1) / df[close_column] - 1`, then drop the last row where `Target` is NaN. |

### 3. Serialize the enriched DataFrame back to a CSV string while preserving the original column order and including the new `Target` column.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect CSV‑formatted text, not a DataFrame object. |
| **Impact** | Provides a seamless interface for the rest of the pipeline, maintaining compatibility with existing loaders. |
| **Complexity** | LOW |
| **Method** | Use `df.to_csv(index=False)` with an in‑memory `StringIO` buffer and return the buffer's contents as `output`. |
