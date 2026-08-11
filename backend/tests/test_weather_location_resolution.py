import pytest
from app.services.ai_orchestrator import ai_orchestrator
from app.models.schemas import ChatRequest

def test_sequential_weather_location_override():
    session_id = "test-weather-loc-sequence-001"

    # 1. Patna
    req1 = ChatRequest(message="will tomorrow rain in Patna", conversation_id=session_id)
    res1 = ai_orchestrator.process_request(req1)
    assert res1.situation is not None
    assert "Patna" in res1.situation.summary
    assert res1.situation.weather_data is not None
    assert res1.situation.weather_data.get("city") == "Patna"

    # 2. Supaul (MUST override Patna!)
    req2 = ChatRequest(message="will tomorrow rain in Supaul", conversation_id=session_id)
    res2 = ai_orchestrator.process_request(req2)
    assert res2.situation is not None
    assert "Supaul" in res2.situation.summary
    assert res2.situation.weather_data is not None
    assert res2.situation.weather_data.get("city") == "Supaul"

    # 3. Triveniganj (MUST override Supaul!)
    req3 = ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id=session_id)
    res3 = ai_orchestrator.process_request(req3)
    assert res3.situation is not None
    assert "Triveniganj" in res3.situation.summary
    assert res3.situation.weather_data is not None
    assert res3.situation.weather_data.get("city") == "Triveniganj"

    # 4. Continuation without location ("what about tomorrow?") -> Retains Triveniganj
    req4 = ChatRequest(message="what about tomorrow?", conversation_id=session_id)
    res4 = ai_orchestrator.process_request(req4)
    assert res4.situation is not None
    assert "Triveniganj" in res4.situation.summary
    assert res4.situation.weather_data is not None
    assert res4.situation.weather_data.get("city") == "Triveniganj"

    # 5. Explicit location override ("how about Chennai?") -> Overrides Triveniganj with Chennai
    req5 = ChatRequest(message="how about Chennai?", conversation_id=session_id)
    res5 = ai_orchestrator.process_request(req5)
    assert res5.situation is not None
    assert "Chennai" in res5.situation.summary
    assert res5.situation.weather_data is not None
    assert res5.situation.weather_data.get("city") == "Chennai"

def test_jurisdiction_override_for_explicit_weather_city():
    session_id = "test-weather-jurisdiction-override"
    # Even if jurisdiction state is Bihar, asking for Chennai weather MUST return Chennai
    req = ChatRequest(
        message="weather tomorrow in Chennai",
        conversation_id=session_id,
        user_context={"state": "Bihar", "country": "IN"}
    )
    res = ai_orchestrator.process_request(req)
    assert res.situation is not None
    assert "Chennai" in res.situation.summary
    assert res.situation.weather_data is not None
    assert res.situation.weather_data.get("city") == "Chennai"
