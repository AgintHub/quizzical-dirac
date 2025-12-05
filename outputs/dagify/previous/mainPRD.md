# multi_factor_quant_strategy_generation - Complete PRD Documentation

## Overview
PRDs for nodes in the 'multi_factor_quant_strategy_generation' module.

## Table of Contents

- [align_and_clean_data](#align_and_clean_data)

- [analyze_feature_importance](#analyze_feature_importance)

- [assemble_feature_matrix](#assemble_feature_matrix)

- [compile_strategy_documentation](#compile_strategy_documentation)

- [compute_cross_asset_features](#compute_cross_asset_features)

- [compute_price_action_features](#compute_price_action_features)

- [compute_regime_features](#compute_regime_features)

- [compute_volatility_features](#compute_volatility_features)

- [create_monitoring_plan](#create_monitoring_plan)

- [define_hyperparameter_grid](#define_hyperparameter_grid)

- [define_strategy_objectives](#define_strategy_objectives)

- [design_risk_controls](#design_risk_controls)

- [draft_execution_logic](#draft_execution_logic)

- [evaluate_models](#evaluate_models)

- [fetch_cross_asset_data](#fetch_cross_asset_data)

- [fetch_price_data](#fetch_price_data)

- [fetch_regime_indicator_data](#fetch_regime_indicator_data)

- [fetch_volatility_data](#fetch_volatility_data)

- [final_deliverables_package](#final_deliverables_package)

- [list_data_sources](#list_data_sources)

- [run_backtest](#run_backtest)

- [select_best_model](#select_best_model)

- [setup_backtest_environment](#setup_backtest_environment)

- [specify_model_architecture](#specify_model_architecture)

- [split_dataset](#split_dataset)

- [summarize_backtest_results](#summarize_backtest_results)

- [train_models](#train_models)



---

## align_and_clean_data

### Description
Synchronize all fetched datasets to a common calendar, handle missing values, and store a clean master dataset.

### Implementation Plan

#### 1. Load each parent node's output into a Pandas DataFrame with Date parsed as `datetime64[ns]` and set as the index.

| Category | Details |
| --- | --- |
| **Reason** | Uniform datetime indexing guarantees a deterministic merge order and simplifies calendar alignment. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.DataFrame` constructors from the primitive lists; e.g., for fetch_price_data build columns Date, Open, High, Low, Close, Volume. Apply `pd.to_datetime(df['Date'])` and `df.set_index('Date', inplace=True)` for all five DataFrames. |

#### 2. Validate that all five DataFrames share the same timezone (UTC) and that there are no duplicate Date entries within any table.

| Category | Details |
| --- | --- |
| **Reason** | Duplicate dates or timezone mismatches cause ambiguous merges and hidden NaNs. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `df.index.duplicated().any()` and raise an exception if true; enforce `df.index = df.index.tz_localize('UTC')` when tz‑naive. |

#### 3. Perform an outer join on the Date index across all five DataFrames using `pd.merge(..., how='outer')` sequentially or `pd.concat(..., axis=1, join='outer')`.

| Category | Details |
| --- | --- |
| **Reason** | Outer join preserves the full universe of dates from any source, creating the superset calendar required for downstream feature engineering. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Start with `master_df = price_df`; iterate over `[cross_asset_df, regime_df, volatility_df]` and execute `master_df = master_df.join(other_df, how='outer')`. Preserve original column names to avoid collisions. |

#### 4. Create a boolean flag `missing_before_fill = master_df.isna().any().any()` to record whether any NaNs exist prior to imputation.

| Category | Details |
| --- | --- |
| **Reason** | The output field `missing_values_filled` must reflect whether forward‑fill actually occurred. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Store the result; after forward‑fill, compute `missing_after_fill = master_df.isna().any().any()` and set `missing_values_filled = missing_before_fill and not missing_after_fill`. |

#### 5. Apply forward‑fill (`ffill`) on the merged DataFrame, then backward‑fill (`bfill`) as a safety net for leading NaNs.

| Category | Details |
| --- | --- |
| **Reason** | Forward‑fill respects causality (using the most recent known value), while a trailing `bfill` ensures the first rows are not dropped unnecessarily. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Execute `master_df.ffill(inplace=True); master_df.bfill(inplace=True)`. |

#### 6. Drop any remaining rows that still contain NaN values after imputation using `master_df.dropna(inplace=True)`.

| Category | Details |
| --- | --- |
| **Reason** | Downstream models cannot handle missing entries; dropping ensures a clean dataset. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Call `master_df.dropna(inplace=True)` and verify `master_df.empty` is false; otherwise raise an alert. |

#### 7. Capture `row_count = master_df.shape[0]` and `column_names = list(master_df.columns)` for output metadata.

| Category | Details |
| --- | --- |
| **Reason** | These fields are required by the downstream schema and useful for sanity‑checking the cleaning step. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Assign variables directly after the final drop operation. |

#### 8. Convert the cleaned DataFrame to a CSV‑formatted string without the index (`index=False`) and store as `cleaned_data_csv`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream nodes expect CSV text; omitting the index avoids an extra unnamed column. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use `cleaned_data_csv = master_df.reset_index().to_csv(index=False, line_terminator='\n')`. |

#### 9. Assemble the final output dictionary matching the declared `output_structure` and return it to the workflow engine.

| Category | Details |
| --- | --- |
| **Reason** | Consistent typing and field naming allow downstream nodes to consume the result without conversion errors. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return `{ 'cleaned_data_csv': cleaned_data_csv, 'row_count': int(row_count), 'column_names': column_names, 'missing_values_filled': bool(missing_values_filled) }`. |


---

## analyze_feature_importance

### Description
Compute and report the importance of each feature for the selected model.

### Implementation Plan

#### 1. Retrieve the best model identifier from the output of the `select_best_model` node.

| Category | Details |
| --- | --- |
| **Reason** | The `model_id` is required to load the selected model for feature importance analysis. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Access the `best_model_identifier` field from the `select_best_model` node's output. |

#### 2. Load the feature matrix from the CSV string provided in the `feature_matrix_csv` field of the `assemble_feature_matrix` node's output.

| Category | Details |
| --- | --- |
| **Reason** | The model needs the feature data used for training to determine feature importances. Loading from CSV ensures consistent data format. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a CSV parsing library (e.g., pandas in Python) to load the `feature_matrix_csv` into a dataframe. |

#### 3. Load the selected model based on the `model_id` retrieved earlier. Assume a model registry or loading function exists. If the model ID contains information about the model type, use that.

| Category | Details |
| --- | --- |
| **Reason** | The model needs to be loaded to calculate feature importances based on its internal structure or through permutation methods. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a model registry or loading function that maps `model_id` to a corresponding model object. Handle potential errors like model not found. |

#### 4. Determine feature importance ranking method. If the model is a tree-based model (e.g., Gradient Boosting), use 'gain' (mean decrease in impurity). If the model is linear/logistic regression, use coefficients as the importance score. If the above are not applicable, or if specified in configuration, use SHAP values.

| Category | Details |
| --- | --- |
| **Reason** | Different model types have different methods for determining feature importance. This step selects the appropriate method. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Implement a conditional logic to select the feature importance method based on the model type. Account for cases where feature importance is not available through direct model introspection. Allow overriding this choice using external config parameters. |

#### 5. Compute feature importances using the chosen method. For 'gain', extract the feature importances directly from the model. For SHAP values, use a SHAP explainer on a subset of the feature matrix.

| Category | Details |
| --- | --- |
| **Reason** | This is the core step where the feature importances are calculated. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Use model-specific methods to compute feature importances. For tree based models, use `model.feature_importances_`. For SHAP, instantiate a `shap.Explainer` object with the model (or model's prediction function) and compute SHAP values for a representative sample of the data. |

#### 6. Rank the features based on their importance scores in descending order.

| Category | Details |
| --- | --- |
| **Reason** | The ranked list provides the most relevant features at the top. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Sort the feature names based on the corresponding importance scores using a sorting algorithm (e.g., `sorted` function in Python with `reverse=True`). |

#### 7. Extract the sorted feature names and corresponding importance scores into separate lists.

| Category | Details |
| --- | --- |
| **Reason** | This prepares the data for the output structure. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Unzip the sorted list of tuples (feature name, importance score). |

#### 8. Populate the output structure with the `model_id`, sorted `feature_names`, `importance_scores`, and `ranking_method`.

| Category | Details |
| --- | --- |
| **Reason** | This provides the results in the required format. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Assign the calculated values to the corresponding fields in the output dictionary. |


---

## assemble_feature_matrix

### Description
Combine all individual feature tables into a single matrix aligned with the target variable.

### Implementation Plan

#### 1. Load the CSV payloads from each parent node (price_action, cross_asset, regime, volatility) into in‑memory data frames using a robust CSV parser that respects ISO‑8601 dates and quoted fields.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that all feature tables are correctly interpreted before any join operation; parsing errors are caught early. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use pandas.read_csv with `parse_dates=['Date']`, `dayfirst=False`, `dtype` inference disabled; wrap in try/except to capture malformed rows. |

#### 2. Standardize the Date column across all data frames to midnight UTC and set it as the index to guarantee exact alignment during the merge.

| Category | Details |
| --- | --- |
| **Reason** | Date inconsistencies (timezones, format variations) would cause mismatched joins and missing rows. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Apply `df['Date'] = pd.to_datetime(df['Date']).dt.normalize()` and then `df.set_index('Date', inplace=True)`. |

#### 3. Perform an inner join on the Date index across the four feature data frames to keep only dates present in every source, thereby guaranteeing a complete feature row for each observation.

| Category | Details |
| --- | --- |
| **Reason** | Target computation requires a complete set of predictors; dropping dates with missing features avoids NaNs later in modeling. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `merged = price_df.join([cross_df, regime_df, vol_df], how='inner')`. |

#### 4. Detect and resolve any duplicate column names that may arise from overlapping feature names (e.g., both price and volatility tables containing a column called `date`).

| Category | Details |
| --- | --- |
| **Reason** | Duplicate columns cause CSV export failures and ambiguous feature references in downstream models. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | After merging, inspect `merged.columns`. For any duplicates, rename using a prefix based on source table (e.g., `price_`, `vol_`). Implement a helper `unique_rename(columns, source_prefix)`. |

#### 5. Compute the target variable – next‑day simple return – using the cleaned primary asset closing price series that resides in the price_action feature table (column `close`).

| Category | Details |
| --- | --- |
| **Reason** | The model learns to predict this target; it must be aligned with the feature row date (i.e., return from t to t+1 assigned to row at date t). |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a series `next_day_return = price_df['close'].shift(-1) / price_df['close'] - 1`. Append as a new column `Target` to the merged data frame. Drop the final row where Target is NaN. |

#### 6. Re‑index the final merged data frame to ensure chronological order (oldest to newest) and reset the index to a regular `Date` column for CSV export.

| Category | Details |
| --- | --- |
| **Reason** | Ordered dates simplify downstream time‑series splits and improve readability of the CSV output. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Execute `merged.sort_index(inplace=True); merged.reset_index(inplace=True)`. |

#### 7. Validate the final matrix: ensure no missing values, confirm that the column count equals sum of unique feature columns plus `Date` and `Target`, and verify that row count matches the expected number of trading days (original dates minus one for target lag).

| Category | Details |
| --- | --- |
| **Reason** | A sanity check prevents propagation of corrupted data into model training and backtesting stages. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Run assertions: `assert merged.isnull().sum().sum() == 0`, `assert 'Target' in merged.columns`, `assert len(merged) == expected_rows`. |

#### 8. Serialize the validated data frame to a CSV‑formatted string with UTF‑8 encoding, ensuring the header line includes `Date` followed by all feature names and finally `Target`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream nodes expect a plain string CSV; consistent encoding avoids hidden character issues. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `feature_matrix_csv = merged.to_csv(index=False, line_terminator='\n')` and store as a Python string. |

#### 9. Return the CSV string as the node output `feature_matrix_csv` and log a concise summary (row count, column count, date range) for observability.

| Category | Details |
| --- | --- |
| **Reason** | Provides transparency for pipeline monitoring and aids debugging if downstream nodes fail. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Construct a log message: `logger.info(f'Feature matrix generated: {len(merged)} rows, {len(merged.columns)} columns, dates {merged["Date"].min()}–{merged["Date"].max()}')` then assign to output. |


---

## compile_strategy_documentation

### Description
Assemble all model, feature, risk, execution, and backtest artifacts into a single strategy dossier.

### Implementation Plan

#### 1. Extract the best‑model metadata (best_model_identifier, sharpe_ratio, max_drawdown, annualized_return) from the `select_best_model` node and store it in a temporary JSON object for reuse across multiple sections.

| Category | Details |
| --- | --- |
| **Reason** | The model metadata drives the narrative for Strategy Overview and Model Architecture, ensuring consistency with the quantitative evaluation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Call the `select_best_model` output, parse the four fields, and assign them to variables (e.g., bestModelId, bestSharpe, bestDD, bestAnnRet). |

#### 2. Create the **Strategy Overview** markdown string using the variables from step 1 together with static strategy objectives (asset universe, holding period) retrieved from the `define_strategy_objectives` node (accessed via the global context). Include a bullet list of performance targets (target Sharpe, max drawdown, annualized return).

| Category | Details |
| --- | --- |
| **Reason** | Provides stakeholders with a concise executive summary that links the chosen model to business goals. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Template string with placeholders: `## Strategy Overview\n- Objective: …\n- Selected Model: ${bestModelId}\n- Expected Sharpe: ${bestSharpe}\n- Max Drawdown (limit): ${bestDD}\n- Expected Annual Return: ${bestAnnRet}`. |

#### 3. Synthesize the **Data & Features** section by enumerating the four data pipelines (price, cross‑asset, regime, volatility) described in the DAG. Use concise bullet points to outline cleaning (forward‑fill, drop‑remaining NaNs) and list engineered features (log returns, moving averages, RSI, MACD, ATR, correlations, spreads, regime flags, GARCH forecasts, implied‑vol deltas).

| Category | Details |
| --- | --- |
| **Reason** | Even though the node does not directly depend on feature‑generation nodes, the documentation must describe the data foundation for reproducibility. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Hard‑code a markdown block based on known feature generation steps from `compute_price_action_features`, `compute_cross_asset_features`, `compute_regime_features`, and `compute_volatility_features`. Use markdown headings and bullet lists. |

#### 4. Generate the **Model Architecture** markdown using the `bestModelId` from step 1 and the model description stored in `specify_model_architecture` (access via global context). Include input shape, component list (e.g., Gradient Boosting, LSTM), and the prediction combination method (e.g., weighted averaging).

| Category | Details |
| --- | --- |
| **Reason** | Provides technical readers with a clear view of the predictive engine that will be deployed. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a markdown template: `## Model Architecture\n- Model ID: ${bestModelId}\n- Components: …\n- Input Shape: …\n- Combination Method: …`. |

#### 5. Construct the **Feature Importance** markdown table. Since explicit importance scores are not directly output by any parent, invoke the `analyze_feature_importance` node (even though not listed as a direct dependency) to retrieve `feature_names` and `importance_scores`. Render them as a pipe‑separated markdown table sorted descending by score. If the node is unavailable, fallback to a placeholder statement indicating that importance data will be added after model inspection.

| Category | Details |
| --- | --- |
| **Reason** | Feature importance is a key deliverable for model transparency; pulling from `analyze_feature_importance` ensures accurate rankings. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Call `analyze_feature_importance`, iterate over zipped lists, format each row as `| Feature | Importance |`, prepend header and alignment row. |

#### 6. Build the **Risk Management** markdown by iterating over the three parallel arrays (`risk_control_names`, `risk_control_thresholds`, `risk_control_formulas`) returned by the `design_risk_controls` node. For each control, output a bullet with the name, threshold (as a human‑readable percentage), and the formula. Include a top‑level heading and a short description of portfolio‑ vs. position‑level controls.

| Category | Details |
| --- | --- |
| **Reason** | Clearly communicating the quantitative risk limits is essential for compliance and for the execution engine to enforce limits. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Loop index i over length of arrays, format: `- **${risk_control_names[i]}**: ${risk_control_thresholds[i]*100}% – `${risk_control_formulas[i]}`. |

#### 7. Insert the **Execution Pseudocode** markdown exactly as emitted by the `draft_execution_logic` node (`execution_logic_pseudocode` field). Prepend a heading and a brief narrative explaining how the pseudocode maps to the risk controls defined earlier.

| Category | Details |
| --- | --- |
| **Reason** | The execution logic must be directly traceable to the risk controls and model signals; reusing the already‑generated pseudocode guarantees consistency. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Wrap the pseudocode string in a markdown fenced code block with language `python` or `pseudo`. |

#### 8. Compose the **Backtest Results** markdown using the seven fields produced by the `summarize_backtest_results` node. Present key metrics in a markdown table, embed the histogram and turnover‑chart descriptions as bullet items, and include the full `markdown_report` content verbatim under a sub‑heading.

| Category | Details |
| --- | --- |
| **Reason** | Stakeholders need a concise performance snapshot together with visual insights; the `summarize_backtest_results` node already aggregates these stats. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a table: `| Metric | Value |` with rows for Annualized Return, Sharpe, Max Drawdown, Turnover, Win Rate. Then add sections: `### Charts` with bullet points using `histogram_description` and `turnover_chart_description`. Append `markdown_report`. |

#### 9. Draft the **Implementation Checklist** markdown as a static ordered list covering: (a) Code deployment, (b) Config file creation, (c) Model serialization, (d) Risk‑control parameters upload, (e) Monitoring plan integration (reference `create_monitoring_plan` output), (f) Performance validation, (g) Documentation upload. Each item should include a checkbox placeholder `[ ]`.

| Category | Details |
| --- | --- |
| **Reason** | A checklist formalizes the hand‑off steps and reduces operational risk during production rollout. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Hard‑code the list: `- [ ] Deploy model code\n- [ ] Add config.yml ...`. |

#### 10. Concatenate all eight section strings in the exact order required by the deliverable (Strategy Overview → Data & Features → Model Architecture → Feature Importance → Risk Management → Execution Pseudocode → Backtest Results → Implementation Checklist) into the final `full_document_markdown` field. Ensure each section begins with a level‑2 markdown heading (`##`). Add a top‑level title (`# Strategy Dossier`) at the very top.

| Category | Details |
| --- | --- |
| **Reason** | A single, ordered markdown file is the final artifact expected by downstream nodes (e.g., `final_deliverables_package`). |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | String concatenation with newline separators: `# Strategy Dossier\n\n${strategy_overview}\n\n${data_and_features}\n...`. |


---

## compute_cross_asset_features

### Description
Create correlation and spread features between the primary asset and each cross‑asset.

### Implementation Plan

#### 1. Load the `cleaned_data_csv` string from the parent node `align_and_clean_data`, parse it into a pandas DataFrame with `Date` parsed as datetime, and set `Date` as the index.

| Category | Details |
| --- | --- |
| **Reason** | Ensures a structured, time‑aligned dataset that can be directly used for rolling calculations and guarantees correct handling of missing dates. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(cleaned_data_csv), parse_dates=['Date'])`; then `df.set_index('Date', inplace=True)`. |

#### 2. Identify the primary asset columns: locate the column ending with `_Close` (or a column named `Primary_Close`). Store its name as `primary_close_col`. All other columns that end with `_Close` and are not the primary are treated as secondary asset price columns.

| Category | Details |
| --- | --- |
| **Reason** | Clear naming conventions avoid ambiguous column selection and make the feature generation robust to future additions of assets. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Iterate over `df.columns`; `primary_close_col = [c for c in df.columns if c.lower().endswith('_close') and 'primary' in c.lower()][0]`; `secondary_close_cols = [c for c in df.columns if c.lower().endswith('_close') and c != primary_close_col]`. |

#### 3. Compute daily log returns for the primary asset and each secondary asset: `log_return = np.log(price).diff()` and store them in a new DataFrame `returns_df` with the same column naming scheme (`<ticker>_ret`).

| Category | Details |
| --- | --- |
| **Reason** | Log returns are additive and preferred for correlation calculations; they also match the definition used in downstream model training. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | For each close column: `returns_df[col.replace('_Close', '_Ret')] = np.log(df[col]).diff()`; drop the first NaN row after diff. |

#### 4. For each secondary asset, compute a rolling 20‑day Pearson correlation between the primary log return series and the secondary log return series using `Series.rolling(window=20).corr()`; store results in a DataFrame `corr_df` with column names `corr_<SecondaryTicker>`.

| Category | Details |
| --- | --- |
| **Reason** | Rolling correlation captures the dynamic relationship between assets, which is a key predictive signal for the strategy. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Loop over `secondary_close_cols`; for each: `sec_ret = returns_df[sec_col.replace('_Close', '_Ret')]`; `corr_series = returns_df[primary_ret_col].rolling(20).corr(sec_ret)`; assign to `corr_df['corr_' + ticker]`. |

#### 5. Compute the daily price spread for each secondary asset as `primary_close - secondary_close`; store in a DataFrame `spread_df` with column names `spread_<SecondaryTicker>`.

| Category | Details |
| --- | --- |
| **Reason** | The spread directly measures relative valuation and is a complementary feature to correlation. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | For each secondary column: `spread_df['spread_' + ticker] = df[primary_close_col] - df[sec_col]`. |

#### 6. Combine `corr_df` and `spread_df` into a single feature DataFrame `features_df` aligned on the same index (Date). Drop any rows that still contain NaNs (the first 19 rows will have NaNs for correlation).

| Category | Details |
| --- | --- |
| **Reason** | A single DataFrame simplifies extraction of output arrays and guarantees that each date has a complete set of features. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `features_df = pd.concat([corr_df, spread_df], axis=1); features_df.dropna(inplace=True)`. |

#### 7. Construct the `date` list by converting the index of `features_df` to ISO‑8601 strings: `date = features_df.index.strftime('%Y-%m-%d').tolist()`.

| Category | Details |
| --- | --- |
| **Reason** | Matches the required output type `List[str]` and provides a human‑readable date format for downstream nodes. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use pandas `strftime` as shown. |

#### 8. Build the `asset_pairs` list: for each secondary ticker, create a string `Primary-<Ticker>`; the order must be the same as the order used when generating correlation and spread columns.

| Category | Details |
| --- | --- |
| **Reason** | Provides a clear mapping from the flattened correlation/spread values back to the underlying asset pair. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Extract ticker from column names (e.g., `col.split('_')[0]`), then `asset_pairs = ['Primary-' + t for t in secondary_tickers]`. |

#### 9. Flatten the correlation values: iterate over `features_df` rows (by date) and for each row concatenate the correlation columns in `asset_pairs` order into a single list; repeat for all dates to obtain `correlations` list.

| Category | Details |
| --- | --- |
| **Reason** | The output schema expects a one‑dimensional list where the temporal dimension is implicit via ordering. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```
correlations = []
for _, row in features_df.iterrows():
    for pair in asset_pairs:
        corr_col = 'corr_' + pair.split('-')[1]
        correlations.append(row[corr_col])
```
 |

#### 10. Flatten the price spread values using the same loop order as correlations, pulling from `spread_<Ticker>` columns into the `price_spreads` list.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the two flattened lists stay perfectly aligned (date‑major, then asset‑pair order). |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Similar to correlation flattening, replace `corr_` with `spread_` in column lookup. |

#### 11. Validate the lengths: `len(date) * len(asset_pairs)` must equal `len(correlations)` and `len(price_spreads)`; raise an exception if mismatched.

| Category | Details |
| --- | --- |
| **Reason** | Catches programming errors early, guaranteeing downstream nodes receive correctly shaped data. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Simple `assert` statements. |

#### 12. Return a JSON‑serializable dictionary containing the four output fields (`date`, `asset_pairs`, `correlations`, `price_spreads`).

| Category | Details |
| --- | --- |
| **Reason** | Conforms to the declared output structure for the node and enables downstream Python code to consume the results directly. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `return {"date": date, "asset_pairs": asset_pairs, "correlations": correlations, "price_spreads": price_spreads}`. |


---

## compute_price_action_features

### Description
Generate technical features from the primary asset price series (e.g., returns, momentum, volatility).

### Implementation Plan

#### 1. Load the `cleaned_data_csv` string output from the parent node `align_and_clean_data` into a pandas DataFrame using `pd.read_csv(io.StringIO(...), parse_dates=['Date'])`.

| Category | Details |
| --- | --- |
| **Reason** | Ensures that the downstream calculations operate on a structured, date‑indexed table that contains the fully cleaned OHLCV columns required for technical indicator computation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `io` and `pandas`; wrap the CSV string in `StringIO`; specify `Date` as the index or a column; verify that columns `Open`, `High`, `Low`, `Close` exist; raise a descriptive error if any are missing. |

#### 2. Validate that the DataFrame is sorted chronologically ascending; if not, sort by `Date` and re‑index to guarantee proper rolling calculations.

| Category | Details |
| --- | --- |
| **Reason** | Rolling windows (moving averages, RSI, etc.) depend on correct temporal order; unsorted data would produce misleading features. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `df['Date'].is_monotonic_increasing`; if false, execute `df = df.sort_values('Date').reset_index(drop=True)`. |

#### 3. Compute daily log returns: `log_return = np.log(df['Close'] / df['Close'].shift(1))` and store as a new Series named `log_return`.

| Category | Details |
| --- | --- |
| **Reason** | Log returns are the foundation for many momentum and risk metrics; using `np.log` provides additive properties over time. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `numpy as np`; handle the first row NaN by leaving it as `np.nan` (it will be removed later). |

#### 4. Calculate 10‑day and 30‑day simple moving averages on the `Close` price: `ma_10 = df['Close'].rolling(window=10, min_periods=10).mean()` and `ma_30 = df['Close'].rolling(window=30, min_periods=30).mean()`.

| Category | Details |
| --- | --- |
| **Reason** | Moving averages capture short‑ and medium‑term trend information; using `min_periods` equal to the window prevents premature values. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use pandas `rolling`; assign results to columns `ma_10` and `ma_30`. |

#### 5. Implement the Relative Strength Index (RSI) with a 14‑day look‑back: calculate upward and downward price changes, compute exponential weighted averages, then apply the RSI formula `100 - (100 / (1 + RS))`.

| Category | Details |
| --- | --- |
| **Reason** | RSI is a widely‑used momentum oscillator; the 14‑day period is standard and provides a balanced signal. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
delta = df['Close'].diff()
up = delta.clip(lower=0)
down = -delta.clip(upper=0)
roll_up = up.ewm(span=14, adjust=False).mean()
roll_down = down.ewm(span=14, adjust=False).mean()
RS = roll_up / roll_down
rsi = 100 - (100 / (1 + RS))
``` Assign to column `rsi`. |

#### 6. Compute MACD (Moving Average Convergence Divergence) using standard parameters (fast EMA 12, slow EMA 26, signal EMA 9): `macd_line = EMA_fast - EMA_slow`; `macd_signal = macd_line.ewm(span=9, adjust=False).mean(); macd = macd_line - macd_signal`.

| Category | Details |
| --- | --- |
| **Reason** | MACD captures trend‑following momentum; the standard parameter set is a de‑facto industry baseline. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
ema_fast = df['Close'].ewm(span=12, adjust=False).mean()
ema_slow = df['Close'].ewm(span=26, adjust=False).mean()
macd_line = ema_fast - ema_slow
macd_signal = macd_line.ewm(span=9, adjust=False).mean()
macd = macd_line - macd_signal
``` Store in column `macd`. |

#### 7. Calculate the Average True Range (ATR) over a 14‑day window: first compute True Range (TR) as the max of three values (high‑low, |high‑prev_close|, |low‑prev_close|), then apply a rolling mean.

| Category | Details |
| --- | --- |
| **Reason** | ATR quantifies recent volatility, essential for risk‑adjusted sizing and stop‑loss logic. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | ```python
high_low = df['High'] - df['Low']
high_prev_close = (df['High'] - df['Close'].shift(1)).abs()
low_prev_close = (df['Low'] - df['Close'].shift(1)).abs()
tr = pd.concat([high_low, high_prev_close, low_prev_close], axis=1).max(axis=1)
atr = tr.rolling(window=14, min_periods=14).mean()
``` Assign to column `atr`. |

#### 8. Assemble all computed feature Series (`log_return`, `ma_10`, `ma_30`, `rsi`, `macd`, `atr`) into a single DataFrame alongside the original `Date` column; drop any rows that contain NaN in any feature column to ensure a fully populated matrix.

| Category | Details |
| --- | --- |
| **Reason** | Down‑stream models cannot handle missing values; removing incomplete rows preserves alignment with the target variable and other feature tables. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create `features_df = pd.DataFrame({ 'Date': df['Date'], 'log_return': log_return, 'ma_10': ma_10, 'ma_30': ma_30, 'rsi': rsi, 'macd': macd, 'atr': atr })`; then `features_df = features_df.dropna().reset_index(drop=True)`. |

#### 9. Generate `feature_names` as a Python list ordered exactly as they appear in the CSV (excluding `Date`): `['log_return', 'ma_10', 'ma_30', 'rsi', 'macd', 'atr']`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream node `assemble_feature_matrix` expects an explicit ordering to correctly align columns during merges. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Hard‑code the list or derive via `features_df.columns.tolist()[1:]`. |

#### 10. Export `features_df` to CSV string without index: `csv_data = features_df.to_csv(index=False)`; compute `row_count = len(features_df)`.

| Category | Details |
| --- | --- |
| **Reason** | The node's output contract requires a CSV‑formatted string and the exact row count for validation in later steps. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use pandas `to_csv`; store result in variable `csv_data`; calculate `row_count = features_df.shape[0]`. |

#### 11. Wrap the entire computation in a try/except block that captures any unexpected errors (e.g., missing columns, division by zero) and raises a custom `ValueError` with a clear message indicating which step failed.

| Category | Details |
| --- | --- |
| **Reason** | Robust error handling simplifies debugging of the DAG and prevents silent failures that would propagate downstream. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | ```python
try:
    # all steps above
except Exception as e:
    raise ValueError(f'compute_price_action_features failed at step X: {e}')
``` |


---

## compute_regime_features

### Description
Derive regime classification signals from macro indicators (e.g., high‑/low‑vol regimes).

### Implementation Plan

#### 1. Load the `cleaned_data_csv` string from the `align_and_clean_data` node, parse it into a pandas DataFrame preserving the original chronological order.

| Category | Details |
| --- | --- |
| **Reason** | The regime classifier needs numeric VIX and PMI series aligned to dates; parsing ensures we work with structured data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` to feed the CSV string into `pd.read_csv`, set `parse_dates=['Date']`, and sort by the Date column if not already sorted. |

#### 2. Validate that the DataFrame contains the required macro columns `VIX` and `PMI`; raise a clear error if either is missing.

| Category | Details |
| --- | --- |
| **Reason** | Early validation prevents downstream logic failures and makes debugging data‑pipeline issues straightforward. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `{'VIX', 'PMI'}.issubset(df.columns)`; if false, construct an informative Exception listing missing columns. |

#### 3. Compute the 75th percentile of the entire VIX series using `numpy.percentile(df['VIX'].dropna(), 75)` and store it as `vix_threshold`.

| Category | Details |
| --- | --- |
| **Reason** | A fixed percentile threshold implements the rule‑based high/low volatility regime definition described in the prompt. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Import `numpy as np`; ensure NaNs are excluded from the percentile calculation. |

#### 4. Create a new column `RegimeLabel` where each row receives `'high_vol'` if its VIX value exceeds `vix_threshold`, otherwise `'low_vol'`.

| Category | Details |
| --- | --- |
| **Reason** | Translates the numeric VIX observation into a categorical regime label required by downstream models. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use vectorised pandas logic: `df['RegimeLabel'] = np.where(df['VIX'] > vix_threshold, 'high_vol', 'low_vol')`. |

#### 5. Create a binary column `PMIFlag` set to `True` when the PMI value is greater than 0 (positive PMI) and `False` otherwise.

| Category | Details |
| --- | --- |
| **Reason** | Provides a simple directional macro signal that can be used as a feature in the assembled matrix. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `df['PMIFlag'] = df['PMI'] > 0` (pandas will produce a boolean series). |

#### 6. Extract three parallel Python lists preserving date order: `dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()`, `regime_labels = df['RegimeLabel'].tolist()`, and `pmi_flags = df['PMIFlag'].tolist()`.

| Category | Details |
| --- | --- |
| **Reason** | The node's output specification demands plain Python lists (primitive types), not pandas objects. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Leverage pandas `.tolist()` after ensuring the DataFrame is sorted by Date. |

#### 7. Return a JSON‑compatible dictionary containing the three lists under the keys `dates`, `regime_labels`, and `pmi_flags` as defined in the output structure.

| Category | Details |
| --- | --- |
| **Reason** | Conforms to the typed node contract, enabling downstream nodes (e.g., `assemble_feature_matrix`) to consume the data without further transformation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | `return {"dates": dates, "regime_labels": regime_labels, "pmi_flags": pmi_flags}`. |


---

## compute_volatility_features

### Description
Generate forecasted volatility inputs using GARCH‑type calculations and implied‑vol trends.

### Implementation Plan

#### 1. Parse the `cleaned_data_csv` string from the `align_and_clean_data` output into a Pandas DataFrame, ensuring the `Date` column is converted to `datetime64[ns]` and set as the index.

| Category | Details |
| --- | --- |
| **Reason** | A structured DataFrame is required for reliable column selection, lag calculations, and model fitting; parsing once avoids repeated I/O. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pd.read_csv(io.StringIO(cleaned_data_csv), parse_dates=['Date'])`; call `df.set_index('Date', inplace=True)`; verify that the index is monotonic and unique. |

#### 2. Validate the presence of the primary asset's price columns (`Close` or equivalent) and the `ImpliedVol` column; raise a descriptive error if missing.

| Category | Details |
| --- | --- |
| **Reason** | The GARCH model needs returns derived from closing prices, and the implied‑vol delta calculation requires the implied volatility series; early validation prevents silent failures later in the pipeline. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Check `{'Close', 'ImpliedVol'}.issubset(df.columns)`; if not, construct an error message listing missing columns. |

#### 3. Compute daily log returns of the primary asset: `log_return = np.log(df['Close'] / df['Close'].shift(1))`; drop the first NaN resulting from the shift.

| Category | Details |
| --- | --- |
| **Reason** | GARCH models are traditionally fit on return series rather than price levels; log returns ensure additive properties and stationarity assumptions. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a new Series `returns = np.log(df['Close']).diff()`; store it in `df['LogReturn']`. |

#### 4. Fit a GARCH(1,1) model to the `LogReturn` series using the `arch` Python library (e.g., `arch.univariate.ConstantMean` with `arch_model(returns, vol='Garch', p=1, q=1)`). Optimize parameters via maximum likelihood.

| Category | Details |
| --- | --- |
| **Reason** | The `arch` package provides a battle‑tested implementation of GARCH models with automatic handling of convergence, parameter constraints, and diagnostics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```python
from arch import arch_model
am = arch_model(df['LogReturn'].dropna(), vol='Garch', p=1, q=1, mean='Zero')
res = am.fit(disp='off')
``` |

#### 5. Generate one‑step‑ahead conditional volatility forecasts for each date in the cleaned data after the model fitting horizon. Use `res.forecast(horizon=1, start=df.index[0])` to obtain the forecasted variance, then take the square‑root to get volatility.

| Category | Details |
| --- | --- |
| **Reason** | A one‑step‑ahead forecast aligns with the downstream model’s need for a forward‑looking volatility input; using the built‑in forecast method guarantees consistency with the fitted parameters. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | ```python
forecast = res.forecast(start=df.index[0], horizon=1)
vol_forecast = np.sqrt(forecast.variance.iloc[:, 0])
``` |

#### 6. Calculate the 5‑day implied‑volatility delta: for each date `t`, compute `ImpVolDelta[t] = df['ImpliedVol'].loc[t] - df['ImpliedVol'].shift(5).loc[t]`. Align the resulting Series with the GARCH forecast Series, dropping dates where the 5‑day lag is unavailable.

| Category | Details |
| --- | --- |
| **Reason** | The 5‑day delta captures recent implied‑vol momentum, a valuable predictive signal; aligning both series ensures a one‑to‑one correspondence in the final output. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | ```python
imp_vol_delta = df['ImpliedVol'] - df['ImpliedVol'].shift(5)
# Align with vol_forecast index
aligned = pd.concat([vol_forecast, imp_vol_delta], axis=1).dropna()
aligned.columns = ['GARCHForecast', 'ImpliedVolDelta']
``` |

#### 7. Extract the final output lists: `dates = aligned.index.strftime('%Y-%m-%d').tolist()`, `garch_forecasts = aligned['GARCHForecast'].astype(float).tolist()`, `implied_vol_delta_5d = aligned['ImpliedVolDelta'].astype(float).tolist()`. Return them in the node’s defined output structure.

| Category | Details |
| --- | --- |
| **Reason** | Converting to plain Python lists matches the typed output contract and facilitates downstream serialization (e.g., JSON or CSV). |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Assign the three lists to the respective output fields; ensure no NaNs remain; optionally log the length of each list for debugging. |

#### 8. Add robust error handling and logging: capture exceptions during CSV parsing, GARCH fitting, and delta calculation; log the error context (e.g., date range, number of observations) and re‑raise a custom `VolatilityFeatureError` with a clear message.

| Category | Details |
| --- | --- |
| **Reason** | The volatility step is mathematically intensive; failures (non‑convergence, insufficient data) must be surfaced early to prevent downstream cascade failures. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Wrap each major block in `try/except`; use Python’s `logging` module to record `INFO` on successful completion and `ERROR` on failure; define a lightweight exception class for clarity. |


---

## create_monitoring_plan

### Description
Define real‑time monitoring metrics, alert thresholds, and model retraining schedule.

### Implementation Plan

#### 1. Extract strategy‑level parameters from `define_strategy_objectives` (primary_tradable_asset, desired_annual_return_pct, risk_tolerance_max_drawdown_pct, holding_period_days, regulatory_constraints) and model performance metrics from `select_best_model` (sharpe_ratio, max_drawdown, annualized_return).

| Category | Details |
| --- | --- |
| **Reason** | These values provide the business context needed to select appropriate monitoring metrics and realistic alert thresholds. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the JSON output of the two parent nodes; store values in a temporary dictionary for later reference. |

#### 2. Define a canonical set of daily live metrics that directly reflect the strategy’s risk‑adjusted performance and operational health. Include at minimum: (1) Realized volatility (30‑day rolling), (2) Forecast volatility (model GARCH forecast), (3) Prediction error (abs(predicted‑return – actual‑return)), (4) Position exposure (gross % of capital), (5) Daily P&L, (6) Cumulative Sharpe ratio, (7) Current drawdown, (8) Turnover rate, (9) Compliance flag (e.g., short‑sell allowed).

| Category | Details |
| --- | --- |
| **Reason** | These metrics cover market risk, model risk, execution risk, and regulatory compliance, matching the objectives and constraints defined earlier. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a static list of metric names; ensure each name is concise and matches downstream naming conventions used in monitoring dashboards. |

#### 3. Populate `daily_live_metrics` output field with the ordered list of metric names defined above, ensuring the list type is `LIST_STR`.

| Category | Details |
| --- | --- |
| **Reason** | The output must conform exactly to the schema expected by downstream nodes and by the final deliverables package. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Assign the list directly to the output variable; no computation required. |

#### 4. Select which of the daily metrics will have active alert thresholds. Prioritize metrics that, if breached, indicate imminent risk: Sharpe ratio, max drawdown, exposure limit, turnover, and compliance flag.

| Category | Details |
| --- | --- |
| **Reason** | Limiting alerts to high‑impact metrics reduces noise and ensures rapid operator response. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create `alert_thresholds_metrics` list containing the subset: ["Sharpe ratio", "Current drawdown", "Gross exposure", "Turnover rate", "Compliance flag"]. |

#### 5. Derive numeric alert thresholds (`alert_thresholds_values`) using both strategy objectives and model performance:  
- Sharpe ratio threshold = max(0.5, 0.8 × model_sharpe_ratio)  
- Drawdown threshold = risk_tolerance_max_drawdown_pct (e.g., 0.15 for 15 %)  
- Gross exposure threshold = 0.20 (20 % of capital)  
- Turnover rate threshold = 0.30 (30 % per month)  
- Compliance flag threshold = 0 (0 = violation).

| Category | Details |
| --- | --- |
| **Reason** | Thresholds are anchored to the model’s historical performance and the strategy’s risk appetite, providing objective triggers. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Compute the Sharpe threshold dynamically using the best model’s sharpe_ratio; other thresholds are static constants derived from `define_strategy_objectives`. Cast all values to float and store in the same order as `alert_thresholds_metrics`. |

#### 6. Validate that the lengths of `alert_thresholds_metrics` and `alert_thresholds_values` match; raise an exception if mismatched.

| Category | Details |
| --- | --- |
| **Reason** | Ensures data integrity before downstream consumption; mismatched arrays would cause runtime errors in monitoring pipelines. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If len(list1) != len(list2): throw ValueError with explanatory message. |

#### 7. Draft a detailed quarterly retraining schedule and assign it to `retraining_schedule`. Include: (a) data window (most recent 2‑years), (b) feature engineering freeze date, (c) hyper‑parameter search period (first week of quarter), (d) back‑test validation (second week), (e) model selection criteria (Sharpe > 0.5 and drawdown < risk_tolerance), (f) production rollout (third week), (g) monitoring hand‑off (fourth week).

| Category | Details |
| --- | --- |
| **Reason** | A clear, repeatable process guarantees that model drift is addressed regularly and that stakeholders know exact timelines. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Compose a multi‑paragraph markdown string outlining each step, dates relative to quarter start, and responsible owners. |

#### 8. Return the four output fields (`daily_live_metrics`, `alert_thresholds_metrics`, `alert_thresholds_values`, `retraining_schedule`) as a JSON object matching the defined `output_structure`.

| Category | Details |
| --- | --- |
| **Reason** | Final step to satisfy the node contract and enable downstream nodes (e.g., `final_deliverables_package`) to consume the monitoring plan. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Serialize the prepared variables into the response payload; ensure correct PrimitiveType mapping (list of strings, list of floats, string). |


---

## define_hyperparameter_grid

### Description
Set the search space for each model component's hyperparameters.

### Implementation Plan

#### 1. Extract the model component list from the parent node `specify_model_architecture` output field `model_components` to verify that both "Gradient Boosting" and "LSTM" are present; abort with a clear error if either component is missing.

| Category | Details |
| --- | --- |
| **Reason** | Ensures alignment between the architecture definition and the hyper‑parameter grid, preventing downstream mismatches. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the `model_components` JSON array, perform a set containment check for the two expected strings, and raise an exception with a descriptive message if validation fails. |

#### 2. Define a static dictionary of hyperparameter names and their allowed ranges for Gradient Boosting: {"n_estimators": "100-500", "learning_rate": "0.01-0.1", "max_depth": "3-10", "subsample": "0.6-1.0", "colsample_bytree": "0.6-1.0"}. Extend the dictionary only if the architecture explicitly requests additional GB parameters (e.g., `max_depth`).

| Category | Details |
| --- | --- |
| **Reason** | Provides a comprehensive yet deterministic search space that matches typical best‑practice ranges for tree‑based ensembles. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Hard‑code the mapping in code; optionally load from a configuration file for future extensibility. |

#### 3. Define a static dictionary of hyperparameter names and their allowed ranges for the LSTM: {"layers": "1-3", "units": "32-128", "dropout": "0-0.3", "learning_rate": "0.0005-0.01", "batch_size": "32-256"}. Include only those keys that appear in the `model_components` list and that are relevant to an LSTM architecture.

| Category | Details |
| --- | --- |
| **Reason** | Captures the most influential architectural and training hyper‑parameters for recurrent networks while staying within realistic computational budgets. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Same as GB dictionary – hard‑code, with optional external config. |

#### 4. Create ordered lists `gb_hyperparameters` and `gb_hyperparameter_ranges` by iterating over the GB dictionary preserving insertion order; similarly create `lstm_hyperparameters` and `lstm_hyperparameter_ranges` from the LSTM dictionary.

| Category | Details |
| --- | --- |
| **Reason** | The output specification explicitly requires ordered parallel arrays; preserving order guarantees deterministic mapping between names and ranges. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use Python's `list(dict.keys())` and `list(dict.values())` constructs. |

#### 5. Assemble a combined JSON object with two top‑level keys: "gradient_boosting" mapping hyperparameter names to range strings, and "lstm" mapping hyperparameter names to range strings. Serialize this object with `json.dumps(..., separators=(',', ':'))` to produce a compact string for `hyperparameter_grid_json`.

| Category | Details |
| --- | --- |
| **Reason** | The downstream `train_models` node expects a single JSON‑string representing the full grid; a compact representation reduces token usage and parsing overhead. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | ```python
import json
grid = {
    "gradient_boosting": dict(zip(gb_hyperparameters, gb_hyperparameter_ranges)),
    "lstm": dict(zip(lstm_hyperparameters, lstm_hyperparameter_ranges))
}
hyperparameter_grid_json = json.dumps(grid, separators=(",", ":"))
``` |

#### 6. Validate the generated JSON string by loading it back with `json.loads` and confirming that the keys and value counts match the previously created lists; if any discrepancy is found, raise a descriptive exception.

| Category | Details |
| --- | --- |
| **Reason** | Defensive programming prevents silent bugs where list ordering or missing entries could corrupt the hyperparameter search. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Round‑trip parse and compare lengths of dicts to list variables. |

#### 7. Return the five output fields (`hyperparameter_grid_json`, `gb_hyperparameters`, `gb_hyperparameter_ranges`, `lstm_hyperparameters`, `lstm_hyperparameter_ranges`) in the exact order defined in the node's output schema.

| Category | Details |
| --- | --- |
| **Reason** | Ensures downstream nodes receive data in the expected format; ordering matters for some orchestration engines. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Package outputs into a dict matching the schema and emit as the node's response. |


---

## define_strategy_objectives

### Description
State the high‑level goals, asset universe, time horizon, and performance targets for the quant strategy.

### Implementation Plan

#### 1. Collect the strategic brief from the user or upstream documentation and split it into five mandatory fields: primary asset, asset universe, target return, drawdown tolerance, and holding period.

| Category | Details |
| --- | --- |
| **Reason** | A deterministic extraction ensures every required output field is populated and prevents downstream null values. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a simple regex pattern (e.g., `Primary Asset: (\S+)`) for each bullet; fallback to a default placeholder if a field is missing. |

#### 2. Validate `primary_tradable_asset` against a curated master ticker list (e.g., Bloomberg, Refinitiv) to guarantee the symbol exists and is tradable in the intended market.

| Category | Details |
| --- | --- |
| **Reason** | Invalid tickers cause data‑fetch failures later in the pipeline. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Load the master ticker CSV into a set; perform O(1) membership test; raise a clear error if not found. |

#### 3. Normalize `asset_universe` by merging the primary asset with any secondary assets mentioned in the brief; de‑duplicate and sort alphabetically.

| Category | Details |
| --- | --- |
| **Reason** | A clean, ordered universe simplifies downstream feature generation and risk‑control loops. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Split the universe string on commas/semicolons, strip whitespace, add primary asset if absent, convert to set, then `sorted(list(set))`. |

#### 4. Parse `desired_annual_return_pct` as a float, enforce a realistic range (1‑100 %), and round to two decimal places.

| Category | Details |
| --- | --- |
| **Reason** | Extreme return expectations break hyper‑parameter search and risk‑control calibration. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | float(value); if value < 1 or > 100 → clamp or raise warning; `round(value, 2)`. |

#### 5. Parse `risk_tolerance_max_drawdown_pct` as a float, ensure it is positive and ≤ 100, and round to two decimals.

| Category | Details |
| --- | --- |
| **Reason** | Drawdown limits drive the design of stop‑loss and VaR controls later in the workflow. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Same parsing logic as return; store as a positive percentage. |

#### 6. Parse `holding_period_days` as an integer, enforce a sensible bound (1‑365 days), and default to 5 days if unspecified.

| Category | Details |
| --- | --- |
| **Reason** | Holding period directly influences feature lag windows and back‑test rebalance frequency. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | int(value); if out‑of‑range → set to default; log the adjustment. |

#### 7. Extract `regulatory_constraints` by scanning the brief for known keywords (e.g., "short‑selling ban", "leverage limit", "region restriction"). Return a list; if none are found, return an empty list.

| Category | Details |
| --- | --- |
| **Reason** | Explicit constraints are needed for `design_risk_controls` and `create_monitoring_plan` nodes. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a dictionary of regex → constraint string; iterate over patterns, append matches; deduplicate. |

#### 8. Assemble the final output dictionary matching the `output_structure` schema and serialize it for downstream nodes.

| Category | Details |
| --- | --- |
| **Reason** | A single, well‑typed payload guarantees type‑safe consumption by all dependent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python dict with the six keys; validate types using a lightweight schema validator (e.g., `jsonschema`); raise if mismatch. |


---

## design_risk_controls

### Description
Define portfolio‑level and position‑level risk limits, stop‑loss rules, and turnover caps.

### Implementation Plan

#### 1. Extract strategy‑level parameters from the `define_strategy_objectives` output: desired annual return, max drawdown tolerance, holding period, and any regulatory constraints.

| Category | Details |
| --- | --- |
| **Reason** | These parameters set the high‑level risk appetite and legal limits that drive quantitative risk control thresholds. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the `define_strategy_objectives` JSON fields; store values in local variables (e.g., `max_drawdown_tol = risk_tolerance_max_drawdown_pct / 100`). |

#### 2. Extract model‑specific performance metrics from `select_best_model`: Sharpe ratio, max drawdown, and annualized return.

| Category | Details |
| --- | --- |
| **Reason** | Model volatility and drawdown behavior inform appropriate VaR limits, stop‑loss levels, and turnover caps that are realistic for the selected model. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the fields `sharpe_ratio`, `max_drawdown`, and `annualized_return` from the best model output; convert percentages to decimals where needed. |

#### 3. Define a canonical list of five core quantitative risk controls: `max_gross_exposure`, `var_99`, `max_asset_weight`, `daily_stop_loss`, `monthly_turnover`.

| Category | Details |
| --- | --- |
| **Reason** | A fixed, well‑known set of controls provides consistency across downstream nodes (documentation, execution, back‑test). |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create an ordered Python list: `["max_gross_exposure", "var_99", "max_asset_weight", "daily_stop_loss", "monthly_turnover"]`. |

#### 4. Compute the numeric thresholds for each control using a blend of strategy objectives and model metrics:
- `max_gross_exposure` = 0.20 (hard‑coded policy or derived from capital allocation guidelines).
- `var_99` = max(0.02, model_max_drawdown * 0.5) to ensure VaR is stricter than historical drawdown.
- `max_asset_weight` = min(0.05, desired_annual_return / 250) – cap at 5% per‑asset.
- `daily_stop_loss` = max(0.02, model_max_drawdown / 10) – a conservative 2% floor.
- `monthly_turnover` = min(0.30, 1 / holding_period_days) – caps turnover proportionally to holding period.

| Category | Details |
| --- | --- |
| **Reason** | Formulas explicitly tie risk limits to both business objectives and empirical model behavior, guaranteeing that controls are neither too lax nor infeasible. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement each formula as a Python expression; ensure all percentages are expressed as decimals. Use `max()`/`min()` to enforce policy caps. |

#### 5. Generate human‑readable implementation strings for each control, preserving the same order as the names list:
- `"GrossExposure <= 0.20"`
- `"VaR_99 <= {var_99:.4f}"`
- `"Weight_per_asset <= {max_asset_weight:.4f}"`
- `"DailyStopLoss <= {daily_stop_loss:.4f}"`
- `"Turnover_monthly <= {monthly_turnover:.4f}"`.

| Category | Details |
| --- | --- |
| **Reason** | Explicit formula strings are required by downstream nodes (e.g., execution pseudocode, back‑test configuration) for direct embedding. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use Python f‑strings to interpolate the computed thresholds; round to 4 decimal places for clarity. |

#### 6. Validate that each threshold respects regulatory constraints (e.g., if `short‑selling ban` is present, enforce `max_asset_weight` ≤ 0 for short positions) and raise an error if any rule violates policy.

| Category | Details |
| --- | --- |
| **Reason** | Ensuring compliance early prevents downstream failures and aligns with the `regulatory_constraints` output. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `regulatory_constraints`; if a constraint mentions short‑selling, adjust `max_asset_weight` or add an additional control such as `short_exposure <= 0`. Use assertions to fail fast. |

#### 7. Assemble the three parallel output lists (`risk_control_names`, `risk_control_thresholds`, `risk_control_formulas`) and return them in the exact order defined by the schema.

| Category | Details |
| --- | --- |
| **Reason** | Correct ordering guarantees that consuming nodes can zip the three lists without ambiguity. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return a JSON object with keys matching the output_structure; each list is built from the earlier steps and verified for equal length. |


---

## draft_execution_logic

### Description
Create pseudo‑code describing order sizing, routing, and real‑time signal handling.

### Implementation Plan

#### 1. Load parent node outputs: retrieve `best_model_identifier` and its performance metrics from `select_best_model`; retrieve `risk_control_names`, `risk_control_thresholds`, and `risk_control_formulas` from `design_risk_controls`.

| Category | Details |
| --- | --- |
| **Reason** | The execution logic must be aware of which model to call and the exact numeric limits to enforce; pulling them up front avoids repeated look‑ups during runtime. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the JSON/structured output of the parent nodes; store values in in‑memory variables `model_id`, `risk_names[]`, `risk_limits[]`, `risk_formulas[]`. |

#### 2. Define a function `fetch_latest_feature_vector()` that reads the most recent row from the persisted feature matrix (produced by `assemble_feature_matrix`). The function returns a dictionary mapping feature names to numeric values.

| Category | Details |
| --- | --- |
| **Reason** | Real‑time inference requires the freshest feature snapshot; encapsulating this in a function isolates I/O and allows unit testing. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement file I/O (e.g., pandas.read_csv with `skiprows=-1`) or query a feature store; ensure datatype conversion to float; include error handling for missing or NaN values. |

#### 3. Create a wrapper `generate_position_signal(feature_vector)` that loads the serialized model identified by `model_id` (e.g., via joblib or torch) and computes a raw signal (e.g., probability or expected return). Normalize the signal to a signed magnitude in [-1, 1].

| Category | Details |
| --- | --- |
| **Reason** | The raw model output may be on an arbitrary scale; normalizing ensures downstream sizing logic remains consistent across models. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Load model with appropriate library; apply `model.predict(feature_vector)`; if output >0.5 map to +1, else -1; optionally scale by (output - 0.5)*2. |

#### 4. Implement `apply_risk_controls(signal, current_exposure, portfolio_state)` that iterates over `risk_names` and evaluates each `risk_formulas` using the current portfolio metrics (gross exposure, VaR, per‑asset weight, daily P&L, turnover). If any rule would be violated, clamp or nullify the signal accordingly and log the adjustment.

| Category | Details |
| --- | --- |
| **Reason** | Risk compliance must be enforced before any order is sent; a systematic loop makes the logic extensible when new controls are added. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | For each control: parse the formula string (e.g., "GrossExposure <= 0.20") into a Python lambda; evaluate with real‑time numbers; if `signal` would cause breach, set `signal = 0` or reduce magnitude; record a string “Control X applied: signal capped to Y” into `risk_control_implementation_details` list. |

#### 5. Define the order sizing formula as a string `order_sizing_formula = "size = min( capital * signal * leverage, risk_limit * capital )"` and also compute the numeric size in a helper `compute_order_size(signal, capital, risk_limits)` following that formula.

| Category | Details |
| --- | --- |
| **Reason** | Both a human‑readable formula (for documentation) and an executable calculation (for the pseudocode) are required by the output spec. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use variables: `capital` (available cash), `leverage` (model‑defined, e.g., 2x), `max_position = risk_limits['max_gross_exposure'] * capital`; final size = min(|signal| * capital * leverage, max_position); preserve sign from `signal`. |

#### 6. Write the final pseudocode block (`execution_logic_pseudocode`) that strings together the above functions in logical order, with explicit comment lines for each major step:
```
# 1. Load latest features
features = fetch_latest_feature_vector()
# 2. Generate raw model signal
raw_signal = generate_position_signal(features)
# 3. Apply risk controls (may adjust signal)
adjusted_signal, rc_details = apply_risk_controls(raw_signal, current_exposure, portfolio_state)
# 4. Compute order size
order_qty = compute_order_size(adjusted_signal, capital, risk_limits)
# 5. Submit limit order
submit_limit_order(symbol, order_qty, limit_price)
```

| Category | Details |
| --- | --- |
| **Reason** | The prompt explicitly asks for concise pseudocode with clear step comments; the block satisfies readability and documentation needs. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Concatenate comment strings and code lines into a single multi‑line string; ensure variable names match those defined earlier; wrap in markdown triple backticks for clarity. |

#### 7. Populate `risk_control_implementation_details` list with the textual logs generated in step 4 (e.g., "Applied max_gross_exposure: signal reduced from 0.8 to 0.4") so that the output documents exactly how each control altered the signal.

| Category | Details |
| --- | --- |
| **Reason** | The output requires a list of implementation details; capturing them during risk‑control evaluation provides traceability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Within `apply_risk_controls`, whenever a control modifies the signal, append a formatted string to a list; return that list to the caller. |

#### 8. Validate the assembled outputs: ensure `execution_logic_pseudocode` is non‑empty string, `risk_control_implementation_details` contains at least one entry (or an empty list if no limits triggered), and `order_sizing_formula` matches the documented expression.

| Category | Details |
| --- | --- |
| **Reason** | Simple sanity checks prevent downstream failures when the compiled strategy document consumes these fields. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Add assert statements or conditional checks; raise descriptive exceptions if any check fails. |


---

## evaluate_models

### Description
Assess all trained candidates on the test set and compute performance metrics.

### Implementation Plan

#### 1. Parse `split_dataset` output CSV strings (`train_csv`, `validation_csv`, `test_csv`) into three Pandas DataFrames with proper dtypes (Date → datetime, numeric columns → float). Validate that the Test DataFrame contains the columns required for model inference (features + Target).

| Category | Details |
| --- | --- |
| **Reason** | Reliable DataFrames are the foundation for generating predictions; parsing errors would cascade into incorrect metric calculations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `io.StringIO` + `pd.read_csv`; enforce `parse_dates=['Date']`; assert required feature columns exist; raise descriptive error if mismatch. |

#### 2. Extract the list of model identifiers from `train_models` output (`hyperparameters`). For each hyperparameter string, generate a deterministic model identifier (e.g., `model_001`, `model_002`, …) and store the corresponding hyperparameter dict by parsing the string back into a Python dict (e.g., using `ast.literal_eval`).

| Category | Details |
| --- | --- |
| **Reason** | The identifiers link the trained models to the evaluation step; parsing keeps the provenance of each candidate. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `hyperparameters`; apply `enumerate` for stable IDs; `ast.literal_eval` to convert string representation to dict; build a dict `model_id -> hyperparams`. |

#### 3. For each candidate model, reconstruct the trained estimator object from persisted storage. Assume a convention where each model is serialized to `models/{model_id}.pkl` using `joblib.dump` during `train_models`. Load with `joblib.load`. If file missing, log a warning and skip the candidate.

| Category | Details |
| --- | --- |
| **Reason** | Evaluation must use the exact parameters learned during training; re‑training would invalidate the validation metrics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Import `joblib`; loop over identifiers; try‑except `FileNotFoundError`; maintain `valid_models` list. |

#### 4. Generate predictions on the Test DataFrame for each valid model. Use the model's `predict` method on the feature matrix (exclude `Target` and `Date`). Store predictions as a NumPy array aligned with the Test dates.

| Category | Details |
| --- | --- |
| **Reason** | Predictions are needed to construct daily position signals and subsequent performance series. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Extract feature columns via `test_df.drop(columns=['Date','Target'])`; ensure same column order as used in training; call `model.predict(X_test)`; cache in dict `model_id -> predictions`. |

#### 5. Convert raw predictions into daily position signals. Adopt a simple long‑short rule: `position = np.sign(prediction)`. Optionally, apply a volatility‑scaled position size using the `GARCHForecast` from `compute_volatility_features` if available; otherwise use unit exposure.

| Category | Details |
| --- | --- |
| **Reason** | A deterministic signal generation rule enables reproducible performance metrics across all candidates. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `positions = np.sign(predictions)`; ensure positions are -1, 0, or +1; store as `model_id -> positions`. |

#### 6. Compute daily portfolio returns for each model: `return_t = position_t * test_df['Target'].values`. This assumes the Target column is the next‑day excess return of the primary asset.

| Category | Details |
| --- | --- |
| **Reason** | Portfolio returns are the direct input for Sharpe, drawdown, turnover and hit‑rate calculations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Element‑wise multiplication; produce a Series `daily_ret` indexed by Date. |

#### 7. Calculate performance metrics per model:
- **Sharpe ratio**: mean(daily_ret) / std(daily_ret) * sqrt(252).
- **Annualized return**: (1 + mean(daily_ret))^252 - 1, expressed in percent.
- **Max drawdown**: use the cumulative product of (1+daily_ret) to build equity curve, then compute peak‑to‑trough decline.
- **Turnover**: average absolute change in position per day (`|Δposition|`) expressed as a percent of the notional (since position values are -1/0/1, turnover = mean(|Δposition|) * 100).
- **Hit‑rate**: proportion of days where `daily_ret > 0`.
Store each metric in its respective list.

| Category | Details |
| --- | --- |
| **Reason** | These metrics directly answer the node's prompt and provide a basis for ranking. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement helper functions: `calc_sharpe`, `calc_ann_return`, `calc_max_dd`, `calc_turnover`, `calc_hit_rate`. Use `numpy` for vectorised operations; guard against zero‑variance (std=0) by returning Sharpe=0. |

#### 8. Assemble a composite ranking score. Define the score as a weighted sum: `score = Sharpe * 0.5 - MaxDrawdown * 0.3 + AnnualizedReturn * 0.2`. Higher scores are better. Compute scores for all candidates and obtain ranks via `np.argsort(-score) + 1` (1 = best).

| Category | Details |
| --- | --- |
| **Reason** | A single numeric ranking enables clear ordering while respecting risk‑adjusted performance. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Create NumPy arrays for each metric; apply weights; use `np.argsort` to produce rank list aligned with `candidate_models`. |

#### 9. Populate the output fields in the order of the original candidate list:
- `candidate_models` = list of identifiers.
- `sharpe_ratios`, `annualized_returns`, `max_drawdowns`, `turnovers`, `hit_rates`, `ranks` = corresponding metric lists.
Convert percentages to float (e.g., 12.5 for 12.5%).

| Category | Details |
| --- | --- |
| **Reason** | Ensures the output conforms exactly to the declared schema for downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Iterate over stored metric dicts; cast to Python `float`; build final dict matching `output_structure`. |

#### 10. Validate the final output: confirm all lists have identical length, no `None` values, and ranks form a permutation of 1..N. If any check fails, raise an exception with a clear message.

| Category | Details |
| --- | --- |
| **Reason** | Pre‑empt downstream failures (e.g., `select_best_model`) caused by malformed output. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `assert len(set(ranks)) == N and max(ranks) == N` etc.; use Python `assert` with custom error text. |

#### 11. Log a concise summary to stdout or a logger: number of evaluated models, best model identifier, its Sharpe and max drawdown. This aids debugging and audit trails.

| Category | Details |
| --- | --- |
| **Reason** | Transparency for users and for automated pipelines that capture logs. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use Python `logging` module at INFO level; format string with f‑interpolation. |


---

## fetch_cross_asset_data

### Description
Download historical price series for secondary assets used for correlation signals.

### Implementation Plan

#### 1. Parse the `data_sources` list produced by `list_data_sources` to extract all secondary‑asset entries (sector ETFs, commodities, FX pairs) while filtering out the primary tradable asset.

| Category | Details |
| --- | --- |
| **Reason** | The parent node provides a plain‑text enumeration; extracting only cross‑asset identifiers ensures we request the correct tickers for correlation features. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use regular expressions or simple string splitting to locate patterns like "Ticker: XYZ"; store results in a Python list `cross_asset_tickers`. Log any ambiguous entries for manual review. |

#### 2. Determine the required date range (start_date, end_date) by querying the primary asset's price data cache (produced later by `fetch_price_data`). If the primary data is not yet available, store a placeholder and defer exact range alignment to the `align_and_clean_data` step.

| Category | Details |
| --- | --- |
| **Reason** | The prompt explicitly demands the same calendar as the primary asset; aligning here avoids later mismatches. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Attempt to read a shared metadata file `primary_price_meta.json` containing `first_date` and `last_date`. If missing, set `start_date = None` and `end_date = None`; later `align_and_clean_data` will intersect calendars. |

#### 3. For each ticker in `cross_asset_tickers`, query a reliable market data API (e.g., Bloomberg Terminal, Refinitiv, or free fallback like Yahoo Finance via `yfinance` library) to download daily **closing** prices.

| Category | Details |
| --- | --- |
| **Reason** | Uniform source selection guarantees data quality and consistent frequency (daily). |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Implement a wrapper function `download_close(ticker, start, end)` that:
- Uses the chosen provider's SDK or REST endpoint.
- Sends start/end parameters if known; otherwise requests full history.
- Retries up to 3 times with exponential back‑off on HTTP errors.
- Logs request IDs and timestamps for auditability.
- Returns a `pandas.Series` indexed by `Date`. |

#### 4. Collect all Series objects into a dictionary `{ticker: series}` and perform an outer join on the `Date` index to produce a unified `DataFrame` `cross_df` where each column is a ticker’s closing price.

| Category | Details |
| --- | --- |
| **Reason** | An outer join preserves all dates present in any series, allowing later forward‑fill or drop‑na handling in `align_and_clean_data`. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use `pd.concat(series_dict, axis=1, join='outer')`. Ensure the index is of dtype `datetime64[ns]` and sorted ascending. |

#### 5. If `start_date` and `end_date` were resolved earlier, slice `cross_df` to `[start_date, end_date]`; otherwise retain the full outer‑joined range and let downstream nodes truncate.

| Category | Details |
| --- | --- |
| **Reason** | Guarantees that when dates are known, the output matches the primary asset calendar; otherwise defers alignment. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Apply `cross_df.loc[start_date:end_date]` when dates are not None. |

#### 6. Convert `cross_df` to a CSV‑formatted string `csv_data` using `cross_df.to_csv(index=True, date_format='%Y-%m-%d')` and capture the list of column names (excluding the index) as `asset_names`.

| Category | Details |
| --- | --- |
| **Reason** | The output schema expects a CSV string and an explicit list of asset identifiers. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Store `csv_data = cross_df.to_csv()`; `asset_names = list(cross_df.columns)`. |

#### 7. Derive `start_date`, `end_date`, and `row_count` from the final DataFrame: `start_date = cross_df.index.min().strftime('%Y-%m-%d')`, `end_date = cross_df.index.max().strftime('%Y-%m-%d')`, `row_count = cross_df.shape[0]`.

| Category | Details |
| --- | --- |
| **Reason** | These scalar metadata fields are required for downstream validation and reporting. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use pandas `min`, `max`, and `shape` attributes; cast to Python native types. |

#### 8. Persist the CSV string and metadata to a temporary storage location (e.g., `/tmp/cross_asset_data.csv`) and register the file path in a workflow context dictionary for downstream nodes that may need to read the raw file.

| Category | Details |
| --- | --- |
| **Reason** | Avoids passing large strings through in‑memory structures and enables `align_and_clean_data` to stream the file efficiently. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Open file in write mode, write `csv_data`; update `workflow_context['cross_asset_path'] = '/tmp/cross_asset_data.csv'`. |

#### 9. Return the five output fields (`csv_data`, `asset_names`, `start_date`, `end_date`, `row_count`) as a JSON‑compatible dictionary to the orchestration engine.

| Category | Details |
| --- | --- |
| **Reason** | Conforms to the node's declared `output_structure` and enables downstream nodes to consume the data directly. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Construct `output = { 'csv_data': csv_data, 'asset_names': asset_names, 'start_date': start_date, 'end_date': end_date, 'row_count': row_count }` and emit via the platform's `return_output(output)` call. |


---

## fetch_price_data

### Description
Download historical price series for the primary asset and any directly traded instruments.

### Implementation Plan

#### 1. Parse the `list_data_sources` output to locate the entry that describes the primary asset's price history (e.g., "Price History: Bloomberg, daily, ticker=SPY").

| Category | Details |
| --- | --- |
| **Reason** | The downstream fetch must know which provider, ticker, and frequency to query; the parent node only supplies a plain list of strings. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use regex pattern matching to extract provider name, ticker symbol, and frequency. Store these in variables `provider`, `ticker`, `frequency`. Validate that `frequency` equals "daily"; if not, raise a configuration error. |

#### 2. Map the identified provider to a concrete data‑access library or API client (e.g., Bloomberg → `blpapi`, Yahoo Finance → `yfinance`, Alpha Vantage → HTTP REST).

| Category | Details |
| --- | --- |
| **Reason** | Different providers have distinct authentication, rate‑limit, and data‑format requirements; abstracting this mapping enables a modular fetch implementation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a provider‑lookup dictionary. For each supported provider, define: authentication method, request function signature, and any required third‑party SDK. If the provider is unsupported, fallback to a generic CSV download if a URL is supplied. |

#### 3. Compute the exact 10‑year date window: `end_date = yesterday (UTC)`, `start_date = end_date - 10 years`. Adjust for market calendar (exclude weekends/holidays).

| Category | Details |
| --- | --- |
| **Reason** | The prompt explicitly requests the last 10 years of daily data; precise bounds avoid off‑by‑one errors and ensure alignment with downstream calendar merging. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use Python's `pandas.tseries.offsets.DateOffset(years=10)` or `datetime` arithmetic. Generate a list of trading days via `pandas_market_calendars` for the primary asset's exchange. |

#### 4. Issue the data request to the selected provider using the determined `ticker`, `start_date`, `end_date`, and daily frequency. Implement pagination or batch requests if the provider limits the number of rows per call.

| Category | Details |
| --- | --- |
| **Reason** | Historical OHLCV data for 10 years can exceed API limits; handling pagination guarantees complete retrieval. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For Bloomberg: use `blpapi` with `HistoricalDataRequest`. For Yahoo Finance: call `yfinance.download(ticker, start=start_date, end=end_date, interval='1d')`. Loop until all dates are received, respecting rate‑limit sleep intervals (e.g., 1‑second pause). |

#### 5. Normalize the raw response into a canonical DataFrame with columns exactly named `Date`, `Open`, `High`, `Low`, `Close`, `Volume`. Convert all numeric columns to `float` (price) and `int` (volume). Ensure `Date` is a `datetime64[ns]` object.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect clean, consistently typed arrays; mismatched column names or dtypes cause merge failures later. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Rename columns using a mapping dict, e.g., `{'Adj Close': 'Close'}` if present. Apply `astype(float)` to price columns and `astype(int)` to volume. Use `pd.to_datetime` for dates, then `dt.strftime('%Y-%m-%d')` for string output. |

#### 6. Handle missing trading days (e.g., holidays) by ensuring the DataFrame contains a row for every business day in the date window. If a date is missing, insert a row with `NaN` values for OHLCV.

| Category | Details |
| --- | --- |
| **Reason** | Later alignment (`align_and_clean_data`) assumes a common calendar; explicit missing rows allow forward‑fill logic to operate correctly. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Create a full date range `pd.date_range(start_date, end_date, freq='B')`. Reindex the DataFrame to this index, using `np.nan` for missing values. |

#### 7. Sort the DataFrame by `Date` ascending and drop any rows that still contain `NaN` after reindexing if the business rule is to exclude incomplete days.

| Category | Details |
| --- | --- |
| **Reason** | Consistent chronological order is required for time‑series feature engineering; eliminating rows with missing data simplifies later processing. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `df.sort_values('Date', inplace=True)`. Optionally `df.dropna(inplace=True)` if policy dictates; otherwise keep NaNs for forward‑fill later. |

#### 8. Extract the columns into the output list structures preserving the chronological order: `dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()`, `opens = df['Open'].tolist()`, etc.

| Category | Details |
| --- | --- |
| **Reason** | The node's output schema demands separate lists rather than a tabular object; converting now avoids extra transformations downstream. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use pandas `.tolist()` on each column. Cast `volumes` explicitly to `int` with `df['Volume'].astype(int).tolist()`. |

#### 9. Validate the final payload: check that `len(dates) == len(opens) == …` and that the count matches the expected number of trading days (~252 * 10 = 2520). Log a warning if the count deviates by more than 2%.

| Category | Details |
| --- | --- |
| **Reason** | Early detection of incomplete fetch prevents silent data quality issues that would cascade into model training. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Compute `expected_days = len(pd.date_range(start_date, end_date, freq='B'))`. Compare lengths; if `abs(len(dates) - expected_days) / expected_days > 0.02`, emit a logger warning. |

#### 10. Record provenance metadata (provider name, ticker, request timestamps, any adjustments made) into a structured log file for auditability.

| Category | Details |
| --- | --- |
| **Reason** | Traceability is essential for compliance and reproducibility of the quant pipeline. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Append a JSON entry to `data_fetch_log.json` with fields `provider`, `ticker`, `start_date`, `end_date`, `row_count`, `adjustments`. |

#### 11. Return the six output fields (`dates`, `opens`, `highs`, `lows`, `closes`, `volumes`) as defined in the node's output structure.

| Category | Details |
| --- | --- |
| **Reason** | Completes the node's contract, enabling downstream nodes to consume the data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Package the lists into a dictionary matching the schema and output via the execution framework. |


---

## fetch_regime_indicator_data

### Description
Collect macro‑economic and market‑regime indicators (e.g., VIX, yield curve, PMI).

### Implementation Plan

#### 1. Identify regime indicators and their data sources from the `list_data_sources` output.

| Category | Details |
| --- | --- |
| **Reason** | The `list_data_sources` node provides the necessary information about the regime indicators to be fetched, including their source and frequency. This step ensures that we are using the correct indicators and data sources as defined by the user's strategy objectives. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the `data_sources` list from the output of the `list_data_sources` node. Filter for entries that are explicitly related to macro-economic and market-regime indicators. Extract the indicator name and data source details (e.g., provider, ticker). |

#### 2. Implement data fetching for each identified regime indicator.

| Category | Details |
| --- | --- |
| **Reason** | Different indicators may require different data fetching methods. Some may be available through APIs, while others might require web scraping or database access. Implementing individual methods increases flexibility and robustness. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each indicator, determine the appropriate data fetching method based on the data source details. Use libraries like `requests` for API calls and `BeautifulSoup` for web scraping. Implement error handling and retry mechanisms for each method. Consider using a data provider library like `yfinance` or `FredPy` for easy data retrieval when appropriate. For Quandl data, use the `quandl` package. For FRED data, use the `fredapi`. |

#### 3. Parse the data into a standardized format: Date and value.

| Category | Details |
| --- | --- |
| **Reason** | Data from different sources may be structured differently. Standardizing the data into a single format makes further processing easier and more reliable.  This facilitates alignment with the price data. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a function to parse the data returned from different data fetching methods into a consistent format: a list of (Date, Value) tuples. Handle different date formats and missing value representations appropriately. |

#### 4. Align all regime indicator time series to a common calendar.

| Category | Details |
| --- | --- |
| **Reason** | Regime indicators and price data might have different trading calendars (e.g., different holidays). Aligning them to a common calendar ensures that the data is comparable and that features are correctly calculated. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Choose the calendar from the `fetch_price_data` output as the reference calendar. For each regime indicator, resample the time series to the reference calendar, filling missing values using forward fill, and truncating values to start and end dates found from the `fetch_price_data` output.  If the price data's dates are explicitly available as a output (e.g `dates`), use them for alignment. Otherwise, analyze the `fetch_price_data` CSV string representation to extract start and end dates for relevant alignment and padding operations. |

#### 5. Create a Pandas DataFrame with 'Date' as the index and one column for each regime indicator. Ensure dates are stored as datetime objects.

| Category | Details |
| --- | --- |
| **Reason** | Pandas DataFrames provide efficient data manipulation and analysis capabilities. Using 'Date' as the index allows for easy time series operations. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Pandas DataFrame with the aligned regime indicator data and dates. Ensure the 'Date' column is set as the index and converted to datetime objects. The column names should reflect the indicator names as extracted in the first step. |

#### 6. Convert the DataFrame to a CSV string.

| Category | Details |
| --- | --- |
| **Reason** | The final output needs to be a CSV string as specified by the output structure. This format is easy to parse and use in subsequent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the `to_csv()` method of the Pandas DataFrame to convert it to a CSV string. The string should include the header row (column names) and the data rows. Set `index=True` to include the Date as the first column. |


---

## fetch_volatility_data

### Description
Retrieve realized and implied volatility metrics needed for forecasting.

### Implementation Plan

#### 1. Parse the output of the parent node **list_data_sources** to extract the provider name, dataset type, and update frequency for any implied‑volatility index (e.g., CBOE VIX, Bloomberg IVOL) that matches the primary asset.

| Category | Details |
| --- | --- |
| **Reason** | The volatility node must know which external feed supplies the implied volatility series; parsing ensures we reference the correct ticker/provider without hard‑coding. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the `data_sources` list, apply a regex pattern like `(?i)implied.*volatility.*: (.+?),` to capture the provider and symbol, store as `implied_vol_source`. |

#### 2. Fetch the primary asset’s daily closing price series using the same endpoint and parameters that **fetch_price_data** used (to guarantee identical date range and calendar).

| Category | Details |
| --- | --- |
| **Reason** | Realized volatility is derived from price returns; using the exact same series guarantees alignment with other feature tables downstream. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Issue an HTTP GET/POST request to the data vendor API (e.g., Bloomberg, Refinitiv) with parameters: ticker = primary asset, fields = Close, frequency = daily, start_date = earliest date from `list_data_sources`, end_date = latest date. Cache the response as a DataFrame `price_df` with columns `Date` and `Close`. |

#### 3. Calculate daily log returns: `r_t = ln(Close_t / Close_{t-1})` and then compute a 30‑day rolling standard deviation of these returns to obtain the realized volatility series.

| Category | Details |
| --- | --- |
| **Reason** | A 30‑day rolling standard deviation of returns is a standard proxy for realized volatility and matches the prompt specification. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Using pandas: `price_df['log_return'] = np.log(price_df['Close'] / price_df['Close'].shift(1))`; `price_df['realized_vol'] = price_df['log_return'].rolling(window=30).std()`; drop the first 30 rows where the window is incomplete. |

#### 4. Retrieve the implied‑volatility index series from the provider identified in step 1 for the exact same date range as `price_df`.

| Category | Details |
| --- | --- |
| **Reason** | Implied volatility must be aligned day‑for‑day with realized volatility to be used later in feature engineering and model training. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Construct a second API request to the implied‑vol provider (e.g., `GET /v1/indices/{symbol}?frequency=daily&start={start}&end={end}`), parse JSON/CSV response into a DataFrame `implied_df` with columns `Date` and `ImpliedVol`. Ensure timezone normalization to UTC. |

#### 5. Merge `price_df` (containing `realized_vol`) and `implied_df` on the `Date` column using an inner join to keep only dates where both series are present.

| Category | Details |
| --- | --- |
| **Reason** | A clean inner join guarantees no missing values downstream, simplifying the cleaning step in `align_and_clean_data`. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | `merged_df = pd.merge(price_df[['Date','realized_vol']], implied_df[['Date','ImpliedVol']], on='Date', how='inner')`. |

#### 6. Validate the merged series: confirm that `merged_df` contains no NaNs, that the length matches the expected calendar (derived from the longest parent series), and that all dates are in ISO‑8601 (`YYYY-MM-DD`) format.

| Category | Details |
| --- | --- |
| **Reason** | Early validation prevents downstream failures in `align_and_clean_data` and ensures data integrity. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | If any NaNs are found, raise an exception with a descriptive error; otherwise, convert the `Date` column to string format with `merged_df['Date'] = merged_df['Date'].dt.strftime('%Y-%m-%d')`. |

#### 7. Populate the output fields: `dates` = list(merged_df['Date']), `realized_vol` = list(merged_df['realized_vol'].astype(float)), `implied_vol` = list(merged_df['ImpliedVol'].astype(float)).

| Category | Details |
| --- | --- |
| **Reason** | Mapping the DataFrame columns to the typed output structure satisfies the contract of the node. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use Python list comprehension or `to_list()` method; ensure float conversion to match `PrimitiveType.LIST_FLOAT`. |

#### 8. Log a concise summary (e.g., number of rows, date range, source identifiers) to a standard logging facility for auditability.

| Category | Details |
| --- | --- |
| **Reason** | Traceability is essential for production pipelines and for debugging any mismatches later in the DAG. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | `logger.info(f"Fetched volatility data: {len(dates)} rows, from {dates[0]} to {dates[-1]}, source={implied_vol_source}")`. |


---

## final_deliverables_package

### Description
Package the strategy dossier, code snippets, monitoring plan, and any configuration files for hand‑off.

### Implementation Plan

#### 1. Extract the compiled strategy markdown (full_document_markdown) from the output of **compile_strategy_documentation** and write it to a file named **Strategy_Document.md**.

| Category | Details |
| --- | --- |
| **Reason** | The strategy dossier is the central deliverable that stakeholders will review; storing it as a markdown file preserves formatting and allows easy viewing. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the string field `full_document_markdown`; open a file handle with UTF‑8 encoding; write the string verbatim; close the file. Ensure newline consistency (LF). |

#### 2. Generate a runnable Python script **model_code.py** that contains: (a) import statements for the selected model's libraries, (b) a function `load_model()` that deserializes the model (placeholder code), (c) a function `predict(features)` that returns model predictions, and (d) a `if __name__ == "__main__"` block demonstrating a mock inference.

| Category | Details |
| --- | --- |
| **Reason** | Providing executable model code enables downstream engineers to quickly load and test the model without re‑implementing logic. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use the `best_model_identifier` from **select_best_model** (available via upstream nodes) to select import statements (e.g., `import xgboost as xgb` or `import torch`). Insert stub code with clear TODO comments where model artefacts would be loaded. Write to `model_code.py` with proper indentation and PEP‑8 compliance. |

#### 3. Create **requirements.txt** by aggregating the Python packages required for the strategy: core data libraries (pandas, numpy), modelling libraries (xgboost, torch, scikit‑learn), back‑testing library (backtrader or zipline), and any auxiliary packages (PyYAML, shap).

| Category | Details |
| --- | --- |
| **Reason** | A complete requirements file guarantees reproducibility of the environment across development, staging, and production. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Compose a list of strings `<package>==<latest_version>`; versions can be pinned using `import pkg_resources; pkg_resources.get_distribution(pkg).version`. Write each entry on a new line to `requirements.txt`. |

#### 4. Serialize the monitoring configuration into **monitoring_plan.md** by transforming the output fields of **create_monitoring_plan** (`daily_live_metrics`, `alert_thresholds_metrics`, `alert_thresholds_values`, `retraining_schedule`) into a markdown document with sections: *Daily Live Metrics*, *Alert Thresholds*, and *Retraining Schedule*.

| Category | Details |
| --- | --- |
| **Reason** | Stakeholders need a human‑readable specification of operational monitoring; markdown is both readable and version‑controllable. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate over `daily_live_metrics` to build a bullet list. For alerts, zip `alert_thresholds_metrics` and `alert_thresholds_values` to produce a table. Append the free‑form `retraining_schedule` as a numbered list. Write the assembled markdown string to `monitoring_plan.md`. |

#### 5. Construct **config.yml** containing key runtime parameters: asset universe, risk control thresholds, model identifier, and back‑test settings. Pull values from the following upstream nodes: **define_strategy_objectives** (asset list, holding period), **design_risk_controls** (risk_control_names, risk_control_thresholds), **select_best_model** (best_model_identifier), and **setup_backtest_environment** (initial_capital, slippage_bps, commission_pct, rebalance_frequency).

| Category | Details |
| --- | --- |
| **Reason** | A YAML configuration centralises all tunable parameters, simplifying deployment and future adjustments. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Create a nested Python dictionary matching the desired hierarchy, e.g., `strategy: { assets: [...], holding_period: X }`, `risk: { controls: [{name:..., threshold:...}, ...] }`, `model: { id: ..., parameters: {} }`, `backtest: { capital: ..., slippage_bps: ..., commission_pct: ..., rebalance: ... }`. Use `yaml.safe_dump` with `default_flow_style=False` to output to `config.yml`. |

#### 6. Assemble the **manifest_files** list in the exact order required by the prompt: `["Strategy_Document.md", "model_code.py", "requirements.txt", "config.yml", "monitoring_plan.md"]`.

| Category | Details |
| --- | --- |
| **Reason** | The manifest must reflect the ordering defined in the specification to avoid downstream parsing errors. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Create a Python list literal with the five filenames in the specified order. |

#### 7. Generate the **manifest_descriptions** list, aligning one‑to‑one with `manifest_files`. Use concise sentences (≤ 30 words) summarising each file’s purpose, e.g., "Comprehensive markdown strategy dossier covering overview, data, model, risk, execution, backtest and checklist."

| Category | Details |
| --- | --- |
| **Reason** | Providing clear descriptions aids auditors and automated documentation tools when unpacking the archive. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Define a list of five strings matching the order of `manifest_files`; ensure each description is unique and accurately reflects the file content. |

#### 8. Set `package_type` to the literal string **"zip"** and `is_ready_for_handoff` to **true** after performing a validation step: (a) confirm all five files exist on disk, (b) verify each file size > 0 bytes, (c) optionally compute a SHA‑256 checksum for each and log it.

| Category | Details |
| --- | --- |
| **Reason** | Explicitly marking the package as ready only after validation prevents incomplete hand‑offs and provides traceability. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `os.path.isfile` and `os.path.getsize` for existence/size checks; raise an exception if any check fails. If all pass, assign `is_ready_for_handoff = True`. Record checks in a log file for audit. |

#### 9. Optionally create an in‑memory ZIP archive (using `io.BytesIO` and `zipfile.ZipFile`) that contains the five files, but **do not** write the archive to disk – the manifest fields are sufficient for downstream agents that will perform the actual archiving.

| Category | Details |
| --- | --- |
| **Reason** | Providing a ready‑to‑use archive object can speed up later stages without violating the current node’s responsibility of only describing the manifest. |
| **Impact** | LOW |
| **Complexity** | MEDIUM |
| **Method** | Instantiate a `BytesIO` buffer, add each file via `ZipFile.writestr(filename, file_contents)`, then close the zip. Store the buffer reference if needed for downstream consumption (not part of the output schema). |


---

## list_data_sources

### Description
Identify all external datasets required for price action, cross‑asset correlation, regime detection, and volatility forecasting.

### Implementation Plan

#### 1. Define a dictionary of potential data sources categorized by the analysis they support (price action, cross-asset correlation, regime detection, volatility forecasting). This will act as a knowledge base for required datasets.

| Category | Details |
| --- | --- |
| **Reason** | Provides a structured way to identify the necessary data sources based on the strategy's requirements. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python dictionary where keys are categories ('price_action', 'cross_asset', 'regime_detection', 'volatility_forecasting') and values are lists of potential data sources with provider information. EXAMPLE: {'price_action': [{'dataset': 'Price History', 'provider': 'Bloomberg', 'frequency': 'daily'}]} |

#### 2. Access the 'define_strategy_objectives' node's output, specifically the 'asset_universe' and the 'primary_tradable_asset' fields.

| Category | Details |
| --- | --- |
| **Reason** | The asset universe dictates which cross-asset data will be considered and the primary tradable asset is the focus of price action and volatility analysis. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Retrieve the 'asset_universe' (LIST_STR) and 'primary_tradable_asset' (STR) output variables from the 'define_strategy_objectives' node. |

#### 3. Based on the 'primary_tradable_asset', identify the primary data source for price history.

| Category | Details |
| --- | --- |
| **Reason** | Price history is fundamental. The selected asset determines the specific data source required. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'price_action'. Select the 'Price History' source and tailor it to the 'primary_tradable_asset'. Generate string output 'Price History: [Provider], [Frequency]' (e.g. 'Price History: Bloomberg, daily'). |

#### 4. For each asset in 'asset_universe' *other* than the primary asset, identify appropriate providers of price data for computing cross-asset correlations.

| Category | Details |
| --- | --- |
| **Reason** | Cross-asset correlation requires price data for each asset under consideration within the strategy. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate through the 'asset_universe', excluding the 'primary_tradable_asset'.  For each secondary asset, check under cross_asset in the data souce dictionary for price data options. Generate strings of the format 'Price History for [Asset]: [Provider], [Frequency]' (e.g., 'Price History for SPY: Yahoo Finance, daily'). |

#### 5. Identify data sources for regime indicators necessary for regime detection. Commonly used indicators include VIX, yield curve data, and PMI.

| Category | Details |
| --- | --- |
| **Reason** | Regime detection relies on macro-economic and market indicators. Accessing these data sources is essential. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'regime_detection'. Generate strings for each indicator of the format '[Indicator Name]: [Provider], [Frequency]' (e.g., 'VIX: CBOE, daily', 'US 10Y-2Y Yield Spread: FRED, daily', 'PMI: ISM, monthly'). |

#### 6. Identify data sources for volatility forecasting, including implied volatility indices and potentially realized volatility data (if available).

| Category | Details |
| --- | --- |
| **Reason** | Volatility forecasting requires volatility data.  Having sources defined beforehand expedites retrieval. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the dictionary of potential data sources under 'volatility_forecasting'. Generate strings for each source of the format '[Dataset Name]: [Provider], [Frequency]' (e.g., 'VIX: CBOE, daily', 'Realized Volatility: Bloomberg, daily'). |

#### 7. Compile all identified data source strings into a single list, ensuring no duplicates. This list will be assigned to the 'data_sources' output variable.

| Category | Details |
| --- | --- |
| **Reason** | A unified list promotes efficient data retrieval in subsequent nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a Python list. Append the data source string from price history, cross-asset price data, regime indicators, and volatility data while removing duplicates. Assign generated list to 'data_sources'. |


---

## run_backtest

### Description
Execute the backtest over the test period and record performance timeseries.

### Implementation Plan

#### 1. Instantiate the backtesting engine using settings from `setup_backtest_environment`.

| Category | Details |
| --- | --- |
| **Reason** | This step initializes the backtesting framework with crucial parameters like initial capital, commission, slippage, rebalance frequency, and risk controls, enabling realistic simulations. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a BacktestingEngine class. Read the `initial_capital` (float), `slippage_bps` (float), `commission_pct` (float), `rebalance_frequency` (str), `risk_controls_summary` (List of str), and `risk_control_enforcement_method` (str) from the `setup_backtest_environment` output. Pass them as arguments to the BacktestingEngine's constructor. |

#### 2. Load the cleaned data from `align_and_clean_data` to feed the backtesting engine as a DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The cleaned data provides the historical price data and features to simulate the trading strategy over time. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Access the `cleaned_data_csv` output of the `align_and_clean_data` node. Convert the CSV formatted data into a Pandas DataFrame using `pd.read_csv()`. The `Date` column should become the index of data frame. |

#### 3. Load best model saved in previous step `select_best_model`

| Category | Details |
| --- | --- |
| **Reason** | We need the best model found previously in order to simulate it in the backtest. So we load the model and use it later. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | The `best_model_identifier` from the output of node `select_best_model` indicates which model to load and use for backtesting. |

#### 4. Implement the core backtesting loop: Iterate through each day in the test set of cleaned data obtained from `split_dataset`.

| Category | Details |
| --- | --- |
| **Reason** | This loop simulates the trading strategy's decision-making process on each day, allowing us to observe its performance over time. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | For each day: (1) Fetch the current feature vector. (2) Generate a trading signal using the loaded model and the current feature vector. (3) Enforce risk controls as defined in `setup_backtest_environment`, using `risk_controls_summary` and `risk_control_enforcement_method` to guide the enforcement. (4) Calculate the order size. (5) Execute the trade, accounting for slippage and commission. (6) Update portfolio positions and capital. (7) Implement rebalancing according to `rebalance_frequency` from `setup_backtest_environment.` |

#### 5. Record the daily equity and executed trades within the backtesting loop so that they can be persisted later

| Category | Details |
| --- | --- |
| **Reason** | This record keeps track of all trades and daily changes in equity, which are key elements for the evaluation of backtest performance. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Daily store the current ‘equity’ value after the execution of each trade. Keep track of the ‘Date’, ‘Symbol’, ‘Quantity’, ‘Price’ and ‘PnL’ of each trade executed. |

#### 6. Format the daily equity curve as a CSV string.

| Category | Details |
| --- | --- |
| **Reason** | The CSV format provides a standard and easily accessible representation of the equity curve for further analysis and visualization. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Convert the recorded daily equity data (Date and Equity) into a Pandas DataFrame. Then, use the `to_csv()` method to generate a CSV formatted string and store in the equity_curve_csv output field. |

#### 7. Format the trades log as a CSV string.

| Category | Details |
| --- | --- |
| **Reason** | The CSV format allows for simple sharing and processing of trade information. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Create a Pandas DataFrame using the `Date`, `Symbol`, `Quantity`, `Price`, and `PnL` data that was tracked within the backtesting loop. Finally, use the DataFrame's `to_csv()` method to create a CSV formatted string. This CSV string needs to be placed into the `trades_log_csv` output field. |

#### 8. Generate textual summary of backtest execution.

| Category | Details |
| --- | --- |
| **Reason** | This summary provides a quick overview of the backtest, including key metrics and any warnings encountered. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Record the runtime of the backtest. Also log any warnings encountered during the backtesting process (e.g., risk control violations, data issues). Construct a string containing the runtime and any warnings, and assign it to the `summary_message` output field. |

#### 9. Set `backtest_success` to True if the backtest completed without runtime errors, otherwise set it to False.

| Category | Details |
| --- | --- |
| **Reason** | This boolean flag indicates the overall success of the backtest execution. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | By default, set the `backtest_success` to True. If any exception is raised during the backtesting loop (e.g., due to data issues or risk control violations), catch it and set `backtest_success` to False. Also, store the error message to the `summary_message`. |


---

## select_best_model

### Description
Pick the model with the highest risk‑adjusted performance according to a predefined criterion.

### Implementation Plan

#### 1. Retrieve candidate model performance metrics from the 'evaluate_models' node output.

| Category | Details |
| --- | --- |
| **Reason** | The `evaluate_models` node provides the necessary performance metrics (Sharpe Ratio, Max Drawdown, and Annualized Return) for each candidate model to determine the best performing one. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Access the `candidate_models`, `sharpe_ratios`, `max_drawdowns`, and `annualized_returns` lists from the `evaluate_models` node's output. |

#### 2. Implement a selection criterion based on Sharpe ratio and maximum drawdown, prioritizing Sharpe Ratio subject to a Max Drawdown threshold.

| Category | Details |
| --- | --- |
| **Reason** | The prompt specifies selecting the model with the 'best combination of Sharpe and low max drawdown'. A sensible approach is to maximize the Sharpe Ratio while ensuring the Max Drawdown is below a predefined risk tolerance threshold.  This reflects a risk-adjusted return perspective. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Define a `max_drawdown_threshold` (e.g., 0.15 for 15%). Iterate through the models. If a model's Max Drawdown is *less than or equal to* the `max_drawdown_threshold`, store it in a list of valid model candidates. From these valid model candidates, choose the model with the highest Sharpe Ratio. |

#### 3. Handle the case where no model satisfies the risk tolerance threshold (max drawdown constraint).

| Category | Details |
| --- | --- |
| **Reason** | It's possible that none of the candidate models meets the Max Drawdown threshold, especially if the financial climate was particularly turbulent during backtesting.  The strategy should degrade gracefully if no model meets the hard constraints. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | If no model satisfies the `max_drawdown_threshold`, select the model with the absolute LOWEST max drawdown. If all the models have very high drawdowns, choose one that has a 'reasonable' Sharpe Ratio. If even that is not avaialble, return null/None for all outputs. Log a warning message to indicate this exceptional case. |

#### 4. Extract the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and 'annualized_return' for selected best model.

| Category | Details |
| --- | --- |
| **Reason** | The output structure requires the model's identifier and its key metrics. This step formats the selected values into the defined output structure. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | After identifying the best model index, retrieve the corresponding values from the `candidate_models`, `sharpe_ratios`, `max_drawdowns`, and `annualized_returns` lists. Store the values into output variables named: `best_model_identifier`, `sharpe_ratio`, `max_drawdown`, and `annualized_return` |

#### 5. Return the 'best_model_identifier', 'sharpe_ratio', 'max_drawdown', and 'annualized_return'.

| Category | Details |
| --- | --- |
| **Reason** | Deliver required data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return the variables created above. The return types must be enforced with exception handling or type coercion to meet the requested output structure types. |


---

## setup_backtest_environment

### Description
Configure a backtesting engine with data, model, risk controls, and transaction cost assumptions.

### Implementation Plan

#### 1. Define the initial capital for the backtest. A reasonable starting point is 1,000,000.00, but this can be adjusted based on the desired scale and risk profile of the strategy.

| Category | Details |
| --- | --- |
| **Reason** | The initial capital is a fundamental parameter that determines the trading size and affects performance metrics like Sharpe ratio and drawdown. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Set the `initial_capital` to 1000000.00. Consider making this configurable via a parameter. |

#### 2. Implement a slippage model. A simple model representing the execution cost is to assume a fixed slippage of 0.5 basis points (0.005%).

| Category | Details |
| --- | --- |
| **Reason** | Slippage accounts for the difference between the expected and actual execution price, especially for large orders or illiquid assets. It provides a more realistic backtest environment. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Set `slippage_bps` to 0.005. Model slippage linearly proportional to trade size for increased realism within the backtesting engine. |

#### 3. Implement a commission model. A standard commission rate is 0.1% per trade (0.001).

| Category | Details |
| --- | --- |
| **Reason** | Commissions are trading costs charged by brokers, which need to be accounted for in the backtest. This impacts the overall profitability. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Set the `commission_pct` to 0.001.  Model this as a percentage of the trade value incurred at both entry and exit. |

#### 4. Define the rebalancing frequency. Common choices are 'daily', 'weekly', or 'monthly'. Choose based on the strategy's typical holding period and desired turnover.

| Category | Details |
| --- | --- |
| **Reason** | Rebalancing ensures that the portfolio maintains its desired asset allocation and risk profile. The frequency affects transaction costs and tracking error. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Set `rebalance_frequency` to 'daily'. Add input validation to ensure allowed values are only 'daily', 'weekly', or 'monthly'. |

#### 5. Extract the list of risk control rules from the `design_risk_controls` node output. The `risk_control_names`, `risk_control_thresholds`, and `risk_control_formulas` are mapped to a human-readable string and stored in `risk_controls_summary` list.

| Category | Details |
| --- | --- |
| **Reason** | This step prepares the risk control information for reporting and integration into the backtesting engine. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate through risk controls from the dependency node `design_risk_controls`. Format each control info a string. Example: `max_gross_exposure 20%`. Construct the output list `risk_controls_summary`. |

#### 6. Define the risk control enforcement method. Choose a method such as 'pre-trade check' or 'post-trade check'.

| Category | Details |
| --- | --- |
| **Reason** | The enforcement method determines how risk controls are applied during the simulation. 'Pre-trade check' aborts trades that violate risk limits, while 'post-trade check' may trigger corrective actions. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Set `risk_control_enforcement_method` to 'pre-trade check that aborts orders violating any rule'. If post-trade, provide method to reduce position size if any risk limit is breached post order execution. |

#### 7. Integrate the cleaned data from the `align_and_clean_data` node. The cleaned data will be used as the price feed for the backtesting engine. CSV format is available in `cleaned_data_csv`.

| Category | Details |
| --- | --- |
| **Reason** | This ensures the backtest uses a consistent and reliable data source, free of missing values and properly aligned for accurate simulation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Parse data in `cleaned_data_csv` and feed into backtest. Handle potential parse errors. |

#### 8. Integrate the selected best model from the `select_best_model` node. The `best_model_identifier` specifies the identifier of the model to load and use during backtesting.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures the backtest reflects the expected performance of the selected model. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `best_model_identifier` to load the persisted model and use it when generating trading signals in the backtesting engine. This assumes a model persistence/loading mechanism is available external to the backtest function. |

#### 9. Implement the chosen risk controls within the backtesting engine. The risk control parameters are from the `design_risk_controls` node.

| Category | Details |
| --- | --- |
| **Reason** | Enforcing risk controls accurately during backtesting is critical to estimating the strategy's risk-adjusted performance. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | For each risk control extracted in previous step from node `design_risk_controls`, implement the corresponding `risk_control_formulas` with the respective `risk_control_thresholds`. Implement checks specified in the `risk_control_enforcement_method`. |


---

## specify_model_architecture

### Description
Choose a concrete predictive model type (e.g., Gradient Boosting + LSTM ensemble).

### Implementation Plan

#### 1. Define the specific model ensemble: Gradient Boosting Machine (GBM) followed by a Long Short-Term Memory (LSTM) network.

| Category | Details |
| --- | --- |
| **Reason** | This ensemble combines the strengths of GBM for feature importance and non-linear relationships with LSTM's ability to capture temporal dependencies in financial time series, fitting the strategy objectives. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Choose GBM from the scikit-learn library and LSTM from TensorFlow/Keras. Use a sequential model construction in Keras for easy stacking. |

#### 2. Determine the input shape for the ensemble. Assume a time series of N features over a window of T days. Hence, the input shape will be (T, N). The T value will likely be decided based on the asset's holding period as derived from the output of `define_strategy_objectives`

| Category | Details |
| --- | --- |
| **Reason** | The input shape is critical for both models. LSTM needs a time series of data. Features are generated in prior nodes (compute_price_action_features, compute_cross_asset_features, compute_regime_features, compute_volatility_features), so shape N is informed by the aggregate features. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Inspect the features computed by the previous nodes (price action, cross-asset, regime, volatility) to determine the total number of features (N). Set T based on a fraction of the `holding_period_days` from `define_strategy_objectives`. For instance if holding period is 60 days, then T can be set to 30 days. |

#### 3. Specify that the Gradient Boosting Machine will process the feature matrix first. It will output feature importance scores and potentially transformed features.

| Category | Details |
| --- | --- |
| **Reason** | GBM offers good feature engineering. Choosing GBM allows transforming existing features into a representation which improves the LSTM's performance. LSTM learns better from well-engineered, or pre-selected features. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Train GBM to produce a prediction. Extract the relative feature importances. Optionally use Tree-based Feature Selection/Transformation techniques from scikit-learn before inputting to LSTM. |

#### 4. Describe how the predictions from GBM and LSTM will be combined using a stacking approach. GBM output are treated as additional features and input into LSTM, or averaged together.

| Category | Details |
| --- | --- |
| **Reason** | Stacking enables the model to learn how to best combine information from each component, creating a more robust and accurate prediction. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement stacking/averaging in Keras. For the staking approach, the features from the GBM predictions are combined with the original set of features and used together as input features into the LSTM network. Train stacked LSTM to combine both feature types. |

#### 5. Generate a textual `model_ensemble_description` summarizing the chosen architecture, including the algorithm for each component, input shape, and prediction combination method. Respect the 200 word limit.

| Category | Details |
| --- | --- |
| **Reason** | The text description provides human-readable documentation of the model ensemble. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Create a formatted string combining the model components, input shape, and prediction combination method.  Use f-strings for string formatting and truncate if string exceeds 200 words or less. |

#### 6. Populate the `model_components` list with string names, e.g., ['Gradient Boosting Machine', 'LSTM'].

| Category | Details |
| --- | --- |
| **Reason** | Provides a clear and structured list of separate model types. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Create a list literals. |

#### 7. Generate a clear representation of `input_shape` as a string. E.g., '(30, 15)' representing 30 days of 15 features.

| Category | Details |
| --- | --- |
| **Reason** | Allows downstream systems to automatically configure the data based on expected form. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Format N and T values derived in bullet 2 into a Tuple format for the string representation. |

#### 8. Create a textual description of ``prediction_combination_method``, explaining how component predictions are combined (e.g., 'Predictions from gradient boosting are averaged with LSTM predictions').

| Category | Details |
| --- | --- |
| **Reason** | Provides a downstream explanation of how final signal is generated from constituent models. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a text description of stackng, weighting or averaging depending on the specific implementation in bullet point 4. |


---

## split_dataset

### Description
Partition the feature matrix into training, validation, and test sets using a time‑based split.

### Implementation Plan

#### 1. Load the feature matrix CSV from the parent node (assemble_feature_matrix).

| Category | Details |
| --- | --- |
| **Reason** | The parent node provides the complete feature matrix that needs to be split into training, validation, and test sets. This is the input for this node's processing. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a CSV parsing library to load the `feature_matrix_csv` output from the `assemble_feature_matrix` node. Handle potential file reading errors. |

#### 2. Convert the loaded CSV data into a Pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Pandas DataFrames provide an efficient and easy-to-use structure for manipulating and splitting tabular data. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the `pd.read_csv()` function in Pandas to convert the CSV string to a DataFrame. Ensure the 'Date' column is correctly parsed as a datetime object. |

#### 3. Calculate the indices for splitting the DataFrame based on the specified proportions (60% training, 20% validation, 20% testing).

| Category | Details |
| --- | --- |
| **Reason** | The problem requires a specific time-based split, so we need to determine the row indices that correspond to these percentages of the total dataset length. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | 1. Get the total number of rows in the DataFrame using `len(df)`. 2. Calculate training set size: `train_size = int(len(df) * 0.6)`. 3. Calculate validation set size `validation_size = int(len(df) * 0.2)`. These sizes are used to slice the dataframe. Round down to integer values to avoid indexing errors. Also note that `test_size` is implicitly `len(df) - train_size - validation_size`. |

#### 4. Split the DataFrame into training, validation, and test sets using the calculated indices.

| Category | Details |
| --- | --- |
| **Reason** | This creates the subsets of the data that will be used for model training, validation, and testing, fulfilling the primary objective of the node. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use DataFrame slicing to create the three datasets: `train_df = df[:train_size]`, `validation_df = df[train_size:train_size + validation_size]`, and `test_df = df[train_size + validation_size:]`. Ensure that there are no overlaps between slices. |

#### 5. Convert each DataFrame subset back into a CSV-formatted string.

| Category | Details |
| --- | --- |
| **Reason** | The output structure requires the split datasets to be in CSV format. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the `df.to_csv()` function in Pandas for each of the three DataFrames (`train_df`, `validation_df`, `test_df`). Ensure `index=False` to avoid including the DataFrame index as a column in the CSV. |

#### 6. Store the CSV strings into the respective output variables: `train_csv`, `validation_csv`, and `test_csv`.

| Category | Details |
| --- | --- |
| **Reason** | This prepares the output data in the format expected by downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Assign the output of `df.to_csv()` for each DataFrame to the corresponding output variable (train_csv, validation_csv, test_csv). |

#### 7. Implement error handling throughout the process.

| Category | Details |
| --- | --- |
| **Reason** | To gracefully handle potential issues such as incorrect data formats, missing dependencies, and to provide informative error messages, robust error handling must be implemented. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `try...except` blocks to catch potential exceptions during CSV parsing, DataFrame manipulation, and file operations. Log errors and provide meaningful feedback. Handle edge cases where the input CSV might be empty or have missing values. |


---

## summarize_backtest_results

### Description
Produce a concise performance summary with key statistics and charts description.

### Implementation Plan

#### 1. Parse the `equity_curve_csv` output from the `run_backtest` node into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | Pandas DataFrames are well-suited for time series analysis and calculation of performance metrics. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `pandas.read_csv()` with the `Date` column as the index and parse the 'Date' column as datetime objects. Handle potential errors (e.g., invalid date formats) gracefully using try-except blocks and logging any issues.  The expected columns are 'Date' and 'Equity'. |

#### 2. Calculate daily returns from the equity curve. 

| Category | Details |
| --- | --- |
| **Reason** | Daily returns are needed to calculate the Sharpe ratio and generate the histogram of returns. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use `equity_curve['Equity'].pct_change()` to compute the daily returns. Handle the first `NaN` value (resulting from the percentage change) by filling it with zero or dropping it, depending if the backtest start at equity zero or not. |

#### 3. Calculate the annualized return.

| Category | Details |
| --- | --- |
| **Reason** | Annualized return is a standard performance metric for evaluating trading strategies. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Calculate the total return over the backtest period.  Then, annualize it using the formula: `(1 + total_return)**(252 / number_of_trading_days) - 1`. 252 is the average number of trading days in a year. Use `len(equity_curve)` to accurately count the trading days. |

#### 4. Calculate the Sharpe ratio.

| Category | Details |
| --- | --- |
| **Reason** | The Sharpe ratio measures risk-adjusted return. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Sharpe Ratio is calculated as: Annualized Return / Annualized Volatility. Where Annualized Volatility is the standard deviation of the returns multiplied by the square root of 252 (trading days in a year).  Use `daily_returns.std() * np.sqrt(252)` to get the annualized volatility. |

#### 5. Calculate the maximum drawdown.

| Category | Details |
| --- | --- |
| **Reason** | Max drawdown indicates the largest peak-to-trough decline during the backtest period and assesses risk. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Calculate the cumulative maximum equity value up to each point in time using `equity_curve['Equity'].cummax()`.  Then, calculate the drawdown as the percentage difference between the cumulative maximum and the current equity value: `(equity_curve['Equity'] - cumulative_max) / cumulative_max`.  The maximum drawdown is the minimum (most negative) value of the drawdown series.  Return the max drawdown as a negative number. |

#### 6. Parse the `trades_log_csv` output from the `run_backtest` node into a pandas DataFrame.

| Category | Details |
| --- | --- |
| **Reason** | The trades log is necessary to determine when to measure turnover. Also need to extract trade direction for win/loss calculation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Read the `trades_log_csv` string into a pandas DataFrame using `pd.read_csv()`.  Ensure the 'Date' column is parsed as dates. The expected columns are 'Date', 'Symbol', 'Quantity', 'Price', and 'PnL'. Implement error handling in case the data is malformed. |

#### 7. Calculate portfolio turnover. Assume a 1 month turnover period.

| Category | Details |
| --- | --- |
| **Reason** | Turnover indicates how frequently the portfolio is rebalanced. |
| **Impact** | MEDIUM |
| **Complexity** | HIGH |
| **Method** | First, the total value traded each month must be computed. Then, divide that by the average portfolio value for the month. Average these monthly turnover values to get overall portfolio turnover.  This requires calculating the portfolio value at the end of each day from `equity_curve_csv`, finding the trade values from `trades_log_csv`, and correctly aggregating turnover for each monthly period. Use resample('M') to group trades into monthly buckets. Implment handling for division by zero (when the average portfolio value is zero). The `turnover` output should represent the average monthly turnover, expressed as a decimal. E.g., 0.30 for 30% turnover per month. |

#### 8. Calculate the win rate.

| Category | Details |
| --- | --- |
| **Reason** | Win rate is calculated by checking how many trades had a positive return. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Extract the PnL and check how many values are positive using boolean indexing into Pandas.  Calculate the win rate as the number of winning trades divided by the total number of trades. `trades_log['PnL'] > 0 `. Return as fraction from 0 to 1. |

#### 9. Generate a description of histogram for daily returns.

| Category | Details |
| --- | --- |
| **Reason** | Used to visualize return distribution. |
| **Impact** | MEDIUM |
| **Complexity** | HIGH |
| **Method** | Generate a histogram of daily returns using `matplotlib.pyplot.hist()`.  Analyze the histogram to identify skewness, kurtosis, and the presence of outliers.  Write a markdown description summarizing these observations. The description should include: general shape of the distribution (normal, skewed), location of the mean return, presence of outliers. Store the generated string in the `histogram_description` output. |

#### 10. Generate a description for the turnover time series chart.

| Category | Details |
| --- | --- |
| **Reason** | Used to visualize trading activity. |
| **Impact** | MEDIUM |
| **Complexity** | HIGH |
| **Method** | The turnover has already been calculated on a monthly basis. Output the turnover values on a time series (`turnover_ts`). Write a markdown description highlighting any trends (increasing, decreasing, stable), spikes, or seasonality in the turnover. Analyze the relationship between turnover and strategy performance. Store the generated markdown string in the `turnover_chart_description` output. |

#### 11. Create a markdown report.

| Category | Details |
| --- | --- |
| **Reason** | Consolidates the statistics and chart descriptions for easy readability and integration with downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Combine the calculated statistics (annualized return, Sharpe ratio, max drawdown, turnover, win rate) and the chart descriptions (`histogram_description`, `turnover_chart_description`) into a markdown report. Use markdown headings and bullet points for clear formatting.  Include a title for the report: 'Backtest Performance Summary'. Store the complete markdown report in the `markdown_report` output. |


---

## train_models

### Description
Perform hyperparameter optimization on the training set and fit each candidate model.

### Implementation Plan

#### 1. Load training and validation datasets from the 'split_dataset' node.

| Category | Details |
| --- | --- |
| **Reason** | These datasets are essential for training and evaluating the candidate models during hyperparameter optimization. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a CSV parsing library (e.g., pandas in Python) to load the 'train_csv' and 'validation_csv' strings from the 'split_dataset' node into dataframes. Ensure the Date column, if present, is parsed correctly as a datetime object. |

#### 2. Load the hyperparameter grid from the 'define_hyperparameter_grid' node.

| Category | Details |
| --- | --- |
| **Reason** | The hyperparameter grid specifies the search space for hyperparameter optimization. It is crucial for determining the different hyperparameter combinations to test. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Parse the 'hyperparameter_grid_json' string from the 'define_hyperparameter_grid' node using a JSON parsing library (e.g., json in Python). Store the hyperparameter grids for both Gradient Boosting and LSTM models separately in dictionaries. |

#### 3. Implement a grid or random search algorithm.

| Category | Details |
| --- | --- |
| **Reason** | The prompt requests a hyperparameter search, and either grid search or random search will fulfill this requirement. Random search often performs better with high-dimensional hyperparameter spaces. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a random search.  For each model type (GB and LSTM), randomly sample hyperparameter combinations from the defined grid.  Use a fixed number of iterations (e.g., 50 for each model). Ensure sampled hyperparameters are within the specified ranges and are of the correct datatype (e.g., integer or float).  Store each hyperparameter combination in a list. |

#### 4. Train each candidate model on the training set.

| Category | Details |
| --- | --- |
| **Reason** | Training is essential for model fitting. Each model needs to learn the relationship between features and target from the training data. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each sampled hyperparameter combination, instantiate a Gradient Boosting model (e.g., from scikit-learn) or an LSTM model (e.g., from TensorFlow/Keras) with the corresponding hyperparameters. Train the model using the training data and the 'fit' method. Use appropriate loss functions and optimizers for each model type (e.g., mean squared error for regression problems). Implement early stopping based on the validation set performance to prevent overfitting. |

#### 5. Evaluate each trained model on the validation set.

| Category | Details |
| --- | --- |
| **Reason** | Evaluation on the validation set provides an unbiased estimate of the model's performance on unseen data. This is crucial for selecting the best hyperparameters. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | For each trained model, predict the target variable on the validation set. Calculate the Sharpe ratio and Root Mean Squared Error (RMSE) using the predicted values and the actual values from the validation set. Ensure proper calculation of Sharpe Ratio considering the risk-free rate (which may need to be a configurable parameter).  RMSE should be computed after scaling the predicted values back to the original scale of the target variable if scaling was applied during preprocessing. |

#### 6. Store hyperparameters, Validation Sharpe Ratios, and Validation RMSE for each candidate model.

| Category | Details |
| --- | --- |
| **Reason** | This information is needed to compare the performance of different models and select the best one. This table will then be used by the 'evaluate_models' node to decide on the best overall model |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create three lists: 'hyperparameters', 'validation_sharpe', and 'validation_rmse'.  For each trained model, store the hyperparameter combination (as a string), the validation Sharpe ratio, and the validation RMSE in the respective lists.  Consider using a standardized string format for the hyperparameters using JSON serialization |

#### 7. Return a table (represented as lists) containing Hyperparameters, ValidationSharpe, ValidationRMSE.

| Category | Details |
| --- | --- |
| **Reason** | This table is the final output, providing the summarized performance of all models. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Return the created lists 'hyperparameters', 'validation_sharpe', and 'validation_rmse' as the output of this node. Confirm that that number of elements in each list are identical, failing if not. Use appropriate error handling if model training fails to prevent exiting on the first failure. Instead, move on to the next model, storing a NaN for the validation metrics. |
