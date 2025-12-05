# setup_backtest_environment PRD

## Description
Configure a backtesting engine with data, model, risk controls, and transaction cost assumptions.


## Implementation Plan

### 1. Define the initial capital for the backtest. A reasonable starting point is 1,000,000.00, but this can be adjusted based on the desired scale and risk profile of the strategy.

| Category | Details |
| --- | --- |
| **Reason** | The initial capital is a fundamental parameter that determines the trading size and affects performance metrics like Sharpe ratio and drawdown. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Set the `initial_capital` to 1000000.00. Consider making this configurable via a parameter. |

### 2. Implement a slippage model. A simple model representing the execution cost is to assume a fixed slippage of 0.5 basis points (0.005%).

| Category | Details |
| --- | --- |
| **Reason** | Slippage accounts for the difference between the expected and actual execution price, especially for large orders or illiquid assets. It provides a more realistic backtest environment. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Set `slippage_bps` to 0.005. Model slippage linearly proportional to trade size for increased realism within the backtesting engine. |

### 3. Implement a commission model. A standard commission rate is 0.1% per trade (0.001).

| Category | Details |
| --- | --- |
| **Reason** | Commissions are trading costs charged by brokers, which need to be accounted for in the backtest. This impacts the overall profitability. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Set the `commission_pct` to 0.001.  Model this as a percentage of the trade value incurred at both entry and exit. |

### 4. Define the rebalancing frequency. Common choices are 'daily', 'weekly', or 'monthly'. Choose based on the strategy's typical holding period and desired turnover.

| Category | Details |
| --- | --- |
| **Reason** | Rebalancing ensures that the portfolio maintains its desired asset allocation and risk profile. The frequency affects transaction costs and tracking error. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Set `rebalance_frequency` to 'daily'. Add input validation to ensure allowed values are only 'daily', 'weekly', or 'monthly'. |

### 5. Extract the list of risk control rules from the `design_risk_controls` node output. The `risk_control_names`, `risk_control_thresholds`, and `risk_control_formulas` are mapped to a human-readable string and stored in `risk_controls_summary` list.

| Category | Details |
| --- | --- |
| **Reason** | This step prepares the risk control information for reporting and integration into the backtesting engine. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Iterate through risk controls from the dependency node `design_risk_controls`. Format each control info a string. Example: `max_gross_exposure 20%`. Construct the output list `risk_controls_summary`. |

### 6. Define the risk control enforcement method. Choose a method such as 'pre-trade check' or 'post-trade check'.

| Category | Details |
| --- | --- |
| **Reason** | The enforcement method determines how risk controls are applied during the simulation. 'Pre-trade check' aborts trades that violate risk limits, while 'post-trade check' may trigger corrective actions. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Set `risk_control_enforcement_method` to 'pre-trade check that aborts orders violating any rule'. If post-trade, provide method to reduce position size if any risk limit is breached post order execution. |

### 7. Integrate the cleaned data from the `align_and_clean_data` node. The cleaned data will be used as the price feed for the backtesting engine. CSV format is available in `cleaned_data_csv`.

| Category | Details |
| --- | --- |
| **Reason** | This ensures the backtest uses a consistent and reliable data source, free of missing values and properly aligned for accurate simulation. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Parse data in `cleaned_data_csv` and feed into backtest. Handle potential parse errors. |

### 8. Integrate the selected best model from the `select_best_model` node. The `best_model_identifier` specifies the identifier of the model to load and use during backtesting.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures the backtest reflects the expected performance of the selected model. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use `best_model_identifier` to load the persisted model and use it when generating trading signals in the backtesting engine. This assumes a model persistence/loading mechanism is available external to the backtest function. |

### 9. Implement the chosen risk controls within the backtesting engine. The risk control parameters are from the `design_risk_controls` node.

| Category | Details |
| --- | --- |
| **Reason** | Enforcing risk controls accurately during backtesting is critical to estimating the strategy's risk-adjusted performance. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | For each risk control extracted in previous step from node `design_risk_controls`, implement the corresponding `risk_control_formulas` with the respective `risk_control_thresholds`. Implement checks specified in the `risk_control_enforcement_method`. |
