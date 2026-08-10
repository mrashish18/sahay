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
  <a href="https://github.com/mrashish18/sahay"><strong>💻 GitHub</strong></a> &nbsp;•&nbsp;
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

## 🎯 What is SAHAY?

SAHAY 2.0 is a constrained civic decision-support navigator that converts plain-language citizen situations into verified public-service guidance, deterministic eligibility evaluations, document checklists, and safety-first emergency assistance.

### The Problem
Accessing government welfare and public services during distress is fragmented and difficult:
- **Fragmented Services:** Welfare programs are scattered across dozens of national, state, and municipal portals.
- **Administrative Complexity:** Citizens rarely know the legal titles of government programs they need.
- **Unclear Eligibility:** Dense legal criteria make self-evaluation confusing and error-prone.
- **Emergency Safety Delays:** Generic tools treat life-threatening flood crises like routine paperwork inquiries.

### The Solution
SAHAY converts natural-language queries into structured, actionable civic outcomes:
- **Relevant Discovery:** Matches citizen situations to official welfare and public assistance programs.
- **Deterministic Eligibility:** Evaluates qualifications through a code-verified rules engine outside the LLM.
- **Action Checklists:** Generates required document lists and direct links to official government portals (`.gov.in`, `usa.gov`).
- **Crisis-First Safety:** Automatically surfaces emergency evacuation steps and priority helplines during disasters.

---

## 💡 Why SAHAY?

| Capability | What SAHAY Does |
| :--- | :--- |
| 🧠 **Conversational Intelligence** | Understands natural-language civic queries and contextual follow-ups |
| 🚨 **Crisis-First Routing** | Safety guidance and emergency helplines take priority during disasters |
| ⚖️ **Deterministic Eligibility** | Eligibility decisions remain code-verified outside the probabilistic LLM |
| 🌐 **Jurisdiction Isolation** | Enforces strict containment between Indian (`IN`) and US (`US`) resources |
| 📚 **Verified Knowledge** | Cites official government portals (`pmkisan.gov.in`, `nfs.delhi.gov.in`, `usa.gov`) |
| 🌦️ **Live Information** | Integrates real-time Open-Meteo weather and current information retrieval |
| 🔐 **Sandboxed TTE** | Isolates dynamic tool execution behind AST static safety boundaries |

---

## ⚙️ How It Works

```text
User Message (Plain Language / Hinglish)
                   ↓
      Semantic NLU Understanding
                   ↓
      Intent, Context & Jurisdiction
                   ↓
Crisis / Public Service / Weather / General Info Routing
                   ↓
      Knowledge Base + Live Information
                   ↓
      Deterministic Rules Eligibility Engine
                   ↓
      Action Plan & Document Guide
                   ↓
      Structured SahayResponse JSON Contract
```

---

## 🧠 Core Intelligence Layer

The backend architecture separates interpretation, safety, decision-making, context, live information, and controlled execution across decoupled services:

| Service | File | Responsibility |
| :--- | :--- | :--- |
| **Orchestration** | [`ai_orchestrator.py`](backend/app/services/ai_orchestrator.py) | Coordinates end-to-end request processing workflow |
| **Semantic NLU** | [`semantic_understanding.py`](backend/app/services/semantic_understanding.py) | Extracts intent, facts, entities & handles ambiguity |
| **Crisis Safety** | [`crisis_navigator.py`](backend/app/services/crisis_navigator.py) | First-class priority routing for emergency & safety situations |
| **Eligibility** | [`eligibility_engine.py`](backend/app/services/eligibility_engine.py) | Code-verified deterministic rule criteria evaluation |
| **Knowledge Base** | [`knowledge_base.py`](backend/app/services/knowledge_base.py) | Accesses verified public-service scheme datasets |
| **Memory** | [`conversation_memory.py`](backend/app/services/conversation_memory.py) | Maintains multi-turn context & jurisdiction state |
| **Live Search** | [`web_search_service.py`](backend/app/services/web_search_service.py) | Retrieves real-time weather & live web information |
| **LLM Provider** | [`llm_provider.py`](backend/app/services/llm_provider.py) | Multi-provider LLM abstraction layer |
| **Tool Execution** | [`tte_engine.py`](backend/app/services/tte_engine.py) | Sandboxed tool proposal with AST static safety checks |

---

## 🖥️ Product Experience

### 🏠 Main Interface
<p align="center">
  <img src="screenshots/sahay-homepage.png" alt="Sahay Civic Navigator — Main Interface" width="95%"/>
