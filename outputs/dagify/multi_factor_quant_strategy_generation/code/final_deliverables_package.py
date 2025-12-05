# -- PRD --
# 1. BULLET: Extract the compiled strategy markdown (full_document_markdown) from the
#   output of **compile_strategy_documentation** and write it to a file named
#   **Strategy_Document.md**.
#   Reason: The strategy dossier is the central deliverable that stakeholders will
#           review; storing it as a markdown file preserves formatting and
#           allows easy viewing.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Read the string field `full_document_markdown`; open a file handle with
#           UTF‑8 encoding; write the string verbatim; close the file.
#           Ensure newline consistency (LF).
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Generate a runnable Python script **model_code.py** that contains: (a) import
#   statements for the selected model's libraries, (b) a function
#   `load_model()` that deserializes the model (placeholder code), (c) a
#   function `predict(features)` that returns model predictions, and (d) a
#   `if __name__ == "__main__"` block demonstrating a mock inference.
#   Reason: Providing executable model code enables downstream engineers to quickly
#           load and test the model without re‑implementing logic.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the `best_model_identifier` from **select_best_model** (available via
#           upstream nodes) to select import statements (e.g., `import
#           xgboost as xgb` or `import torch`). Insert stub code with clear
#           TODO comments where model artefacts would be loaded. Write to
#           `model_code.py` with proper indentation and PEP‑8 compliance.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Create **requirements.txt** by aggregating the Python packages required for
#   the strategy: core data libraries (pandas, numpy), modelling libraries
#   (xgboost, torch, scikit‑learn), back‑testing library (backtrader or
#   zipline), and any auxiliary packages (PyYAML, shap).
#   Reason: A complete requirements file guarantees reproducibility of the environment
#           across development, staging, and production.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Compose a list of strings `<package>==<latest_version>`; versions can be
#           pinned using `import pkg_resources;
#           pkg_resources.get_distribution(pkg).version`. Write each entry
#           on a new line to `requirements.txt`.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Serialize the monitoring configuration into **monitoring_plan.md** by
#   transforming the output fields of **create_monitoring_plan**
#   (`daily_live_metrics`, `alert_thresholds_metrics`,
#   `alert_thresholds_values`, `retraining_schedule`) into a markdown
#   document with sections: *Daily Live Metrics*, *Alert Thresholds*, and
#   *Retraining Schedule*.
#   Reason: Stakeholders need a human‑readable specification of operational monitoring;
#           markdown is both readable and version‑controllable.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Iterate over `daily_live_metrics` to build a bullet list. For alerts, zip
#           `alert_thresholds_metrics` and `alert_thresholds_values` to
#           produce a table. Append the free‑form `retraining_schedule` as
#           a numbered list. Write the assembled markdown string to
#           `monitoring_plan.md`.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Construct **config.yml** containing key runtime parameters: asset universe,
#   risk control thresholds, model identifier, and back‑test settings. Pull
#   values from the following upstream nodes: **define_strategy_objectives**
#   (asset list, holding period), **design_risk_controls**
#   (risk_control_names, risk_control_thresholds), **select_best_model**
#   (best_model_identifier), and **setup_backtest_environment**
#   (initial_capital, slippage_bps, commission_pct, rebalance_frequency).
#   Reason: A YAML configuration centralises all tunable parameters, simplifying
#           deployment and future adjustments.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Create a nested Python dictionary matching the desired hierarchy, e.g.,
#           `strategy: { assets: [...], holding_period: X }`, `risk: {
#           controls: [{name:..., threshold:...}, ...] }`, `model: { id:
#           ..., parameters: {} }`, `backtest: { capital: ...,
#           slippage_bps: ..., commission_pct: ..., rebalance: ... }`. Use
#           `yaml.safe_dump` with `default_flow_style=False` to output to
#           `config.yml`.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Assemble the **manifest_files** list in the exact order required by the
#   prompt: `["Strategy_Document.md", "model_code.py", "requirements.txt",
#   "config.yml", "monitoring_plan.md"]`.
#   Reason: The manifest must reflect the ordering defined in the specification to
#           avoid downstream parsing errors.
#   Impact: LOW
#   Complexity: LOW
#   Method: Create a Python list literal with the five filenames in the specified
#           order.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Generate the **manifest_descriptions** list, aligning one‑to‑one with
#   `manifest_files`. Use concise sentences (≤ 30 words) summarising each
#   file’s purpose, e.g., "Comprehensive markdown strategy dossier covering
#   overview, data, model, risk, execution, backtest and checklist."
#   Reason: Providing clear descriptions aids auditors and automated documentation
#           tools when unpacking the archive.
#   Impact: LOW
#   Complexity: LOW
#   Method: Define a list of five strings matching the order of `manifest_files`;
#           ensure each description is unique and accurately reflects the
#           file content.
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Set `package_type` to the literal string **"zip"** and `is_ready_for_handoff`
#   to **true** after performing a validation step: (a) confirm all five
#   files exist on disk, (b) verify each file size > 0 bytes, (c) optionally
#   compute a SHA‑256 checksum for each and log it.
#   Reason: Explicitly marking the package as ready only after validation prevents
#           incomplete hand‑offs and provides traceability.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use `os.path.isfile` and `os.path.getsize` for existence/size checks; raise
#           an exception if any check fails. If all pass, assign
#           `is_ready_for_handoff = True`. Record checks in a log file for
#           audit.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Optionally create an in‑memory ZIP archive (using `io.BytesIO` and
#   `zipfile.ZipFile`) that contains the five files, but **do not** write the
#   archive to disk – the manifest fields are sufficient for downstream
#   agents that will perform the actual archiving.
#   Reason: Providing a ready‑to‑use archive object can speed up later stages without
#           violating the current node’s responsibility of only describing
#           the manifest.
#   Impact: LOW
#   Complexity: MEDIUM
#   Method: Instantiate a `BytesIO` buffer, add each file via
#           `ZipFile.writestr(filename, file_contents)`, then close the
#           zip. Store the buffer reference if needed for downstream
#           consumption (not part of the output schema).
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


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


