# Sahay — Jurisdiction Policy & Multi-Jurisdiction System Specification

## 1. Executive Summary
**Sahay** is designed with a multi-jurisdiction data architecture, with **India (`IN`)** designated as the primary user-facing jurisdiction for the hackathon MVP.

Every public welfare scheme, emergency resource, and RAG knowledge chunk maintains explicit, unambiguous jurisdiction metadata. Sahay strictly enforces jurisdiction boundary boundaries at the retrieval, eligibility evaluation, and crisis navigation layers.

---

## 2. Jurisdiction Hierarchy & Metadata Schema
Every record in the Sahay knowledge base is tagged with explicit jurisdiction metadata:

```json
{
  "country": "IN",
  "jurisdiction_level": "NATIONAL",
  "region": null,
  "issuing_authority": "Ministry of Housing and Urban Affairs, Govt of India",
  "source_url": "https://pmaymis.gov.in"
}
```

For State-level services:
```json
{
  "country": "IN",
  "jurisdiction_level": "STATE",
  "region": "Bihar",
  "issuing_authority": "Disaster Management Department, Govt of Bihar",
  "source_url": "https://disastermgmt.bihar.gov.in"
}
```

For US / International resources:
```json
{
  "country": "US",
  "jurisdiction_level": "FEDERAL",
  "region": null,
  "issuing_authority": "Federal Emergency Management Agency (FEMA)",
  "source_url": "https://www.fema.gov/assistance/individual"
}
```

---

## 3. Strict Boundary Rules
1. **No Mislabeling:** US resources (e.g. FEMA, SNAP) are preserved in the dataset with `country: "US"` but are strictly excluded from default India user retrieval.
2. **No Invented Schemes:** Indian public services are drawn exclusively from authentic government portals (`https://pmaymis.gov.in`, `https://pmkisan.gov.in`, `https://disastermgmt.bihar.gov.in`, `https://nfs.delhi.gov.in`).
3. **Explicit User Location:** User location is collected explicitly or flagged as `missing_information`. Sahay never guesses user country or state from IP address or language alone.
4. **State Boundary Exclusion:** State-specific schemes (e.g. Delhi Ration Scheme) are excluded when the user is located in another state (e.g. Bihar).
5. **Deterministic Ineligibility:** The Eligibility Engine evaluates jurisdiction matching as a mandatory pre-check, returning `INELIGIBLE` for country/state mismatches.
