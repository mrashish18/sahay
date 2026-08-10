# 📊 SAHAY 2.0 — Hackathon Presentation Deck (10 Slides)

---

## 📸 SLIDE 1 — SAHAY 2.0: CIVIC NAVIGATOR

### **AI-Powered Public-Service & Crisis Assistance Navigator**

> *"When citizens face emergencies, bureaucratic complexity, or personal distress — Sahay transforms confusion into actionable civic guidance."*

- **Product:** SAHAY 2.0 Civic Navigator
- **Core Technology:** FastAPI, Pydantic v2, PostgreSQL + pgvector, React + Vite + Tailwind CSS, Open-Meteo Weather API
- **Key Differentiator:** Deterministic rules-based eligibility, safety-first crisis routing, and multi-turn conversational intelligence.

---

## 🚨 SLIDE 2 — THE PROBLEM

### **Public-Service Discovery is Fragmented, Confusing, and Unsafe in Emergencies**

1. **Navigational Bureaucracy**
   - Citizens do not know exact administrative program titles (e.g. *NFSA Food Security*, *PMAY Housing*, *Ayushman Bharat*).
2. **Generic LLM Hallucinations**
   - General AI chatbots fabricate legal eligibility claims, invent non-existent government programs, or cite invalid links.
3. **Emergency Response Delays**
   - Unspecialized AI applications treat life-threatening flood emergencies like routine paperwork inquiries.
4. **Context Loss**
   - Multi-turn follow-ups (*"Am I eligible for it?"*) fail when bots lose location, scheme, or state context across turns.

---

## 💡 SLIDE 3 — THE SOLUTION

### **Transforming Natural Language into Verified Civic Action**

```text
User Question ("Ration chahiye mere bachon ke liye")
                      ↓
  Semantic NLU & Intent Classification (PUBLIC_SERVICE / Food)
                      ↓
   Knowledge Base Retrieval (SCH-IN-014 / NFSA Food Scheme)
                      ↓
 Deterministic Eligibility Engine (Evaluates income & employment facts)
                      ↓
  Actionable Checklist & Source Traceability (pmkisan.gov.in)
```

- **Safety-First Routing:** Crisis queries bypass paperwork and immediately surface physical evacuation instructions & emergency helplines.
- **Deterministic Rules Engine:** Code-enforced eligibility logic ensures zero hallucinated approvals.
- **Actionable Guidance:** Surfaces required document checklists, step-by-step next steps, and direct `.gov.in` issuing authority links.

---

## ⚡ SLIDE 4 — WHY SAHAY IS DIFFERENT

| Feature | Generic LLM Chatbots | Sahay 2.0 Civic Navigator |
|:---|:---|:---|
| **Crisis Handling** | Text advice mixed with paperwork | **First-Class Priority:** Evacuation steps & helplines top priority |
| **Eligibility Determination** | Probabilistic LLM guesses | **Deterministic Rule Engine:** Code-verified criteria |
| **Source Traceability** | Web search links or hallucinations | **Verified Portal Cites:** Direct official `.gov.in` links |
| **Jurisdiction Boundary** | Bleeds US/India data across queries | **Strict Isolation:** India & US datasets isolated at engine level |
| **Conversational Memory** | Drops context on follow-ups | **Context Resolution:** Resolves active scheme pronouns across turns |
| **Dynamic Tooling** | Unchecked function calling | **Sandboxed TTE:** AST-analyzed static validation & human approval |

---

## 🗺️ SLIDE 5 — LIVE USER JOURNEY MATRIX

1. **Turn 1 — Public Service Intent:**  
   `"Ration chahiye mere bachon ke liye"`  
   ➔ Classified as `PUBLIC_SERVICE` / Food Security → Maps to `SCH-IN-014` (NFSA).

2. **Turn 2 — Active Scheme Pronoun Resolution:**  
   `"Am I eligible for it?"`  
   ➔ Resolves `"it"` to active scheme `SCH-IN-014`. Evaluates income/employment facts deterministically.

