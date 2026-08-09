import pytest
from app.services.ai_orchestrator import ai_orchestrator
from app.models.schemas import ChatRequest, FlowType

def test_query_a_weather_patna_open_meteo():
    """TEST A: 'Will it rain tomorrow in Patna?' -> WEB_SEARCH_REQUIRED, Real Open-Meteo data, 0 government schemes."""
    req = ChatRequest(
        message="Will it rain tomorrow in Patna?",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.WEB_SEARCH_REQUIRED
    assert len(res.recommendations) == 0  # ZERO government schemes!
    assert res.situation.weather_data is not None
    wx = res.situation.weather_data
    assert wx["city"] == "Patna"
    assert wx["source_name"] == "Open-Meteo Weather Forecast"
    assert wx["source_url"] == "https://open-meteo.com"
    assert "Open-Meteo" in res.sources[0].title
    assert "weather.gov" not in res.sources[0].url

def test_query_b_weather_no_city():
    """TEST B: 'Will it rain tomorrow?' without city -> Ask for city in Bihar."""
    req = ChatRequest(
        message="Will it rain tomorrow?",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.WEB_SEARCH_REQUIRED
    assert len(res.recommendations) == 0  # ZERO government schemes!
    assert len(res.missing_information) > 0
    assert res.missing_information[0].field == "city"
    assert "Which city in Bihar" in res.missing_information[0].question

def test_query_c_what_is_python():
    """TEST C: 'What is Python?' -> GENERAL_INFORMATION, 0 government schemes, natural AI response."""
    req = ChatRequest(
        message="What is Python?",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.GENERAL_INFORMATION
    assert len(res.recommendations) == 0  # ZERO government schemes for Python query!
    assert "programming language" in res.situation.summary

def test_query_d_food_grocery_support():
    """TEST D: 'I lost my job and need grocery support for my children.' -> PUBLIC_SERVICE, NFSA ranked #1."""
    req = ChatRequest(
        message="I lost my job and need grocery support for my children.",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.PUBLIC_SERVICE
    assert res.situation.primary_intent == "FOOD_ASSISTANCE"
    assert len(res.recommendations) > 0
    top_scheme = res.recommendations[0]
    assert "Food" in top_scheme.title or "Ration" in top_scheme.title or "Grocery" in top_scheme.category

def test_query_e_crisis_flooding():
    """TEST E: 'My house was damaged by flooding and we have nowhere to stay.' -> CRISIS, safety first."""
    req = ChatRequest(
        message="My house was damaged by flooding and we have nowhere to stay.",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.CRISIS
    assert res.urgency.level.value == "CRISIS"
    assert len(res.recommendations) > 0
    assert "Flood" in res.recommendations[0].title or "Relief" in res.recommendations[0].title

def test_query_f_eligibility_pmay():
    """TEST F: 'Am I eligible for PMAY?' -> ELIGIBILITY_CHECK."""
    req = ChatRequest(
        message="Am I eligible for PMAY?",
        user_context={"country": "IN", "state": "Bihar"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.ELIGIBILITY_CHECK
    assert len(res.recommendations) > 0
    assert "PMAY" in res.recommendations[0].title or "Housing" in res.recommendations[0].title
