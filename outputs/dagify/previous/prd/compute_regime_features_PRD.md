# compute_regime_features PRD

## Description
Derive regime classification signals from macro indicators (e.g., high‑/low‑vol regimes).


## Implementation Plan

### 1. Load the `cleaned_data_csv` string from the `align_and_clean_data` node, parse it into a pandas DataFrame preserving the original chronological order.

| Category | Details |
| --- | --- |
| **Reason** | The regime classifier needs numeric VIX and PMI series aligned to dates; parsing ensures we work with structured data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` to feed the CSV string into `pd.read_csv`, set `parse_dates=['Date']`, and sort by the Date column if not already sorted. |

### 2. Validate that the DataFrame contains the required macro columns `VIX` and `PMI`; raise a clear error if either is missing.

| Category | Details |
| --- | --- |
| **Reason** | Early validation prevents downstream logic failures and makes debugging data‑pipeline issues straightforward. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `{'VIX', 'PMI'}.issubset(df.columns)`; if false, construct an informative Exception listing missing columns. |

### 3. Compute the 75th percentile of the entire VIX series using `numpy.percentile(df['VIX'].dropna(), 75)` and store it as `vix_threshold`.

| Category | Details |
| --- | --- |
| **Reason** | A fixed percentile threshold implements the rule‑based high/low volatility regime definition described in the prompt. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `numpy as np`; ensure NaNs are excluded from the percentile calculation. |

### 4. Create a new column `RegimeLabel` where each row receives `'high_vol'` if its VIX value exceeds `vix_threshold`, otherwise `'low_vol'`.

| Category | Details |
| --- | --- |
| **Reason** | Translates the numeric VIX observation into a categorical regime label required by downstream models. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use vectorised pandas logic: `df['RegimeLabel'] = np.where(df['VIX'] > vix_threshold, 'high_vol', 'low_vol')`. |

### 5. Create a binary column `PMIFlag` set to `True` when the PMI value is greater than 0 (positive PMI) and `False` otherwise.

| Category | Details |
| --- | --- |
| **Reason** | Provides a simple directional macro signal that can be used as a feature in the assembled matrix. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `df['PMIFlag'] = df['PMI'] > 0` (pandas will produce a boolean series). |

### 6. Extract three parallel Python lists preserving date order: `dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()`, `regime_labels = df['RegimeLabel'].tolist()`, and `pmi_flags = df['PMIFlag'].tolist()`.

| Category | Details |
| --- | --- |
| **Reason** | The node's output specification demands plain Python lists (primitive types), not pandas objects. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Leverage pandas `.tolist()` after ensuring the DataFrame is sorted by Date. |

### 7. Return a JSON‑compatible dictionary containing the three lists under the keys `dates`, `regime_labels`, and `pmi_flags` as defined in the output structure.

| Category | Details |
| --- | --- |
| **Reason** | Conforms to the typed node contract, enabling downstream nodes (e.g., `assemble_feature_matrix`) to consume the data without further transformation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `return {"dates": dates, "regime_labels": regime_labels, "pmi_flags": pmi_flags}`. |
