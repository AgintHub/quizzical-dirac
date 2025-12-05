# extract_implied_vol_list PRD

## Description
Extracts the implied volatility column from a validated DataFrame and returns it as a list of floats.


## Implementation Plan

### 1. Validate that the DataFrame contains an 'implied_vol' column of numeric type.

| Category | Details |
| --- | --- |
| **Reason** | Ensures downstream calculations receive correct data and prevents runtime type errors. |
| **Impact** | Provides early failure detection and clearer error messages, improving reliability of the volatility pipeline. |
| **Complexity** | LOW |
| **Method** | Use pandas `if 'implied_vol' not in df.columns` check and `pd.api.types.is_numeric_dtype(df['implied_vol'])` to verify presence and type. |

### 2. Convert the 'implied_vol' column to a plain Python list of floats.

| Category | Details |
| --- | --- |
| **Reason** | The downstream Pydantic model expects a native Python list, not a pandas Series. |
| **Impact** | Ensures compatibility with the `FetchVolatilityDataOutput` model and downstream serialization. |
| **Complexity** | LOW |
| **Method** | Apply `df['implied_vol'].astype(float).tolist()` after validation. |

### 3. Implement robust error handling that raises a descriptive `ValueError` if validation fails.

| Category | Details |
| --- | --- |
| **Reason** | Facilitates debugging and maintains data integrity across the workflow. |
| **Impact** | Consumers of the shim receive clear feedback, reducing silent failures and simplifying troubleshooting. |
| **Complexity** | MEDIUM |
| **Method** | Wrap validation and conversion in a try/except block; raise `ValueError` with message indicating missing column or non‑numeric data. |
