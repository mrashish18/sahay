import pytest
from app.models.schemas import ChatRequest, FlowType
from app.services.ai_orchestrator import ai_orchestrator
from app.services.conversation_memory import conversation_memory

@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Ensure clean session store for every test."""
    yield
    for cid in list(conversation_memory._sessions.keys()):
        conversation_memory.clear_session(cid)

def test_conversation_a_weather_sequence():
    """
    Conversation A: Weather multi-turn location sequence & topic retention.
    Turn 1: weather in Patna -> Patna
    Turn 2: tomorrow? -> Patna
    Turn 3: what about Supaul? -> Supaul
    Turn 4: and Triveniganj? -> Triveniganj
    Turn 5: what about there tomorrow? -> Triveniganj
    """
    cid = "test_conv_a"

    # Turn 1
    r1 = ai_orchestrator.process_request(ChatRequest(message="weather in Patna", conversation_id=cid))
    assert r1.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Patna" in r1.situation.summary
    assert r1.decision_metadata is not None
    assert r1.decision_metadata.intent == "WEATHER"

    # Turn 2
    r2 = ai_orchestrator.process_request(ChatRequest(message="tomorrow?", conversation_id=cid))
    assert r2.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Patna" in r2.situation.summary

    # Turn 3
    r3 = ai_orchestrator.process_request(ChatRequest(message="what about Supaul?", conversation_id=cid))
    assert r3.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Supaul" in r3.situation.summary

    # Turn 4
    r4 = ai_orchestrator.process_request(ChatRequest(message="and Triveniganj?", conversation_id=cid))
    assert r4.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Triveniganj" in r4.situation.summary

    # Turn 5
    r5 = ai_orchestrator.process_request(ChatRequest(message="what about there tomorrow?", conversation_id=cid))
    assert r5.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Triveniganj" in r5.situation.summary

def test_conversation_b_public_service_eligibility():
    """
    Conversation B: Public service & eligibility multi-turn sequence.
    Turn 1: I need food assistance -> NFSA guidance
    Turn 2: in Bihar -> Bihar context
    Turn 3: am I eligible? -> NFSA eligibility check
    Turn 4: what documents do I need? -> NFSA document checklist
    """
    cid = "test_conv_b"

    # Turn 1
    r1 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance", conversation_id=cid))
    assert r1.flow == FlowType.PUBLIC_SERVICE
    assert len(r1.recommendations) > 0

    # Turn 2
    r2 = ai_orchestrator.process_request(ChatRequest(message="in Bihar", conversation_id=cid, user_context={"state": "Bihar"}))
    assert r2.flow in [FlowType.PUBLIC_SERVICE, FlowType.ELIGIBILITY_CHECK]

    # Turn 3
    r3 = ai_orchestrator.process_request(ChatRequest(message="am I eligible?", conversation_id=cid))
    assert r3.flow == FlowType.ELIGIBILITY_CHECK
    assert len(r3.eligibility) > 0

    # Turn 4
    r4 = ai_orchestrator.process_request(ChatRequest(message="what documents do I need?", conversation_id=cid))
    assert r4.flow in [FlowType.DOCUMENT_GUIDANCE, FlowType.PUBLIC_SERVICE, FlowType.ELIGIBILITY_CHECK]
    assert len(r4.documents) > 0 or "ration" in r4.situation.summary.lower() or "document" in r4.situation.summary.lower()

def test_conversation_c_us_jurisdiction_isolation():
    """
    Conversation C: US Jurisdiction Isolation.
    Turn 1: I need food assistance in the US -> US SNAP program
    Turn 2: what documents do I need? -> US SNAP documents
    Turn 3: am I eligible? -> US SNAP eligibility
    """
    cid = "test_conv_c"

    # Turn 1
    r1 = ai_orchestrator.process_request(ChatRequest(message="I need food assistance in the US", conversation_id=cid, user_context={"country": "US"}))
    assert r1.flow == FlowType.PUBLIC_SERVICE
    for rec in r1.recommendations:
        assert rec.country == "US"
        assert rec.scheme_id != "SCH-IN-014"

    # Turn 2
    r2 = ai_orchestrator.process_request(ChatRequest(message="what documents do I need?", conversation_id=cid, user_context={"country": "US"}))
    for rec in r2.recommendations:
        assert rec.country == "US"

    # Turn 3
    r3 = ai_orchestrator.process_request(ChatRequest(message="am I eligible?", conversation_id=cid, user_context={"country": "US"}))
    for rec in r3.recommendations:
        assert rec.country == "US"

def test_conversation_d_crisis_multi_turn():
    """
    Conversation D: Emergency crisis multi-turn safety guidance.
    Turn 1: There is a flood near me -> CRISIS flow
    Turn 2: what should I do? -> Action plan safety steps
    Turn 3: where can I get help? -> Emergency helpline / resources
    """
    cid = "test_conv_d"

    # Turn 1
    r1 = ai_orchestrator.process_request(ChatRequest(message="There is a flood near me", conversation_id=cid))
    assert r1.flow == FlowType.CRISIS
    assert r1.urgency.level.value == "CRISIS"

    # Turn 2
    r2 = ai_orchestrator.process_request(ChatRequest(message="what should I do?", conversation_id=cid))
    assert r2.flow == FlowType.CRISIS
    assert len(r2.action_plan) > 0

    # Turn 3
    r3 = ai_orchestrator.process_request(ChatRequest(message="where can I get help?", conversation_id=cid))
    assert r3.flow == FlowType.CRISIS
    assert len(r3.sources) > 0 or len(r3.action_plan) > 0

def test_conversation_e_cross_topic_isolation():
    """
    Conversation E: Topic-scoped context isolation (Weather vs Service).
    Turn 1: weather in Chennai -> Weather for Chennai
    Turn 2: I need help with a government scheme in Bihar -> Public Service for Bihar
    Turn 3: what documents do I need? -> Scheme documents (Chennai weather MUST NOT leak!)
    """
    cid = "test_conv_e"

    # Turn 1
    r1 = ai_orchestrator.process_request(ChatRequest(message="weather in Chennai", conversation_id=cid))
    assert r1.flow == FlowType.WEB_SEARCH_REQUIRED
    assert "Chennai" in r1.situation.summary

    # Turn 2
    r2 = ai_orchestrator.process_request(ChatRequest(message="I need help with a government scheme in Bihar", conversation_id=cid, user_context={"state": "Bihar"}))
    assert r2.flow == FlowType.PUBLIC_SERVICE
    assert "Chennai" not in r2.situation.summary
    for rec in r2.recommendations:
        assert "Chennai" not in rec.summary

    # Turn 3
    r3 = ai_orchestrator.process_request(ChatRequest(message="what documents do I need?", conversation_id=cid))
    assert "Chennai" not in r3.situation.summary
