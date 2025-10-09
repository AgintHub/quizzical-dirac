# define_asset_universe PRD

## Description
Enumerate tradable assets and instruments.


## Implementation Plan

### 1. Review the selected trading strategy from the 'choose_trading_strategy' node to understand the asset classes and instruments that align with the strategy.

| Category | Details |
| --- | --- |
| **Reason** | Ensure that the asset universe is consistent with the chosen trading strategy. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the output from 'choose_trading_strategy' node, specifically the 'selected_strategy' field. |

### 2. Identify a list of asset classes and instruments that are relevant to the selected trading strategy, keeping in mind market liquidity, trading hours, and other factors.

| Category | Details |
| --- | --- |
| **Reason** | Create a relevant and tradable asset universe. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use market data and research to identify asset classes and instruments, consider factors such as market capitalization, liquidity, and volatility. |

### 3. Limit the list of asset classes and instruments to 10 or fewer items to ensure a focused asset universe.

| Category | Details |
| --- | --- |
| **Reason** | Prevent over-diversification and ensure manageability. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a filtering process to narrow down the list of asset classes and instruments. |

### 4. Validate the asset universe by checking for duplicates, ensuring that the listed asset classes and instruments are tradable, and verifying that they align with the selected trading strategy.

| Category | Details |
| --- | --- |
| **Reason** | Ensure accuracy and validity of the asset universe. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use data validation techniques and review the list against the trading strategy and market data. |

### 5. Output the list of asset classes and instruments, the number of assets in the list, and a boolean indicating whether the asset universe is valid.

| Category | Details |
| --- | --- |
| **Reason** | Provide a clear and usable output for downstream nodes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the output structure defined for this node to format the output. |
