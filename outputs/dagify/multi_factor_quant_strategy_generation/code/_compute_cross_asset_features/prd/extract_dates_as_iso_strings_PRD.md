# extract_dates_as_iso_strings PRD

## Description
Converts a pandas DatetimeIndex into a list of ISO‑8601 formatted date strings.


## Implementation Plan

### 1. Parse the incoming `df_index` into a pandas DatetimeIndex if it is not already one.

| Category | Details |
| --- | --- |
| **Reason** | The shim may receive the index as a raw string representation, a list, or a pandas Index; normalising it ensures consistent processing. |
| **Impact** | Guarantees that downstream date extraction works reliably regardless of input format. |
| **Complexity** | MEDIUM |
| **Method** | Use `pd.to_datetime` with `errors='raise'` to coerce the input; handle cases where the input is already a DatetimeIndex by bypassing conversion. |

### 2. Convert each timestamp in the normalized DatetimeIndex to an ISO‑8601 date string (YYYY‑MM‑DD).

| Category | Details |
| --- | --- |
| **Reason** | The downstream `ComputeCrossAssetFeaturesOutput` expects dates strictly in ISO format for sorting and serialization. |
| **Impact** | Produces a deterministic, standards‑compliant list of date strings that can be consumed by JSON‑based APIs or other services. |
| **Complexity** | LOW |
| **Method** | Iterate over the index (or use `.strftime('%Y-%m-%d')`) and collect results into a Python list. |

### 3. Validate and sort the resulting list to ensure ascending chronological order and remove any `NaT` entries.

| Category | Details |
| --- | --- |
| **Reason** | Data pipelines assume dates are monotonic; missing or out‑of‑order dates can cause misalignment of features. |
| **Impact** | Prevents downstream alignment errors and guarantees that the `date` field matches the ordering of flattened feature arrays. |
| **Complexity** | LOW |
| **Method** | Filter out `pd.NaT` values, then apply `sorted()` on the list; optionally assert that the length matches the original index length minus any NaT rows. |
