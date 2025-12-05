# build_asset_pairs_list PRD

## Description
Generates a list of cross‑asset pair identifiers from a comma‑separated string of secondary close column names.


## Implementation Plan

### 1. Parse the incoming comma‑separated string of secondary close column names into a clean Python list.

| Category | Details |
| --- | --- |
| **Reason** | The upstream node supplies secondary column names as a single string; converting it to a list is required for deterministic processing. |
| **Impact** | Ensures that each secondary asset is individually recognized, eliminating parsing errors downstream. |
| **Complexity** | LOW |
| **Method** | Use `str.split(',')` followed by `strip()` on each element to produce `List[str] secondary_cols`. |

### 2. Strip the `_Close` suffix from each column name to obtain the raw ticker symbol.

| Category | Details |
| --- | --- |
| **Reason** | Column names follow the `<Ticker>_Close` convention; the ticker is the meaningful identifier for asset‑pair construction. |
| **Impact** | Produces clean ticker strings that can be safely concatenated with the primary asset identifier. |
| **Complexity** | LOW |
| **Method** | Iterate over `secondary_cols` and apply `col.replace('_Close', '')` (or regex) to generate `ticker` list. |

### 3. Combine each ticker with the primary asset identifier to form pair strings in the format `Primary-SecondaryTicker`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream features expect asset pairs to be explicitly named; embedding the primary asset provides consistent ordering for correlation and spread flattening. |
| **Impact** | Creates the `output` list required by `ComputeCrossAssetFeaturesOutput.asset_pairs`, enabling correct feature alignment. |
| **Complexity** | MEDIUM |
| **Method** | Retrieve the primary ticker from a known source (e.g., a configuration file, environment variable, or a dedicated helper function `identify_primary_ticker()`), then build each pair with an f‑string: `f"{primary_ticker}-{ticker}"`. |
