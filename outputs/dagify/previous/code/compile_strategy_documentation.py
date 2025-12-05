# -- PRD --
# 1. BULLET: Extract the best‑model metadata (best_model_identifier, sharpe_ratio,
#   max_drawdown, annualized_return) from the `select_best_model` node and
#   store it in a temporary JSON object for reuse across multiple sections.
#   Reason: The model metadata drives the narrative for Strategy Overview and Model
#           Architecture, ensuring consistency with the quantitative
#           evaluation.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Call the `select_best_model` output, parse the four fields, and assign them
#           to variables (e.g., bestModelId, bestSharpe, bestDD,
#           bestAnnRet).
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create the **Strategy Overview** markdown string using the variables from
#   step 1 together with static strategy objectives (asset universe, holding
#   period) retrieved from the `define_strategy_objectives` node (accessed
#   via the global context). Include a bullet list of performance targets
#   (target Sharpe, max drawdown, annualized return).
#   Reason: Provides stakeholders with a concise executive summary that links the
#           chosen model to business goals.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Template string with placeholders: `## Strategy Overview\n- Objective: …\n-
#           Selected Model: ${bestModelId}\n- Expected Sharpe:
#           ${bestSharpe}\n- Max Drawdown (limit): ${bestDD}\n- Expected
#           Annual Return: ${bestAnnRet}`.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Synthesize the **Data & Features** section by enumerating the four data
#   pipelines (price, cross‑asset, regime, volatility) described in the DAG.
#   Use concise bullet points to outline cleaning (forward‑fill,
#   drop‑remaining NaNs) and list engineered features (log returns, moving
#   averages, RSI, MACD, ATR, correlations, spreads, regime flags, GARCH
#   forecasts, implied‑vol deltas).
#   Reason: Even though the node does not directly depend on feature‑generation nodes,
#           the documentation must describe the data foundation for
#           reproducibility.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Hard‑code a markdown block based on known feature generation steps from
#           `compute_price_action_features`,
#           `compute_cross_asset_features`, `compute_regime_features`, and
#           `compute_volatility_features`. Use markdown headings and bullet
#           lists.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Generate the **Model Architecture** markdown using the `bestModelId` from
#   step 1 and the model description stored in `specify_model_architecture`
#   (access via global context). Include input shape, component list (e.g.,
#   Gradient Boosting, LSTM), and the prediction combination method (e.g.,
#   weighted averaging).
#   Reason: Provides technical readers with a clear view of the predictive engine that
#           will be deployed.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Create a markdown template: `## Model Architecture\n- Model ID:
#           ${bestModelId}\n- Components: …\n- Input Shape: …\n-
#           Combination Method: …`.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Construct the **Feature Importance** markdown table. Since explicit
#   importance scores are not directly output by any parent, invoke the
#   `analyze_feature_importance` node (even though not listed as a direct
#   dependency) to retrieve `feature_names` and `importance_scores`. Render
#   them as a pipe‑separated markdown table sorted descending by score. If
#   the node is unavailable, fallback to a placeholder statement indicating
#   that importance data will be added after model inspection.
#   Reason: Feature importance is a key deliverable for model transparency; pulling
#           from `analyze_feature_importance` ensures accurate rankings.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Call `analyze_feature_importance`, iterate over zipped lists, format each
#           row as `| Feature | Importance |`, prepend header and alignment
#           row.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Build the **Risk Management** markdown by iterating over the three parallel
#   arrays (`risk_control_names`, `risk_control_thresholds`,
#   `risk_control_formulas`) returned by the `design_risk_controls` node. For
#   each control, output a bullet with the name, threshold (as a
#   human‑readable percentage), and the formula. Include a top‑level heading
#   and a short description of portfolio‑ vs. position‑level controls.
#   Reason: Clearly communicating the quantitative risk limits is essential for
#           compliance and for the execution engine to enforce limits.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Loop index i over length of arrays, format: `-
#           **${risk_control_names[i]}**:
#           ${risk_control_thresholds[i]*100}% –
#           `${risk_control_formulas[i]}`.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Insert the **Execution Pseudocode** markdown exactly as emitted by the
#   `draft_execution_logic` node (`execution_logic_pseudocode` field).
#   Prepend a heading and a brief narrative explaining how the pseudocode
#   maps to the risk controls defined earlier.
#   Reason: The execution logic must be directly traceable to the risk controls and
#           model signals; reusing the already‑generated pseudocode
#           guarantees consistency.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Wrap the pseudocode string in a markdown fenced code block with language
#           `python` or `pseudo`.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Compose the **Backtest Results** markdown using the seven fields produced by
#   the `summarize_backtest_results` node. Present key metrics in a markdown
#   table, embed the histogram and turnover‑chart descriptions as bullet
#   items, and include the full `markdown_report` content verbatim under a
#   sub‑heading.
#   Reason: Stakeholders need a concise performance snapshot together with visual
#           insights; the `summarize_backtest_results` node already
#           aggregates these stats.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Create a table: `| Metric | Value |` with rows for Annualized Return,
#           Sharpe, Max Drawdown, Turnover, Win Rate. Then add sections:
#           `### Charts` with bullet points using `histogram_description`
#           and `turnover_chart_description`. Append `markdown_report`.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Draft the **Implementation Checklist** markdown as a static ordered list
#   covering: (a) Code deployment, (b) Config file creation, (c) Model
#   serialization, (d) Risk‑control parameters upload, (e) Monitoring plan
#   integration (reference `create_monitoring_plan` output), (f) Performance
#   validation, (g) Documentation upload. Each item should include a checkbox
#   placeholder `[ ]`.
#   Reason: A checklist formalizes the hand‑off steps and reduces operational risk
#           during production rollout.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Hard‑code the list: `- [ ] Deploy model code\n- [ ] Add config.yml ...`.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Concatenate all eight section strings in the exact order required by the
#   deliverable (Strategy Overview → Data & Features → Model Architecture →
#   Feature Importance → Risk Management → Execution Pseudocode → Backtest
#   Results → Implementation Checklist) into the final
#   `full_document_markdown` field. Ensure each section begins with a level‑2
#   markdown heading (`##`). Add a top‑level title (`# Strategy Dossier`) at
#   the very top.
#   Reason: A single, ordered markdown file is the final artifact expected by
#           downstream nodes (e.g., `final_deliverables_package`).
#   Impact: HIGH
#   Complexity: LOW
#   Method: String concatenation with newline separators: `# Strategy
#           Dossier\n\n${strategy_overview}\n\n${data_and_features}\n...`.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class SelectBestModelOutput(BaseModel):
    """Pydantic model for select_best_model node outputs."""
    best_model_identifier: str = Field(..., description="Identifier of the selected best model.")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the selected model.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the selected model.")
    annualized_return: float = Field(..., description="Annualized return of the selected model.")


