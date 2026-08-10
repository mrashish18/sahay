import re
import pytest
from app.models.schemas import ChatRequest, FlowType
from app.services.ai_orchestrator import ai_orchestrator
from app.services.conversation_memory import conversation_memory

# TEST A: NFSA Eligibility Pronoun Lock
def test_a_nfsa_pronoun_lock():
    cid = "t-a-nfsa"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="mujhe ration chahiye", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="am i eligible for it?", conversation_id=cid))
    assert r2.flow == FlowType.ELIGIBILITY_CHECK
    assert len(r2.recommendations) == 1
    assert r2.recommendations[0].scheme_id == "SCH-IN-014"

# TEST B: Explicit PMAY Override
def test_b_pmay_override():
    cid = "t-b-pmay"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="mujhe ration chahiye", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="pmay milega mujhe", conversation_id=cid))
    assert r2.flow == FlowType.ELIGIBILITY_CHECK
    assert len(r2.recommendations) == 1
    assert r2.recommendations[0].scheme_id == "SCH-IN-001"

# TEST C: Explicit Ayushman Override (SCH-IN-006)
def test_c_ayushman_override():
    cid = "t-c-ayushman"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="mujhe ration chahiye", conversation_id=cid))
    ai_orchestrator.process_request(ChatRequest(message="pmay milega mujhe", conversation_id=cid))
    r3 = ai_orchestrator.process_request(ChatRequest(message="ayushman milega?", conversation_id=cid))
    assert r3.flow == FlowType.ELIGIBILITY_CHECK
    assert len(r3.recommendations) == 1
    assert r3.recommendations[0].scheme_id == "SCH-IN-006"
    assert "Ayushman" in r3.recommendations[0].title

# TEST D: Hinglish Flood Crisis (No FEMA, No Internal Text)
def test_d_hinglish_flood_crisis():
    cid = "t-d-flood"
    conversation_memory.clear_session(cid)
    r = ai_orchestrator.process_request(ChatRequest(message="mera ghar pani me doob gya", conversation_id=cid, user_context={"country": "IN", "state": "Bihar"}))
    assert r.flow == FlowType.CRISIS
    assert len(r.recommendations) > 0
    assert r.recommendations[0].scheme_id == "SCH-IN-003"
    
    full_text = (r.situation.summary + " " + " ".join(s.title for s in r.sources)).lower()
    assert "fema" not in full_text
    assert "public service navigation query" not in full_text
    assert "household_facts" not in full_text

# TEST E: Weather Bhagalpur Night Continuation
def test_e_weather_bhagalpur_night():
    cid = "t-e-wx"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="Will it rain tomorrow in Bhagalpur?", conversation_id=cid))
    ai_orchestrator.process_request(ChatRequest(message="aur raat me", conversation_id=cid))
    r3 = ai_orchestrator.process_request(ChatRequest(message="weather", conversation_id=cid))
    assert r3.flow == FlowType.WEB_SEARCH_REQUIRED
    wx = r3.situation.weather_data
    assert wx is not None
    assert wx["city"] == "Bhagalpur"
    assert wx["time_period"] == "night"

# TEST F: Explicit Patna Weather Resets Time Period to Daily
def test_f_patna_resets_night_period():
    cid = "t-f-wx"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="Will it rain tomorrow in Bhagalpur?", conversation_id=cid))
    ai_orchestrator.process_request(ChatRequest(message="aur raat me", conversation_id=cid))
    r3 = ai_orchestrator.process_request(ChatRequest(message="barish kal patna", conversation_id=cid))
    assert r3.flow == FlowType.WEB_SEARCH_REQUIRED
    wx = r3.situation.weather_data
    assert wx is not None
    assert wx["city"] == "Patna"
    assert wx.get("time_period") is None

# TEST G: Kal Rain Hogi Kya Inherits Patna but Daily
def test_g_kal_rain_hogi_kya_inherits_patna_daily():
    cid = "t-g-wx"
    conversation_memory.clear_session(cid)
    ai_orchestrator.process_request(ChatRequest(message="barish kal patna", conversation_id=cid))
    r2 = ai_orchestrator.process_request(ChatRequest(message="kal rain hogi kya", conversation_id=cid))
    assert r2.flow == FlowType.WEB_SEARCH_REQUIRED
    wx = r2.situation.weather_data
    assert wx is not None
    assert wx["city"] == "Patna"
    assert wx.get("time_period") is None

# TEST H: Jurisdiction Replacement (Bihar -> US -> Bihar)
def test_h_jurisdiction_replacement():
    cid = "t-h-juris"
    conversation_memory.clear_session(cid)
    r1 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in Bihar.", conversation_id=cid))
    assert r1.recommendations[0].country == "IN"
    
    r2 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in the US.", conversation_id=cid))
    assert r2.recommendations[0].country == "US"
    
    r3 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in Bihar.", conversation_id=cid))
    assert r3.recommendations[0].country == "IN"
