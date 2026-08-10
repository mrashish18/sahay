# Sahay Architecture Specification

## Overview

**Sahay 2.0** is a public-service & crisis assistance navigator built with a modular workflow separating natural language understanding, deterministic eligibility evaluation, source traceability, and sandboxed tool evolution.

```text
User Question
      │
      ▼
┌─────────────────────────┐
│ React Frontend (Vite)   │
└───────────┬─────────────┘
            │ REST API (SahayResponse JSON)
            ▼
┌─────────────────────────┐
│  FastAPI Backend Engine │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     AI Orchestrator     │
└───────────┬─────────────┘
            │
            ├─────────────────────────────────┬─────────────────────────────────┐
            │                                 │                                 │
            ▼                                 ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│ Semantic NLU Analyzer   │       │  Crisis Navigator       │       │  Public Service RAG     │
│ (Fact & Intent Extract) │       │  (Priority Safety Lane) │       │  (pgvector Store)       │
└───────────┬─────────────┘       └───────────┬─────────────┘       └───────────┬─────────────┘
            │                                 │                                 │
            └─────────────────────────────────┼─────────────────────────────────┘
                                              │
                                              ▼
                              =================================
                              [DETERMINISTIC ELIGIBILITY BOUND]
                              =================================
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │ Eligibility Engine     │
                                  │ (Rules Evaluation)     │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │ Evidence & Action Plan │
                                  │ (Document Guide)       │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                 ┌──────────────────────────┐
                                 │ SahayResponse (Contract) │
                                 └──────────────────────────┘
```

---

## Security Boundaries & Firewalls

```text
                               +-----------------------------------+
                               |       SAHAY SECURITY ENGINE       |
                               +-----------------------------------+
                                                 |
         +-----------------------+---------------+-----------------------+
         |                       |               |                       |
         v                       v               v                       v
┌─────────────────┐     ┌─────────────────┐    ┌─────────────────┐     ┌─────────────────┐
│  DETERMINISTIC  │     │  CRISIS SAFETY  │    │  JURISDICTION   │     │   TTE SANDBOX   │
│   ELIGIBILITY   │     │    FIREWALL     │    │   CONTAINMENT   │     │    BOUNDARY     │
├─────────────────┤     ├─────────────────┤    ├─────────────────┤     ├─────────────────┤
│ Rules engine    │     │ Emergency safety│    │ National/state  │     │ AST parsing     │
│ evaluates facts │     │ instructions    │    │ policy filters  │     │ blocks sys/os.  │
│ deterministically│    │ top priority.   │    │ isolate IN & US │     │ Human approval  │
│ LLM cannot alter│     │ TTE disabled    │    │ welfare data    │     │ required for    │
│ eligibility     │     │ unconditionally │    │ completely.     │     │ tool activation │
└─────────────────┘     └─────────────────┘    └─────────────────┘     └─────────────────┘
```

---

## Modular Pipeline Specification

1. **Frontend Layer (`sahay-frontend`)**
   - Built with React 18, TypeScript 5.2, Vite 6.4, and Tailwind CSS 3.4.
   - Strictly renders structured JSON response payloads from `SahayResponse`.
   - Displays clear urgency badges (`CRISIS`, `HIGH`, `NORMAL`, `INFORMATIONAL`).

2. **AI Orchestrator (`app/services/ai_orchestrator.py`)**
   - Entry point for requests; routes query flow across specialized intent lanes (`CRISIS`, `PUBLIC_SERVICE`, `ELIGIBILITY_CHECK`, `GENERAL_INFORMATION`, `WEB_SEARCH_REQUIRED`, `AMBIGUOUS`).

3. **Semantic Understanding Engine (`app/services/semantic_understanding.py`)**
   - Extracts structured context (employment status, household income, state/district location, family count).
   - Manages multi-turn conversation memory, pronoun resolution (*"Am I eligible for it?"*), and payload topic switching.

4. **Crisis Navigator (`app/services/crisis_navigator.py`)**
   - High-priority safety lane triggered by emergency intent or extreme urgency.
   - Immediately surfaces physical evacuation steps, emergency shelter helplines, and government disaster relief (`SCH-IN-003`).

5. **Eligibility Engine (`app/services/eligibility_engine.py`)**
   - Evaluates confirmed user facts against structured criteria rules.
   - Outputs status (`LIKELY_ELIGIBLE`, `POTENTIALLY_ELIGIBLE`, `INELIGIBLE`, `UNCERTAIN`).
   - Strictly separates legal rule evaluation from probabilistic text generation.

6. **Tool Execution Engine (TTE) (`app/services/tte_engine.py`)**
   - Demonstrates safe, dynamic tool synthesis.
   - Static AST validation (`ast.parse`) rejects dangerous module imports (`sys`, `os`, `subprocess`).
   - Human approval (`PROPOSED` → `APPROVED`) is mandatory before promotion to active registry.
