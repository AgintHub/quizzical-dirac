# get_primary_asset_date_range PRD

## Description
Returns a dictionary with the ISO‑8601 start_date and end_date of the primary asset based on its metadata, or empty values if unavailable.


## Implementation Plan

### 1. Read primary‑asset metadata from the configured source (e.g., a database, API, or configuration file).

| Category | Details |
| --- | --- |
| **Reason** | The date range must reflect the actual coverage of the primary asset's historical data. |
| **Impact** | Ensures downstream nodes (like fetch_cross_asset_data) request data only for dates that exist for the primary asset, preventing empty or misaligned time series. |
| **Complexity** | MEDIUM |
| **Method** | Implement a lightweight accessor that queries the metadata store (SQL SELECT, REST GET, or file read) and extracts the 'start_date' and 'end_date' fields, parsing them into ISO‑8601 format. |

### 2. Validate and normalize the extracted dates, defaulting to empty strings when metadata is missing or malformed.

| Category | Details |
| --- | --- |
| **Reason** | Robustness: downstream logic expects string values and will skip slicing if dates are falsy. |
| **Impact** | Prevents runtime errors in date parsing and allows the workflow to continue gracefully when the primary asset lacks date information. |
| **Complexity** | LOW |
| **Method** | Use Python's datetime.strptime with a try/except block; on failure set date variables to "" and log a warning. |

### 3. Serialize the result as a JSON string matching the declared output type.

| Category | Details |
| --- | --- |
| **Reason** | The node contract specifies a PrimitiveType.STR output, so callers must be able to deserialize the dict. |
| **Impact** | Provides a consistent, language‑agnostic payload for any downstream node or external system. |
| **Complexity** | LOW |
| **Method** | Return json.dumps({"start_date": start_date, "end_date": end_date}) from the shim function. |