class DesignRiskControlsOutput(BaseModel):
    """Pydantic model for design_risk_controls node outputs."""
    risk_control_names: List[str] = Field(..., description="Identifier for each risk control (e.g., max_gross_exposure, var_99, max_asset_weight, daily_stop_loss, monthly_turnover).")
    risk_control_thresholds: List[float] = Field(..., description="Numeric threshold for each risk control in the same order as risk_control_names (e.g., 0.20 for 20% gross exposure, 0.02 for 2% VaR).")
    risk_control_formulas: List[str] = Field(..., description="Short implementation formula or rule for each risk control (e.g., \"GrossExposure <= 0.20\", \"VaR_99 <= 0.02\").")


class DraftExecutionLogicOutput(BaseModel):
    """Pydantic model for draft_execution_logic node outputs."""
    execution_logic_pseudocode: str = Field(..., description="Pseudocode outlining the order execution logic, including fetching features, generating signals, applying risk controls, sizing orders, and sending limit orders.")
    risk_control_implementation_details: List[str] = Field(..., description="Details on how risk controls are implemented within the execution logic, referencing specific risk limits defined in the Design Risk Controls node.")
    order_sizing_formula: str = Field(..., description="The formula or method used to determine the order size based on the model's signal, risk limits, and available capital.")


class SummarizeBacktestResultsOutput(BaseModel):
    """Pydantic model for summarize_backtest_results node outputs."""
    annualized_return: float = Field(..., description="Annualized return of the strategy expressed as a decimal (e.g., 0.12 for 12%).")
    sharpe_ratio: float = Field(..., description="Annualized Sharpe ratio of the strategy.")
    max_drawdown: float = Field(..., description="Maximum drawdown of the equity curve expressed as a decimal (e.g., -0.25 for -25%).")
    turnover: float = Field(..., description="Average portfolio turnover per period (e.g., monthly turnover as a decimal).")
    win_rate: float = Field(..., description="Proportion of winning trades (range 0\u20111).")
    histogram_description: str = Field(..., description="Markdown description of the histogram chart for daily returns, including key observations.")
    turnover_chart_description: str = Field(..., description="Markdown description of the turnover time\u2011series chart, highlighting trends or spikes.")
    markdown_report: str = Field(..., description="Full markdown report containing the statistics and chart descriptions.")


class CompileStrategyDocumentationOutput(BaseModel):
    """Pydantic model for compile_strategy_documentation node outputs."""
    strategy_overview: str = Field(..., description="Markdown text summarizing the high\u2011level strategy intent, asset universe, time horizon, and performance goals.")
    data_and_features: str = Field(..., description="Markdown description of data sources, cleaning steps, and a concise list of engineered features.")
    model_architecture: str = Field(..., description="Markdown detailing the selected model(s), algorithmic components, input shapes, and how predictions are combined.")
    feature_importance: str = Field(..., description="Markdown table (or bullet list) ranking features by importance scores (e.g., gain, SHAP).")
    risk_management: str = Field(..., description="Markdown outlining the portfolio\u2011level and position\u2011level risk controls, limits, and stop\u2011loss rules.")
    execution_pseudocode: str = Field(..., description="Markdown block containing the pseudo\u2011code for real\u2011time signal generation, risk filtering, order sizing, and order submission.")
    backtest_results: str = Field(..., description="Markdown summary of backtest performance metrics and brief description of supporting charts.")
    implementation_checklist: str = Field(..., description="Markdown checklist of items required to operationalize the strategy (e.g., code deployment, config files, monitoring setup).")
    full_document_markdown: str = Field(..., description="The complete compiled strategy dossier, concatenating all sections in proper heading order.")


def compile_strategy_documentation(select_best_model_input: SelectBestModelOutput, design_risk_controls_input: DesignRiskControlsOutput, draft_execution_logic_input: DraftExecutionLogicOutput, summarize_backtest_results_input: SummarizeBacktestResultsOutput, **kwargs) -> CompileStrategyDocumentationOutput:
    """Assemble all model, feature, risk, execution, and backtest artifacts into a single strategy dossier.

    Args:
        select_best_model_input: Input from the 'select_best_model' node.
        design_risk_controls_input: Input from the 'design_risk_controls' node.
        draft_execution_logic_input: Input from the 'draft_execution_logic' node.
        summarize_backtest_results_input: Input from the 'summarize_backtest_results' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CompileStrategyDocumentationOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return CompileStrategyDocumentationOutput(
        strategy_overview="",
        data_and_features="",
        model_architecture="",
        feature_importance="",
        risk_management="",
        execution_pseudocode="",
        backtest_results="",
        implementation_checklist="",
        full_document_markdown="",
    )