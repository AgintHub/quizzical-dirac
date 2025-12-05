# extract_cross_asset_tickers PRD

## Description
Extracts a list of cross‑asset ticker symbols from a plain‑text description of data sources.


## Implementation Plan

### 1. Tokenize each line of the `data_sources` string and identify ticker symbols using regular‑expression patterns.

| Category | Details |
| --- | --- |
| **Reason** | Data‑source descriptions are free‑form text; a reliable pattern match is needed to reliably pull out tickers. |
| **Impact** | Ensures that the downstream `fetch_cross_asset_data` node receives accurate ticker identifiers, preventing download failures. |
| **Complexity** | MEDIUM |
| **Method** | Compile a regex such as `(?i)\b([A-Z]{1,5})(?:\.[A-Z]{1,2})?\b` to capture common ticker formats, iterate over lines, and collect matches while ignoring duplicates. |

### 2. Normalize and validate extracted tickers against a known asset‑type whitelist (e.g., equities, ETFs, futures).

| Category | Details |
| --- | --- |
| **Reason** | Raw text may contain non‑ticker words or malformed symbols that would cause downstream API errors. |
| **Impact** | Filters out invalid entries, reducing unnecessary network calls and improving overall data quality. |
| **Complexity** | LOW |
| **Method** | Maintain a set of allowed prefix/suffix patterns (e.g., no spaces, optional suffix like .X), and discard any match that fails these rules; optionally cross‑check against a cached symbol lookup service. |

### 3. Return the unique list of tickers in the order they appear, preserving deterministic output for caching.

| Category | Details |
| --- | --- |
| **Reason** | Downstream processes may rely on consistent ordering for reproducibility and caching mechanisms. |
| **Impact** | Provides stable input to downstream nodes, enabling cache hits and easier debugging. |
| **Complexity** | LOW |
| **Method** | Use an OrderedDict or a simple list with a membership set to track insertion order while eliminating duplicates before returning. |
