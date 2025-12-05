# _compute_regime_features - Complete PRD Documentation

## Overview
PRDs for nodes in the '_compute_regime_features' module.

## Table of Contents

- [parse_csv_to_dataframe](#parse_csv_to_dataframe)

- [validate_required_columns](#validate_required_columns)

- [compute_vix_threshold](#compute_vix_threshold)

- [create_regime_labels](#create_regime_labels)

- [create_pmi_flags](#create_pmi_flags)

- [extract_date_list](#extract_date_list)

- [extract_regime_labels_list](#extract_regime_labels_list)

- [extract_pmi_flags_list](#extract_pmi_flags_list)



---

## parse_csv_to_dataframe

### Description
Parses a CSV‑formatted string and returns a serialized representation of the resulting pandas DataFrame.

### Implementation Plan

#### 1. Parse the CSV string into a pandas DataFrame using `pd.read_csv` with an in‑memory `StringIO` buffer.

| Category | Details |
| --- | --- |
| **Reason** | Provides a reliable, battle‑tested CSV parser that handles common delimiters, quoting, and type inference. |
| **Impact** | Downstream nodes receive a correctly structured DataFrame, enabling accurate calculations and feature engineering. |
| **Complexity** | LOW |
| **Method** | Import `pandas` and `io.StringIO`; call `pd.read_csv(StringIO(csv_string))`. |

#### 2. Validate the parsed DataFrame and raise informative errors for empty input or malformed CSV data.

| Category | Details |
| --- | --- |
| **Reason** | Prevents silent failures that would propagate obscure errors to later stages of the pipeline. |
| **Impact** | Improves overall pipeline robustness and makes debugging easier for users. |
| **Complexity** | MEDIUM |
| **Method** | Check if the DataFrame is empty or if required columns are missing; wrap parsing in a try/except block and raise `ValueError` with a clear message. |

#### 3. Serialize the DataFrame to a JSON string (using `df.to_json(orient="split")`) before returning it.

| Category | Details |
| --- | --- |
| **Reason** | The shim’s output type is defined as `STR`; serialization ensures compatibility with the typed contract while preserving the full tabular structure. |
| **Impact** | Allows downstream nodes to deserialize the string back into an identical DataFrame without loss of information. |
| **Complexity** | MEDIUM |
| **Method** | After successful parsing, call `df.to_json(orient="split")` and assign the result to the `output` field. |


---

## validate_required_columns

### Description
Ensures that a pandas DataFrame contains all specified required columns, raising an informative error if any are missing.

### Implementation Plan

#### 1. Check that all required column names exist in the DataFrame's columns.

| Category | Details |
| --- | --- |
| **Reason** | Missing columns would cause downstream processing to fail or produce incorrect results. |
| **Impact** | Prevents runtime errors later in the pipeline by catching schema mismatches early. |
| **Complexity** | LOW |
| **Method** | Convert df.columns to a set, compute the set difference with the required columns list, and store any missing names. |

#### 2. If any required columns are missing, raise a ValueError that lists the absent columns.

| Category | Details |
| --- | --- |
| **Reason** | Providing a descriptive exception helps developers quickly identify and fix data source issues. |
| **Impact** | Stops execution with a clear, actionable error message, improving debuggability and data quality assurance. |
| **Complexity** | LOW |
| **Method** | If the missing‑columns set is non‑empty, construct an error string like "Missing required columns: col1, col2" and raise ValueError with that message. |


---

## compute_vix_threshold

### Description
Calculates the 75th percentile value of a VIX time‑series string to use as the high‑volatility threshold.

### Implementation Plan

#### 1. Parse the input string into a numeric pandas Series, coercing non‑numeric entries to NaN and dropping them.

| Category | Details |
| --- | --- |
| **Reason** | The shim may receive raw CSV/JSON text with mixed types; ensuring a clean numeric Series prevents calculation errors. |
| **Impact** | Guarantees that subsequent percentile computation operates on valid data, reducing runtime exceptions. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv` with `StringIO` (if CSV) or `json.loads` (if JSON), then `pd.to_numeric(errors='coerce')` followed by `dropna()`. |

#### 2. Compute the 75th percentile of the cleaned Series using NumPy or pandas quantile functionality.

| Category | Details |
| --- | --- |
| **Reason** | The threshold definition for high‑volatility regimes is the 75th percentile of VIX values. |
| **Impact** | Provides a deterministic, data‑driven cutoff that downstream nodes can rely on for regime labeling. |
| **Complexity** | MEDIUM |
| **Method** | Call `series.quantile(0.75, interpolation='nearest')` and cast the result to a Python float. |

#### 3. Validate that the resulting threshold is a finite float; raise a descriptive error if not.

| Category | Details |
| --- | --- |
| **Reason** | Edge cases (e.g., empty series) would produce NaN, which would corrupt downstream logic. |
| **Impact** | Early failure with clear messaging aids debugging and ensures pipeline robustness. |
| **Complexity** | LOW |
| **Method** | Check `math.isfinite(threshold)`; if false, raise `ValueError` with context about the input series. |


---

## create_regime_labels

### Description
Assigns a regime label of "high_vol" or "low_vol" to each row in the input DataFrame based on whether the VIX value meets or exceeds the supplied threshold.

### Implementation Plan

#### 1. Parse the input CSV string into a pandas DataFrame and verify that a numeric 'VIX' column exists.

| Category | Details |
| --- | --- |
| **Reason** | The shim must operate on a structured data object and cannot proceed without the required VIX values. |
| **Impact** | Prevents runtime errors and ensures downstream logic receives a correctly shaped DataFrame. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(StringIO(dataframe))` to load the data; raise a descriptive ValueError if the 'VIX' column is missing or not numeric. |

#### 2. Create a new column named 'RegimeLabel' where each row receives "high_vol" if its VIX value is greater than or equal to the parsed `vix_threshold`, otherwise "low_vol".

| Category | Details |
| --- | --- |
| **Reason** | The core business rule for regime classification is based on the VIX percentile threshold. |
| **Impact** | Enables downstream nodes to segment the time series into high‑ and low‑volatility regimes for further analysis. |
| **Complexity** | MEDIUM |
| **Method** | Convert `vix_threshold` to a float, then apply `np.where(df['VIX'] >= vix_threshold, 'high_vol', 'low_vol')` to generate the new column efficiently. |

#### 3. Serialize the enriched DataFrame back to a CSV string and return it as the `output` field.

| Category | Details |
| --- | --- |
| **Reason** | The surrounding pipeline expects CSV‑formatted text for interoperability between nodes. |
| **Impact** | Provides a consistent data exchange format, allowing subsequent nodes to parse the result without additional conversion steps. |
| **Complexity** | LOW |
| **Method** | Call `df.to_csv(index=False)` and assign the resulting string to the `output` key in the shim's return payload. |


---

## create_pmi_flags

### Description
This shim function takes a DataFrame and adds a boolean 'PMI_Flag' column based on whether the 'PMI' column values are positive or negative.

### Implementation Plan

#### 1. Implement the core logic to create the 'PMI_Flag' column.

| Category | Details |
| --- | --- |
| **Reason** | This is the primary functionality of the shim, enabling downstream processes to easily identify positive and negative PMI values. |
| **Impact** | Adds a new column to the DataFrame, facilitating the extraction of PMI direction information efficiently. |
| **Complexity** | LOW |
| **Method** | Iterate through the 'PMI' column and create a new boolean column 'PMI_Flag'. Set 'True' if the 'PMI' value is greater than zero, and 'False' otherwise. Use a vectorized operation (e.g., pandas .apply() or numpy.where()) for performance. |

#### 2. Handle missing 'PMI' values gracefully.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring that the shim doesn't crash or produce incorrect results when encountering missing data is critical to the overall system's stability. |
| **Impact** | Prevents errors and ensures that missing PMI observations are handled appropriately (potentially flagged as 'False' or handled with a separate sentinel value). |
| **Complexity** | MEDIUM |
| **Method** | Check for NaN or None values in the 'PMI' column. Consider imputing with 0 for neutrality, or assign a default 'False' value to 'PMI_Flag'. Document the handling strategy clearly. |

#### 3. Return a string representation of the DataFrame with the new 'PMI_Flag' column.

| Category | Details |
| --- | --- |
| **Reason** | The integration of this function within the current framework requires the dataframe to be passed as string to avoid serialization issues. |
| **Impact** | Allows passing data to subsequent nodes that rely on downstream processing using the correct datatype. |
| **Complexity** | LOW |
| **Method** | Use `dataframe.to_csv()` and return the resulting csv string. |


---

## extract_date_list

### Description
Extracts an ordered list of ISO‑8601 date strings from the provided DataFrame.

### Implementation Plan

#### 1. Parse the input CSV string into a pandas DataFrame and verify a date column or index exists.

| Category | Details |
| --- | --- |
| **Reason** | The shim must operate on a concrete DataFrame; parsing ensures the raw string is usable and validation prevents downstream errors. |
| **Impact** | Guarantees that subsequent date extraction works on a correctly structured DataFrame, avoiding crashes in dependent nodes. |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv` with `StringIO`; if the DataFrame has a DateTimeIndex use `df.index`, otherwise look for a column named 'date' (case‑insensitive) and convert it with `pd.to_datetime`. |

#### 2. Sort the DataFrame chronologically and convert the date values to ISO‑8601 strings.

| Category | Details |
| --- | --- |
| **Reason** | Regime‑feature generation expects dates in ascending order and in a standardized string format. |
| **Impact** | Ensures deterministic ordering of outputs and compatibility with downstream models that consume ISO‑8601 dates. |
| **Complexity** | MEDIUM |
| **Method** | If dates are in a column, set it as the index with `df.set_index('date', inplace=True)`. Then call `df.sort_index(inplace=True)`. Extract the index with `df.index.strftime('%Y-%m-%d')` to produce a list of strings. |

#### 3. Return the list of formatted dates as the `output` field while preserving the original CSV string as `dataframe`.

| Category | Details |
| --- | --- |
| **Reason** | The shim’s contract requires both the derived list and the unchanged input for possible re‑use. |
| **Impact** | Provides the necessary output for the `ComputeRegimeFeatures` node and retains input provenance for debugging or caching. |
| **Complexity** | LOW |
| **Method** | Assign the list to a variable `dates_list` and construct the return dictionary `{ 'output': dates_list, 'dataframe': dataframe }` (or the appropriate Pydantic model wrapper). |


---

## extract_regime_labels_list

### Description
Extracts the ordered list of regime labels from a CSV‑encoded DataFrame string.

### Implementation Plan

#### 1. Parse the input CSV string into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The shim receives raw CSV text; converting it to a structured DataFrame enables column‑wise operations. |
| **Impact** | Provides a reliable in‑memory representation for subsequent extraction steps and validates CSV integrity. |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(dataframe))` within a try/except block to catch parsing errors and raise a clear exception if the CSV is malformed. |

#### 2. Validate that the `regime_label` column exists and extract its values in row order.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring the required column prevents downstream key errors and guarantees the output aligns with dates generated earlier. |
| **Impact** | Returns a deterministic List[str] that downstream nodes (e.g., `ComputeRegimeFeaturesOutput`) can rely on for correct mapping to dates. |
| **Complexity** | LOW |
| **Method** | Check `'regime_label' in df.columns`; if missing, raise a `ValueError`. Then obtain `df['regime_label'].astype(str).tolist()` to produce the output list. |


---

## extract_pmi_flags_list

### Description
Extracts an ordered list of boolean PMI direction flags (true for positive PMI, false for negative PMI) from a CSV‑formatted dataframe string.

### Implementation Plan

#### 1. Parse the CSV string into a pandas DataFrame and verify that a 'PMI' column exists.

| Category | Details |
| --- | --- |
| **Reason** | The shim operates on tabular data; converting the string to a DataFrame enables column‑wise operations and ensures the required input is present. |
| **Impact** | Prevents runtime errors downstream by guaranteeing the presence and correct type of the PMI data before extraction. |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` together with `pandas.read_csv`; raise a descriptive ValueError if `'PMI' not in df.columns`. |

#### 2. Create a boolean list where each entry is `True` if the corresponding PMI value is greater than zero, otherwise `False`, preserving the original row order.

| Category | Details |
| --- | --- |
| **Reason** | The downstream model expects a List[bool] reflecting the sign of PMI for each date in the same order as other output lists. |
| **Impact** | Provides the exact format required by `ComputeRegimeFeaturesOutput.pmi_flags`, enabling correct regime feature computation. |
| **Complexity** | MEDIUM |
| **Method** | Compute `flags = (df['PMI'] > 0).astype(bool).tolist()`; ensure any missing or non‑numeric values are handled (e.g., treat NaN as `False` or raise an error based on business rules). |