class CreateMonitoringPlanOutput(BaseModel):
    """Pydantic model for create_monitoring_plan node outputs."""
    daily_live_metrics: str = Field(..., description="List of daily live metrics to track (e.g., realized volatility, prediction error)")
    alert_thresholds_metrics: str = Field(..., description="List of the metric names used in alert thresholds")
    alert_thresholds_values: float = Field(..., description="List of the threshold values, corresponding to alert_thresholds_metrics")
    retraining_schedule: str = Field(..., description="Outline of the quarterly retraining process")


class FinalDeliverablesPackageOutput(BaseModel):
    """Pydantic model for final_deliverables_package node outputs."""
    manifest_files: List[str] = Field(..., description="Names of files included in the deliverable package, e.g., Strategy_Document.md, model_code.py, requirements.txt, config.yml, monitoring_plan.md.")
    manifest_descriptions: List[str] = Field(..., description="Brief description for each file in the manifest, in the same order as manifest_files.")
    package_type: str = Field(..., description="Archive format of the package, e.g., "zip".")
    is_ready_for_handoff: bool = Field(..., description="Indicates whether the package has been validated and is ready for hand\u2011off.")


def final_deliverables_package(compile_strategy_documentation_input: CompileStrategyDocumentationOutput, create_monitoring_plan_input: CreateMonitoringPlanOutput, **kwargs) -> FinalDeliverablesPackageOutput:
    """Package the strategy dossier, code snippets, monitoring plan, and any configuration files for hand‑off.

    Args:
        compile_strategy_documentation_input: Input from the 'compile_strategy_documentation' node.
        create_monitoring_plan_input: Input from the 'create_monitoring_plan' node.
        **kwargs: Additional keyword arguments.

    Returns:
        FinalDeliverablesPackageOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return FinalDeliverablesPackageOutput(
        manifest_files=[],
        manifest_descriptions=[],
        package_type="",
        is_ready_for_handoff=False,
    )