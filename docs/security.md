# Sahay Security Specification

## Core Principles

1. **PII Minimization**: Sahay does not collect or store full names, social security numbers, bank account numbers, or precise addresses unless explicitly needed for session evaluation.
2. **Non-Hallucinatory Disclaimers**: Every response contains legal disclaimer language confirming that Sahay is an independent navigation tool and not an official legal granting authority.
3. **Source Traceability**: Factual scheme recommendations must reference an official issuing authority and verified URL.
4. **Input Validation**: All API inputs pass through Pydantic v2 schemas enforcing strict type constraints.
5. **Tool Permission Boundaries**: Tools registered in the Tool Registry are categorized by permission tiers (`READ_ONLY`, `PUBLIC_LOOKUP`, `SANDBOX_EVAL`).
