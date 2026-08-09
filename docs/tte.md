# Controlled Test-Time Tool Evolution (TTE) Architecture

## Overview

Test-Time Tool Evolution (TTE) allows **Sahay** to identify tool gaps during problem solving (e.g. needing a custom scheme income eligibility calculator) and propose new capabilities dynamically.

**CRITICAL SECURITY GUARANTEE:** Sahay **NEVER** allows arbitrary execution of generated code directly in production runtimes (`exec()` or `eval()` are strictly prohibited).

## Safe TTE Lifecycle

```
[User Request / Agent Task]
           │
           ▼
 [Tool Gap Detection]  <-- Agent identifies missing capability
           │
           ▼
    [Tool Proposal]    <-- Defines tool spec (name, inputs, outputs, code)
           │
           ▼
[AST & Static Linter]  <-- Validates no unsafe imports (os, sys, subprocess, net)
           │
           ▼
   [Sandbox Execution] <-- Executed in isolated temporary container with timeouts
           │
           ▼
     [Unit Tests]      <-- Synthetic test cases run against tool
           │
           ▼
 [Human/Admin Gate]    <-- Requires explicit API call / human approval (/api/v1/tte/approve)
           │
           ▼
 [Versioned Registry]  <-- Marked ACTIVE and registered in tool_registry table
```

## Security & Isolation Controls
1. **Forbidden Operations:**
   - No filesystem access outside temporary sandbox folder.
   - No network calls or socket connections.
   - No dynamic subprocess or shell execution.
   - No persistence or credential access.
2. **Version Control & Audit:**
   - Every proposal is assigned a unique `proposal_id`.
   - Audit trail stores `created_at`, `approved_by`, and execution logs.
