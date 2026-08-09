# Sahay — Crisis Navigator Architecture & Specification

## 1. Overview
The **Crisis Navigator** is a first-class workflow inside **Sahay** designed to detect, prioritize, and guide users through urgent crisis situations (disasters, floods, fires, medical emergencies, safety threats, food insecurity, and displacement).

Unlike standard public-service queries, crisis handling strictly prioritizes **Immediate Physical Safety** and **Emergency Resources** above administrative eligibility forms or long-term program documentation.

---

## 2. Supported Crisis Categories
- `DISASTER` (General natural or man-made disasters)
- `FLOOD` (Heavy rainfall, flooding, submersion)
- `FIRE` (Residential or urban fire emergencies)
- `EARTHQUAKE` (Seismic events and structural collapses)
- `CYCLONE` / `STORM` (High winds, severe tropical storms)
- `LANDSLIDE` (Mudslides and earth movements)
- `DISPLACEMENT` (Immediate loss of home requiring emergency lodging)
- `HOMELESSNESS` (Acute shelter loss)
- `FOOD_INSECURITY` (Acute lack of food/water)
- `MEDICAL_EMERGENCY` (Acute health crises requiring immediate care)
- `SAFETY_THREAT` (Physical danger or abuse requiring safe shelter)
- `LOST_DOCUMENTS` (Crisis-induced loss of official identity papers)
- `OTHER` (Unclassified emergency situations)

---

## 3. Deterministic Priority Ordering Algorithm
When a request is classified as `CRISIS`, the system executes the following response order:

```text
1. Immediate Safety Steps
2. Emergency & Crisis Resources
3. Immediate Assistance (Shelter / Food / Medical)
4. Public-Service Assistance
5. Deterministic Eligibility Assessment
6. Required Documents Guide
7. Prioritized Action Plan & Verified Sources
```

LLMs are strictly barred from reordering emergency priorities.

---

## 4. No Fake Emergency Data Policy
Sahay strictly enforces a zero-fabrication policy for emergency resources:
- All emergency resource entries must originate from verified knowledge base records or official government emergency portals (e.g. `https://disastermanagement.gov.in`).
- If no authentic local resource is available in the database, Sahay displays a transparent advisory instructing the user to contact local municipal emergency dispatch.

---

## 5. Security & TTE Boundary
- Dynamic Tool Evolution (TTE) is strictly disabled during crisis workflows.
- Retrieved evidence chunks are wrapped inside untrusted data tags (`<retrieved_evidence trust="UNTRUSTED_DATA">`).
- Prompt injection attempts cannot override system safety boundaries or alter eligibility outcomes.
