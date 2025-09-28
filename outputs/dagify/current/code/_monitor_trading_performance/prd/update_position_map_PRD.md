# update_position_map PRD

## Description
Updates the position map with a new trade, detects closures, and returns details about the update.


## Implementation Plan

### 1. Validate and normalize input arguments, converting price and quantity to float and ensuring side is either 'buy' or 'sell'.

| Category | Details |
| --- | --- |
| **Reason** | Correct data types are essential for arithmetic and comparison operations during position updates. |
| **Impact** | Prevents runtime errors and ensures accurate position tracking. |
| **Complexity** | LOW |
| **Method** | Use Python's `float()` for conversion and a simple set check for side; raise `ValueError` on failure. |

### 2. Implement position update logic: add quantity for 'buy', subtract for 'sell'; detect when the cumulative quantity for an instrument reaches zero to flag a closed position.

| Category | Details |
| --- | --- |
| **Reason** | Core functionality of maintaining an accurate ledger of open positions. |
| **Impact** | Provides the basis for calculating P&L and updating equity curves downstream. |
| **Complexity** | MEDIUM |
| **Method** | Maintain `position_map` as a dict of `{instrument: {'side': str, 'quantity': float, 'entry_price': float}}`; update or close entries accordingly and return a structured result. |

### 3. Return a comprehensive result dictionary with flags indicating closure, the entry price, original side, and closed quantity for downstream consumption.

| Category | Details |
| --- | --- |
| **Reason** | Standardizes the output format so other nodes can reliably parse the update outcome. |
| **Impact** | Enables consistent downstream processing and simplifies debugging. |
| **Complexity** | LOW |
| **Method** | Build a `dict` with the required keys and serialize it as a JSON-compatible string if necessary. |
