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

## 🏆 Verification

- ✅ Backend: 77/77 tests passed
- ✅ Frontend: 0 TypeScript errors
- ✅ Production build: Passed
- ✅ Conversational benchmark: 18/18 scenarios

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

A modular architecture separates the civic interface, intelligence engine, verified data, evaluation assets, and deployment configuration.

```text
sahay/
│
├── backend/          → FastAPI API + civic intelligence engine
├── frontend/         → React + TypeScript user interface
├── data/             → Verified public-service knowledge
├── docs/             → Architecture, demo & presentation assets
├── evaluations/      → Benchmark datasets & evaluation scenarios
├── screenshots/      → Product screenshots & visual evidence
├── scripts/          → Data ingestion & indexing utilities
│
├── docker-compose.yml → Containerized deployment
├── .env.example       → Environment configuration template
└── README.md          → Project documentation
```

### 🧠 Core Intelligence Layer

The intelligence layer separates interpretation, safety, decision-making, context, live information retrieval, and controlled tool execution.

| Service | Responsibility | Role |
| :--- | :--- | :--- |
| **`ai_orchestrator.py`** | Coordinates end-to-end workflows | Orchestration |
| **`semantic_understanding.py`** | Intent, facts, entities & ambiguity | NLU |
| **`crisis_navigator.py`** | Safety-first emergency routing | Safety |
| **`eligibility_engine.py`** | Deterministic eligibility evaluation | Decision |
| **`knowledge_base.py`** | Verified civic scheme knowledge | Trusted Data |
| **`conversation_memory.py`** | Multi-turn context & jurisdiction state | Context |
| **`web_search_service.py`** | Live weather & current information | Retrieval |
| **`llm_provider.py`** | LLM provider abstraction | AI Layer |
| **`tte_engine.py`** | Sandboxed tool proposal/execution | Isolation |

### 🔄 Architecture Flow

```text
User
  ↓
React + TypeScript UI
  ↓
FastAPI API
  ↓
Semantic Understanding
  ↓
AI Orchestrator
  ├── Crisis Navigator ─────→ Safety Guidance
  ├── Knowledge Base ───────→ Verified Services
  ├── Eligibility Engine ───→ Deterministic Decision
  ├── Web Search ────────────→ Current Information
  └── TTE Engine ───────────→ Sandboxed Tools
  ↓
Structured SahayResponse
  ↓
User
```

> **🛡️ Trust Boundary:** The LLM interprets language and context; deterministic services remain responsible for eligibility decisions, crisis safety routing, jurisdiction isolation, and controlled tool execution.

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

## 📜 Legal & Acknowledgements

**License:** No open-source license has currently been declared. SAHAY 2.0 is provided for hackathon evaluation and demonstration purposes.

**© Copyright 2026 Ashish Kumar — All rights reserved.**  
SAHAY / SAHAY 2.0, including original source code, architecture, documentation, and project design assets, is owned by Ashish Kumar.

Third-party libraries, frameworks, APIs, icons, and services remain subject to their respective licenses and terms. Government/public-service information referenced by SAHAY remains subject to the terms of its official sources.

### 🤝 Built With

FastAPI • React • TypeScript • Vite • Tailwind CSS • PostgreSQL • pgvector • Pytest • Open-Meteo • Ollama/OpenAI • Lucide Icons

<br/>

<p align="center">
  <strong>SAHAY 2.0</strong><br>
  <em>Because navigating public services shouldn't require navigating bureaucracy.</em>
</p>

<p align="center">
  Built for civic empowerment • Designed for trust • Engineered for impact
</p>