3. **Turn 3 — Explicit Scheme Override:**  
   `"ayushman milega?"`  
   ➔ Immediately switches context from Ration to `SCH-IN-006` (Ayushman Bharat Health Insurance).

4. **Turn 4 — Crisis Priority Intercept:**  
   `"Mera ghar flood me damage ho gaya Bihar me"`  
   ➔ Urgency: `CRISIS`. Immediately surfaces Bihar Emergency Flood Relief (`SCH-IN-003`) & shelter instructions. **NO FEMA/US leakage.**

5. **Turn 5 — Weather Intelligence:**  
   `"kal Patna me mausam kaisa rahega?"`  
   ➔ Fetches live Open-Meteo weather API forecast for Patna (temperature range, precipitation probability, sky condition).

---

## 🏗️ SLIDE 6 — SYSTEM ARCHITECTURE

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

- **Deterministic Eligibility Boundary:** Code rules strictly isolate legal criteria evaluation from LLM text generation.
- **Crisis Safety Boundary:** Emergency routing unconditionally intercepts physical danger requests.
- **Jurisdiction Boundary:** National and state jurisdiction policies enforce resource containment.

---

## 🛡️ SLIDE 7 — SAFETY & TRUST ARCHITECTURE

- **Deterministic Rule Boundaries:** Code-enforced rule evaluation prevents fabricated scheme approvals.
- **Crisis Priority Isolation:** Physical safety guidance and emergency contacts surface above administrative steps.
- **Jurisdiction Firewall:** National and regional datasets (`IN` vs `US`) are contained at database, retrieval, and prompt levels.
- **Sandboxed Tool Evolution (TTE):** Static AST analysis (`ast.parse`) rejects dangerous modules (`os`, `sys`, `subprocess`). Unapproved tools cannot execute.
- **Input & Transport Hardening:** Pydantic schema validation caps incoming payload sizes and sanitizes error responses.

---

## 🛠️ SLIDE 8 — TECHNOLOGY STACK

- **Frontend:** React 18, TypeScript 5.2, Vite 6.4, Tailwind CSS 3.4, Lucide Icons
- **Backend API:** Python 3.11+, FastAPI 0.110, Pydantic v2.6, AsyncIO, Uvicorn
- **Database & Storage:** PostgreSQL 16 with `pgvector` extension for vector similarity search
- **AI & Retrieval:** Modular Multi-Provider LLM layer (Ollama local / OpenAI compatible), Open-Meteo Weather API
- **Testing & Quality:** Pytest 8.1 (77 automated test suites), TypeScript strict compiler
- **Containerization:** Docker & Docker Compose multi-service orchestration

---

## 🧪 SLIDE 9 — VERIFICATION & AUDIT RESULTS

### **100% Empirically Verified Production Baseline**

- **Backend Pytest Suite:** `77 / 77 PASSED` (0 errors in 32.00s)
- **TypeScript Static Check:** `0 ERRORS` (`npx tsc --noEmit`)
- **Production Frontend Build:** `PASSED` (`npx vite build` in 2.53s)
- **Protected Scenarios:** 18 benchmark conversational scenarios verified & frozen
- **Security Audit:** 0 secret leaks, 0 untrusted code execution paths, sanitized server-side error logging

---

## 🗺️ SLIDE 10 — IMPACT & FUTURE ROADMAP

### **Social Impact**
Empowers vulnerable citizens, disaster victims, and low-literacy families to navigate complex public assistance without bureaucratic barriers or technical friction.

### **Future Evolution**
1. **Multi-State Scheme Dataset Expansion:** Ingest municipal and state-level welfare programs across all Indian states.
2. **Indian Language Speech Processing:** Native voice input and audio response generation (Hindi, Maithili, Bhojpuri, Bengali).
3. **Location-Aware Dispatch:** Automated district-level mapping to local ration shops, shelters, and e-District centers.
4. **Offline Disaster Relief Mode:** Local cached scheme navigation for crisis response in low-connectivity disaster zones.

---

<div align="center">

**Sahay 2.0 — Civic Intelligence for Real-World Needs**

*Find the right help. Understand your options. Know what to do next.*

</div>
