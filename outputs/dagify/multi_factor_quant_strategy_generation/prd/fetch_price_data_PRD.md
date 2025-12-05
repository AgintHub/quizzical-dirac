# fetch_price_data PRD

## Description
Download historical price series for the primary asset and any directly traded instruments.


## Implementation Plan

### 1. Parse the `list_data_sources` output to locate the entry that describes the primary asset's price history (e.g., "Price History: Bloomberg, daily, ticker=SPY").

| Category | Details |
| --- | --- |
| **Reason** | The downstream fetch must know which provider, ticker, and frequency to query; the parent node only supplies a plain list of strings. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use regex pattern matching to extract provider name, ticker symbol, and frequency. Store these in variables `provider`, `ticker`, `frequency`. Validate that `frequency` equals "daily"; if not, raise a configuration error. |

### 2. Map the identified provider to a concrete data‑access library or API client (e.g., Bloomberg → `blpapi`, Yahoo Finance → `yfinance`, Alpha Vantage → HTTP REST).

| Category | Details |
| --- | --- |
| **Reason** | Different providers have distinct authentication, rate‑limit, and data‑format requirements; abstracting this mapping enables a modular fetch implementation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a provider‑lookup dictionary. For each supported provider, define: authentication method, request function signature, and any required third‑party SDK. If the provider is unsupported, fallback to a generic CSV download if a URL is supplied. |

### 3. Compute the exact 10‑year date window: `end_date = yesterday (UTC)`, `start_date = end_date - 10 years`. Adjust for market calendar (exclude weekends/holidays).

| Category | Details |
| --- | --- |
| **Reason** | The prompt explicitly requests the last 10 years of daily data; precise bounds avoid off‑by‑one errors and ensure alignment with downstream calendar merging. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use Python's `pandas.tseries.offsets.DateOffset(years=10)` or `datetime` arithmetic. Generate a list of trading days via `pandas_market_calendars` for the primary asset's exchange. |

### 4. Issue the data request to the selected provider using the determined `ticker`, `start_date`, `end_date`, and daily frequency. Implement pagination or batch requests if the provider limits the number of rows per call.

| Category | Details |
| --- | --- |
| **Reason** | Historical OHLCV data for 10 years can exceed API limits; handling pagination guarantees complete retrieval. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For Bloomberg: use `blpapi` with `HistoricalDataRequest`. For Yahoo Finance: call `yfinance.download(ticker, start=start_date, end=end_date, interval='1d')`. Loop until all dates are received, respecting rate‑limit sleep intervals (e.g., 1‑second pause). |

### 5. Normalize the raw response into a canonical DataFrame with columns exactly named `Date`, `Open`, `High`, `Low`, `Close`, `Volume`. Convert all numeric columns to `float` (price) and `int` (volume). Ensure `Date` is a `datetime64[ns]` object.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect clean, consistently typed arrays; mismatched column names or dtypes cause merge failures later. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Rename columns using a mapping dict, e.g., `{'Adj Close': 'Close'}` if present. Apply `astype(float)` to price columns and `astype(int)` to volume. Use `pd.to_datetime` for dates, then `dt.strftime('%Y-%m-%d')` for string output. |

### 6. Handle missing trading days (e.g., holidays) by ensuring the DataFrame contains a row for every business day in the date window. If a date is missing, insert a row with `NaN` values for OHLCV.

| Category | Details |
| --- | --- |
| **Reason** | Later alignment (`align_and_clean_data`) assumes a common calendar; explicit missing rows allow forward‑fill logic to operate correctly. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Create a full date range `pd.date_range(start_date, end_date, freq='B')`. Reindex the DataFrame to this index, using `np.nan` for missing values. |

### 7. Sort the DataFrame by `Date` ascending and drop any rows that still contain `NaN` after reindexing if the business rule is to exclude incomplete days.

| Category | Details |
| --- | --- |
| **Reason** | Consistent chronological order is required for time‑series feature engineering; eliminating rows with missing data simplifies later processing. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `df.sort_values('Date', inplace=True)`. Optionally `df.dropna(inplace=True)` if policy dictates; otherwise keep NaNs for forward‑fill later. |

### 8. Extract the columns into the output list structures preserving the chronological order: `dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()`, `opens = df['Open'].tolist()`, etc.

| Category | Details |
| --- | --- |
| **Reason** | The node's output schema demands separate lists rather than a tabular object; converting now avoids extra transformations downstream. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use pandas `.tolist()` on each column. Cast `volumes` explicitly to `int` with `df['Volume'].astype(int).tolist()`. |

### 9. Validate the final payload: check that `len(dates) == len(opens) == …` and that the count matches the expected number of trading days (~252 * 10 = 2520). Log a warning if the count deviates by more than 2%.

| Category | Details |
| --- | --- |
| **Reason** | Early detection of incomplete fetch prevents silent data quality issues that would cascade into model training. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Compute `expected_days = len(pd.date_range(start_date, end_date, freq='B'))`. Compare lengths; if `abs(len(dates) - expected_days) / expected_days > 0.02`, emit a logger warning. |

### 10. Record provenance metadata (provider name, ticker, request timestamps, any adjustments made) into a structured log file for auditability.

| Category | Details |
| --- | --- |
| **Reason** | Traceability is essential for compliance and reproducibility of the quant pipeline. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Append a JSON entry to `data_fetch_log.json` with fields `provider`, `ticker`, `start_date`, `end_date`, `row_count`, `adjustments`. |

### 11. Return the six output fields (`dates`, `opens`, `highs`, `lows`, `closes`, `volumes`) as defined in the node's output structure.

| Category | Details |
| --- | --- |
| **Reason** | Completes the node's contract, enabling downstream nodes to consume the data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Package the lists into a dictionary matching the schema and output via the execution framework. |
