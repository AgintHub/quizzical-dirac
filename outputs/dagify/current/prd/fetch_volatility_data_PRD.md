# fetch_volatility_data PRD

## Description
Retrieve realized and implied volatility metrics needed for forecasting.


## Implementation Plan

### 1. Parse the output of the parent node **list_data_sources** to extract the provider name, dataset type, and update frequency for any implied‑volatility index (e.g., CBOE VIX, Bloomberg IVOL) that matches the primary asset.

| Category | Details |
| --- | --- |
| **Reason** | The volatility node must know which external feed supplies the implied volatility series; parsing ensures we reference the correct ticker/provider without hard‑coding. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the `data_sources` list, apply a regex pattern like `(?i)implied.*volatility.*: (.+?),` to capture the provider and symbol, store as `implied_vol_source`. |

### 2. Fetch the primary asset’s daily closing price series using the same endpoint and parameters that **fetch_price_data** used (to guarantee identical date range and calendar).

| Category | Details |
| --- | --- |
| **Reason** | Realized volatility is derived from price returns; using the exact same series guarantees alignment with other feature tables downstream. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Issue an HTTP GET/POST request to the data vendor API (e.g., Bloomberg, Refinitiv) with parameters: ticker = primary asset, fields = Close, frequency = daily, start_date = earliest date from `list_data_sources`, end_date = latest date. Cache the response as a DataFrame `price_df` with columns `Date` and `Close`. |

### 3. Calculate daily log returns: `r_t = ln(Close_t / Close_{t-1})` and then compute a 30‑day rolling standard deviation of these returns to obtain the realized volatility series.

| Category | Details |
| --- | --- |
| **Reason** | A 30‑day rolling standard deviation of returns is a standard proxy for realized volatility and matches the prompt specification. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Using pandas: `price_df['log_return'] = np.log(price_df['Close'] / price_df['Close'].shift(1))`; `price_df['realized_vol'] = price_df['log_return'].rolling(window=30).std()`; drop the first 30 rows where the window is incomplete. |

### 4. Retrieve the implied‑volatility index series from the provider identified in step 1 for the exact same date range as `price_df`.

| Category | Details |
| --- | --- |
| **Reason** | Implied volatility must be aligned day‑for‑day with realized volatility to be used later in feature engineering and model training. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Construct a second API request to the implied‑vol provider (e.g., `GET /v1/indices/{symbol}?frequency=daily&start={start}&end={end}`), parse JSON/CSV response into a DataFrame `implied_df` with columns `Date` and `ImpliedVol`. Ensure timezone normalization to UTC. |

### 5. Merge `price_df` (containing `realized_vol`) and `implied_df` on the `Date` column using an inner join to keep only dates where both series are present.

| Category | Details |
| --- | --- |
| **Reason** | A clean inner join guarantees no missing values downstream, simplifying the cleaning step in `align_and_clean_data`. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `merged_df = pd.merge(price_df[['Date','realized_vol']], implied_df[['Date','ImpliedVol']], on='Date', how='inner')`. |

### 6. Validate the merged series: confirm that `merged_df` contains no NaNs, that the length matches the expected calendar (derived from the longest parent series), and that all dates are in ISO‑8601 (`YYYY-MM-DD`) format.

| Category | Details |
| --- | --- |
| **Reason** | Early validation prevents downstream failures in `align_and_clean_data` and ensures data integrity. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If any NaNs are found, raise an exception with a descriptive error; otherwise, convert the `Date` column to string format with `merged_df['Date'] = merged_df['Date'].dt.strftime('%Y-%m-%d')`. |

### 7. Populate the output fields: `dates` = list(merged_df['Date']), `realized_vol` = list(merged_df['realized_vol'].astype(float)), `implied_vol` = list(merged_df['ImpliedVol'].astype(float)).

| Category | Details |
| --- | --- |
| **Reason** | Mapping the DataFrame columns to the typed output structure satisfies the contract of the node. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use Python list comprehension or `to_list()` method; ensure float conversion to match `PrimitiveType.LIST_FLOAT`. |

### 8. Log a concise summary (e.g., number of rows, date range, source identifiers) to a standard logging facility for auditability.

| Category | Details |
| --- | --- |
| **Reason** | Traceability is essential for production pipelines and for debugging any mismatches later in the DAG. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | `logger.info(f"Fetched volatility data: {len(dates)} rows, from {dates[0]} to {dates[-1]}, source={implied_vol_source}")`. |
