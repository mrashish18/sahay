# Sahay 2.0 — Architecture & Intelligence System Memory (BRAIN.md)

## 🏛️ System Overview
Sahay is an intelligent, conversational public-service & crisis assistance navigator built on top of FastAPI, Pydantic v2, PostgreSQL/pgvector, React + Vite, Open-Meteo Weather API, and Ollama/OpenAI LLM providers.

---

## 🏗️ Architecture & Component Boundaries

```
                                 +-----------------------------------+
                                 |    React + Vite + Tailwind UI     |
                                 +-----------------+-----------------+
                                                   |
                                                   v  REST / JSON API
                                 +-----------------+-----------------+
                                 |       FastAPI Backend Server      |
                                 +-----------------+-----------------+
                                                   |
                                 +-----------------+-----------------+
                                 |  Semantic Understanding Engine    |
                                 |  - Contextual Temporal Classifier |
                                 |  - Topic Reset & Ambiguity Guard  |
                                 |  - Multi-Turn Weather Follow-Up   |
                                 |  - Typo & Hinglish Resolution     |
                                 +-----------------+-----------------+
                                                   |
                        +--------------------------+--------------------------+
                        |                                                     |
                        v                                                     v
         +--------------+--------------+                       +--------------+--------------+
         |     Capability Router       |                       |  Open-Meteo & LLM Provider   |
         |  - CRISIS (Priority #1)     |                       |  - Open-Meteo Hourly Weather |
         |  - WEATHER (Hourly API)     |                       |  - OllamaProvider (qwen3:8b) |
         |  - AMBIGUOUS (Clarification)|                       |  - OpenAIProvider            |
         |  - GENERAL_INFORMATION      |                       |  - MockLLMProvider Fallback  |
         |  - PUBLIC_SERVICE           |                       +-----------------------------+
         |  - ELIGIBILITY_CHECK        |
         |  - DOCUMENT_GUIDANCE        |
         +--------------+--------------+
                        |
                        v
         +--------------+--------------+
         | Sahay RAG & Vector Search   |
         |  - Authentic Scheme Dataset |
         |  - Relevance Filtered Recs  |
         +-----------------------------+
```

---

## ⚙️ Key Configuration & Environment Variables

```env
# AI Provider Abstraction
LLM_PROVIDER=ollama                     # 'ollama', 'openai', or 'mock'
OLLAMA_BASE_URL=http://localhost:11434  # Local Ollama endpoint
OLLAMA_MODEL=qwen3:8b                   # Configurable model (qwen3:8b, qwen2.5:7b)
OPENAI_API_KEY=sk-...                   # Fallback for OpenAI (Backend-only)
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

---

## 🔒 Security, Ambiguity & Safety Guarantees

1. **Ambiguity Protection**: Unknown or un-contextual queries (e.g. `"what about evening?"` without weather context, or `"tomorrow + Patna + evening"`) are **NEVER** forced into `PUBLIC_SERVICE`. They resolve to `FlowType.AMBIGUOUS` with clarification and **ZERO** scheme cards.
2. **Context Reset**: Topic switches (e.g. asking `"what is pythn"`) reset active weather location context so previous weather sessions do not hijack future generic follow-ups.
3. **Multi-Turn Weather Follow-Ups**: Preserves location (Patna) and date (tomorrow) across follow-up queries like `"what about evening?"`, retrieving Open-Meteo hourly metrics (5:00 PM – 8:59 PM).
4. **Recommendation Relevance Threshold**: Unrelated schemes (NCS Jobseeker, Birth/Death Registration) are excluded from food assistance queries. Generic scheme padding is eliminated.
5. **Deterministic Eligibility**: LLMs never make official legal claims. `EligibilityEngine` evaluates rules deterministically.
6. **Crisis Priority Guarantee**: Crisis detection (`CRISIS`) unconditionally overrides normal RAG/Web flows and places physical safety instructions first.

---

## 🧪 Automated Testing & Verification Baseline

- **Pytest Test Suite**: `65/65 PASSED` (100% pass rate in 19.09s)
- **TypeScript Type Check**: `0 ERRORS` (`npx tsc --noEmit`)
- **Vite Production Build**: `PASSED` (`dist/` generated cleanly in 4.60s)
- **Live HTTP Server Verification**: Verified on `http://127.0.0.1:8002/api/v1/chat` across all 5 manual browser evaluation scenarios.
