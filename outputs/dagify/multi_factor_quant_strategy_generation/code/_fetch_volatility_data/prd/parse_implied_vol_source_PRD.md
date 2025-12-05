# parse_implied_vol_source PRD

## Description
Extracts the implied volatility provider identifier from a plain‑text list of data‑source descriptions.


## Implementation Plan

### 1. Implement robust string parsing to split `data_sources` into individual lines and extract the provider name from the line that mentions implied volatility.

| Category | Details |
| --- | --- |
| **Reason** | The input is a free‑form text block; reliable extraction requires deterministic line handling and pattern matching. |
| **Impact** | Accurately identifies the correct provider, enabling downstream calls to fetch implied volatility data. |
| **Complexity** | MEDIUM |
| **Method** | Use Python's `str.splitlines()` to obtain lines, then apply a regular expression such as `r"Implied\s*Volatility\s*[:\-]?\s*(.+?)(?:,|$)"` (case‑insensitive) to capture the provider name; trim whitespace before returning. |

### 2. Add fallback heuristics to handle variations in wording (e.g., "IV Index", "Implied Vol", or provider name appearing before the dataset type).

| Category | Details |
| --- | --- |
| **Reason** | Data source descriptions may not follow a strict template, and missing the provider would break the pipeline. |
| **Impact** | Improves resilience against inconsistencies in source listings, reducing false negatives. |
| **Complexity** | LOW |
| **Method** | If the primary regex fails, iterate through lines and check for keywords like "implied vol", "iv index", then split the line on ':' or '-' and take the segment that is not the dataset type as the provider. |

### 3. Validate the extracted provider against a whitelist of known implied volatility providers and return an empty string if validation fails.

| Category | Details |
| --- | --- |
| **Reason** | Prevent propagation of misspelled or unsupported provider names to downstream fetch functions. |
| **Impact** | Ensures only supported providers are used, avoiding runtime errors in `fetch_implied_volatility_data`. |
| **Complexity** | LOW |
| **Method** | Maintain a set such as `{"CBOE", "Bloomberg", "Refinitiv"}`; after extraction, check `provider.strip()` against the set (case‑insensitive). If not found, log a warning and return `""`. |
