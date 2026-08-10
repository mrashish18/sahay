<div align="center">

# 🏛️ SAHAY 2.0 — Civic Navigator

<p align="center">
  <img
    src="screenshots/sahay-thumbnail.png"
    alt="SAHAY 2.0 Civic Navigator — AI-Powered Public-Service and Crisis Assistance Navigator"
    width="100%"
  />
</p>

<p align="center">
  <strong>Find the help you need. Know what to do next.</strong>
</p>

<br/>

**AI-Powered Public-Service & Crisis Assistance Navigator**

*When citizens face emergencies, bureaucratic complexity, or personal distress — Sahay transforms confusion into actionable, verified civic guidance.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#-technology-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#-technology-stack)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#-technology-stack)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#-technology-stack)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#-technology-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#-technology-stack)
[![Pytest](https://img.shields.io/badge/Pytest-77%2F77_PASSED-success?style=for-the-badge&logo=pytest&logoColor=white)](#-verified-results)

<br/>

[Architecture Specification](docs/architecture.md) • [Judge Demo Script](docs/demo-script.md) • [Presentation Deck](docs/presentation_deck.md) • [Submission Checklist](docs/submission_checklist.md)

</div>

---

## ⚡ Judge Quick Start

If you have 60 seconds to evaluate **SAHAY 2.0**, follow this recommended inspection flow:

1. **Start the Stack:** Run `python -m uvicorn app.main:app --port 8000` (backend) & `npm run dev` (frontend).
2. **Public Service Discovery:** Ask `"Ration chahiye mere bachon ke liye"` → See automatic mapping to `SCH-IN-014` (NFSA Food Security).
3. **Active Pronoun Resolution:** Follow up with `"Am I eligible for it?"` → Watch the Deterministic Rules Engine evaluate your income facts for `SCH-IN-014`.
4. **Explicit Scheme Switching:** Ask `"ayushman milega?"` → See immediate context switch to `SCH-IN-006` (Ayushman Bharat).
5. **Safety-First Crisis Intercept:** Ask `"Mera ghar flood me damage ho gaya Bihar me"` → See instant high-urgency crisis routing, evacuation steps, and zero US/FEMA resource leakage.
6. **Live Weather Query:** Ask `"kal Patna me mausam kaisa rahega?"` → Observe real-time Open-Meteo API data integration.
7. **Inspect Documentation & Verification:** Read the full [Judge Demo Script](docs/demo-script.md) and review our 77/77 passing test suite.

---

## 📌 One-Minute Pitch

**SAHAY is not just a chatbot.** It is an intelligent civic decision-support navigator designed to bridge the gap between vulnerable citizens and official public welfare programs. 

When people experience job loss, health crises, or natural disasters, navigating public assistance is overwhelming. Government portals are fragmented, legal guidelines are opaque, and generic AI chatbots often hallucinate non-existent schemes or grant false eligibility claims.

Sahay solves this by pairing **natural-language conversational intelligence (including Hinglish)** with a **Deterministic Rules-Based Eligibility Engine** and a **Safety-First Crisis Intercept System**. Every recommendation links directly to verified government portals (`.gov.in`, `usa.gov`), ensuring zero fabricated legal approvals.

---

## 🚨 The Problem

Accessing public services and emergency welfare during personal distress or disaster is broken:

| Challenge | Real-World Impact |
| :--- | :--- |
| **Fragmented Information** | Welfare programs are scattered across dozens of national, state, and municipal portals. |
| **Administrative Jargon** | Citizens rarely know the official administrative title of the scheme they need. |
| **Opaque Eligibility** | Official guidelines use dense legal criteria, making self-evaluation error-prone. |
| **Document Delays** | Applicants face rejection due to missing or unverified document requirements. |
| **Emergency Safety Delays** | Generic AI bots treat life-threatening flood crises like routine administrative paperwork. |
| **AI Hallucinations** | Unbounded LLMs invent fake welfare schemes, incorrect rules, or fake legal approvals. |

---

## 💡 The Solution

Sahay functions as a secure, transparent **civic navigation layer** that transforms raw human situations into structured, actionable outcomes — backed by deterministic rule boundaries and verified source traceability.

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

| Feature | Generic LLM Chatbots | Sahay 2.0 Civic Navigator |
|:---|:---|:---|
| **Crisis Priority** | Text advice mixed with paperwork | **First-Class Priority:** Evacuation steps & helplines top priority |
| **Eligibility Evaluation** | Probabilistic LLM guesses | **Deterministic Rule Engine:** Code-verified criteria evaluation |
| **Source Traceability** | Generic web links / hallucinations | **Verified Portal Cites:** Direct official `.gov.in` and `usa.gov` links |
| **Jurisdiction Firewall** | Bleeds US/India data across queries | **Strict Isolation:** India & US datasets contained at retrieval layer |
| **Conversational State** | Drops context on follow-up questions | **Context Resolution:** Resolves active scheme pronouns across turns |
| **Tool Evolution** | Unchecked API function calling | **Sandboxed TTE:** Static AST validation & mandatory human approval |

---

## ✨ Core Capabilities

- **🚨 Crisis Navigator:** Unconditionally surfaces physical evacuation instructions and emergency shelter helplines *before* paperwork during disasters.
- **⚖️ Deterministic Eligibility Engine:** Evaluates user facts against structured criteria rules in code — LLMs never decide legal eligibility.
- **🗣️ Multi-Turn Conversational Memory:** Tracks active schemes, user facts, location, and time parameters across multi-turn conversations.
- **🌐 Jurisdiction Isolation:** Strict policy filters guarantee Indian queries receive only Indian resources (`SCH-IN-*`) with zero US leakage, and vice versa.
- **🔗 Verified Source Traceability:** All scheme guidance links directly to authoritative government portals (`pmkisan.gov.in`, `nfs.delhi.gov.in`).
- **☀️ Weather Intelligence:** Integrated with Open-Meteo API for real-time weather forecasts and flood-impact context.
- **🔧 Sandboxed TTE Engine:** Demonstrates safe, AST-analyzed dynamic tool creation with mandatory human approval gates.

---

## 🖼️ Product Showcase

### 🏠 Main Product Interface

<p align="center">
  <img src="screenshots/sahay-homepage.png" alt="Sahay Civic Navigator — Conversational public-service assistance" width="90%"/>
</p>
<p align="center">
  <em>Sahay Civic Navigator — Natural language public-service discovery and structured civic cards</em>
</p>

---

### 🚨 Safety-First Crisis Navigation

<p align="center">
  <img src="screenshots/sahay-crisis-assistance.png" alt="Safety-first crisis routing for emergency situations" width="90%"/>
</p>
<p align="center">
  <em>First-Class Crisis Routing — Emergency evacuation guidance and priority helplines surface above paperwork</em>
</p>

<br/>

<p align="center">
  <img src="screenshots/sahay-emergency-flood-assistance.png" alt="Flood emergency assistance and verified relief navigation" width="90%"/>
</p>
<p align="center">
  <em>Flood Emergency Assistance — Verified Bihar Flood Relief navigation (`SCH-IN-003`) with zero US resource leakage</em>
</p>

---

### 🌤️ Weather Intelligence Sequence

<p align="center">
  <img src="screenshots/sahay-weather-query.png" alt="1. QUERY — User asks for local weather forecast" width="90%"/>
</p>
<p align="center">
  <em>1. QUERY — User asks for local weather forecast</em>
</p>

<br/>

<p align="center">
  <img src="screenshots/sahay-weather-response.png" alt="2. INTELLIGENCE — NLU classifies weather intent & resolves location" width="90%"/>
</p>
<p align="center">
  <em>2. INTELLIGENCE — NLU classifies weather intent & resolves location</em>
</p>

<br/>

<p align="center">
  <img src="screenshots/sahay-weather-result.png" alt="3. RESULT — Real-time Open-Meteo API forecast payload rendered" width="90%"/>
</p>
<p align="center">
  <em>3. RESULT — Real-time Open-Meteo API forecast payload rendered</em>
</p>

---

### 🛡️ Public Trust & Verified Sources

<p align="center">
  <img src="screenshots/sahay-public-trust.png" alt="Sahay Public Trust Architecture" width="90%"/>
</p>
<p align="center">
  <em>Public Trust Architecture — Verified source traceability, deterministic eligibility, and legal disclaimers</em>
</p>

---

### ⚙️ How It Works

<p align="center">
  <img src="screenshots/sahay-how-it-works.png" alt="Sahay System Workflow" width="90%"/>
</p>
<p align="center">
  <em>End-to-End System Workflow — From plain-language query to structured SahayResponse JSON contract</em>
</p>

---

### 🔧 Sandboxed Tool Execution Engine (TTE)

<p align="center">
  <img src="screenshots/sahay-tool-registry.png" alt="Sahay Tool Execution Engine" width="90%"/>
</p>
<p align="center">
  <em>Tool Execution Engine (TTE) — Sandboxed dynamic tool proposals with AST static analysis and human approval gates</em>
</p>

---

## 🎬 5-Minute Judge Demo Flow

```text
Turn 01: "Ration chahiye mere bachon ke liye"
 └─► Flow: PUBLIC_SERVICE / Food ──► Maps to SCH-IN-014 (NFSA Food Security)

Turn 02: "Am I eligible for it?"
 └─► Pronoun Resolution: Resolves "it" to SCH-IN-014 ──► Evaluates income & employment facts deterministically

Turn 03: "pmay milega mujhe"
 └─► Explicit Switch: Swaps active scheme payload to SCH-IN-001 (PMAY Housing)

Turn 04: "ayushman milega?"
 └─► Explicit Switch: Swaps active scheme payload to SCH-IN-006 (Ayushman Bharat Health Insurance)

Turn 05: "Mera ghar flood me damage ho gaya Bihar me"
 └─► Flow: CRISIS (Urgency: CRISIS) ──► Evacuation steps, Bihar Relief (SCH-IN-003), 0 US/FEMA resource leakage

Turn 06: "What about evening?" (after General Query)
 └─► Flow: AMBIGUOUS ──► Prompts user for necessary clarification before making assumptions
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

- **Verified Source Traceability:** Every scheme recommendation links directly to authoritative government portals.
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

## 🚨 Crisis Safety Boundary

When a user query exhibits emergency intent or high urgency (e.g. floods, displacement, physical danger):
1. **Urgency Assessment:** Urgency level is rated `CRISIS`.
2. **Immediate Evacuation Guidance:** Surfaces physical safety steps (move to high ground, turn off main switches).
3. **Emergency Helplines:** Surfaces state disaster management contacts and shelter links (`SCH-IN-003`).
4. **Tool Isolation:** TTE dynamic code execution is unconditionally disabled during crisis routing.

---

## 🌐 Jurisdiction Isolation

Sahay strictly enforces national and state jurisdiction policies:
- **India/Bihar Context:** Returns only Indian national and Bihar state programs (`SCH-IN-*`). Never leaks US resources (FEMA, SNAP).
- **US Context:** Returns only US federal and state programs. Never leaks Indian schemes.

---

## 🧠 Conversational Intelligence

Sahay maintains active session state across multiple turns via `conversation_memory.py`:
- **Pronoun Resolution:** Follow-up questions like *"Am I eligible for it?"* resolve `"it"` to the active scheme in memory.
- **Payload Clearing:** Switching topics (e.g. Weather → Ration or Ration → Weather) automatically clears stale context payloads.
- **Location & Time Retention:** Preserves city location and time parameters for follow-up queries.

---

## 🔧 TTE Security Boundary

The Test-Time Tool Evolution (TTE) engine demonstrates sandboxed dynamic tool creation:
- **AST Validation:** `ast.parse` static analysis blocks forbidden module imports (`sys`, `os`, `subprocess`).
- **Human Approval Gate:** Dynamic tool proposals (`PROPOSED`) require explicit approval (`APPROVED`) before promotion to active registry.
- **Crisis Exemption:** Dynamic tools are disabled during emergency crisis routing.

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

## 🚀 Quick Start & Installation

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

## 🏃 Running Locally

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

## 🧪 Testing & Verification

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

## 📊 Verified Results

| Verification Suite | Result | Status |
|:---|:---|:---|
| **Backend Pytest Suite** | **77 / 77 PASSED** (0 failures in 32.00s) | ✅ Verified |
| **Frontend TypeScript Check** | **0 ERRORS** (`npx tsc --noEmit`) | ✅ Verified |
| **Production Vite Build** | **PASSED** (`npx vite build` in 2.46s) | ✅ Verified |
| **Conversational Invariants** | **18 / 18 Scenarios Verified** | ✅ Verified |
| **Security Audit** | **0 Secret Leaks / Inputs Sanitized** | ✅ Verified |

---

## 🚢 Deployment

Deploy with Docker Compose:

```bash
docker-compose up --build -d
```

Starts PostgreSQL (`pgvector`), FastAPI backend, and React frontend as a unified stack.

---

## 🗺️ Roadmap

- **Expanded Dataset Integration:** Ingest additional state and municipal welfare schemes across all Indian states.
- **Indian Language Speech Interface:** Add native voice input and text-to-speech (Hindi, Maithili, Bhojpuri, Bengali).
- **Location-Aware District Dispatch:** Automated mapping to local ration shops, shelter centers, and e-District portals.
- **Offline Relief Mode:** Lightweight cached navigation for crisis response in low-connectivity disaster zones.

---

## 📜 License

Refer to repository details for licensing terms.

---

## © Copyright

Copyright © 2026 Ashish Kumar. All rights reserved.

*Sahay — because navigating public services shouldn't require navigating bureaucracy.*
