import pytest
from app.services.ai_orchestrator import ai_orchestrator
from app.models.schemas import ChatRequest, FlowType
from app.services.conversation_memory import conversation_memory

@pytest.fixture(autouse=True)
def cleanup_sessions():
    yield
    for cid in list(conversation_memory._sessions.keys()):
        conversation_memory.clear_session(cid)

def test_01_patna_to_patna():
    r = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Patna", conversation_id="w01"))
    assert "Patna" in r.situation.summary

def test_02_supaul_to_supaul():
    r = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Supaul", conversation_id="w02"))
    assert "Supaul" in r.situation.summary

def test_03_triveniganj_to_triveniganj():
    r = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id="w03"))
    assert "Triveniganj" in r.situation.summary

def test_04_patna_to_supaul():
    cid = "w04"
    ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Supaul", conversation_id=cid))
    assert "Supaul" in r2.situation.summary

def test_05_supaul_to_triveniganj():
    cid = "w05"
    ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Supaul", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id=cid))
    assert "Triveniganj" in r2.situation.summary

def test_06_triveniganj_to_chennai():
    cid = "w06"
    ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Chennai", conversation_id=cid))
    assert "Chennai" in r2.situation.summary

def test_07_chennai_to_triveniganj():
    cid = "w07"
    ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Chennai", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id=cid))
    assert "Triveniganj" in r2.situation.summary

def test_08_triveniganj_to_what_about_tomorrow():
    cid = "w08"
    ai_orchestrator.process_request(ChatRequest(message="will tomorrow rain in Triveniganj", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="what about tomorrow?", conversation_id=cid))
    assert "Triveniganj" in r2.situation.summary

def test_09_chennai_to_what_about_tomorrow():
    cid = "w09"
    ai_orchestrator.process_request(ChatRequest(message="weather in Chennai", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="what about tomorrow?", conversation_id=cid))
    assert "Chennai" in r2.situation.summary

def test_10_how_about_chennai():
    cid = "w10"
    ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="how about Chennai?", conversation_id=cid))
    assert "Chennai" in r2.situation.summary

def test_11_and_supaul():
    cid = "w11"
    ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="and Supaul?", conversation_id=cid))
    assert "Supaul" in r2.situation.summary

def test_12_what_about_there():
    cid = "w12"
    ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="what about there tomorrow?", conversation_id=cid))
    assert "Patna" in r2.situation.summary

def test_13_explicit_location_after_previous():
    cid = "w13"
    ai_orchestrator.process_request(ChatRequest(message="weather in Delhi", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="will it rain in Mumbai tomorrow", conversation_id=cid))
    assert "Mumbai" in r2.situation.summary

def test_14_no_location_with_existing_context():
    cid = "w14"
    ai_orchestrator.process_request(ChatRequest(message="weather in Gaya", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="tomorrow evening?", conversation_id=cid))
    assert "Gaya" in r2.situation.summary

def test_15_no_location_without_context():
    cid = "w15"
    r = ai_orchestrator.process_request(ChatRequest(message="Will it rain tomorrow?", conversation_id=cid, user_context={"state": "Bihar"}))
    assert len(r.missing_information) > 0 or "city" in r.situation.summary.lower()

def test_16_unknown_location():
    cid = "w16"
    r = ai_orchestrator.process_request(ChatRequest(message="weather in Xyzabc12345", conversation_id=cid))
    assert r.flow == FlowType.WEB_SEARCH_REQUIRED

def test_17_misspelled_location():
    cid = "w17"
    r = ai_orchestrator.process_request(ChatRequest(message="weather in wether tomorow in Patna", conversation_id=cid))
    assert "Patna" in r.situation.summary

def test_18_district_vs_state():
    cid = "w18"
    r = ai_orchestrator.process_request(ChatRequest(message="weather in Supaul district", conversation_id=cid))
    assert "Supaul" in r.situation.summary

def test_19_global_city_geocoding():
    cid = "w19"
    r = ai_orchestrator.process_request(ChatRequest(message="weather in London tomorrow", conversation_id=cid))
    assert "London" in r.situation.summary

def test_20_weather_followed_by_public_service():
    cid = "w20"
    ai_orchestrator.process_request(ChatRequest(message="weather in Chennai", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in Bihar", conversation_id=cid, user_context={"state": "Bihar"}))
    assert r2.flow == FlowType.PUBLIC_SERVICE
    assert "Chennai" not in r2.situation.summary

def test_21_public_service_followed_by_weather():
    cid = "w21"
    ai_orchestrator.process_request(ChatRequest(message="I need food assistance in Bihar", conversation_id=cid, user_context={"state": "Bihar"}))
    r2 = ai_orchestrator.process_request(ChatRequest(message="weather in Patna tomorrow", conversation_id=cid))
    assert r2.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Patna" in r2.situation.summary

def test_22_weather_context_does_not_leak_into_jurisdiction():
    cid = "w22"
    ai_orchestrator.process_request(ChatRequest(message="weather in New York", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in Bihar", conversation_id=cid, user_context={"country": "IN", "state": "Bihar"}))
    for rec in r2.recommendations:
        assert rec.country == "IN"

def test_23_jurisdiction_does_not_leak_into_weather():
    cid = "w23"
    ai_orchestrator.process_request(ChatRequest(message="I need food assistance in the US", conversation_id=cid, user_context={"country": "US"}))
    r2 = ai_orchestrator.process_request(ChatRequest(message="weather in Chennai tomorrow", conversation_id=cid))
    assert "Chennai" in r2.situation.summary

def test_24_repeated_identical_request():
    cid = "w24"
    r1 = ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    assert "Patna" in r1.situation.summary
    assert "Patna" in r2.situation.summary

def test_25_rapid_alternating_locations():
    cid = "w25"
    locs = ["Patna", "Supaul", "Triveniganj", "Chennai", "Delhi", "Patna"]
    for loc in locs:
        r = ai_orchestrator.process_request(ChatRequest(message=f"weather in {loc}", conversation_id=cid))
        assert loc in r.situation.summary

def test_26_stale_user_context_multi_turn_sequence():
    cid = "w26"
    sequence = [
        ("will tomorrow rain in Patna", {"city": "Patna"}, "Patna"),
        ("will tomorrow rain in Supaul", {"city": "Patna"}, "Supaul"),
        ("will tomorrow rain in Triveniganj", {"city": "Supaul"}, "Triveniganj"),
        ("what about tomorrow?", {}, "Triveniganj"),
        ("how about Chennai?", {"city": "Triveniganj"}, "Chennai"),
        ("will tomorrow rain in Triveniganj", {"city": "Chennai"}, "Triveniganj")
    ]
    for msg, ctx, exp_city in sequence:
        r = ai_orchestrator.process_request(ChatRequest(message=msg, conversation_id=cid, user_context=ctx))
        assert exp_city in r.situation.summary, f"Failed on '{msg}' with user_context={ctx}: expected {exp_city} in {r.situation.summary}"
        assert r.decision_metadata.validation_status == "PASSED"
        assert r.decision_metadata.selected_tool == "weather_forecast"
