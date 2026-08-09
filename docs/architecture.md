# Sahay Architecture Specification

## Overview

**Sahay** is a public-service & crisis assistance navigator built with a modular workflow separating natural language understanding, deterministic eligibility evaluation, source traceability, and tool evolution.

```
React (UI)  --->  FastAPI (Backend)  --->  AI Orchestrator
                                                 |
            +------------------------------------+------------------------------------+
            |                                    |                                    |
            v                                    v                                    v
   Situation Analyzer                     Crisis Agent                      Public Service Navigator
(Fact & Intent Extraction)           (Emergency Routing)                    (RAG Knowledge Base)
            |                                                                         |
            +------------------------------------+------------------------------------+
                                                 v
                                        Eligibility Engine
                                 (Deterministic Rules Evaluation)
                                                 v
                                       Evidence & Source Agent
                                                 v
                                           Action Planner
                                                 v
                                       SahayResponse (Contract)
```

## Modular Pipeline

1. **Frontend (React + Vite + Tailwind CSS - `sahay-frontend`)**
   - Renders structured JSON response from `SahayResponse`.
   - Never parses unstructured raw text blobs.
   - Provides clear badges for `CRISIS`, `HIGH`, `NORMAL`, and `INFORMATIONAL` urgency states.

2. **AI Orchestrator (`app/services/ai_orchestrator.py`)**
   - Receives the request and classifies intent (`CRISIS`, `PUBLIC_SERVICE`, `ELIGIBILITY_CHECK`).
   - Routes flow to appropriate specialized sub-engines.

3. **Situation Analyzer (`app/services/situation_analyzer.py`)**
   - Extracts structured facts (employment, household income, location, family size).
   - Detects missing facts and prepares clarification prompts.

4. **Crisis Agent**
   - Activated when urgency score exceeds threshold (e.g. > 0.7) or crisis keywords are present.
   - Immediately surfaces emergency hotlines and shelter info at top of response.

5. **Eligibility Engine (`app/services/eligibility_engine.py`)**
   - Compares user facts against JSONB rule criteria in `schemes`.
   - Outputs status (`LIKELY_ELIGIBLE`, `POTENTIALLY_ELIGIBLE`, `INELIGIBLE`, `UNCERTAIN`).
   - Separates deterministic rule evaluation from LLM probabilistic inference.

6. **Action Planner & Document Guide**
   - Generates sequential action steps and required document checklists with acquisition directions.
