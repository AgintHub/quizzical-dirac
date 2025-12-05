# define_compute_order_size_function PRD

## Description
Generates a Python function (as a string) that computes order size based on a user‑provided sizing formula.


## Implementation Plan

### 1. Parse the supplied `formula` string into a safe abstract syntax tree (AST) and ensure only allowed arithmetic operators and identifiers are present.

| Category | Details |
| --- | --- |
| **Reason** | User‑provided formulas could contain malicious code or unsupported constructs; parsing and validation prevent execution of unsafe code. |
| **Impact** | Guarantees that the generated function is syntactically correct and secure, avoiding runtime errors or security breaches. |
| **Complexity** | MEDIUM |
| **Method** | Use Python's `ast` module to parse the expression, traverse the AST to whitelist nodes (`BinOp`, `Name`, `Num`, etc.), and reject any disallowed constructs. |

### 2. Validate that all identifiers used in the formula belong to the permitted variable set (`capital`, `signal`, `leverage`, `risk_limit`).

| Category | Details |
| --- | --- |
| **Reason** | Restricting variable names ensures the function operates only on known inputs and prevents accidental reference to undefined symbols. |
| **Impact** | Prevents NameError exceptions at runtime and reinforces the security model by limiting the execution context. |
| **Complexity** | LOW |
| **Method** | After AST validation, extract `Name` nodes and compare them against a whitelist; raise a clear error if any unknown identifier is found. |

### 3. Compose the final function definition as a formatted string that embeds the validated expression and returns the computed size.

| Category | Details |
| --- | --- |
| **Reason** | Downstream nodes expect the function definition as a string to embed in generated pseudocode. |
| **Impact** | Provides a ready‑to‑use, self‑contained function that can be inserted into execution‑logic pseudocode without further transformation. |
| **Complexity** | LOW |
| **Method** | Create a template like `def compute_order_size(capital, signal, leverage, risk_limit):
    return {expression}` and fill `{expression}` with the sanitized formula using an f‑string. |
