<div align="center">

<br/>

# 🏛️ SAHAY

### **Civic Navigator**

**AI-Powered Public-Service & Crisis Assistance Navigator**

*When citizens face emergencies, bureaucratic complexity, or personal distress — Sahay transforms confusion into actionable civic guidance.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#tech-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#tech-stack)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#tech-stack)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#tech-stack)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#tech-stack)

<br/>

[GitHub Repository](https://github.com/mrashish18/sahay)

<br/>

<img src="screenshots/sahay-homepage.png" alt="Sahay Civic Navigator — Main Interface" width="85%"/>

<br/>

*The Sahay Civic Navigator — natural-language civic discovery, crisis routing, and public service guidance in one conversational interface.*

</div>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Sahay Approach](#-the-sahay-approach)
- [Key Capabilities](#-key-capabilities)
- [Product Showcase](#%EF%B8%8F-product-showcase)
- [System Architecture](#-system-architecture)
- [How It Works](#-how-it-works)
- [User Journeys](#-example-user-journeys)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Run Locally](#%EF%B8%8F-run-locally)
- [Trust & Safety Principles](#-trust--safety-principles)
- [Hackathon Highlights](#-hackathon-highlights)
- [Future Roadmap](#%EF%B8%8F-future-roadmap)
- [Contributing](#-contributing)
- [License & Acknowledgements](#-license--acknowledgements)

---

## 🚨 The Problem

Accessing public services and emergency welfare during personal distress or crisis is overwhelming, confusing, and fragmented:

| Challenge | Impact |
| :--- | :--- |
| **Fragmented Information** | Government assistance programs are scattered across dozens of national, state, and district portals |
| **Service Misalignment** | Citizens often don't know the official name of the welfare program that fits their situation |
| **Complex Eligibility Criteria** | Official guidelines use dense administrative language, making self-evaluation difficult |
| **Unclear Document Requirements** | Applicants face rejection or delays due to missing or incorrect documentation |
| **High-Stakes Emergency Needs** | During crises (floods, displacement), citizens need immediate safety guidance — not paperwork |
| **AI Chatbot Hallucinations** | Standard LLMs can hallucinate non-existent schemes, incorrect procedures, or guarantee approvals they cannot grant |

> **Bottom line:** A flood-displaced family in Bihar shouldn't need to search five government websites to find if they qualify for emergency housing assistance — or worse, receive fabricated information from an AI chatbot.

---

## 💡 The Sahay Approach

Sahay functions as an intelligent **civic navigation layer** that transforms raw human situations into structured, actionable outcomes — without hallucination.

```mermaid
flowchart LR
    A["🗣️ Human Situation<br/><i>Plain language, Hinglish, or regional input</i>"] --> B["🧠 Semantic Understanding<br/>Engine"]
    B --> C["🎯 Intent & Context<br/>Resolution"]
    C --> D["📚 Authentic Scheme &<br/>Crisis Database"]
    D --> E["⚖️ Deterministic<br/>Eligibility Engine"]
    E --> F["📋 Document<br/>Checklist"]
    F --> G["✅ Step-by-Step<br/>Action Plan"]
```

### Design Principles

| Principle | Implementation |
| :--- | :--- |
| **Safety First** | Crisis situations unconditionally prioritize physical safety over administrative processes |
| **Zero Hallucination** | Eligibility evaluation uses deterministic rule-based logic, never LLM-generated legal claims |
| **Source Transparency** | Every recommendation links to verified government portals and issuing authorities |
| **Conversational Intelligence** | Accepts natural language including Hinglish (`"ration chahiye mere bacho ke liye"`) |
| **Ambiguity Protection** | Prefers clarification over guessing — generic inputs never force-trigger scheme cards |

---

## ✨ Key Capabilities

<table>
  <tr>
    <td width="50%">

### 🗣️ Conversational Civic Assistance
Accepts unstructured English, Hinglish, or regional inputs to understand citizen needs conversationally. Multi-turn conversation memory maintains context across follow-up questions.

### 🚨 Priority Crisis Navigation
Unconditionally prioritizes emergency physical safety, disaster helplines, and shelter resources during floods, fires, earthquakes, and displacement crises.

### 🔍 Public-Service & Program Discovery
Matches user situations with verified social welfare programs — food assistance (NFSA/PMGKAY), housing (PMAY), farmer support (PM-KISAN), health insurance (Ayushman Bharat), and more.

### ⚖️ Deterministic Eligibility Evaluation
Evaluates criteria transparently using a rule-based engine — reporting *"You may be eligible"* or *"More information needed"* without making false legal claims.

</td>
<td width="50%">

### 📋 Document Guidance Checklist
Generates complete checklists of required and optional documents, detailing exact issuing authorities and where to obtain them.

### 🌦️ Live Weather Assistance
Integrates with Open-Meteo API for real-time daily and hourly weather forecasts (temperature, rain probability, wind) with time-period support (morning, afternoon, evening, night).

### 🌍 Multi-Jurisdiction System
Strict jurisdiction boundaries ensure Indian schemes only appear for Indian users and US resources (FEMA, SNAP) only appear for US context. No cross-contamination.

### 🛡️ Controlled Tool Execution (TTE)
Operates a versioned Tool Registry with AST static analysis and sandboxed execution for safe, auditable tool evolution — no `exec()` or `eval()` ever.

</td>
  </tr>
</table>

---

## 🖼️ Product Showcase

### Civic Navigator Interface

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="screenshots/sahay-homepage.png" alt="Sahay Homepage" width="100%"/>
      <br/><b>Main Product Interface</b><br/><i>Natural-language query bar and quick-start civic pathways.</i>
    </td>
    <td width="50%" align="center">
      <img src="screenshots/sahay-how-it-works.png" alt="How It Works" width="100%"/>
      <br/><b>System & Workflow Overview</b><br/><i>Architectural flow from user input to structured guidance.</i>
    </td>
  </tr>
</table>

### Crisis & Emergency Assistance

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="screenshots/sahay-crisis-assistance.png" alt="Crisis Assistance" width="100%"/>
      <br/><b>Crisis Assistance Workflow</b><br/><i>Immediate safety guidelines and emergency helpline routing.</i>
    </td>
    <td width="50%" align="center">
      <img src="screenshots/sahay-emergency-flood-assistance.png" alt="Emergency Flood Assistance" width="100%"/>
      <br/><b>Emergency Flood Assistance</b><br/><i>Disaster shelter, relief resources, and immediate safety steps.</i>
    </td>
  </tr>
</table>

### Trust, Safety & Weather

<table width="100%">
  <tr>
    <td width="33%" align="center">
      <img src="screenshots/sahay-public-trust.png" alt="Public Trust" width="100%"/>
      <br/><b>Public Trust & Safety</b><br/><i>Grounded responses and verified source citations.</i>
    </td>
    <td width="33%" align="center">
      <img src="screenshots/sahay-tool-registry.png" alt="Tool Registry" width="100%"/>
      <br/><b>TTE Tool Registry</b><br/><i>Sandboxed tool inspection and security linting.</i>
    </td>
    <td width="33%" align="center">
      <img src="screenshots/sahay-weather-result.png" alt="Weather Result" width="100%"/>
      <br/><b>Live Weather Forecast</b><br/><i>Open-Meteo temperature & rain probability.</i>
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        SAHAY CIVIC NAVIGATOR                           │
  │                                                                        │
  │   React + TypeScript + Tailwind CSS (Frontend)                         │
  │   ┌────────────────────────────────────────────────────────────────┐   │
  │   │  Chat Interface  │  Structured Response View  │  Dashboard    │   │
  │   │  Quick Actions    │  Judge Scenarios Bar       │  TTE Modal   │   │
  │   └────────────────────────────────────────────────────────────────┘   │
  │                              │ REST API                                │
  │   ┌──────────────────────────┴─────────────────────────────────────┐   │
  │   │              FastAPI Backend (Async, Pydantic v2)              │   │
  │   │                                                                │   │
  │   │   ┌──────────────────┐    ┌──────────────────────────────┐    │   │
  │   │   │  Conversation    │    │     AI Orchestrator          │    │   │
  │   │   │  Memory          │───▶│  (Central Intelligence       │    │   │
  │   │   │  (Multi-Turn)    │    │   Flow Router)               │    │   │
  │   │   └──────────────────┘    └───────┬──────────────────────┘    │   │
  │   │                                   │                            │   │
  │   │          ┌────────────────────────┼────────────────────┐       │   │
  │   │          ▼                        ▼                    ▼       │   │
  │   │   ┌─────────────┐   ┌──────────────────┐   ┌─────────────┐   │   │
  │   │   │   Crisis     │   │    Semantic       │   │  Weather /  │   │   │
  │   │   │  Navigator   │   │  Understanding   │   │  Web Search │   │   │
  │   │   │  (Safety     │   │    Engine         │   │  Service    │   │   │
  │   │   │   First)     │   │  (NLU + Context)  │   │  (Open-     │   │   │
  │   │   └─────────────┘   └───────┬──────────┘   │   Meteo)    │   │   │
  │   │                             │               └─────────────┘   │   │
  │   │          ┌──────────────────┼─────────────────────┐           │   │
  │   │          ▼                  ▼                     ▼           │   │
  │   │   ┌─────────────┐   ┌─────────────┐   ┌──────────────────┐  │   │
  │   │   │  Knowledge   │   │ Eligibility  │   │   TTE Engine     │  │   │
  │   │   │  Base        │   │  Engine      │   │ (Sandboxed Tool  │  │   │
  │   │   │  (Authentic  │   │ (Determini-  │   │  Evolution)      │  │   │
  │   │   │   Schemes)   │   │  stic Rules) │   └──────────────────┘  │   │
  │   │   └──────┬──────┘   └──────┬──────┘                          │   │
  │   │          │                  │                                  │   │
  │   │          ▼                  ▼                                  │   │
  │   │   ┌─────────────────────────────────────────────────────┐     │   │
  │   │   │        RAG Pipeline (pgvector Similarity Search)    │     │   │
  │   │   └─────────────────────────────────────────────────────┘     │   │
  │   └────────────────────────────────────────────────────────────────┘   │
  │                              │                                         │
  │   ┌──────────────────────────┴─────────────────────────────────────┐   │
  │   │      PostgreSQL 16 + pgvector  │  Ollama / OpenAI LLM Layer   │   │
  │   └────────────────────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ How It Works

Sahay employs a **multi-stage intelligence pipeline** that separates language understanding from deterministic decision-making:

```text
User Input (English / Hinglish / Regional)
   │
   ▼
[Semantic Understanding Engine]  ──►  Context Normalization & Ambiguity Guard
   │
   ├─► CRISIS Intent            ──►  Emergency Safety Hotlines & Immediate Relief
   ├─► WEATHER Intent           ──►  Open-Meteo Hourly/Daily Forecast API
   ├─► GENERAL INFORMATION      ──►  Conversational Knowledge Response
   ├─► AMBIGUOUS Intent         ──►  Conversational Clarification Prompt
   └─► PUBLIC SERVICE Intent    ──►  Vector Search (pgvector RAG) + Knowledge Base
                                           │
                                           ▼
                                [Eligibility Engine]
                                (Deterministic Rule Evaluation)
                                           │
                                           ▼
                                [Document Checklist & Action Planner]
                                           │
                                           ▼
                                [Structured SahayResponse]
```

### Core Pipeline Components

| Component | File | Responsibility |
| :--- | :--- | :--- |
| **Semantic Understanding Engine** | `semantic_understanding.py` | Normalizes input, handles typos/Hinglish, extracts locations and time periods, resolves multi-turn follow-ups |
| **AI Orchestrator** | `ai_orchestrator.py` | Central intelligence flow router — classifies intent and dispatches to specialized engines |
| **Crisis Navigator** | `crisis_navigator.py` | Intercepts physical safety emergencies to present safety guidelines first, before any administrative data |
| **Eligibility Engine** | `eligibility_engine.py` | Evaluates criteria against confirmed user facts deterministically — no LLM hallucination |
| **Knowledge Base** | `knowledge_base.py` | Loads, indexes, and retrieves authentic government scheme datasets |
| **RAG Pipeline** | `rag_service.py` | Vector similarity search over scheme embeddings stored in PostgreSQL with pgvector |
| **Web Search / Weather** | `web_search_service.py` | Open-Meteo API integration for real-time weather; web search for supplemental info |
| **Conversation Memory** | `conversation_memory.py` | Maintains multi-turn context: location, jurisdiction, active scheme, time period |
| **LLM Provider** | `llm_provider.py` | Multi-provider LLM integration layer (Ollama, OpenAI, mock) |
| **TTE Engine** | `tte_engine.py` | Sandboxed tool evolution with AST static analysis and security linting |
| **Situation Analyzer** | `situation_analyzer.py` | Extracts structured facts (employment, income, location, family size) |
| **Tool Registry** | `tool_registry.py` | Versioned tool management with human approval gates |

---

## 👤 Example User Journeys

### Journey 1: Citizen Seeking Food Assistance (Hinglish)

> **User**: `"ration chahiye mere bacho ke liye"` *(I need ration for my children)*
>
> **Sahay**: Classifies intent as `FOOD_ASSISTANCE` → queries authentic knowledge base → returns **National Food Security Act (NFSA)** with document requirements and application steps.
>
> **User**: `"Am I eligible for it?"`
>
> **Sahay**: Locks context to NFSA (SCH-IN-014) → runs deterministic eligibility check → asks for missing facts conversationally (*"Could you share your location and family details so I can check your eligibility?"*).

---

### Journey 2: Family Affected by Emergency Flooding

> **User**: `"My house was damaged by flooding and we have nowhere to stay."`
>
> **Sahay**: Intercepts as `CRISIS` → places **immediate physical safety guidelines first** → provides NDRF / State Disaster Relief helpline numbers → details emergency shelter procedures.

> **User** (Hinglish): `"mera ghar pani me doob gya"` *(My house drowned in water)*
>
> **Sahay**: Recognizes Hinglish crisis expression → same safety-first routing → no internal text leaks.

---

### Journey 3: Weather Forecast with Follow-Ups

> **User**: `"Will it rain tomorrow in Patna?"`
>
> **Sahay**: Queries Open-Meteo API → returns daily forecast for Patna with temperature and rain probability.
>
> **User**: `"what about evening?"`
>
> **Sahay**: Inherits Patna + tomorrow context → returns hourly evening (5:00 PM – 8:59 PM) forecast.

---

### Journey 4: Multi-Scheme Eligibility Navigation

> **User**: `"mujhe ration chahiye"` → `"Am I eligible for it?"` → `"pmay milega mujhe"` → `"ayushman milega?"`
>
> **Sahay**: Tracks scheme context across turns:
> - Turn 1: NFSA food assistance (SCH-IN-014)
> - Turn 2: Eligibility check locked to SCH-IN-014
> - Turn 3: Explicit PMAY override → switches to PMAY (SCH-IN-001)
> - Turn 4: Explicit Ayushman override → switches to Ayushman Bharat (SCH-IN-006)

---

### Journey 5: Jurisdiction Isolation

> **User**: `"I need food assistance in Bihar."` → then in new context: `"I need food assistance in the US."`
>
> **Sahay**: Bihar query returns **Indian resources only** (no FEMA, no SNAP). US query returns **US resources only** (no Bihar schemes). Strict jurisdiction boundaries prevent cross-contamination.

---

## 💻 Tech Stack

<a id="tech-stack"></a>

### Frontend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| React | 18.2 | Component-based UI framework |
| TypeScript | 5.2 | Type-safe application code |
| Vite | 5.1 | Fast frontend build tooling and dev server |
| Tailwind CSS | 3.4 | Utility-first styling |
| Lucide React | 0.344 | Civic icon library |

### Backend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| Python | 3.11+ | Backend runtime |
| FastAPI | 0.110+ | Asynchronous REST API framework |
| Pydantic | v2.6+ | High-performance data validation |
| SQLAlchemy | 2.0+ | Async database ORM |
| AsyncPG | 0.29+ | PostgreSQL async driver |

### AI & Data
| Technology | Purpose |
| :--- | :--- |
| Ollama / OpenAI API | Multi-provider LLM integration layer |
| PostgreSQL 16 + pgvector | Vector database for RAG document embeddings |
| Open-Meteo Weather API | Global live weather forecast integration |

### Testing & Infrastructure
| Technology | Purpose |
| :--- | :--- |
| Pytest | Automated backend unit and integration testing |
| Docker & Docker Compose | Containerized multi-service orchestration |

---

## 📁 Project Structure

```text
sahay/
├── backend/
│   ├── app/
│   │   ├── api/                  # REST API routes (/api/v1/chat, health)
│   │   ├── models/               # Pydantic & SQLAlchemy data schemas
│   │   ├── services/             # Core Sahay engine services
│   │   │   ├── ai_orchestrator.py        # Central intelligence flow router
│   │   │   ├── semantic_understanding.py # Query normalization & ambiguity guard
│   │   │   ├── crisis_navigator.py       # Priority safety & emergency routing
│   │   │   ├── eligibility_engine.py     # Deterministic rules-based evaluation
│   │   │   ├── knowledge_base.py         # Authentic scheme dataset provider
│   │   │   ├── rag_service.py            # Vector embeddings & similarity search
│   │   │   ├── web_search_service.py     # Open-Meteo API & web search
│   │   │   ├── conversation_memory.py    # Multi-turn context management
│   │   │   ├── llm_provider.py           # Multi-provider LLM integration
│   │   │   ├── situation_analyzer.py     # Fact extraction (income, location)
│   │   │   ├── tool_registry.py          # Versioned tool management
│   │   │   └── tte_engine.py             # Sandboxed Tool Execution Engine
│   │   ├── config.py             # Settings & environment configuration
│   │   └── main.py               # FastAPI application entrypoint
│   ├── tests/                    # Backend pytest suite (12 test modules)
│   ├── pyproject.toml            # Backend dependencies & build settings
│   └── requirements.txt          # Python package requirements
├── frontend/
│   ├── src/
│   │   ├── components/           # 16 React UI components
│   │   │   ├── ChatInterface.tsx         # Main chat conversation view
│   │   │   ├── StructuredResponseView.tsx# Civic response card renderer
│   │   │   ├── Hero.tsx                  # Landing page hero section
│   │   │   ├── Dashboard.tsx             # System dashboard
│   │   │   ├── JudgeScenariosBar.tsx     # Pre-loaded demo scenarios
│   │   │   └── ...                       # Header, Footer, QuickActions, etc.
│   │   ├── services/             # Frontend API client
│   │   ├── types/                # TypeScript interface definitions
│   │   ├── App.tsx               # Main React application workspace
│   │   ├── index.css             # Tailwind CSS tokens & styling
│   │   └── main.tsx              # React DOM entrypoint
│   ├── package.json              # Frontend dependencies & scripts
│   └── vite.config.ts            # Vite bundler configuration
├── data/
│   └── raw/
│       └── authentic_schemes.json # Verified government scheme dataset
├── docs/                          # Architecture & policy documentation
│   ├── architecture.md            # System architecture specification
│   ├── crisis-navigator.md        # Crisis navigator design
│   ├── jurisdiction-policy.md     # Multi-jurisdiction rules
│   ├── tte.md                     # TTE security specification
│   └── demo-script.md            # Demo walkthrough script
├── screenshots/                   # Product screenshots
├── docker-compose.yml             # Multi-container orchestration
├── .env.example                   # Environment configuration template
└── README.md                      # This file
```

---

## 🛠️ Run Locally

### Prerequisites

- **Node.js** v18+ and `npm`
- **Python** 3.11+
- **Docker & Docker Compose** *(optional, for PostgreSQL with pgvector)*

---

### Step 1 — Clone Repository

```bash
git clone https://github.com/mrashish18/sahay.git
cd sahay
```

### Step 2 — Environment Configuration

```bash
cp .env.example .env
```

Key environment variables:

```env
ENVIRONMENT=development
PORT=8000
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/sahay_db"
LLM_PROVIDER=mock        # Options: mock, ollama, openai, gemini, anthropic
EMBEDDING_PROVIDER=mock   # Options: mock, openai, gemini
```

---

### Step 3 — Run Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run automated tests
python -m pytest

# Start FastAPI server
python -m uvicorn app.main:app --reload --port 8000
```

> Backend runs at `http://127.0.0.1:8000` — Swagger docs at `http://127.0.0.1:8000/docs`

---

### Step 4 — Run Frontend

```bash
cd frontend

# Install dependencies
npm install

# Type-check
npx tsc --noEmit

# Launch dev server
npm run dev
```

> Frontend runs at `http://localhost:5173`

---

### Alternative — Docker Compose

```bash
docker-compose up --build
```

Starts PostgreSQL (pgvector), FastAPI backend, and React frontend as a single stack.

---

## 🛡️ Trust & Safety Principles

Sahay is built around **public trust** — citizens interacting with government welfare information deserve accuracy, not hallucination.

| Principle | Enforcement |
| :--- | :--- |
| **Zero Hallucination** | Eligibility is evaluated by deterministic rule engine, never LLM-generated legal claims |
| **Source Traceability** | Every recommendation cites verified government portals (`pmaymis.gov.in`, `pmkisan.gov.in`, `nfs.delhi.gov.in`) |
| **Crisis Safety Priority** | Emergency routing unconditionally places physical safety above administrative paperwork |
| **Jurisdiction Boundaries** | Indian schemes never bleed into US results and vice versa — enforced at retrieval, eligibility, and crisis layers |
| **No Invented Schemes** | Knowledge base contains only authentic schemes from official government sources |
| **Ambiguity Guards** | Generic or ambiguous inputs trigger clarification prompts, never premature scheme recommendations |
| **TTE Security** | No `exec()`, no `eval()`, no filesystem/network access — AST-validated and human-gated tool evolution |
| **Prompt Injection Defense** | Retrieved evidence is wrapped in untrusted data tags; injection attempts cannot alter eligibility or safety outcomes |

---

## 🏆 Hackathon Highlights

<table>
  <tr>
    <td width="50%">

**🌍 Real-World Social Impact**
Empowers vulnerable citizens and disaster-affected families to access public assistance — in plain language, including Hinglish.

**🧠 Controlled Multimodal Router**
Specialized intent routing across 5 distinct lanes: Crisis, Weather, Public Service, General Info, and Ambiguous — each with isolated handling logic.

**🛡️ Ambiguity Guardrails**
Prevents premature or incorrect government scheme recommendations when context is missing. Sahay asks before it assumes.

</td>
<td width="50%">

**⚖️ Deterministic Eligibility**
Rule-based evaluation separates factual determination from LLM probability — no hallucinated approvals, no fabricated schemes.

**🔧 Sandboxed TTE**
Demonstrates safe, AST-analyzed, human-gated tool evolution for future capability extensions without runtime risk.

**📦 End-to-End Functional Stack**
Production-ready TypeScript UI, async FastAPI backend, pgvector RAG, multi-turn conversation memory, live weather API, and comprehensive pytest suite — all working together.

</td>
  </tr>
</table>

---

## 🗺️ Future Roadmap

- **Expanded Dataset Integration** — Ingest additional national and municipal scheme datasets across states
- **Multilingual Support** — Add native Indian language speech and text processing (Hindi, Maithili, Bhojpuri, Bengali)
- **Voice Interaction** — Integrate speech-to-text and text-to-speech for low-literacy accessibility
- **Location-Aware Dispatch** — Auto-detect district jurisdiction for localized shelter and ration shop mapping
- **Offline Relief Mode** — Support lightweight local caching for crisis navigation during network outages

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/civic-enhancement`)
3. Ensure backend tests pass (`python -m pytest`) and TypeScript builds clean (`npx tsc --noEmit`)
4. Commit changes (`git commit -m 'Add civic feature'`)
5. Push to branch and submit a Pull Request

---

## 📄 License & Acknowledgements

### License

Refer to repository details for licensing terms.

### Credits & Acknowledgements

- **FastAPI** & **Pydantic** — Asynchronous Python API framework and data validation
- **React** & **Vite** — Frontend component engine and build pipeline
- **PostgreSQL** & **pgvector** — Database storage and vector similarity search
- **Open-Meteo** — Global open-source weather forecast API
- **Ollama** — Local LLM runtime
- **Lucide Icons** — Clean UI icon assets
- **Tailwind CSS** — Utility-first CSS framework

---

<div align="center">

**Built with ❤️ for civic empowerment**

*Sahay — because navigating public services shouldn't require navigating bureaucracy.*

</div>
