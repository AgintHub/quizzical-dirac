# identify_primary_close_column PRD

## Description
Identifies and returns the column name that contains the primary asset's closing price from a comma‑separated list of DataFrame column names.


## Implementation Plan

### 1. Parse the `columns` string into a list of clean column identifiers.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives column names as a single string; converting it to a list enables programmatic analysis. |
| **Impact** | Provides a reliable, order‑preserving collection of column names for downstream heuristics. |
| **Complexity** | LOW |
| **Method** | Split the string on commas, strip whitespace from each token, and store the result in a Python list. |

### 2. Apply a deterministic heuristic to select the primary close column from the parsed list.

| Category | Details |
| --- | --- |
| **Reason** | Multiple close‑price columns may exist (primary and secondary assets); a consistent rule is needed to isolate the primary one. |
| **Impact** | Ensures downstream feature calculations (correlations, spreads) use the correct reference asset, preventing data leakage or misalignment. |
| **Complexity** | MEDIUM |
| **Method** | 1️⃣ Look for a column that matches the pattern `*Primary*_Close` (case‑insensitive). 2️⃣ If none, select the first column that ends with `_Close` or contains the word `Close`. 3️⃣ If still ambiguous, fallback to the first column in the list. Return the chosen column name. |
