<div align="center">

# 🏛️ SAHAY 2.0 — Civic Navigator

<p align="center">
  <img
    src="screenshots/sahay-thumbnail.png"
    alt="SAHAY 2.0 — Civic Navigator"
    width="100%"
  />
</p>

<p align="center">
  <strong>AI-Powered Public-Service & Crisis Assistance Navigator</strong>
</p>

<p align="center">
  <em>Find the help you need. Know what to do next.</em>
</p>

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#-technology-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#-technology-stack)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#-technology-stack)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#-technology-stack)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#-technology-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#-technology-stack)
[![Pytest](https://img.shields.io/badge/Pytest-77%2F77_PASSED-success?style=for-the-badge&logo=pytest&logoColor=white)](#-verification)

<br/>

[🚀 Live Demo](#-quick-start) • [📖 Architecture](docs/architecture.md) • [🎬 Judge Demo](docs/demo-script.md) • [📊 Presentation](docs/presentation_deck.md) • [🧪 Verification](docs/submission_checklist.md) • [🚢 Deployment](#-deployment)

</div>

---

## ⚡ What is SAHAY?

**SAHAY is not simply a chatbot.** It is a constrained civic decision-support navigator that converts complex, plain-language citizen situations into verified public-service guidance, deterministic eligibility evaluations, and safety-first emergency assistance.

When citizens face job loss, administrative confusion, or sudden natural disasters, finding the right government assistance is fragmented and overwhelming. Generic AI chatbots often hallucinate non-existent schemes, invent rules, or grant false eligibility claims.

Sahay bridges this gap by combining **natural language understanding (including Hinglish)** with a **Deterministic Rules-Based Eligibility Engine** and a **First-Class Crisis Intercept System**. Every recommendation cites verified official government portals (`pmkisan.gov.in`, `nfs.delhi.gov.in`, `usa.gov`), ensuring 100% source traceability and zero fabricated approvals.

---

## 🚨 The Problem

Accessing public assistance during personal distress or crisis is broken:

| Problem | Why It Matters |
| :--- | :--- |
| **Fragmented Services** | Welfare programs are scattered across dozens of national, state, and municipal websites. |
| **Difficult Terminology** | Citizens rarely know the official administrative title of the welfare program they need. |
| **Eligibility Confusion** | Dense legal criteria make self-evaluation confusing and error-prone for families. |
| **Missing Documentation** | Applicants face delays or rejection due to unverified document requirements. |
| **Emergency Safety Delays** | Generic AI bots treat life-threatening flood crises like routine paperwork inquiries. |
| **AI Hallucination Risk** | Unbounded LLMs invent non-existent schemes, incorrect rules, or false approvals. |

---

## 💡 The SAHAY Approach

Sahay transforms raw citizen situations into structured, actionable civic outcomes via a constrained multi-stage pipeline:

```text
Citizen Situation (Plain Language / Hinglish)
                     ↓
        Semantic NLU Understanding
                     ↓
        Intent & Urgency Classification
                     ↓
        Knowledge Base + Live Search Retrieval
                     ↓
        Deterministic Rules Eligibility Engine
                     ↓
        Action Plan & Document Guide
                     ↓
        Verified SahayResponse JSON Contract
```

---

## 🏆 Differentiation

| Capability | Generic AI Assistant | SAHAY 2.0 |
| :--- | :--- | :--- |
| **Crisis Priority** | Text advice mixed with paperwork | **First-Class Priority:** Evacuation steps & helplines top priority |
| **Eligibility Evaluation** | Probabilistic LLM guesses | **Deterministic Rule Engine:** Code-verified criteria evaluation |
| **Source Traceability** | Generic web links / hallucinations | **Verified Portal Cites:** Direct official `.gov.in` and `usa.gov` links |
| **Jurisdiction Firewall** | Bleeds US/India data across queries | **Strict Isolation:** India & US datasets contained at retrieval layer |
| **Conversational Memory** | Drops context on follow-up questions | **Context Resolution:** Resolves active scheme pronouns across turns |
| **Tool Execution Safety** | Unchecked API function calling | **Sandboxed TTE:** Static AST validation & mandatory human approval |

---

## 🖼️ Product Showcase

### 🏠 Product Experience

<p align="center">
  <img src="screenshots/sahay-homepage.png" alt="Sahay Civic Navigator — Main Interface" width="90%"/>
</p>
<p align="center">
  <em>Sahay Civic Navigator — Natural language public-service discovery and structured civic cards</em>
</p>

---

### 🚨 Crisis Intelligence

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

### 🌤️ Live Weather Intelligence

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

### 🛡️ Trust & Safety

<p align="center">
  <img src="screenshots/sahay-public-trust.png" alt="Sahay Public Trust Architecture" width="90%"/>
</p>
<p align="center">
  <em>Public Trust Architecture — Verified source traceability, deterministic eligibility, and legal disclaimers</em>
</p>

---

### ⚙️ System Workflow

<p align="center">
  <img src="screenshots/sahay-how-it-works.png" alt="Sahay System Workflow" width="90%"/>
</p>
<p align="center">
  <em>End-to-End System Workflow — From plain-language query to structured SahayResponse JSON contract</em>
</p>

---

### 🔧 Sandboxed Tool Execution

<p align="center">
  <img src="screenshots/sahay-tool-registry.png" alt="Sahay Tool Execution Engine" width="90%"/>
</p>
<p align="center">
  <em>Tool Execution Engine (TTE) — Sandboxed dynamic tool proposals with AST static analysis and human approval gates</em>
</p>

---

## 🎬 5-Minute Judge Demo

Follow the complete step-by-step walkthrough in **[docs/demo-script.md](docs/demo-script.md)**:

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

## 🏗️ Architecture

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

Read the full technical specification in **[docs/architecture.md](docs/architecture.md)**.

---

## 🛡️ Trust Architecture

- **Deterministic Eligibility:** Legal rules in `app/services/eligibility_engine.py` evaluate criteria strictly in Python. Probabilistic LLM outputs can **never** grant eligibility.
- **Crisis Safety Boundary:** Emergencies automatically route to priority evacuation instructions and helpline data, bypassing routine discovery.
- **Jurisdiction Isolation:** National and state jurisdiction policies enforce strict containment between Indian (`IN`) and US (`US`) resources.
- **Source Traceability:** Every scheme cites authoritative government portals (`.gov.in`, `usa.gov`).
- **TTE Security:** Dynamic tools require AST static analysis (`ast.parse`) blocking dangerous modules (`sys`, `os`, `subprocess`) and mandatory human approval (`APPROVED`).

---

## 📊 Verification

All verification checks have been empirically executed and passed:

| Verification Suite | Result | Status |
| :--- | :--- | :--- |
| **Backend Pytest Suite** | **77 / 77 Passed** (0 failures in 32.00s) | ✅ Verified |
| **Frontend TypeScript Check** | **0 Errors** (`npx tsc --noEmit`) | ✅ Verified |
| **Production Vite Build** | **Passed** (`npx vite build` in 2.46s) | ✅ Verified |
| **Protected Scenarios** | **18 / 18 Verified** | ✅ Verified |

---

## 💻 Technology Stack

- **Frontend:** React 18.2, TypeScript 5.2, Vite 6.4.3, Tailwind CSS 3.4, Lucide Icons
- **Backend API:** Python 3.11+, FastAPI 0.110, Pydantic v2.6, AsyncIO, Uvicorn
- **Database & Vector:** PostgreSQL 16, `pgvector` extension for vector similarity search
- **AI & Retrieval:** Multi-Provider LLM Layer (Ollama / OpenAI compatible), Open-Meteo Weather API
- **Testing & Build:** Pytest 8.1 (77 test suites), TypeScript strict compiler, Vite bundler
- **Containerization:** Docker & Docker Compose multi-service deployment

---

## 📁 Project Structure

```text
sahay/
├── backend/              # FastAPI application & AI orchestration engine
├── frontend/             # React + TypeScript user interface
├── data/                 # Authentic government welfare dataset (authentic_schemes.json)
├── docs/                 # Architecture, presentation & judge walkthrough docs
├── evaluations/          # Benchmark dataset & evaluation scenarios (benchmark.json)
├── screenshots/          # High-resolution application product evidence
├── scripts/              # Dataset ingestion & vector indexing scripts
├── docker-compose.yml    # Multi-container containerization
├── .env.example          # Environment configuration template
└── README.md             # Project documentation
```

### Core Intelligence Services

```text
backend/app/services/
├── ai_orchestrator.py        # Central workflow router
├── semantic_understanding.py # NLU, fact extraction, & intent analyzer
├── crisis_navigator.py       # Emergency safety router
├── eligibility_engine.py     # Deterministic rule evaluator
├── knowledge_base.py         # Authentic scheme dataset provider
├── conversation_memory.py    # Multi-turn context state manager
├── web_search_service.py     # Open-Meteo weather & live search
├── llm_provider.py           # Multi-provider LLM layer
└── tte_engine.py             # Sandboxed Tool Execution Engine
```

---

## 🚀 Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/mrashish18/sahay.git
cd sahay
cp .env.example .env
```

### 2. Run Backend (PowerShell / Windows)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

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

## 📚 Documentation

| Document | Purpose |
| :--- | :--- |
| **[Architecture Specification](docs/architecture.md)** | Full technical system design and security boundaries |
| **[Judge Demo Script](docs/demo-script.md)** | 5-minute step-by-step judge walkthrough |
| **[Presentation Deck](docs/presentation_deck.md)** | 10-slide judge presentation deck |
| **[Submission Checklist](docs/submission_checklist.md)** | Final verification checklist |

---

## 🚢 Deployment

Deploy the full stack with Docker Compose:

```bash
docker-compose up --build -d
```

---

## 🗺️ Roadmap

- **Multi-State Scheme Dataset Expansion:** Ingest state and municipal welfare programs across all Indian states.
- **Indian Language Speech Interface:** Add native voice input and text-to-speech (Hindi, Maithili, Bhojpuri, Bengali).
- **Location-Aware District Dispatch:** Automated mapping to local ration shops, shelter centers, and e-District portals.
- **Offline Relief Mode:** Lightweight cached navigation for crisis response in low-connectivity disaster zones.

---

## 📜 License

License: See repository licensing information.

---

## © Copyright

Copyright © 2026 Ashish Kumar. All rights reserved.

*Sahay — because navigating public services shouldn't require navigating bureaucracy.*
