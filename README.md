<div align="center">

<br/>

# 🏛️ SAHAY 2.0

### **Civic Navigator**

**AI-Powered Public-Service & Crisis Assistance Navigator**

*When citizens face emergencies, bureaucratic complexity, or personal distress — Sahay transforms confusion into actionable civic guidance.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#-technology-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#-technology-stack)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#-technology-stack)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#-technology-stack)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#-technology-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#-technology-stack)
[![Pytest](https://img.shields.io/badge/Pytest-77%2F77_PASSED-success?style=for-the-badge&logo=pytest&logoColor=white)](#-verification-results)

<br/>

[GitHub Repository](https://github.com/mrashish18/sahay) • [Architecture Specification](docs/architecture.md) • [Judge Demo Script](docs/demo-script.md) • [Presentation Deck](docs/presentation_deck.md)

<br/>

<img src="screenshots/sahay-thumbnail.png" alt="Sahay 2.0 Civic Navigator — Hero Cover" width="90%"/>

<br/>

*SAHAY is not just a chatbot. It is a civic decision-support navigator that converts ambiguous citizen requests into verified public-service guidance, deterministic eligibility evaluation, and safety-first crisis assistance.*

</div>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Why Sahay is Different](#-why-sahay-is-different)
- [Key Features](#-key-features)
- [Core User Journeys](#-core-user-journeys)
- [System Architecture](#-system-architecture)
- [Safety & Trust](#-safety--trust)
- [Deterministic Eligibility](#-deterministic-eligibility)
- [Crisis Handling](#-crisis-handling)
- [Conversational Context](#-conversational-context)
- [Jurisdiction Isolation](#-jurisdiction-isolation)
- [Weather Intelligence](#-weather-intelligence)
- [TTE Sandbox Boundary](#-tte-sandbox-boundary)
- [Product Showcase](#-product-showcase)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Configuration](#-environment-configuration)
- [Running Locally](#-running-locally)
- [Testing](#-testing)
- [Verification Results](#-verification-results)
- [Deployment](#-deployment)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)
- [Copyright](#-copyright)

---

## 🚨 The Problem

Accessing public services and emergency welfare during personal distress or crisis is overwhelming, confusing, and fragmented:

| Challenge | Impact |
| :--- | :--- |
| **Fragmented Portals** | Government assistance programs are scattered across dozens of national, state, and district websites |
| **Administrative Terminology** | Citizens rarely know the official name of the welfare program that fits their situation |
| **Opaque Eligibility** | Official guidelines use dense legal text, making self-evaluation error-prone |
| **Document Delays** | Applicants face rejection due to missing or unverified documentation requirements |
| **High-Stakes Emergency Crises** | During disasters (floods, displacement), citizens need physical safety guidance before paperwork |
| **LLM Hallucinations** | Unbounded AI models fabricate non-existent schemes, incorrect rules, or fake approvals |

---

## 💡 The Solution

Sahay functions as an intelligent **civic navigation layer** that transforms raw human situations into structured, actionable outcomes — backed by deterministic rule boundaries and zero fabricated claims.

```mermaid
flowchart LR
    A["🗣️ Human Request<br/><i>Plain language, Hinglish, or regional text</i>"] --> B["🧠 Semantic NLU<br/>Analyzer"]
    B --> C["🎯 Intent & Urgency<br/>Classification"]
    C --> D["📚 Knowledge Base &<br/>Live API Retrieval"]
    D --> E["⚖️ Deterministic<br/>Eligibility Engine"]
    E --> F["📋 Document Checklist &<br/>Source Links"]
    F --> G["✅ Actionable<br/>SahayResponse Contract"]
```

---

## ⚡ Why Sahay is Different

| Feature | Unbounded AI Chatbots | Sahay 2.0 Civic Navigator |
|:---|:---|:---|
| **Crisis Priority** | Mixed text advice & forms | **Safety-First Routing:** Evacuation steps & helplines top priority |
| **Eligibility Evaluation** | Probabilistic LLM guesses | **Deterministic Rule Engine:** Code-verified criteria evaluation |
| **Source Traceability** | Generic web links / hallucinations | **Verified Portal Cites:** Direct official `.gov.in` and `usa.gov` links |
| **Jurisdiction Firewall** | Bleeds US/India data | **Strict Isolation:** India & US datasets contained at retrieval layer |
| **Conversational State** | Drops context on follow-ups | **Context Resolution:** Resolves active scheme pronouns across turns |
| **Tool Evolution** | Unchecked API function calling | **Sandboxed TTE:** Static AST validation & mandatory human approval |

---

## ✨ Key Features

- **🚨 Safety-First Crisis Navigator:** Unconditionally surfaces physical evacuation instructions and emergency shelter helplines *before* administrative paperwork.
- **⚖️ Deterministic Rules-Based Eligibility Engine:** Evaluates user facts (income, employment, location) against structured code rules — legal eligibility is never decided by an LLM.
- **🗣️ Natural Language & Hinglish Support:** Seamlessly handles queries like *"Ration chahiye mere bachon ke liye"* or *"Mera ghar flood me damage ho gaya"*.
- **🔗 Verified Source Traceability:** Cites authoritative government portals (`pmkisan.gov.in`, `nfs.delhi.gov.in`, `usa.gov`).
- **☀️ Real-Time Weather Intelligence:** Integrated with Open-Meteo API for real-time weather forecasts and flood-impact context.
- **🛡️ Sandboxed Tool Execution Engine (TTE):** Demonstrates safe, AST-analyzed, human-gated dynamic tool synthesis.

---

## 🗺️ Core User Journeys

```text
Turn 1: "Ration chahiye mere bachon ke liye"
 └─► Flow: PUBLIC_SERVICE / Food ──► Maps to SCH-IN-014 (NFSA Food Security)

Turn 2: "Am I eligible for it?"
 └─► Resolves "it" to active scheme SCH-IN-001/SCH-IN-014 ──► Evaluates income & employment facts deterministically

Turn 3: "ayushman milega?"
 └─► Topic Switch: Swaps active scheme payload to SCH-IN-006 (Ayushman Bharat Health Insurance)

Turn 4: "Mera ghar flood me damage ho gaya Bihar me"
 └─► Flow: CRISIS (Urgency: CRISIS) ──► Immediate evacuation steps, Bihar Flood Relief (SCH-IN-003), 0 US resource leakage
```

---

## 🏗️ System Architecture

```text
                                +-----------------------------------+
                                |     React Frontend (Vite UI)      |
                                +-----------------------------------+
                                                  | REST API (SahayResponse JSON)
                                                  v
                                +-----------------------------------+
                                |    FastAPI AI Orchestrator        |
                                +-----------------------------------+
                                                  |
              +-----------------------------------+-----------------------------------+
              |                                   |                                   |
              v                                   v                                   v
   Semantic NLU Analyzer                 Crisis Navigator                  Public Service RAG Engine
  (Intent, Facts, Urgency)           (Emergency & Safety First)              (pgvector / Knowledge Base)
              |                                                                       |
              +-----------------------------------+-----------------------------------+
                                                  |
                                                  v
                                      Eligibility Engine (Rules)
                                                  |
                                                  v
                                     Action Planner & Document Guide
                                                  |
                                                  v
                                      SahayResponse JSON Contract
```

---

## 🛡️ Safety & Trust

- **Verified Source Traceability:** Every scheme recommendation links to authoritative government portals.
- **Deterministic Eligibility Boundary:** Code rules strictly isolate legal criteria evaluation from LLM text generation.
- **Safety-First Crisis Routing:** Life-threatening emergencies bypass routine public-service discovery to surface immediate safety guidance.
- **Ambiguity Protection:** Ambiguous or generic user inputs trigger clarification prompts rather than premature scheme recommendations.

---

## ⚖️ Deterministic Eligibility

Legal eligibility for public welfare programs is evaluated using explicit code rules in `app/services/eligibility_engine.py`:
- User facts (income, employment, household size, location) are compared against criteria conditions.
- Output statuses: `LIKELY_ELIGIBLE`, `POTENTIALLY_ELIGIBLE`, `INELIGIBLE`, `UNCERTAIN`.
- Probabilistic LLM outputs can **never** override rule-based eligibility determinations.

---

## 🚨 Crisis Handling

When a user query exhibits emergency intent or high urgency (e.g. floods, displacement, physical danger):
1. **Urgency Assessment:** Urgency level is rated `CRISIS`.
2. **Immediate Evacuation Guidance:** Surfaces physical safety steps (move to high ground, turn off main switches).
3. **Emergency Helplines:** Surfaces state disaster management contacts and shelter links (`SCH-IN-003`).
4. **Tool Isolation:** TTE dynamic code execution is unconditionally disabled during crisis routing.

---

## 🧠 Conversational Context

Sahay maintains active session state across multiple turns via `conversation_memory.py`:
- **Pronoun Resolution:** Follow-up questions like *"Am I eligible for it?"* resolve `"it"` to the active scheme in memory.
- **Payload Clearing:** Switching topics (e.g. Weather → Ration or Ration → Weather) automatically clears stale context payloads.
- **Location & Time Retention:** Preserves city location and time parameters for follow-up queries.

---

## 🌐 Jurisdiction Isolation

Sahay strictly enforces national and state jurisdiction policies:
- **India/Bihar Context:** Returns only Indian national and Bihar state programs (`SCH-IN-*`). Never leaks US resources (FEMA, SNAP).
- **US Context:** Returns only US federal and state programs. Never leaks Indian schemes.

---

## 🌤️ Weather Intelligence

Integrates Open-Meteo real-time weather API for live weather lookups:
- Fetches real-time temperature, precipitation probability, and sky conditions.
- Retains city location context across follow-up queries (*"What about tomorrow?"*).
- New explicit location inputs reset stale prior city parameters.

---

## 🔧 TTE Sandbox Boundary

The Test-Time Tool Evolution (TTE) engine demonstrates sandboxed dynamic tool creation:
- **AST Validation:** `ast.parse` static analysis blocks forbidden module imports (`sys`, `os`, `subprocess`).
- **Human Approval Gate:** Dynamic tool proposals (`PROPOSED`) require explicit approval (`APPROVED`) before promotion to active registry.
- **Crisis Exemption:** Dynamic tools are disabled during emergency crisis routing.

---

## 🖼️ Product Showcase

<div align="center">

<img src="screenshots/sahay-homepage.png" alt="Sahay Homepage" width="85%"/>

*Sahay Civic Navigator — Natural Language Interface*

<br/>

<img src="screenshots/sahay-crisis-assistance.png" alt="Sahay Crisis Assistance" width="85%"/>

*First-Class Crisis Navigator — Immediate Emergency & Safety First Routing*

<br/>

<img src="screenshots/sahay-tool-registry.png" alt="Sahay Tool Registry" width="85%"/>

*Tool Execution Engine (TTE) — Sandboxed Dynamic Tool Management*

</div>

---

## 💻 Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Frontend** | React 18.2, TypeScript 5.2, Vite 6.4.3, Tailwind CSS 3.4, Lucide Icons |
| **Backend API** | Python 3.11+, FastAPI 0.110, Pydantic v2.6, Uvicorn |
| **Database & Vector** | PostgreSQL 16, `pgvector` extension for vector similarity search |
| **AI & Retrieval** | Multi-Provider LLM Layer (Ollama / OpenAI compatible), Open-Meteo Weather API |
| **Testing & Build** | Pytest 8.1 (77 test suites), TypeScript compiler, Vite bundler |
| **Orchestration** | Docker & Docker Compose multi-service deployment |

---

## 📁 Project Structure

```text
sahay/
├── backend/                           ── FastAPI backend application
│   ├── app/
│   │   ├── api/v1/endpoints/          ── REST endpoints (chat, health, services, tools)
│   │   ├── models/                    ── Pydantic data schemas (SahayResponse)
│   │   ├── services/                  ── Core intelligence engine services
│   │   │   ├── ai_orchestrator.py     ★   Central workflow router
│   │   │   ├── semantic_understanding.py ★ NLU, fact & intent analyzer
│   │   │   ├── crisis_navigator.py    ★   Emergency safety router
│   │   │   ├── eligibility_engine.py  ★   Deterministic rule evaluator
│   │   │   ├── knowledge_base.py      ★   Authentic scheme dataset provider
│   │   │   ├── conversation_memory.py ★   Multi-turn context state manager
│   │   │   ├── web_search_service.py  ★   Open-Meteo weather & live search
│   │   │   ├── llm_provider.py        ★   Multi-provider LLM abstraction
│   │   │   └── tte_engine.py              Sandboxed Tool Execution Engine
│   │   ├── config.py                  ── Environment settings
│   │   └── main.py                    ── FastAPI application entrypoint
│   ├── tests/                         ── 13 pytest test modules (77 test suites)
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/                          ── React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── App.tsx                    ★   Application root workspace
│   │   ├── components/                ── 16 React components
│   │   ├── services/                  ── Frontend API client (api.ts)
│   │   ├── types/                     ── TypeScript interface definitions
│   │   └── index.css                  ── Tailwind CSS design tokens
│   ├── package.json
│   └── vite.config.ts
│
├── data/raw/
│   └── authentic_schemes.json         ── Verified government scheme dataset
├── docs/                              ── Architecture, presentation, & demo docs
│   ├── architecture.md                    Architecture specification
│   ├── demo-script.md                     5-minute judge demo script
│   ├── presentation_deck.md               10-slide presentation deck
│   └── submission_checklist.md            Submission verification checklist
├── screenshots/                       ── Application product screenshots
├── docker-compose.yml                 ── Multi-container orchestration
├── .env.example                       ── Environment template
└── README.md
```

---

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/mrashish18/sahay.git
cd sahay

# Set up environment configuration
cp .env.example .env
```

---

## ⚙️ Environment Configuration

Key settings in `.env`:

```env
ENVIRONMENT=development
PORT=8000
SECRET_KEY="dev_secret_key_change_in_production"
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/sahay_db"
LLM_PROVIDER=mock        # Options: mock, ollama, openai
EMBEDDING_PROVIDER=mock   # Options: mock, openai
OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

---

## 🚀 Running Locally

### Backend (Python FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

The React frontend will start at `http://localhost:5173`.

---

## 🧪 Testing

Run backend test suite:

```bash
cd backend
python -m pytest
```

Run frontend type check:

```bash
cd frontend
npx tsc --noEmit
```

---

## ✅ Verification Results

- **Backend Pytest Suite:** `77 / 77 PASSED` (0 errors in 32.00s)
- **Frontend TypeScript Check:** `0 ERRORS` (`npx tsc --noEmit`)
- **Production Build:** `PASSED` (`npx vite build` in 2.53s)
- **Protected Scenarios:** 18 benchmark conversational scenarios verified

---

## 🚢 Deployment

Deploy with Docker Compose:

```bash
docker-compose up --build -d
```

Starts PostgreSQL (`pgvector`), FastAPI backend, and React frontend as a unified stack.

---

## 🗺️ Future Roadmap

- **Expanded Dataset Integration:** Ingest additional state and municipal welfare schemes.
- **Indian Language Speech Interface:** Add native voice input and text-to-speech (Hindi, Maithili, Bhojpuri, Bengali).
- **Location-Aware District Dispatch:** Automated mapping to local ration shops, shelters, and e-District centers.
- **Offline Relief Mode:** Lightweight cached navigation for crisis response in disaster-affected low-connectivity zones.

---

## 📄 License

Refer to repository details for licensing terms.

---

## © Copyright

Copyright © 2026 Ashish Kumar. All rights reserved.

*Sahay — because navigating public services shouldn't require navigating bureaucracy.*
