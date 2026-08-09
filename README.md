<div align="center">

# Sahay

### Civic Navigator
**Public-Service & Crisis Assistance Navigator**

*Helping people find the right public-service and crisis assistance when they need it most.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](#)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#)

[Live Demo](#) • [GitHub Repository](#) • [Project Documentation](#)

<br/>

![Sahay Civic Navigator](screenshots/sahay-homepage.png)

*The Sahay Civic Navigator main interface — facilitating natural-language civic discovery, crisis routing, and public service assistance.*

</div>

---

## 📌 What is Sahay?

**Sahay** is an AI-powered civic assistance platform designed to help citizens navigate public services, emergency welfare, government social programs, eligibility requirements, mandatory documents, and crisis assistance through an intelligent, conversational interface.

Rather than forcing citizens to fill out complex forms or wade through fragmented government portals, Sahay accepts plain, human natural-language descriptions of personal or emergency situations. It processes these inputs through a **controlled, context-aware semantic understanding engine** to deliver verified assistance, step-by-step document checklists, deterministic eligibility guidance, and actionable next steps — without hallucinative claims or unsupported legal promises.

---

## 🚨 The Problem → 💡 The Solution

### The Problem

Accessing public services and emergency welfare during personal distress or crisis is overwhelming, confusing, and fragmented:

- **Fragmented Information**: Government assistance programs are scattered across dozens of national, state, and district web portals.
- **Service Misalignment**: Citizens often do not know the official name of the welfare program or scheme that fits their situation.
- **Complex Eligibility Criteria**: Official guidelines are written in dense administrative language, making self-evaluation difficult.
- **Unclear Document Requirements**: Applicants frequently face rejection or delays due to missing or incorrect documentation.
- **High-Stakes Emergency Needs**: During crises (e.g. floods or displacement), citizens require immediate physical safety guidance rather than administrative paperwork.
- **AI Chatbot Hallucinations**: Standard LLMs can hallucinate non-existent welfare schemes, incorrect application procedures, or guarantee official approvals they cannot grant.

### The Sahay Approach

Sahay functions as an intelligent **civic navigation layer** that transforms raw human situations into structured, actionable outcomes:

```mermaid
flowchart LR
    A[Human Situation] --> B[Semantic Understanding Engine]
    B --> C[Intent & Context Resolution]
    C --> D[Authentic Scheme & Crisis Database]
    D --> E[Deterministic Eligibility Engine]
    E --> F[Document Checklist]
    F --> G[Step-by-Step Action Plan]
```

---

## ✨ Key Capabilities

| Feature | Description |
| :--- | :--- |
| **Conversational Civic Assistance** | Accepts unstructured English, Hinglish, or regional inputs to understand citizen needs conversationally. |
| **Priority Crisis Navigation** | Unconditionally prioritizes emergency physical safety, disaster helplines, and shelter resources during floods or crises. |
| **Public-Service & Program Discovery** | Matches user situations with verified social welfare programs, food assistance (NFSA/PMGKAY), housing (PMAY), and employment support. |
| **Deterministic Eligibility Evaluation** | Evaluates criteria transparently using a rule-based engine ("You may be eligible") without making false legal claims. |
| **Document Guidance Checklist** | Generates complete checklists of required and optional documents, detailing exact issuing authorities. |
| **Step-by-Step Action Plan** | Provides sequential, prioritized action plans from document collection to application submission. |
| **Live Weather Assistance** | Integrates with Open-Meteo API for real-time daily and hourly weather forecasts (temperature, rain probability, wind). |
| **Ambiguity Protection & Guardrails** | Prefers clarification over guessing; generic unknown inputs never force-trigger public service cards. |
| **Controlled Tool Execution (TTE)** | Operates a versioned Tool Registry with AST static analysis and sandboxed execution for safe tool expansion. |
| **Public Trust & Transparency** | Cites verified government portals and issuing sources for every recommendation presented. |

---

## 🖼️ Product Showcase

### 1. Civic Navigator

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="screenshots/sahay-homepage.png" alt="Sahay Homepage" width="100%"/>
      <br/><b>Main Product Interface</b><br/><i>Natural-language query bar and quick-start civic pathways.</i>
    </td>
    <td width="50%" align="center">
      <img src="screenshots/sahay-how-it-works.png" alt="Sahay How It Works" width="100%"/>
      <br/><b>System & Workflow Overview</b><br/><i>Architectural flow from user input to structured guidance.</i>
    </td>
  </tr>
</table>

---

### 2. Crisis & Emergency Assistance

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="screenshots/sahay-crisis-assistance.png" alt="Sahay Crisis Assistance" width="100%"/>
      <br/><b>Crisis Assistance Workflow</b><br/><i>Immediate safety guidelines and emergency helpline routing.</i>
    </td>
    <td width="50%" align="center">
      <img src="screenshots/sahay-emergency-flood-assistance.png" alt="Sahay Emergency Flood Assistance" width="100%"/>
      <br/><b>Emergency Flood Public Assistance</b><br/><i>Disaster shelter, relief resources, and immediate safety steps.</i>
    </td>
  </tr>
</table>

---

### 3. Trust & Controlled Assistance

<table width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="screenshots/sahay-public-trust.png" alt="Sahay Public Trust" width="100%"/>
      <br/><b>Public Trust & Safety Principles</b><br/><i>Grounded responses, verified sources, and transparent disclaimers.</i>
    </td>
    <td width="50%" align="center">
      <img src="screenshots/sahay-tool-registry.png" alt="Sahay Tool Registry" width="100%"/>
      <br/><b>Tool Registry & TTE Inspector</b><br/><i>Sandboxed tool inspection and security linter execution.</i>
    </td>
  </tr>
</table>

---

### 4. Weather Assistance

<table width="100%">
  <tr>
    <td width="33%" align="center">
      <img src="screenshots/sahay-weather-query.png" alt="Weather Query" width="100%"/>
      <br/><b>1. Weather Inquiry</b><br/><i>User asks for weather forecast.</i>
    </td>
    <td width="33%" align="center">
      <img src="screenshots/sahay-weather-response.png" alt="Weather Response" width="100%"/>
      <br/><b>2. Live API Processing</b><br/><i>Open-Meteo integration.</i>
    </td>
    <td width="33%" align="center">
      <img src="screenshots/sahay-weather-result.png" alt="Weather Result" width="100%"/>
      <br/><b>3. Forecast Output</b><br/><i>Temperature & rain probability.</i>
    </td>
  </tr>
</table>

---

## ⚙️ How It Works

Sahay combines a high-performance **FastAPI backend** with a modern **React + TypeScript frontend**, employing a multi-stage intelligence pipeline:

```text
User Input
   │
   ▼
[Semantic Understanding Engine]  ──►  Context Normalization & Ambiguity Guard
   │
   ├─► CRISIS Intent            ──►  Emergency Safety Hotlines & Immediate Relief
   ├─► WEATHER Intent           ──►  Open-Meteo Hourly Forecast API
   ├─► GENERAL INFORMATION      ──►  Conversational Knowledge Response
   ├─► AMBIGUOUS Intent        ──►  Conversational Clarification Prompt
   └─► PUBLIC SERVICE Intent    ──►  Vector Search (pgvector RAG) + Knowledge Base
                                           │
                                           ▼
                                [Eligibility Engine]
                                           │
                                           ▼
                                [Document Checklist & Action Planner]
                                           │
                                           ▼
                                [Structured Sahay Response]
```

### Core Architecture Components

1. **Semantic Understanding Engine**: Normalizes user input, handles typos/Hinglish, extracts locations and time periods, and resolves multi-turn follow-ups.
2. **Crisis Navigator**: Instantly intercepts physical safety emergencies, disaster displacement, or medical crisis inputs to present safety guidelines first.
3. **Deterministic Eligibility Engine**: Evaluates criteria against confirmed user facts deterministically, ensuring transparent reasoning without LLM hallucination.
4. **pgvector RAG Pipeline**: Performs vector similarity search over authentic government scheme datasets stored in PostgreSQL.
5. **Open-Meteo Integration**: Fetches real-time weather metrics (daily and hourly time-periods like morning, afternoon, evening, night).
6. **Trusted Tool Execution (TTE) Engine**: Manages dynamic tool creation with AST static code analysis, security linting, and sandboxed unit test execution.

---

## 💻 Tech Stack

### Frontend
- **React 18**: Component-based UI framework
- **TypeScript 5**: Type-safe application code
- **Vite 5**: Fast frontend build tooling and dev server
- **Tailwind CSS 3.4**: Utility-first styling
- **Lucide React**: Civic icon library

### Backend
- **Python 3.11+**: Backend runtime environment
- **FastAPI 0.110**: Asynchronous REST API framework
- **Pydantic v2**: High-performance data validation schemas
- **SQLAlchemy 2.0 & AsyncPG**: Async database ORM and driver

### AI & Data
- **Ollama / OpenAI API**: Multi-provider LLM integration layer
- **PostgreSQL 16 & pgvector**: Vector database for RAG document embeddings
- **Open-Meteo Weather API**: Global live weather forecast integration

### Testing & Infrastructure
- **Pytest**: Automated backend unit and integration testing
- **Docker & Docker Compose**: Containerized application setup

---

## 📁 Project Structure

```text
SahayAI/
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
│   │   │   ├── rag_service.py            # Vector embeddings & search
│   │   │   ├── web_search_service.py     # Open-Meteo API & web search
│   │   │   ├── tool_registry.py          # Controlled tool management
│   │   │   └── tte_engine.py             # Sandboxed Tool Execution Engine
│   │   ├── config.py             # Settings & environment configuration
│   │   └── main.py               # FastAPI application entrypoint
│   ├── tests/                    # Backend pytest suite
│   ├── pyproject.toml            # Backend dependencies & build settings
│   └── requirements.txt          # Python package requirements
├── frontend/
│   ├── src/
│   │   ├── components/           # Civic Navigator React UI components
│   │   ├── services/             # Frontend API client
│   │   ├── types/                # TypeScript interface definitions
│   │   ├── App.tsx               # Main React application workspace
│   │   ├── index.css             # Tailwind CSS tokens & styling
│   │   └── main.tsx              # React DOM entrypoint
│   ├── package.json              # Frontend dependencies & scripts
│   └── vite.config.ts            # Vite bundler configuration
├── screenshots/                  # High-resolution application screenshots
├── docker-compose.yml            # Multi-container orchestration
├── .env.example                  # Environment configuration template
└── README.md                     # Project documentation
```

---

## 🛠️ Run Locally

### Prerequisites
- **Node.js** v18+ and `npm`
- **Python** 3.11+
- **Docker & Docker Compose** (Optional, for PostgreSQL database)

---

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/sahay.git
cd sahay
```

### Step 2: Environment Configuration
Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env
```

Key environment variables in `.env`:
```env
ENVIRONMENT=development
PORT=8000
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/sahay_db"
LLM_PROVIDER=mock  # Options: mock, ollama, openai
```

---

### Step 3: Run Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # On Linux/macOS
# .\venv\Scripts\activate       # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Run automated tests
python -m pytest

# Start FastAPI server
python -m uvicorn app.main:app --reload --port 8000
```
*Backend runs at `http://127.0.0.1:8000` with Swagger documentation at `http://127.0.0.1:8000/docs`.*

---

### Step 4: Run Frontend

```bash
cd frontend

# Install Node dependencies
npm install

# Type-check TypeScript code
npx tsc --noEmit

# Launch Vite development server
npm run dev
```
*Frontend runs at `http://localhost:5173`.*

---

### Option B: Run via Docker Compose

```bash
docker-compose up --build
```

---

## 👤 Example User Journeys

### Journey 1: Citizen Seeking Food Assistance
- **User Query**: `"ration chahiye mere bacho ke liye"`
- **Sahay Action**: Classifies intent as `FOOD_ASSISTANCE`, queries authentic knowledge base, returns National Food Security Act (NFSA) / PMGKAY Free Ration support with document requirements and application steps.

### Journey 2: Family Affected by Emergency Flooding
- **User Query**: `"My house was damaged by flooding and we have nowhere to stay."`
- **Sahay Action**: Intercepts as `CRISIS`, places immediate physical safety guidelines first, provides NDRF / State Disaster Relief numbers, and details emergency shelter procedures.

### Journey 3: Citizen Checking Local Weather Forecast
- **User Query**: `"Will it rain tomorrow in Patna?"` ➔ Follow-up: `"what about evening?"`
- **Sahay Action**: Queries Open-Meteo API for Patna weather, then inherits Patna and tomorrow context for turn 2 to return the specific evening (5:00 PM – 8:59 PM) hourly rain probability and temperature.

### Journey 4: Citizen Inquiring About Housing Scheme Eligibility
- **User Query**: `"Am I eligible for PMAY?"`
- **Sahay Action**: Routes to `ELIGIBILITY_CHECK`, evaluates income bracket and housing ownership rules deterministically, and presents required income certificates and identity documents.

---

## 💡 Why Sahay?

- **Civic Accessibility**: Converts complex administrative procedures into accessible natural language.
- **Crisis-First Safety**: Prioritizes emergency relief over administrative forms during disasters.
- **Actionable Guidance**: Goes beyond generic explanations to provide itemized document checklists and step-by-step action plans.
- **Controlled Intelligence**: Prevents hallucinated programs through rule-based eligibility checks and vector-retrieved scheme datasets.
- **Trust & Source Transparency**: Links directly to official government portals for every recommendation.
- **Practical Real-World Value**: Built around authentic social welfare schemes and live weather API integrations.

---

## 🏆 Hackathon Highlights

- **Real-World Social Impact**: Empowers vulnerable citizens and disaster-affected families to access public assistance effortlessly.
- **Controlled Multimodal Router**: Implements specialized intent routing (Crisis, Weather, Public Service, General Info, Ambiguous).
- **Ambiguity Guardrails**: Prevents premature or incorrect government scheme recommendations when context is missing.
- **Sandboxed Tool Execution (TTE)**: Demonstrates safe, static-analyzed tool execution for future feature extensions.
- **End-to-End Functional Stack**: Clean, production-ready TypeScript UI backed by asynchronous FastAPI and pgvector database services.

---

## 🗺️ Future Roadmap

- **Expanded Dataset Integration**: Ingest additional national and municipal scheme datasets across states.
- **Multilingual Support**: Add native Indian language speech and text processing (Hindi, Maithili, Bhojpuri, Bengali).
- **Voice Interaction**: Integrate speech-to-text and text-to-speech for low-literacy accessibility.
- **Location-Aware Dispatch**: Auto-detect district jurisdiction for localized shelter and ration shop mapping.
- **Offline Relief Mode**: Support lightweight local caching for crisis navigation during network outages.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/civic-enhancement`).
3. Ensure backend tests pass (`python -m pytest`) and TypeScript builds clean (`npx tsc --noEmit`).
4. Commit changes (`git commit -m 'Add civic feature'`).
5. Push to branch and submit a Pull Request.

---

## 📄 License & Acknowledgements

### License
This repository is released under the **MIT License**.

### Credits & Acknowledgements
- **FastAPI** & **Pydantic**: Asynchronous Python API framework and data validation.
- **React** & **Vite**: Frontend component engine and build pipeline.
- **PostgreSQL** & **pgvector**: Database storage and vector similarity search.
- **Open-Meteo**: Global open-source weather forecast API.
- **Lucide Icons**: Clean UI icon assets.
