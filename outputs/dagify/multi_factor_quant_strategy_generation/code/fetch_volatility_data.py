from ._fetch_volatility_data.parse_implied_vol_source import parse_implied_vol_source
from ._fetch_volatility_data.fetch_primary_asset_prices import fetch_primary_asset_prices
from ._fetch_volatility_data.calculate_realized_volatility import calculate_realized_volatility
from ._fetch_volatility_data.fetch_implied_volatility_data import fetch_implied_volatility_data
from ._fetch_volatility_data.merge_volatility_data import merge_volatility_data
from ._fetch_volatility_data.validate_volatility_data import validate_volatility_data
from ._fetch_volatility_data.extract_dates_list import extract_dates_list
from ._fetch_volatility_data.extract_realized_vol_list import extract_realized_vol_list
from ._fetch_volatility_data.extract_implied_vol_list import extract_implied_vol_list
from ._fetch_volatility_data.log_volatility_data_summary import log_volatility_data_summary

from pydantic import BaseModel, Field
from typing import List


# -- PRD --
# 1. BULLET: Parse the output of the parent node **list_data_sources** to extract the
#   provider name, dataset type, and update frequency for any
#   implied‑volatility index (e.g., CBOE VIX, Bloomberg IVOL) that matches
#   the primary asset.
#   Reason: The volatility node must know which external feed supplies the implied
#           volatility series; parsing ensures we reference the correct
#           ticker/provider without hard‑coding.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Read the `data_sources` list, apply a regex pattern like
#           `(?i)implied.*volatility.*: (.+?),` to capture the provider and
#           symbol, store as `implied_vol_source`.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Fetch the primary asset’s daily closing price series using the same endpoint
#   and parameters that **fetch_price_data** used (to guarantee identical
#   date range and calendar).
#   Reason: Realized volatility is derived from price returns; using the exact same
#           series guarantees alignment with other feature tables
#           downstream.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Issue an HTTP GET/POST request to the data vendor API (e.g., Bloomberg,
#           Refinitiv) with parameters: ticker = primary asset, fields =
#           Close, frequency = daily, start_date = earliest date from
#           `list_data_sources`, end_date = latest date. Cache the response
#           as a DataFrame `price_df` with columns `Date` and `Close`.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Calculate daily log returns: `r_t = ln(Close_t / Close_{t-1})` and then
#   compute a 30‑day rolling standard deviation of these returns to obtain
#   the realized volatility series.
#   Reason: A 30‑day rolling standard deviation of returns is a standard proxy for
#           realized volatility and matches the prompt specification.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Using pandas: `price_df['log_return'] = np.log(price_df['Close'] /
#           price_df['Close'].shift(1))`; `price_df['realized_vol'] =
#           price_df['log_return'].rolling(window=30).std()`; drop the
#           first 30 rows where the window is incomplete.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Retrieve the implied‑volatility index series from the provider identified in
#   step 1 for the exact same date range as `price_df`.
#   Reason: Implied volatility must be aligned day‑for‑day with realized volatility to
#           be used later in feature engineering and model training.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Construct a second API request to the implied‑vol provider (e.g., `GET
#           /v1/indices/{symbol}?frequency=daily&start={start}&end={end}`),
#           parse JSON/CSV response into a DataFrame `implied_df` with
#           columns `Date` and `ImpliedVol`. Ensure timezone normalization
#           to UTC.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Merge `price_df` (containing `realized_vol`) and `implied_df` on the `Date`
#   column using an inner join to keep only dates where both series are
#   present.
#   Reason: A clean inner join guarantees no missing values downstream, simplifying the
#           cleaning step in `align_and_clean_data`.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: `merged_df = pd.merge(price_df[['Date','realized_vol']],
#           implied_df[['Date','ImpliedVol']], on='Date', how='inner')`.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Validate the merged series: confirm that `merged_df` contains no NaNs, that
#   the length matches the expected calendar (derived from the longest parent
#   series), and that all dates are in ISO‑8601 (`YYYY-MM-DD`) format.
#   Reason: Early validation prevents downstream failures in `align_and_clean_data` and
#           ensures data integrity.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: If any NaNs are found, raise an exception with a descriptive error;
#           otherwise, convert the `Date` column to string format with
#           `merged_df['Date'] =
#           merged_df['Date'].dt.strftime('%Y-%m-%d')`.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Populate the output fields: `dates` = list(merged_df['Date']), `realized_vol`
#   = list(merged_df['realized_vol'].astype(float)), `implied_vol` =
#   list(merged_df['ImpliedVol'].astype(float)).
#   Reason: Mapping the DataFrame columns to the typed output structure satisfies the
#           contract of the node.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Use Python list comprehension or `to_list()` method; ensure float
#           conversion to match `PrimitiveType.LIST_FLOAT`.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Log a concise summary (e.g., number of rows, date range, source identifiers)
#   to a standard logging facility for auditability.
#   Reason: Traceability is essential for production pipelines and for debugging any
#           mismatches later in the DAG.
#   Impact: LOW
#   Complexity: LOW
#   Method: `logger.info(f"Fetched volatility data: {len(dates)} rows, from {dates[0]}
#           to {dates[-1]}, source={implied_vol_source}")`.
# -- END PRD --



