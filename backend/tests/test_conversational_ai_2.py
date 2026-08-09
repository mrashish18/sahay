import pytest
from app.services.ai_orchestrator import ai_orchestrator
from app.models.schemas import ChatRequest, FlowType

def test_1_weather_context_followup():
    cid = "sess-weather-ctx-01"
    req1 = ChatRequest(conversation_id=cid, message="Will it rain tomorrow in Patna?", user_context={"state": "Bihar"})
    res1 = ai_orchestrator.process_request(req1)
    assert res1.flow == FlowType.WEB_SEARCH_REQUIRED
    assert res1.situation.weather_data["city"] == "Patna"

    req2 = ChatRequest(conversation_id=cid, message="what about evening?", user_context={"state": "Bihar"})
    res2 = ai_orchestrator.process_request(req2)
    assert res2.flow == FlowType.WEB_SEARCH_REQUIRED
    assert res2.situation.weather_data is not None
    assert res2.situation.weather_data["city"] == "Patna"
    assert res2.situation.weather_data.get("time_period") == "evening"

def test_2_no_weather_context_followup_ambiguous():
    cid = "sess-python-no-weather-01"
    req1 = ChatRequest(conversation_id=cid, message="what is pythn")
    res1 = ai_orchestrator.process_request(req1)
    assert res1.flow == FlowType.GENERAL_INFORMATION
    assert len(res1.recommendations) == 0

    req2 = ChatRequest(conversation_id=cid, message="what about evening?")
    res2 = ai_orchestrator.process_request(req2)
    assert res2.flow == FlowType.AMBIGUOUS
    assert len(res2.recommendations) == 0
    assert len(res2.action_plan) == 0
    assert "Sure — evening for what?" in res2.situation.summary or "clarify" in res2.situation.summary.lower() or "evening" in res2.situation.summary.lower()

def test_3_location_plus_time_without_domain_ambiguous():
    req = ChatRequest(message="tomorrow + Patna + evening", user_context={"state": "Bihar"})
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.AMBIGUOUS
    assert len(res.recommendations) == 0
    assert len(res.action_plan) == 0
    assert "weather in Patna" in res.situation.summary

def test_4_explicit_weather_query_in_patna():
    req = ChatRequest(message="what about evening weather in Patna?")
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.WEB_SEARCH_REQUIRED
    assert res.situation.weather_data is not None
    assert res.situation.weather_data["city"] == "Patna"

def test_5_hinglish_weather_patna():
    req = ChatRequest(message="kal patna me barish hogi kya")
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.WEB_SEARCH_REQUIRED
    assert res.situation.weather_data["city"] == "Patna"

def test_6_weather_night_followup():
    cid = "sess-weather-night-01"
    req1 = ChatRequest(conversation_id=cid, message="Will it rain tomorrow in Patna?", user_context={"state": "Bihar"})
    res1 = ai_orchestrator.process_request(req1)
    
    req2 = ChatRequest(conversation_id=cid, message="and at night?")
    res2 = ai_orchestrator.process_request(req2)
    assert res2.flow == FlowType.WEB_SEARCH_REQUIRED
    assert res2.situation.weather_data["city"] == "Patna"
    assert res2.situation.weather_data.get("time_period") == "night"

def test_7_what_is_python():
    req = ChatRequest(message="what is Python?")
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.GENERAL_INFORMATION
    assert len(res.recommendations) == 0

def test_8_food_assistance_public_service():
    req = ChatRequest(message="ration chahiye mere bacho ke liye", user_context={"state": "Bihar"})
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.PUBLIC_SERVICE
    assert res.situation.primary_intent == "FOOD_ASSISTANCE"
    assert 1 <= len(res.recommendations) <= 2
    assert "Food Security" in res.recommendations[0].title or "Ration" in res.recommendations[0].title

def test_9_pmay_eligibility_check():
    req = ChatRequest(message="PMAY milega kya")
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.ELIGIBILITY_CHECK

def test_10_crisis_flood_damage():
    req = ChatRequest(message="mera ghar flood me damage ho gaya hai aur rehne ki jagah nahi hai", user_context={"state": "Bihar"})
    res = ai_orchestrator.process_request(req)
    assert res.flow == FlowType.CRISIS
