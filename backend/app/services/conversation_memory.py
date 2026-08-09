import time
from typing import Dict, Any, List, Optional

class ConversationSession:
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.messages: List[Dict[str, str]] = []
        self.active_topic: Optional[str] = None
        self.active_location: Optional[str] = None
        self.pending_question: Optional[str] = None
        self.confirmed_facts: Dict[str, Any] = {}
        self.last_tool_used: Optional[str] = None
        self.last_updated: float = time.time()

    def add_message(self, sender: str, text: str):
        self.messages.append({
            "sender": sender,
            "text": text,
            "timestamp": time.strftime("%H:%M:%S")
        })
        self.last_updated = time.time()

    def update_context(
        self,
        active_topic: Optional[str] = None,
        location: Optional[str] = None,
        pending_question: Optional[str] = None,
        new_facts: Optional[Dict[str, Any]] = None,
        tool_used: Optional[str] = None
    ):
        if active_topic:
            self.active_topic = active_topic
        if location:
            self.active_location = location
        if pending_question is not None:
            self.pending_question = pending_question
        if new_facts:
            self.confirmed_facts.update(new_facts)
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