</p>
<p align="center">
  <em>Natural language public-service discovery with verified program cards and document guidance</em>
</p>

---

### 🚨 Crisis-Aware Assistance
<p align="center">
  <img src="screenshots/sahay-crisis-assistance.png" alt="Safety-first crisis routing for emergency situations" width="95%"/>
</p>
<p align="center">
  <em>First-Class Crisis Routing — Emergency evacuation guidance and priority helplines surface above paperwork</em>
</p>

---

### 🌤️ Live Weather Integration
<p align="center">
  <img src="screenshots/sahay-weather-result.png" alt="Real-time weather forecast payload rendered" width="95%"/>
</p>
<p align="center">
  <em>Real-time Open-Meteo weather forecast integration with location and time-period resolution</em>
</p>

---

### 🛡️ Public Trust Architecture
<p align="center">
  <img src="screenshots/sahay-public-trust.png" alt="Sahay Public Trust Architecture" width="95%"/>
</p>
<p align="center">
  <em>Public Trust Architecture — Verified source traceability, deterministic eligibility, and legal disclaimers</em>
</p>

---

### 🔧 Sandboxed Tool Execution
<p align="center">
  <img src="screenshots/sahay-tool-registry.png" alt="Sahay Tool Execution Engine" width="95%"/>
</p>
<p align="center">
  <em>Tool Execution Engine (TTE) — Sandboxed dynamic tool proposals with AST static analysis and approval gates</em>
</p>

---

## 🎬 Try These Scenarios

| Scenario | Example Query | Demonstrates |
| :--- | :--- | :--- |
| 🥫 **Public Service** | *"mujhe ration chahiye"* | Scheme discovery & document checklist |
| ⚖️ **Eligibility** | *"am I eligible for it?"* | Active scheme pronoun resolution & rule evaluation |
| 🚨 **Crisis Routing** | *"mera ghar pani me doob gaya"* | Emergency safety guidance & helpline dispatch |
| 🌦️ **Live Weather** | *"will it rain tomorrow in Patna?"* | Real-time weather forecast integration |
| 🧠 **General Information** | *"What is Python?"* | Intent separation & factual response |

---

## 🛡️ Trust & Safety

- **Deterministic Eligibility:** Legal criteria in `eligibility_engine.py` are evaluated strictly in Python. Probabilistic LLM outputs can **never** grant eligibility.
- **Crisis Safety Boundary:** Emergencies automatically route to priority evacuation instructions and helpline data, bypassing routine discovery.
- **Jurisdiction Isolation:** National and state policies enforce strict containment between Indian (`IN`) and US (`US`) resources.
- **Source Traceability:** Every scheme cites authoritative government portals (`.gov.in`, `usa.gov`).
- **Sandboxed Execution:** Dynamic tool proposals require AST static analysis (`ast.parse`) blocking dangerous modules (`sys`, `os`, `subprocess`).

---

## 🧰 Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18.2, TypeScript 5.2, Vite 6.4.3 |
| **Styling** | Tailwind CSS 3.4, Lucide Icons |
| **Backend API** | FastAPI 0.110, Python 3.11+, Pydantic v2 |
| **Database & Vector** | PostgreSQL 16, `pgvector` extension |
| **AI & Retrieval** | Multi-Provider LLM Layer (Ollama / OpenAI), Open-Meteo API |
| **Testing** | Pytest 8.1 (77 test suites) |
| **Deployment** | Vercel (Frontend) + Docker Compose (Containerized Stack) |

---

## 🚀 Live Demo

- **Live Application:** [Open SAHAY Live Demo](https://sahay-cyan.vercel.app/)
- **Source Repository:** [GitHub Repository](https://github.com/mrashish18/sahay)

> *Note: The production interface is deployed on Vercel. For local execution with full FastAPI capabilities, run the backend locally or via Docker Compose.*

---

## 📚 Documentation

- 🏗️ **[Architecture Specification](docs/architecture.md)** — Detailed technical design, system pipeline, and trust boundaries

---

## ⚡ Quick Start

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

## ✅ Engineering Status

| Check | Result |
| :--- | :--- |
| **Backend Pytest Suite** | **77 / 77 Passed** |
| **TypeScript Compiler** | **0 Errors** (`npx tsc --noEmit`) |
| **Production Vite Build** | **Passed** (`npm run build`) |
| **Protected Scenarios** | **18 / 18 Verified** |

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
