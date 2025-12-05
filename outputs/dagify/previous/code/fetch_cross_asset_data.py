# -- PRD --
# 1. BULLET: Parse the `data_sources` list produced by `list_data_sources` to extract all
#   secondary‑asset entries (sector ETFs, commodities, FX pairs) while
#   filtering out the primary tradable asset.
#   Reason: The parent node provides a plain‑text enumeration; extracting only
#           cross‑asset identifiers ensures we request the correct tickers
#           for correlation features.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use regular expressions or simple string splitting to locate patterns like
#           "Ticker: XYZ"; store results in a Python list
#           `cross_asset_tickers`. Log any ambiguous entries for manual
#           review.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Determine the required date range (start_date, end_date) by querying the
#   primary asset's price data cache (produced later by `fetch_price_data`).
#   If the primary data is not yet available, store a placeholder and defer
#   exact range alignment to the `align_and_clean_data` step.
#   Reason: The prompt explicitly demands the same calendar as the primary asset;
#           aligning here avoids later mismatches.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Attempt to read a shared metadata file `primary_price_meta.json` containing
#           `first_date` and `last_date`. If missing, set `start_date =
#           None` and `end_date = None`; later `align_and_clean_data` will
#           intersect calendars.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: For each ticker in `cross_asset_tickers`, query a reliable market data API
#   (e.g., Bloomberg Terminal, Refinitiv, or free fallback like Yahoo Finance
#   via `yfinance` library) to download daily **closing** prices.
#   Reason: Uniform source selection guarantees data quality and consistent frequency
#           (daily).
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Implement a wrapper function `download_close(ticker, start, end)` that: -
#           Uses the chosen provider's SDK or REST endpoint. - Sends
#           start/end parameters if known; otherwise requests full history.
#           - Retries up to 3 times with exponential back‑off on HTTP
#           errors. - Logs request IDs and timestamps for auditability. -
#           Returns a `pandas.Series` indexed by `Date`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Collect all Series objects into a dictionary `{ticker: series}` and perform
#   an outer join on the `Date` index to produce a unified `DataFrame`
#   `cross_df` where each column is a ticker’s closing price.
#   Reason: An outer join preserves all dates present in any series, allowing later
#           forward‑fill or drop‑na handling in `align_and_clean_data`.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use `pd.concat(series_dict, axis=1, join='outer')`. Ensure the index is of
#           dtype `datetime64[ns]` and sorted ascending.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: If `start_date` and `end_date` were resolved earlier, slice `cross_df` to
#   `[start_date, end_date]`; otherwise retain the full outer‑joined range
#   and let downstream nodes truncate.
#   Reason: Guarantees that when dates are known, the output matches the primary asset
#           calendar; otherwise defers alignment.
#   Impact: LOW
#   Complexity: LOW
#   Method: Apply `cross_df.loc[start_date:end_date]` when dates are not None.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Convert `cross_df` to a CSV‑formatted string `csv_data` using
#   `cross_df.to_csv(index=True, date_format='%Y-%m-%d')` and capture the
#   list of column names (excluding the index) as `asset_names`.
#   Reason: The output schema expects a CSV string and an explicit list of asset
#           identifiers.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Store `csv_data = cross_df.to_csv()`; `asset_names =
#           list(cross_df.columns)`.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Derive `start_date`, `end_date`, and `row_count` from the final DataFrame:
#   `start_date = cross_df.index.min().strftime('%Y-%m-%d')`, `end_date =
#   cross_df.index.max().strftime('%Y-%m-%d')`, `row_count =
#   cross_df.shape[0]`.
#   Reason: These scalar metadata fields are required for downstream validation and
#           reporting.
#   Impact: LOW
#   Complexity: LOW
#   Method: Use pandas `min`, `max`, and `shape` attributes; cast to Python native
#           types.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Persist the CSV string and metadata to a temporary storage location (e.g.,
#   `/tmp/cross_asset_data.csv`) and register the file path in a workflow
#   context dictionary for downstream nodes that may need to read the raw
#   file.
#   Reason: Avoids passing large strings through in‑memory structures and enables
#           `align_and_clean_data` to stream the file efficiently.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Open file in write mode, write `csv_data`; update
#           `workflow_context['cross_asset_path'] =
#           '/tmp/cross_asset_data.csv'`.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Return the five output fields (`csv_data`, `asset_names`, `start_date`,
#   `end_date`, `row_count`) as a JSON‑compatible dictionary to the
#   orchestration engine.
#   Reason: Conforms to the node's declared `output_structure` and enables downstream
#           nodes to consume the data directly.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Construct `output = { 'csv_data': csv_data, 'asset_names': asset_names,
#           'start_date': start_date, 'end_date': end_date, 'row_count':
#           row_count }` and emit via the platform's
#           `return_output(output)` call.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class ListDataSourcesOutput(BaseModel):
    """Pydantic model for list_data_sources node outputs."""
    data_sources: str = Field(..., description="Plain list of data source descriptions, each including the dataset type, provider name, and update frequency (e.g., \"Price History: Bloomberg, daily\").")


class FetchCrossAssetDataOutput(BaseModel):
    """Pydantic model for fetch_cross_asset_data node outputs."""
    csv_data: str = Field(..., description="CSV\u2011formatted string of the resulting table, with a \"Date\" column followed by a column for each cross\u2011asset's closing price.")
    asset_names: List[str] = Field(..., description="List of cross\u2011asset identifiers (e.g., ticker symbols) that were fetched.")
    start_date: str = Field(..., description="ISO\u20118601 formatted first date of the returned series.")
    end_date: str = Field(..., description="ISO\u20118601 formatted last date of the returned series.")
    row_count: int = Field(..., description="Number of rows (dates) in the returned table.")


def fetch_cross_asset_data(list_data_sources_input: ListDataSourcesOutput, **kwargs) -> FetchCrossAssetDataOutput:
    """Download historical price series for secondary assets used for correlation signals.

    Args:
        list_data_sources_input: Input from the 'list_data_sources' node.
        **kwargs: Additional keyword arguments.

    Returns:
        FetchCrossAssetDataOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return FetchCrossAssetDataOutput(
        csv_data="",
        asset_names=[],
        start_date="",
        end_date="",
        row_count=0,
    )