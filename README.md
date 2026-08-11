<div align="center">

# 🏛️ SAHAY 2.0
### Civic Navigator

<p align="center">
  <strong>AI-Powered Public-Service & Crisis Assistance Navigator</strong>
</p>

<p align="center">
  <em>Find the help you need. Know what to do next.</em>
</p>

<br/>

<p align="center">
  <a href="https://sahay-cyan.vercel.app/"><strong>🚀 Live Demo</strong></a> &nbsp;•&nbsp;
  <a href="https://github.com/mrashish18/sahay"><strong>💻 GitHub Repository</strong></a> &nbsp;•&nbsp;
  <a href="docs/architecture.md"><strong>🏗️ Architecture Specification</strong></a>
</p>

<br/>

<p align="center">
  <img src="screenshots/sahay-thumbnail.png" alt="SAHAY 2.0 — Civic Navigator" width="100%"/>
</p>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#-technology-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#-technology-stack)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#-technology-stack)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#-technology-stack)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#-technology-stack)
[![Pytest](https://img.shields.io/badge/Pytest-77%2F77_PASSED-success?style=for-the-badge&logo=pytest&logoColor=white)](#-engineering-status)

</div>

---

## 🔗 Live Demo & API

<p align="center">
  <a href="https://sahay-cyan.vercel.app/"><img src="https://img.shields.io/badge/🌐%20Live%20Demo-Open%20Sahay-00C7B7?style=for-the-badge" alt="Live Demo"></a>
  <a href="https://sahay-cyan.vercel.app/api/docs"><img src="https://img.shields.io/badge/📚%20API%20Docs-Swagger%20UI-85EA2D?style=for-the-badge&logo=swagger" alt="API Docs"></a>
  <a href="https://sahay-cyan.vercel.app/api/openapi.json"><img src="https://img.shields.io/badge/📄%20OpenAPI-JSON%20Schema-3178C6?style=for-the-badge" alt="OpenAPI"></a>
  <a href="https://sahay-cyan.vercel.app/api/v1/tools"><img src="https://img.shields.io/badge/🧰%20Tools-Registry-FF9900?style=for-the-badge" alt="Tools Registry"></a>
  <a href="https://sahay-cyan.vercel.app/api/health"><img src="https://img.shields.io/badge/❤️%20Health%20Check-HTTP%20200-22C55E?style=for-the-badge" alt="Health Check"></a>
</p>

| Resource | Link | Description |
| :--- | :--- | :--- |
| 🌐 **Live Application** | [Open Sahay](https://sahay-cyan.vercel.app/) | Production Sahay web application |
| ❤️ **Backend Health** | [Health Check](https://sahay-cyan.vercel.app/api/health) | Backend health status |
| 📚 **API Documentation** | [Swagger UI](https://sahay-cyan.vercel.app/api/docs) | Interactive FastAPI API documentation |
| 📄 **OpenAPI Specification** | [OpenAPI JSON](https://sahay-cyan.vercel.app/api/openapi.json) | Raw OpenAPI 3.1 specification |
| 🧰 **Tools Registry** | [View Tools](https://sahay-cyan.vercel.app/api/v1/tools) | Active Sahay tool registry |
| 💬 **Chat API** | [`POST /api/v1/chat`](https://sahay-cyan.vercel.app/api/v1/chat) | Sahay AI chat endpoint (*POST-only with JSON body*) |

<p align="center">
  <img src="https://img.shields.io/badge/Deployment-Full--Stack%20Vercel-000000?style=flat-square&logo=vercel" alt="Vercel Deployment">
  <img src="https://img.shields.io/badge/Architecture-Same--Origin%20API-22C55E?style=flat-square" alt="Same Origin API">
  <img src="https://img.shields.io/badge/Repository-Public-2563EB?style=flat-square" alt="Public Repository">
</p>

### 🏗️ Production Architecture

- **Frontend**: [https://sahay-cyan.vercel.app/](https://sahay-cyan.vercel.app/)
- **Backend API**: [https://sahay-cyan.vercel.app/api/health](https://sahay-cyan.vercel.app/api/health)
- **API Documentation**: [https://sahay-cyan.vercel.app/api/docs](https://sahay-cyan.vercel.app/api/docs)

Sahay is deployed as a single full-stack Vercel application. The React/Vite frontend is served from the primary domain, while the FastAPI backend is exposed through same-origin `/api/*` serverless routes. This allows desktop and mobile clients to communicate with the production backend without localhost dependencies or a separately hosted backend.

---

## 📌 Executive Summary

**SAHAY 2.0** is an intelligent, constrained civic decision-support platform engineered to bridge the gap between plain-language citizen queries and verified government welfare services.

In times of personal distress or disaster, citizens face overwhelming administrative barriers: scattered welfare portals, dense legal jargon, complex eligibility rules, and dangerous delays during emergency crises. SAHAY transforms unstructured citizen input (in English, Hindi, or Hinglish) into **verified public-service program discovery**, **code-verified deterministic eligibility evaluations**, **actionable document checklists**, and **safety-first crisis routing**.

> 💡 **Core Philosophy:** *AI interprets citizen context; deterministic code evaluates legal criteria; crisis safety takes absolute priority above administrative paperwork.*

---

## 🎯 The Problem & The SAHAY Solution

### 🚨 The Problem
1. **Fragmented Welfare Portals:** Public services and emergency assistance are scattered across dozens of national, state, and municipal websites.
2. **Administrative Complexity:** Citizens rarely know the formal legal titles of government programs (e.g. searching for *"ration for my children"* instead of *"NFSA SCH-IN-014"*).
3. **Confusing Legal Criteria:** Dense eligibility rules lead to self-evaluation confusion and missed benefits.
4. **Emergency Safety Delays:** Standard conversational AI models treat life-threatening flood crises like routine paperwork inquiries, risking citizen safety.

### ✨ The SAHAY Solution
- **Natural-Language Discovery:** Maps plain-language citizen situations directly to official welfare schemes.
- **Deterministic Rules Engine:** Evaluates legal qualifications in Python code outside probabilistic LLM text generation.
- **Actionable Document Checklists:** Provides exact document requirement lists and verified direct links to official government portals (`.gov.in`, `usa.gov`).
- **First-Class Crisis Routing:** Automatically surfaces physical evacuation steps and priority helplines during emergency disasters.

---

## 💡 Why SAHAY?

| Architectural Dimension | What SAHAY Guarantees |
| :--- | :--- |
| 🧠 **Conversational Intelligence** | Understands multi-turn natural queries, Hinglish phrasing, active scheme pronouns, and contextual follow-ups |
| 🚨 **Crisis-First Priority** | Physical safety guidance and emergency helplines unconditionally intercept disaster queries |
| ⚖️ **Deterministic Eligibility** | Legal criteria decisions remain code-verified in Python outside the probabilistic LLM |
| 🌐 **Jurisdiction Isolation** | Enforces strict containment between Indian (`IN`) and US (`US`) welfare resources |
| 📚 **Verified Source Traceability** | Cites official government portals (`pmkisan.gov.in`, `nfs.delhi.gov.in`, `usa.gov`) to eliminate fabrication risk |
| 🌦️ **Live Information Integration** | Integrates real-time Open-Meteo weather API forecasts with location and temporal context resolution |
| 🔐 **Sandboxed Tool Execution (TTE)** | Isolates dynamic tool evaluation behind AST static analysis (`ast.parse`) safety controls |

---

## ⚙️ How It Works

```text
               User Query (English / Hinglish)
                             │
                             ▼
              [ Semantic NLU Understanding ]
        (Extracts Intent, Facts, Location & Jurisdiction)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ Crisis Safety Route ]         [ Standard Civic Route ]
 (Evacuation & Helplines)         (Knowledge Base Retrieval)
            │                                 │
            └────────────────┬────────────────┘
                             ▼
              [ Live Information Integration ]
            (Open-Meteo Weather / Web Search API)
                             │
                             ▼
           [ Deterministic Eligibility Engine ]
        (Code-Verified Rule Criteria Evaluation)
                             │
                             ▼
             [ Action Plan & Document Guide ]
                             │
                             ▼
          Structured SahayResponse JSON Payload
```

---

## 📸 Product Showcase

### 🏠 Civic Assistance & Trust
<p align="center">
  <img src="screenshots/sahay-homepage.png" alt="Sahay Civic Navigator — Main Interface" width="48%"/>
  &nbsp;
  <img src="screenshots/sahay-public-trust.png" alt="Sahay Public Trust Architecture" width="48%"/>
</p>
<p align="center">
  <em>Natural-language public-service discovery paired with verified source traceability & legal disclaimers</em>
</p>

<br/>

### 🚨 Crisis & Safety Routing
<p align="center">
  <img src="screenshots/sahay-crisis-assistance.png" alt="Safety-first crisis routing" width="48%"/>
  &nbsp;
  <img src="screenshots/sahay-emergency-flood-assistance.png" alt="Emergency flood relief guidance" width="48%"/>
</p>
<p align="center">
  <em>First-Class Crisis Routing — Physical evacuation steps & priority helplines surface above paperwork</em>
</p>

<br/>

### 🌦️ Live Intelligence Integration
<p align="center">
  <img src="screenshots/sahay-weather-query.png" alt="Weather query in Hinglish" width="48%"/>
  &nbsp;
  <img src="screenshots/sahay-weather-result.png" alt="Real-time Open-Meteo weather payload" width="48%"/>
</p>
<p align="center">
  <em>End-to-end request processing flow paired with Sandboxed AST Tool Execution Engine (TTE) controls</em>
</p>

---

## 🧠 Core Intelligence Architecture

The backend architecture separates interpretation, safety, decision-making, context, live information, and controlled execution across decoupled services:

| Component | Service File | Architectural Responsibility |
| :--- | :--- | :--- |
| **Orchestrator** | [`ai_orchestrator.py`](backend/app/services/ai_orchestrator.py) | Coordinates end-to-end request processing workflow and fallback logic |
| **Semantic NLU** | [`semantic_understanding.py`](backend/app/services/semantic_understanding.py) | Extracts intent, user facts, location entities, and active pronoun state |
| **Crisis Safety** | [`crisis_navigator.py`](backend/app/services/crisis_navigator.py) | First-class priority routing for emergency disasters & safety threats |
| **Eligibility** | [`eligibility_engine.py`](backend/app/services/eligibility_engine.py) | Code-verified deterministic rule criteria evaluation outside the LLM |
| **Knowledge Base** | [`knowledge_base.py`](backend/app/services/knowledge_base.py) | Hybrid RAG retrieval across verified public-service scheme datasets |
| **Memory** | [`conversation_memory.py`](backend/app/services/conversation_memory.py) | Maintains multi-turn context, location history, and active scheme state |
| **Live Search** | [`web_search_service.py`](backend/app/services/web_search_service.py) | Retrieves real-time Open-Meteo weather & live web information |
| **LLM Provider** | [`llm_provider.py`](backend/app/services/llm_provider.py) | Multi-provider LLM abstraction layer with strict response schema formatting |
| **Tool Execution** | [`tte_engine.py`](backend/app/services/tte_engine.py) | Sandboxed tool proposal engine with AST static security linter |

---

## 🎬 Judge-Ready Demonstration Scenarios

| Scenario | Example Query | Core Capability Tested |
| :--- | :--- | :--- |
| 🥫 **Public Service Discovery** | *"mujhe ration chahiye"* | Scheme matching & required document checklist generation |
| ⚖️ **Contextual Eligibility** | *"am I eligible for it?"* | Active scheme pronoun resolution (`it` → `SCH-IN-014`) & rule evaluation |
| 🚨 **Crisis Safety Routing** | *"mera ghar pani me doob gaya"* | Emergency flood safety guidance & official helpline dispatch |
| 🌦️ **Live Weather Forecast** | *"will tomorrow rain in Patna?"* | Real-time Open-Meteo API integration with location/temporal context |
| 🧠 **General Knowledge** | *"What is Python?"* | Intent separation & factual response without triggering scheme tools |

---

## 🛡️ Trust & Safety Engineering

- **Deterministic Eligibility Isolation:** Legal qualification rules in `eligibility_engine.py` are executed strictly in Python code. Probabilistic LLM outputs can **never** grant or deny eligibility.
- **Crisis Safety Intercept:** Emergency disaster queries unconditionally trigger priority evacuation instructions and official helpline dispatch before administrative paperwork.
- **Jurisdiction Containment:** National and state jurisdiction policies enforce strict boundary rules, preventing Indian schemes from leaking into US queries (and vice versa).
- **Verifiable Source Traceability:** Scheme recommendations cite official government portals (`.gov.in`, `usa.gov`), eliminating hallucination risk for public benefits.
- **AST Static Sandbox Security:** Dynamic Tool Execution (TTE) proposals undergo static AST analysis (`ast.parse`) blocking dangerous imports (`sys`, `os`, `subprocess`) and network access.

---

## 🧰 Technology Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Frontend UI** | React 18.2, TypeScript 5.2, Vite 6.4.3 | Responsive Single Page Application with dynamic response rendering |
| **Styling** | Tailwind CSS 3.4, Lucide Icons | Modern glassmorphism dark theme with accessibility support |
| **Backend API** | FastAPI 0.110, Python 3.11+, Pydantic v2 | High-performance asynchronous REST API architecture |
| **Database & Vector** | PostgreSQL 16, `pgvector` extension | Vector similarity search and relational scheme storage |
| **AI & Retrieval** | Multi-Provider LLM Layer, Open-Meteo API | Hybrid RAG retrieval and real-time live forecast integration |
| **Testing & Quality** | Pytest 8.1 (77 test suites), TypeScript | 100% clean test suite and 0 TypeScript compilation errors |
| **Deployment** | Vercel (Full-Stack) | Unified same-origin deployment for React SPA & FastAPI Serverless API |

---

## 🚀 Live Deployment & Verification

- **🌐 Live Production Application:** [Open SAHAY Live Demo](https://sahay-cyan.vercel.app/)
- **❤️ Backend Health Status:** [https://sahay-cyan.vercel.app/api/health](https://sahay-cyan.vercel.app/api/health)
- **📚 Interactive Swagger API Docs:** [https://sahay-cyan.vercel.app/api/docs](https://sahay-cyan.vercel.app/api/docs)
- **📄 OpenAPI Specification:** [https://sahay-cyan.vercel.app/api/openapi.json](https://sahay-cyan.vercel.app/api/openapi.json)
- **🧰 Active Tools Registry:** [https://sahay-cyan.vercel.app/api/v1/tools](https://sahay-cyan.vercel.app/api/v1/tools)
- **💻 GitHub Source Repository:** [https://github.com/mrashish18/sahay](https://github.com/mrashish18/sahay)

> *Note: Production uses a unified same-origin Vercel deployment where API requests route dynamically to `/api/*` serverless functions. For local standalone development, run the FastAPI backend server on `http://localhost:8002`.*

---

## 📚 Technical Documentation

- 🏗️ **[Architecture Specification](docs/architecture.md)** — System architecture, data flow, modular pipeline, and trust boundaries
- 🛡️ **[Security Documentation](docs/security.md)** — Security model, validation, PII minimization, and safety boundaries
- 📊 **[Evaluation Framework](docs/evaluation.md)** — Evaluation methodology, benchmark scenarios, and reproducible results

---

## ⚡ Quick Start

### 1. Clone Repository & Configure Environment
```bash
git clone https://github.com/mrashish18/sahay.git
cd sahay
cp .env.example .env
```

### 2. Run Backend Server (PowerShell / Windows)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8002 --reload
```

### 3. Run Frontend Server
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## ✅ Engineering Status

| Verification Check | Result | Command / Method |
| :--- | :--- | :--- |
| **Backend Pytest Suite** | **77 / 77 Passed** | `python -m pytest` |
| **TypeScript Compiler** | **0 Errors** | `npx tsc --noEmit` |
| **Production Vite Build** | **Passed** | `npm run build` (`dist/` compiled in 2.49s) |
| **Protected Scenarios** | **18 / 18 Verified** | Comprehensive NLU, Crisis & Weather matrix |

---

## 🔭 Future Roadmap

| Area | Future Direction |
| :--- | :--- |
| 🌍 **Civic Coverage** | Expand verified public-service coverage across additional states and jurisdictions |
| 🗣️ **Multilingual Access** | Enhance regional-language NLU and voice-assisted interaction |
| 🔌 **Government Integrations** | Connect with official government service APIs where publicly available |
| 📡 **Low-Connectivity Support** | Provide cached essential guidance for low-bandwidth environments |
| ♿ **Accessibility** | Expand screen-reader and low-literacy accessibility features |
| 🚨 **Crisis Intelligence** | Extend safety-first routing to additional disaster types and regional resources |

---

## 📜 License & Copyright

**Copyright © 2026 Ashish Kumar. All rights reserved.**

SAHAY 2.0 is provided for hackathon evaluation, demonstration, and educational purposes. Third-party libraries, frameworks, APIs, and services remain subject to their respective licenses and terms.

---

<p align="center">

**SAHAY 2.0 — Civic Navigator**

*Because navigating public services shouldn't require navigating bureaucracy.*

**Built for civic empowerment • Designed for trust • Engineered for impact**

</p>
