# compile_strategy_documentation PRD

## Description
Assemble all model, feature, risk, execution, and backtest artifacts into a single strategy dossier.


## Implementation Plan

### 1. Extract the best‑model metadata (best_model_identifier, sharpe_ratio, max_drawdown, annualized_return) from the `select_best_model` node and store it in a temporary JSON object for reuse across multiple sections.

| Category | Details |
| --- | --- |
| **Reason** | The model metadata drives the narrative for Strategy Overview and Model Architecture, ensuring consistency with the quantitative evaluation. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Call the `select_best_model` output, parse the four fields, and assign them to variables (e.g., bestModelId, bestSharpe, bestDD, bestAnnRet). |

### 2. Create the **Strategy Overview** markdown string using the variables from step 1 together with static strategy objectives (asset universe, holding period) retrieved from the `define_strategy_objectives` node (accessed via the global context). Include a bullet list of performance targets (target Sharpe, max drawdown, annualized return).

| Category | Details |
| --- | --- |
| **Reason** | Provides stakeholders with a concise executive summary that links the chosen model to business goals. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Template string with placeholders: `## Strategy Overview\n- Objective: …\n- Selected Model: ${bestModelId}\n- Expected Sharpe: ${bestSharpe}\n- Max Drawdown (limit): ${bestDD}\n- Expected Annual Return: ${bestAnnRet}`. |

### 3. Synthesize the **Data & Features** section by enumerating the four data pipelines (price, cross‑asset, regime, volatility) described in the DAG. Use concise bullet points to outline cleaning (forward‑fill, drop‑remaining NaNs) and list engineered features (log returns, moving averages, RSI, MACD, ATR, correlations, spreads, regime flags, GARCH forecasts, implied‑vol deltas).

| Category | Details |
| --- | --- |
| **Reason** | Even though the node does not directly depend on feature‑generation nodes, the documentation must describe the data foundation for reproducibility. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Hard‑code a markdown block based on known feature generation steps from `compute_price_action_features`, `compute_cross_asset_features`, `compute_regime_features`, and `compute_volatility_features`. Use markdown headings and bullet lists. |

### 4. Generate the **Model Architecture** markdown using the `bestModelId` from step 1 and the model description stored in `specify_model_architecture` (access via global context). Include input shape, component list (e.g., Gradient Boosting, LSTM), and the prediction combination method (e.g., weighted averaging).

| Category | Details |
| --- | --- |
| **Reason** | Provides technical readers with a clear view of the predictive engine that will be deployed. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Create a markdown template: `## Model Architecture\n- Model ID: ${bestModelId}\n- Components: …\n- Input Shape: …\n- Combination Method: …`. |

### 5. Construct the **Feature Importance** markdown table. Since explicit importance scores are not directly output by any parent, invoke the `analyze_feature_importance` node (even though not listed as a direct dependency) to retrieve `feature_names` and `importance_scores`. Render them as a pipe‑separated markdown table sorted descending by score. If the node is unavailable, fallback to a placeholder statement indicating that importance data will be added after model inspection.

| Category | Details |
| --- | --- |
| **Reason** | Feature importance is a key deliverable for model transparency; pulling from `analyze_feature_importance` ensures accurate rankings. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Call `analyze_feature_importance`, iterate over zipped lists, format each row as `| Feature | Importance |`, prepend header and alignment row. |

### 6. Build the **Risk Management** markdown by iterating over the three parallel arrays (`risk_control_names`, `risk_control_thresholds`, `risk_control_formulas`) returned by the `design_risk_controls` node. For each control, output a bullet with the name, threshold (as a human‑readable percentage), and the formula. Include a top‑level heading and a short description of portfolio‑ vs. position‑level controls.

| Category | Details |
| --- | --- |
| **Reason** | Clearly communicating the quantitative risk limits is essential for compliance and for the execution engine to enforce limits. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Loop index i over length of arrays, format: `- **${risk_control_names[i]}**: ${risk_control_thresholds[i]*100}% – `${risk_control_formulas[i]}`. |

### 7. Insert the **Execution Pseudocode** markdown exactly as emitted by the `draft_execution_logic` node (`execution_logic_pseudocode` field). Prepend a heading and a brief narrative explaining how the pseudocode maps to the risk controls defined earlier.

| Category | Details |
| --- | --- |
| **Reason** | The execution logic must be directly traceable to the risk controls and model signals; reusing the already‑generated pseudocode guarantees consistency. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Wrap the pseudocode string in a markdown fenced code block with language `python` or `pseudo`. |

### 8. Compose the **Backtest Results** markdown using the seven fields produced by the `summarize_backtest_results` node. Present key metrics in a markdown table, embed the histogram and turnover‑chart descriptions as bullet items, and include the full `markdown_report` content verbatim under a sub‑heading.

| Category | Details |
| --- | --- |
| **Reason** | Stakeholders need a concise performance snapshot together with visual insights; the `summarize_backtest_results` node already aggregates these stats. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Create a table: `| Metric | Value |` with rows for Annualized Return, Sharpe, Max Drawdown, Turnover, Win Rate. Then add sections: `### Charts` with bullet points using `histogram_description` and `turnover_chart_description`. Append `markdown_report`. |

### 9. Draft the **Implementation Checklist** markdown as a static ordered list covering: (a) Code deployment, (b) Config file creation, (c) Model serialization, (d) Risk‑control parameters upload, (e) Monitoring plan integration (reference `create_monitoring_plan` output), (f) Performance validation, (g) Documentation upload. Each item should include a checkbox placeholder `[ ]`.

| Category | Details |
| --- | --- |
| **Reason** | A checklist formalizes the hand‑off steps and reduces operational risk during production rollout. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Hard‑code the list: `- [ ] Deploy model code\n- [ ] Add config.yml ...`. |

### 10. Concatenate all eight section strings in the exact order required by the deliverable (Strategy Overview → Data & Features → Model Architecture → Feature Importance → Risk Management → Execution Pseudocode → Backtest Results → Implementation Checklist) into the final `full_document_markdown` field. Ensure each section begins with a level‑2 markdown heading (`##`). Add a top‑level title (`# Strategy Dossier`) at the very top.

| Category | Details |
| --- | --- |
| **Reason** | A single, ordered markdown file is the final artifact expected by downstream nodes (e.g., `final_deliverables_package`). |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | String concatenation with newline separators: `# Strategy Dossier\n\n${strategy_overview}\n\n${data_and_features}\n...`. |