class ListDataSourcesOutput(BaseModel):
    """Pydantic model for list_data_sources node outputs."""
    data_sources: str = Field(..., description="Plain list of data source descriptions, each including the dataset type, provider name, and update frequency (e.g., "Price History: Bloomberg, daily").")


class FetchVolatilityDataOutput(BaseModel):
    """Pydantic model for fetch_volatility_data node outputs."""
    dates: List[str] = Field(..., description="List of dates for which volatility data is provided, formatted as YYYY-MM-DD.")
    realized_vol: List[float] = Field(..., description="30\u2011day rolling realized volatility values corresponding to each date.")
    implied_vol: List[float] = Field(..., description="Implied volatility index values for the primary asset corresponding to each date.")


def fetch_volatility_data(list_data_sources_input: ListDataSourcesOutput, **kwargs) -> FetchVolatilityDataOutput:
    """Retrieve realized and implied volatility metrics needed for forecasting.

    Args:
        list_data_sources_input: Input from the 'list_data_sources' node.
        **kwargs: Additional keyword arguments.

    Returns:
        FetchVolatilityDataOutput: Object containing outputs for this node.
    """
    # Parse data sources to extract implied volatility provider information
    implied_vol_source: str = parse_implied_vol_source(data_sources=list_data_sources_input.data_sources)
    
    # Fetch primary asset price data using same parameters as fetch_price_data
    price_df = fetch_primary_asset_prices(data_sources=list_data_sources_input.data_sources)
    
    # Calculate daily log returns and 30-day rolling realized volatility
    realized_vol_df = calculate_realized_volatility(price_df=price_df, window=30)
    
    # Retrieve implied volatility index series from identified provider
    implied_vol_df = fetch_implied_volatility_data(
        provider_source=implied_vol_source,
        start_date=realized_vol_df['Date'].min(),
        end_date=realized_vol_df['Date'].max()
    )
    
    # Merge realized and implied volatility data on date
    merged_df = merge_volatility_data(
        realized_df=realized_vol_df,
        implied_df=implied_vol_df
    )
    
    # Validate merged series for completeness and data integrity
    validated_df = validate_volatility_data(merged_df=merged_df)
    
    # Extract output lists from validated DataFrame
    dates_list: List[str] = extract_dates_list(df=validated_df)
    realized_vol_list: List[float] = extract_realized_vol_list(df=validated_df)
    implied_vol_list: List[float] = extract_implied_vol_list(df=validated_df)
    
    # Log summary for auditability
    log_volatility_data_summary(
        dates=dates_list,
        source=implied_vol_source,
        row_count=len(dates_list)
    )
    
    return FetchVolatilityDataOutput(
        dates=dates_list,
        realized_vol=realized_vol_list,
        implied_vol=implied_vol_list
    )