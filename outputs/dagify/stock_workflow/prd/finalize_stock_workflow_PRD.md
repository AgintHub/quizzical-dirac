# finalize_stock_workflow PRD

## Description
Finalize the stock workflow


## Implementation Plan

### 1. Verify that the review_stock_offering node has completed successfully and produced a compliant document.

| Category | Details |
| --- | --- |
| **Reason** | This ensures that all necessary revisions have been made and the document is accurate and complete. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Check the review_complete and compliance_status outputs of the review_stock_offering node |

### 2. Confirm that all steps in the stock workflow have been completed by checking the outputs of all predecessor nodes.

| Category | Details |
| --- | --- |
| **Reason** | This ensures that all necessary steps have been taken and the stock is ready for issuance. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Check the outputs of the calculate_stock_valuation, define_stock_structure, draft_stock_offering, and review_stock_offering nodes |

### 3. Generate a list of comments or notes regarding the finalization process.

| Category | Details |
| --- | --- |
| **Reason** | This provides a record of any issues or concerns that arose during the finalization process. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Use a template to generate a list of comments based on the outputs of predecessor nodes |

### 4. Set the workflow_finalized output to true if all steps have been completed and the stock is ready for issuance.

| Category | Details |
| --- | --- |
| **Reason** | This indicates that the stock workflow has been successfully finalized. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a conditional statement to set the output based on the outputs of predecessor nodes |

### 5. Set the is_ready_for_issuance output to true if all steps have been completed and the stock is ready for issuance.

| Category | Details |
| --- | --- |
| **Reason** | This indicates that the stock is ready for issuance. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a conditional statement to set the output based on the outputs of predecessor nodes |
