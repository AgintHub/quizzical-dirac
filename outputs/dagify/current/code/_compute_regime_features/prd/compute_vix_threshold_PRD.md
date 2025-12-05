# compute_vix_threshold PRD

## Description
Calculates the 75th percentile value of a VIX time‑series string to use as the high‑volatility threshold.


## Implementation Plan

### 1. Parse the input string into a numeric pandas Series, coercing non‑numeric entries to NaN and dropping them.

| Category | Details |
| --- | --- |
| **Reason** | The shim may receive raw CSV/JSON text with mixed types; ensuring a clean numeric Series prevents calculation errors. |
| **Impact** | Guarantees that subsequent percentile computation operates on valid data, reducing runtime exceptions. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv` with `StringIO` (if CSV) or `json.loads` (if JSON), then `pd.to_numeric(errors='coerce')` followed by `dropna()`. |

### 2. Compute the 75th percentile of the cleaned Series using NumPy or pandas quantile functionality.

| Category | Details |
| --- | --- |
| **Reason** | The threshold definition for high‑volatility regimes is the 75th percentile of VIX values. |
| **Impact** | Provides a deterministic, data‑driven cutoff that downstream nodes can rely on for regime labeling. |
| **Complexity** | MEDIUM |
| **Method** | Call `series.quantile(0.75, interpolation='nearest')` and cast the result to a Python float. |

### 3. Validate that the resulting threshold is a finite float; raise a descriptive error if not.

| Category | Details |
| --- | --- |
| **Reason** | Edge cases (e.g., empty series) would produce NaN, which would corrupt downstream logic. |
| **Impact** | Early failure with clear messaging aids debugging and ensures pipeline robustness. |
| **Complexity** | LOW |
| **Method** | Check `math.isfinite(threshold)`; if false, raise `ValueError` with context about the input series. |
