import time
from typing import Dict, Any, List, Optional

class ConversationSession:
    """
    State-machine driven conversation session memory for Sahay 2.0.
    Tracks active context, pending clarifications, confirmed facts, entity references,
    and history across turns.
    """
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.messages: List[Dict[str, str]] = []

        self.active_topic: Optional[str] = None
        self.active_intent: Optional[str] = None
        self.active_domain: Optional[str] = None
        self.active_scheme: Optional[str] = None  # e.g. "SCH-IN-014" or "NFSA"

        self.location: Optional[str] = None       # e.g. "Patna"
        self.country: Optional[str] = "IN"
        self.state: Optional[str] = None          # e.g. "Bihar"

        self.date_reference: Optional[str] = None # e.g. "tomorrow"
        self.time_period: Optional[str] = None    # e.g. "evening", "night", "morning"

        # Topic-Scoped Context Containers (Isolated Topic Memory)
        self.weather_context: Dict[str, Any] = {
            "location": None,
            "date_reference": None,
            "time_period": None,
            "geocoded_city": None
        }
        self.service_context: Dict[str, Any] = {
            "scheme_id": None,
            "category": None,
            "country": "IN",
            "state": None
        }
        self.crisis_context: Dict[str, Any] = {
            "location": None,
            "disaster_type": None,
            "urgency_level": None
        }
        self.eligibility_context: Dict[str, Any] = {
            "scheme_id": None,
            "user_attributes": {}
        }

        self.pending_clarification: Optional[str] = None  # e.g. "city", "weather_confirm"
        self.pending_intent: Optional[str] = None         # e.g. "WEATHER"
        self.pending_entities: Dict[str, Any] = {}

        self.last_user_query: Optional[str] = None
        self.last_assistant_response: Optional[str] = None
        self.confirmed_facts: Dict[str, Any] = {}
        self.last_tool_used: Optional[str] = None
        self.last_updated: float = time.time()

    def add_message(self, sender: str, text: str):
        self.messages.append({
            "sender": sender,
            "text": text,
            "timestamp": time.strftime("%H:%M:%S")
        })
        if sender == "USER":
            self.last_user_query = text
        else:
            self.last_assistant_response = text
        self.last_updated = time.time()

    def clear_pending(self):
        """Clears pending clarification and pending intent state."""
        self.pending_clarification = None
        self.pending_intent = None
        self.pending_entities = {}

    def set_pending(self, intent: str, clarification: str, entities: Optional[Dict[str, Any]] = None):
        """Sets pending clarification state."""
        self.pending_intent = intent
        self.pending_clarification = clarification
        self.pending_entities = entities or {}

    def reset_topic(self, new_topic: str, new_domain: Optional[str] = None):
        """
        Updates active topic and clears stale pending state when user switches topics.
        If topic changes away from WEATHER, clears weather context.
        """
        if self.active_topic != new_topic:
            self.clear_pending()
            if self.active_topic == "WEATHER" and new_topic != "WEATHER":
                self.weather_context = {"location": None, "date_reference": None, "time_period": None, "geocoded_city": None}
                self.location = None
                self.date_reference = None
                self.time_period = None
            if self.active_topic == "FOOD_ASSISTANCE" and new_topic not in ["FOOD_ASSISTANCE", "ELIGIBILITY_CHECK", "PUBLIC_SERVICE"]:
                self.active_scheme = None

        self.active_topic = new_topic
        if new_domain:
            self.active_domain = new_domain

    def resolve_reference(self, text: str) -> Optional[str]:
        """
        Resolves entity references like 'it', 'this', 'that', 'the scheme', 'the ration'
        to the active scheme or topic.
        """
        text_lower = text.lower().strip()
        ref_words = ["it", "this", "that", "the scheme", "the program", "this assistance", "the ration", "the scholarship"]

        if any(w in text_lower.split() or w in text_lower for w in ref_words):
            if self.service_context.get("scheme_id"):
                return self.service_context["scheme_id"]
            if self.active_scheme:
                return self.active_scheme
            if self.active_topic:
                return self.active_topic
        return None

    def update_context(
        self,
        active_topic: Optional[str] = None,
        active_intent: Optional[str] = None,
        active_domain: Optional[str] = None,
        active_scheme: Optional[str] = None,
        location: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        date_reference: Optional[str] = None,
        time_period: Optional[str] = None,
        pending_clarification: Optional[str] = None,
        pending_intent: Optional[str] = None,
        pending_entities: Optional[Dict[str, Any]] = None,
        new_facts: Optional[Dict[str, Any]] = None,
        tool_used: Optional[str] = None
    ):
        if active_topic is not None:
            self.active_topic = active_topic
        if active_intent is not None:
            self.active_intent = active_intent
        if active_domain is not None:
            self.active_domain = active_domain

        if active_scheme is not None:
            self.active_scheme = active_scheme
            self.service_context["scheme_id"] = active_scheme
            self.eligibility_context["scheme_id"] = active_scheme

        # Topic-scoped updates
        if active_topic == "WEATHER" or active_intent == "WEATHER":
            if location is not None:
                self.weather_context["location"] = location
                self.location = location
            if date_reference is not None:
                self.weather_context["date_reference"] = date_reference
                self.date_reference = date_reference
            self.weather_context["time_period"] = time_period
            self.time_period = time_period
        else:
            if location is not None:
                self.location = location
            if date_reference is not None:
                self.date_reference = date_reference
            self.time_period = time_period

        if state is not None:
            self.state = state
            self.service_context["state"] = state
        if country is not None:
            self.country = country
            self.service_context["country"] = country
            if country == "US":
                self.state = None
                self.service_context["state"] = None

        if pending_clarification is not None:
            self.pending_clarification = pending_clarification
        if pending_intent is not None:
            self.pending_intent = pending_intent
        if pending_entities is not None:
            self.pending_entities = pending_entities

        if new_facts:
            self.confirmed_facts.update(new_facts)
            self.eligibility_context["user_attributes"].update(new_facts)
        if tool_used:
            self.last_tool_used = tool_used

        self.last_updated = time.time()


class ConversationMemoryStore:
    """
    In-Memory Session Store for Multi-Turn Conversation Memory.
    Tracks session topics, confirmed user facts, active location context,
    and pending clarification questions across turns.
    """
    def __init__(self):
        self._sessions: Dict[str, ConversationSession] = {}

    def get_or_create_session(self, conversation_id: str) -> ConversationSession:
        if conversation_id not in self._sessions:
            self._sessions[conversation_id] = ConversationSession(conversation_id)
        return self._sessions[conversation_id]

    def clear_session(self, conversation_id: str):
        if conversation_id in self._sessions:
            del self._sessions[conversation_id]

conversation_memory = ConversationMemoryStore()

