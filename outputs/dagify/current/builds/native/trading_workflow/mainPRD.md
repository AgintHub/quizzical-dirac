# trading_workflow - Complete PRD Documentation

## Overview
PRDs for nodes in the 'trading_workflow' module.

## Table of Contents

- [choose_trading_strategy](#choose_trading_strategy)

- [compile_trading_dashboard_outline](#compile_trading_dashboard_outline)

- [define_asset_universe](#define_asset_universe)

- [define_trading_objectives](#define_trading_objectives)

- [define_trading_performance_metrics](#define_trading_performance_metrics)

- [design_risk_management_framework](#design_risk_management_framework)

- [develop_trading_plan](#develop_trading_plan)

- [set_trading_parameters](#set_trading_parameters)



---

## choose_trading_strategy

### Description
Identify the high-level trading strategy category.

### Implementation Plan

#### 1. Review the trading objectives provided by the 'define_trading_objectives' node to understand the purpose, risk tolerance, and long-term vision of the trading system.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the selected trading strategy aligns with the overall goals of the trading system. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Analyze the bullet list of trading objectives to identify key themes and priorities. |

#### 2. Research and list potential high-level trading strategy categories that could achieve the trading objectives (e.g., trend following, mean reversion, statistical arbitrage).

| Category | Details |
| --- | --- |
| **Reason** | This step provides a comprehensive set of potential strategies to consider. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Utilize domain expertise and literature review to compile a list of relevant trading strategies. |

#### 3. Evaluate each potential trading strategy category against the trading objectives, considering factors such as risk tolerance, potential returns, and complexity.

| Category | Details |
| --- | --- |
| **Reason** | This step enables an informed decision about which strategy best aligns with the trading objectives. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Apply a decision-making framework, such as a weighted scoring model, to assess each strategy's suitability. |

#### 4. Select the primary trading strategy category that best serves the trading objectives and provide a one-sentence rationale for the selection.

| Category | Details |
| --- | --- |
| **Reason** | This step formalizes the chosen strategy and justifies the decision. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Document the selected strategy and rationale in a clear and concise manner. |


---

## compile_trading_dashboard_outline

### Description
Framework for trading performance monitoring.

### Implementation Plan

#### 1. Review the trading plan output from the 'develop_trading_plan' node to understand the strategy, risk management controls, and execution details.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the dashboard outline aligns with the overall trading plan. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Analyze the trading plan document and identify key components. |

#### 2. Identify the key performance metrics for the trading system from the 'define_trading_performance_metrics' node.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the dashboard includes relevant performance metrics. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Review the performance metrics document and extract relevant metrics. |

#### 3. Determine the essential risk management controls from the 'design_risk_management_framework' node.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the dashboard addresses risk management. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Examine the risk management framework document and identify key controls. |

#### 4. Create a list of potential slide titles for the trading performance dashboard based on the trading plan, performance metrics, and risk management controls.

| Category | Details |
| --- | --- |
| **Reason** | This step generates a comprehensive list of potential dashboard slides. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use a template or brainstorming approach to generate a list of potential slide titles. |

#### 5. Organize and prioritize the list of potential slide titles to create a cohesive 10-slide outline.

| Category | Details |
| --- | --- |
| **Reason** | This step refines the list into a logical and concise dashboard outline. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use a systematic approach to categorize and prioritize the slide titles. |

#### 6. Finalize the 10-slide outline and ensure that it covers strategy, risk, and performance metrics.

| Category | Details |
| --- | --- |
| **Reason** | This step produces the final output for the node. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Review and refine the outline to ensure completeness and accuracy. |


---

## define_asset_universe

### Description
Enumerate tradable assets and instruments.

### Implementation Plan

#### 1. Review the selected trading strategy from the 'choose_trading_strategy' node to understand the asset classes and instruments that align with the strategy.

| Category | Details |
| --- | --- |
| **Reason** | Ensure that the asset universe is consistent with the chosen trading strategy. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the output from 'choose_trading_strategy' node, specifically the 'selected_strategy' field. |

#### 2. Identify a list of asset classes and instruments that are relevant to the selected trading strategy, keeping in mind market liquidity, trading hours, and other factors.

| Category | Details |
| --- | --- |
| **Reason** | Create a relevant and tradable asset universe. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use market data and research to identify asset classes and instruments, consider factors such as market capitalization, liquidity, and volatility. |

#### 3. Limit the list of asset classes and instruments to 10 or fewer items to ensure a focused asset universe.

| Category | Details |
| --- | --- |
| **Reason** | Prevent over-diversification and ensure manageability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a filtering process to narrow down the list of asset classes and instruments. |

#### 4. Validate the asset universe by checking for duplicates, ensuring that the listed asset classes and instruments are tradable, and verifying that they align with the selected trading strategy.

| Category | Details |
| --- | --- |
| **Reason** | Ensure accuracy and validity of the asset universe. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use data validation techniques and review the list against the trading strategy and market data. |

#### 5. Output the list of asset classes and instruments, the number of assets in the list, and a boolean indicating whether the asset universe is valid.

| Category | Details |
| --- | --- |
| **Reason** | Provide a clear and usable output for downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the output structure defined for this node to format the output. |


---

## define_trading_objectives

### Description
Produce a bullet list of the trading system's core objectives.

### Implementation Plan

#### 1. Review and analyze the trading system's purpose, risk tolerance, and long-term vision to identify key objectives.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the objectives are well-defined and aligned with the overall goals of the trading system. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a template to guide the analysis, including questions such as: What is the primary purpose of the trading system? What is the risk tolerance of the system? What are the long-term goals of the system? |

#### 2. Identify and prioritize the key objectives, ensuring they are specific, measurable, achievable, relevant, and time-bound (SMART).

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the objectives are clear, actionable, and aligned with the overall goals of the trading system. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a prioritization framework, such as MoSCoW or Kano, to categorize and prioritize the objectives. |

#### 3. Formulate a concise bullet list of the top objectives, focusing on purpose, risk tolerance, and long-term vision.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the objectives are communicated clearly and effectively to stakeholders. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a bullet list template to organize and format the objectives, ensuring they are concise and easy to understand. |

#### 4. Review and refine the bullet list to ensure it meets the requirements of the prompt and is free of errors.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the output meets the requirements and is of high quality. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use a quality control checklist to review the output, including criteria such as: Does the list meet the length requirement? Are the objectives clear and concise? Are there any errors in formatting or content? |


---

## define_trading_performance_metrics

### Description
Specify metrics for evaluating trading performance.

### Implementation Plan

#### 1. Review the trading plan and objectives to understand the context for performance metrics.

| Category | Details |
| --- | --- |
| **Reason** | This ensures that the performance metrics align with the trading plan and objectives. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Analyze the trading plan and objectives document. |

#### 2. Research and gather information on the four key performance metrics: return, volatility, Sharpe ratio, and maximum drawdown.

| Category | Details |
| --- | --- |
| **Reason** | This provides a comprehensive understanding of each metric and its significance in evaluating trading performance. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Conduct a literature review of financial texts, academic papers, and reputable online resources. |

#### 3. Write a one-sentence explanation for each of the four key performance metrics.

| Category | Details |
| --- | --- |
| **Reason** | This provides a concise and clear description of each metric. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use simple and clear language to describe each metric, ensuring that the explanation is concise and accurate. |

#### 4. Ensure that the explanations for each metric are accurate, concise, and relevant to the trading plan and objectives.

| Category | Details |
| --- | --- |
| **Reason** | This ensures that the performance metrics are properly understood and applied in the context of the trading plan. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Review and revise the explanations for each metric, using expert judgment and feedback from stakeholders. |

#### 5. Format the output according to the specified output structure.

| Category | Details |
| --- | --- |
| **Reason** | This ensures that the output is organized and easy to understand. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use a template or format guide to ensure consistency in the output structure. |


---

## design_risk_management_framework

### Description
Outline quantitative and qualitative risk controls.

### Implementation Plan

#### 1. Review the output from the 'set_trading_parameters' node to understand the quantitative trading parameters such as position size, stop-loss level, and take-profit level.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the risk controls are aligned with the trading parameters. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Verify that the output from 'set_trading_parameters' includes position size, stop-loss level, and take-profit level. |

#### 2. Identify the target metrics for risk management, including position limits, VaR limits, stop-loss rules, and liquidity thresholds.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the risk controls are aligned with the target metrics. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use the output from 'set_trading_parameters' to determine the target metrics for risk management. |

#### 3. Define position limits as a risk control to limit the maximum exposure to a single asset or asset class.

| Category | Details |
| --- | --- |
| **Reason** | This step helps to mitigate the risk of large losses due to over-exposure to a single asset or asset class. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a percentage of the overall portfolio value to determine the position limit. |

#### 4. Define VaR limits as a risk control to limit the potential loss in value of the portfolio over a specific time horizon with a given probability.

| Category | Details |
| --- | --- |
| **Reason** | This step helps to mitigate the risk of large losses due to market volatility. |
| **Impact** | HIGH |
| **Complexity** | HIGH |
| **Method** | Use historical data and statistical models to determine the VaR limit. |

#### 5. Define stop-loss rules as a risk control to limit the loss on a single trade or asset.

| Category | Details |
| --- | --- |
| **Reason** | This step helps to mitigate the risk of large losses due to adverse market movements. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a percentage of the position value to determine the stop-loss level. |

#### 6. Define liquidity thresholds as a risk control to ensure that the portfolio can be liquidated quickly and at a fair price.

| Category | Details |
| --- | --- |
| **Reason** | This step helps to mitigate the risk of large losses due to illiquidity. |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use historical data and market analysis to determine the liquidity thresholds. |


---

## develop_trading_plan

### Description
Create a detailed trading plan including strategy, risk management, and execution details.

### Implementation Plan

#### 1. Review and synthesize the outputs from the parent nodes, including the chosen trading strategy, asset universe, trading parameters, and risk management framework.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that all necessary information is gathered and considered before creating the trading plan. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a checklist to ensure all required information is present and correct. |

#### 2. Create a concise description of the chosen trading strategy, including its key components and objectives.

| Category | Details |
| --- | --- |
| **Reason** | This step provides a clear and concise overview of the trading strategy. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a template to ensure the description covers all necessary points. |

#### 3. Outline the key risk management controls, including position limits, stop-loss rules, and liquidity thresholds.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the trading plan includes effective risk management measures. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a risk management framework template to ensure all necessary controls are included. |

#### 4. Summarize the execution details, outlining how trades will be executed within the trading plan.

| Category | Details |
| --- | --- |
| **Reason** | This step provides clarity on how the trading plan will be implemented. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a standard template for execution details. |

#### 5. List the target asset classes and tradable instruments identified for the trading strategy.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the trading plan is specific to the chosen asset universe. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a standard template for listing asset classes and instruments. |

#### 6. Define the numerical trading parameters, including position size, stop-loss level, and take-profit level.

| Category | Details |
| --- | --- |
| **Reason** | This step ensures that the trading plan includes specific and measurable trading parameters. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a standard template for defining trading parameters. |


---

## set_trading_parameters

### Description
Quantify trading parameters such as position sizing and stop-loss levels.

### Implementation Plan

#### 1. Retrieve the selected trading strategy from the output of the 'choose_trading_strategy' node.

| Category | Details |
| --- | --- |
| **Reason** | The trading parameters need to be aligned with the chosen strategy. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Access the 'selected_strategy' field from the output of 'choose_trading_strategy' node. |

#### 2. Map the selected trading strategy to a set of predefined trading parameter ranges.

| Category | Details |
| --- | --- |
| **Reason** | Different strategies require different parameter settings. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a strategy-parameter mapping framework to determine the parameter ranges for the selected strategy. |

#### 3. Determine the position size based on the strategy-parameter mapping and risk management considerations.

| Category | Details |
| --- | --- |
| **Reason** | Position sizing is critical for risk management and strategy execution. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Apply a position sizing algorithm that considers the strategy, risk tolerance, and market conditions. |

#### 4. Calculate the stop-loss level based on the strategy-parameter mapping and risk management considerations.

| Category | Details |
| --- | --- |
| **Reason** | Stop-loss levels are essential for limiting potential losses. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use a stop-loss calculation algorithm that considers the strategy, risk tolerance, and market volatility. |

#### 5. Calculate the take-profit level based on the strategy-parameter mapping and profit target considerations.

| Category | Details |
| --- | --- |
| **Reason** | Take-profit levels are necessary for locking in profits. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Apply a take-profit calculation algorithm that considers the strategy, profit targets, and market conditions. |

#### 6. Format the trading parameters into a 3-row table for presentation.

| Category | Details |
| --- | --- |
| **Reason** | Clear presentation of trading parameters is essential for easy understanding and implementation. |
| **Impact** | LOW |
| **Complexity** | LOW |
| **Method** | Use a table formatting library to create a 3-row table with columns for parameter names and values. |
