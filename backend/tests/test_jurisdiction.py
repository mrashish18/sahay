import pytest
from app.services.rag_service import RAGService
from app.services.knowledge_base import KnowledgeBaseService
from app.services.eligibility_engine import eligibility_engine
from app.services.ai_orchestrator import ai_orchestrator
from app.models.schemas import ChatRequest, FlowType, EligibilityStatus

def test_jurisdiction_1_india_user_vs_us_scheme_excluded():
    rag = RAGService()
    # Search India queries for flood shelter -> US FEMA chunks must be excluded
    results_in = rag.search_knowledge("flood emergency shelter housing", country="IN")
    for r in results_in:
        assert r.country == "IN"
        assert r.scheme_id != "SCH-GOV-001" # Exclude US FEMA scheme

def test_jurisdiction_2_us_user_vs_us_scheme_eligible():
    rag = RAGService()
    # Search US queries -> US FEMA chunks retrievable when country="US"
    results_us = rag.search_knowledge("disaster emergency housing shelter", country="US")
    assert len(results_us) > 0
    assert any(r.country == "US" for r in results_us)

def test_jurisdiction_3_bihar_user_vs_bihar_scheme():
    rag = RAGService()
    results = rag.search_knowledge("flood relief grant", country="IN", state="Bihar")
    assert len(results) > 0
    bihar_results = [r for r in results if r.scheme_id == "SCH-IN-003"]
    assert len(bihar_results) > 0

def test_jurisdiction_4_bihar_user_vs_delhi_scheme_excluded():
    rag = RAGService()
    # Bihar user searching food grains -> Delhi-only scheme (SCH-IN-004) must be excluded
    results = rag.search_knowledge("food grains ration card", country="IN", state="Bihar")
    delhi_results = [r for r in results if r.scheme_id == "SCH-IN-004"]
    assert len(delhi_results) == 0

def test_jurisdiction_5_india_national_scheme_retrievable():
    rag = RAGService()
    # India national scheme (PMAY / PM-KISAN) retrievable across any Indian state
    results_bihar = rag.search_knowledge("housing construction grant", country="IN", state="Bihar")
    pmay_results = [r for r in results_bihar if r.scheme_id == "SCH-IN-001"]
    assert len(pmay_results) > 0

def test_scenario_6_missing_location_handled_safely():
    req = ChatRequest(message="What financial assistance programs exist?")
    resp = ai_orchestrator.process_request(req)
    # Missing location should produce missing_information prompt
    assert any(item.field == "location" for item in resp.missing_information)

def test_scenario_7_india_crisis_does_not_return_us_fema():
    req = ChatRequest(message="My house was damaged by flooding in Bihar and we need emergency shelter.")
    resp = ai_orchestrator.process_request(req)
    
    assert resp.flow == FlowType.CRISIS
    # Verify recommendations contain Indian emergency housing or Bihar relief, NOT US FEMA
    for rec in resp.recommendations:
        assert rec.country == "IN"
        assert rec.scheme_id != "SCH-GOV-001"

def test_scenario_8_rag_metadata_preservation():
    rag = RAGService()
    results = rag.search_knowledge("PM-KISAN farmer income", country="IN")
    assert len(results) > 0
    pmkisan_res = [r for r in results if r.scheme_id == "SCH-IN-002"][0]
    assert pmkisan_res.country == "IN"
    assert pmkisan_res.jurisdiction_level == "NATIONAL"
    assert pmkisan_res.source_url == "https://pmkisan.gov.in"

def test_scenario_9_eligibility_jurisdiction_mismatch():
    # Scheme is restricted to country US
    rules_us = {"country": "US", "conditions": []}
    facts_in = {"country": "IN"}
    res = eligibility_engine.evaluate_scheme("SCH-GOV-001", rules_us, facts_in)
    assert res.status == EligibilityStatus.INELIGIBLE
    assert "Jurisdiction Mismatch" in res.unmet_criteria[0]

def test_scenario_10_no_fabricated_jurisdiction():
    kb = KnowledgeBaseService()
    scheme = kb.get_scheme("SCH-IN-003") # Bihar scheme
    assert scheme["country"] == "IN"
    assert scheme["region"] == "Bihar"
    assert scheme["jurisdiction_level"] == "STATE"
