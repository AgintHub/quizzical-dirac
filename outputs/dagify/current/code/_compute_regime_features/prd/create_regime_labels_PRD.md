# create_regime_labels PRD

## Description
Assigns a regime label of "high_vol" or "low_vol" to each row in the input DataFrame based on whether the VIX value meets or exceeds the supplied threshold.


## Implementation Plan

### 1. Parse the input CSV string into a pandas DataFrame and verify that a numeric 'VIX' column exists.

| Category | Details |
| --- | --- |
| **Reason** | The shim must operate on a structured data object and cannot proceed without the required VIX values. |
| **Impact** | Prevents runtime errors and ensures downstream logic receives a correctly shaped DataFrame. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(StringIO(dataframe))` to load the data; raise a descriptive ValueError if the 'VIX' column is missing or not numeric. |

### 2. Create a new column named 'RegimeLabel' where each row receives "high_vol" if its VIX value is greater than or equal to the parsed `vix_threshold`, otherwise "low_vol".

| Category | Details |
| --- | --- |
| **Reason** | The core business rule for regime classification is based on the VIX percentile threshold. |
| **Impact** | Enables downstream nodes to segment the time series into high‑ and low‑volatility regimes for further analysis. |
| **Complexity** | MEDIUM |
| **Method** | Convert `vix_threshold` to a float, then apply `np.where(df['VIX'] >= vix_threshold, 'high_vol', 'low_vol')` to generate the new column efficiently. |

### 3. Serialize the enriched DataFrame back to a CSV string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The surrounding pipeline expects CSV‑formatted text for interoperability between nodes. |
| **Impact** | Provides a consistent data exchange format, allowing subsequent nodes to parse the result without additional conversion steps. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` and assign the resulting string to the `output` key in the shim's return payload. |
