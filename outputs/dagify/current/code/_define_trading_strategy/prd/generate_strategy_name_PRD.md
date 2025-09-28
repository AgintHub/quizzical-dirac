# generate_strategy_name PRD

## Description
Creates a concise, descriptive trading strategy name based on provided entry rules and timeframes.


## Implementation Plan

### 1. Extract key phrases from the entry rules and assemble them into a base name, ensuring uniqueness by appending a short hash if duplicates occur.

| Category | Details |
| --- | --- |
| **Reason** | A meaningful base name improves strategy identification and reduces ambiguity when multiple strategies share similar rules. |
| **Impact** | Facilitates quick understanding and retrieval of strategy characteristics in downstream processes. |
| **Complexity** | LOW |
| **Method** | Use NLP token extraction (e.g., regex or spaCy) to find nouns/adjectives, concatenate them, and generate a UUID hash if needed. |

### 2. Normalize and aggregate the timeframes string (e.g., '1h,4h,1d') into a concise suffix and attach it to the base name.

| Category | Details |
| --- | --- |
| **Reason** | Including timeframes in the name conveys the strategy’s temporal coverage and differentiates multi-timeframe approaches. |
| **Impact** | Provides immediate context to users and other system components without requiring deeper inspection. |
| **Complexity** | MEDIUM |
| **Method** | Parse the comma‑separated list, map standard abbreviations (1h → 1H), sort alphabetically, and join with hyphens. |

### 3. Sanitize the resulting name by removing illegal characters, trimming whitespace, and enforcing a maximum length (e.g., 64 characters).

| Category | Details |
| --- | --- |
| **Reason** | Ensures compatibility with file systems, database keys, and external integrations that may impose naming constraints. |
| **Impact** | Prevents runtime errors and storage issues in downstream components. |
| **Complexity** | LOW |
| **Method** | Apply a regex pattern to filter out non‑alphanumeric characters, collapse multiple spaces, and truncate to the allowed length. |
