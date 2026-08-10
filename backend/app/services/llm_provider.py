import os
import json
import logging
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.config import settings
from app.models.schemas import FlowType, UrgencyLevel, Urgency, MissingInfoItem

logger = logging.getLogger(__name__)

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_situation_analysis(self, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_grounded_response(self, system_prompt: str, user_message: str, grounding_data: Dict[str, Any]) -> str:
        pass


class OllamaProvider(BaseLLMProvider):
    """
    Ollama Local LLM Provider for local inference without API keys.
    Default Model: qwen3:8b (or configured via OLLAMA_MODEL).
    Base URL: http://localhost:11434 (or configured via OLLAMA_BASE_URL).
    Falls back gracefully to OpenAIProvider or MockLLMProvider if Ollama server is offline.
    """
    def __init__(self, base_url: str = None, model_name: str = None):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", settings.OLLAMA_BASE_URL)).rstrip("/")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", settings.OLLAMA_MODEL)

    def is_reachable(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "Sahay-Backend/2.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate_situation_analysis(self, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.is_reachable():
            logger.info(f"Ollama server at {self.base_url} is unreachable. Falling back to OpenAI/Mock provider.")
            if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "mock_key":
                return OpenAIProvider().generate_situation_analysis(user_message, user_context)
            return MockLLMProvider().generate_situation_analysis(user_message, user_context)

        try:
            system_prompt = (
                "You are Sahay's Semantic NLU Analyzer. Return a valid JSON object only with: "
                "flow (CRISIS, PUBLIC_SERVICE, ELIGIBILITY_CHECK, DOCUMENT_GUIDANCE, GENERAL_INFORMATION, WEB_SEARCH_REQUIRED, AMBIGUOUS), "
                "primary_intent, secondary_intents (list), normalized_query, summary, extracted_facts (dict), "
                "urgency (object with level: CRISIS, HIGH, NORMAL, INFORMATIONAL, score 0-1, reasoning), "
                "missing_information (list of objects with field, question, importance)."
            )
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Message: {user_message}\nContext: {json.dumps(user_context or {})}"}
                ],
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.1}
            }
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data.get("message", {}).get("content", "")
                return json.loads(content)
        except Exception as err:
            logger.warning(f"Ollama inference error: {str(err)}. Falling back to MockLLMProvider.")
            return MockLLMProvider().generate_situation_analysis(user_message, user_context)

    def generate_grounded_response(self, system_prompt: str, user_message: str, grounding_data: Dict[str, Any]) -> str:
        if not self.is_reachable():
            return MockLLMProvider().generate_grounded_response(system_prompt, user_message, grounding_data)

        try:
            full_user_content = f"User Question: {user_message}\nGrounding Data:\n{json.dumps(grounding_data, indent=2)}"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_user_content}
                ],
                "stream": False,
                "options": {"temperature": 0.2}
            }
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("message", {}).get("content", "").strip()
        except Exception as err:
            logger.warning(f"Ollama response generation error: {str(err)}.")
            return MockLLMProvider().generate_grounded_response(system_prompt, user_message, grounding_data)


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic, offline-capable LLM Provider for development, automated testing, and fallback.
    Classifies intent taxonomy, extracts facts, rates urgency, and detects missing information.
    """
    
    CRISIS_KEYWORDS = [
        "flood", "flooding", "shelter", "homeless", "evicted", "disaster",
        "emergency", "nowhere to stay", "fire", "earthquake", "starving", "abuse",
        "don't feel safe", "safe to stay", "safety threat", "chest pain", "cyclone", "storm", "landslide"
    ]
    
    HIGH_URGENCY_KEYWORDS = [
        "job lost", "unemployed", "no income", "medical emergency", "disabled", "cannot pay rent", "layoff"
    ]

    def generate_situation_analysis(self, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        text_lower = user_message.lower().strip()
        user_context = user_context or {}
        extracted_facts: Dict[str, Any] = dict(user_context)
        missing_info: list = []
        secondary_intents: list = []

        if "in the us" in text_lower or "in us" in text_lower or "united states" in text_lower:
            extracted_facts["country"] = "US"
        elif "bihar" in text_lower:
            extracted_facts["country"] = "IN"
            extracted_facts["state"] = "Bihar"
        elif "delhi" in text_lower:
            extracted_facts["country"] = "IN"
            extracted_facts["state"] = "Delhi"
        elif "country" not in extracted_facts:
            extracted_facts["country"] = "IN"

        if any(w in text_lower for w in ["flood", "flooding", "disaster"]):
            extracted_facts["disaster_impact"] = "flood"
            extracted_facts["disaster_declared"] = True

        if any(w in text_lower for w in ["nowhere to stay", "evicted", "homeless", "need shelter"]):
            extracted_facts["displacement"] = True

        if any(w in text_lower for w in ["unemployed", "job lost", "layoff", "lost my job"]):
            extracted_facts["employment_status"] = "unemployed"

        import re
        match_dep = re.search(r'(\d+)\s*(children|child|dependents)', text_lower)
        if match_dep:
            extracted_facts["dependents"] = int(match_dep.group(1))

        if text_lower in ["i need help with my house.", "i need help with my house", "help with house", "need help"]:
            flow = FlowType.AMBIGUOUS.value
            primary_intent = "AMBIGUOUS"
            urgency_level = UrgencyLevel.NORMAL.value
            urgency_score = 0.30
            urgency_reason = "Ambiguous housing query requiring clarification before scheme retrieval."
            summary = "User query regarding house is ambiguous."
            missing_info.append({
                "field": "housing_intent",
                "question": "I can help with that. Are you looking for housing assistance, help after disaster damage, or help with housing costs?",
                "importance": "high"
            })
        elif any(w in text_lower for w in ["eligibility", "eligible", "qualify", "qualification"]):
            flow = FlowType.ELIGIBILITY_CHECK.value
            primary_intent = "ELIGIBILITY_CHECK"
            urgency_level = UrgencyLevel.NORMAL.value
            urgency_score = 0.40
            urgency_reason = "Query requesting structured eligibility evaluation."
            summary = "I can help check whether you may qualify for this program."
            missing_info.append({
                "field": "location_and_family",
                "question": "I can help check whether you may qualify for this program. I need a couple of details first: what is your current location and household situation?",
                "importance": "high"
            })
        elif any(w in text_lower for w in self.CRISIS_KEYWORDS):
            flow = FlowType.CRISIS.value
            primary_intent = "CRISIS"
            urgency_level = UrgencyLevel.CRISIS.value
            urgency_score = 0.95
            urgency_reason = "Urgent crisis situation involving displacement, emergency shelter, or physical safety."
            summary = "EMERGENCY ASSISTANCE: Your safety is the top priority. Please move to higher ground or a designated shelter immediately. Below are emergency relief steps and official disaster assistance resources."
        elif any(w in text_lower for w in ["grocery", "food", "ration", "eat", "feed", "pds"]):
            flow = FlowType.PUBLIC_SERVICE.value
            primary_intent = "FOOD_ASSISTANCE"
            if "employment_status" in extracted_facts or "job" in text_lower:
                secondary_intents.append("UNEMPLOYMENT_SUPPORT")
            urgency_level = UrgencyLevel.HIGH.value if "job" in text_lower or "children" in text_lower else UrgencyLevel.NORMAL.value
            urgency_score = 0.75 if urgency_level == UrgencyLevel.HIGH.value else 0.40
            urgency_reason = "Public service request for food security and grocery assistance."
            summary = "User seeking food assistance and grocery support for family."
        elif any(w in text_lower for w in ["job", "unemployed", "employment", "career", "skill"]):
            flow = FlowType.PUBLIC_SERVICE.value
            primary_intent = "UNEMPLOYMENT_SUPPORT"
            urgency_level = UrgencyLevel.HIGH.value
            urgency_score = 0.70
            urgency_reason = "Public service request for unemployment support and jobseeker assistance."
            summary = "User seeking unemployment support and career placement assistance."
        else:
            flow = FlowType.PUBLIC_SERVICE.value
            primary_intent = "GENERAL_PUBLIC_SERVICE"
            urgency_level = UrgencyLevel.NORMAL.value
            urgency_score = 0.30
            urgency_reason = "Standard public service informational inquiry."
            summary = "Assistance request for public service scheme options."

        return {
            "flow": flow,
            "primary_intent": primary_intent,
            "secondary_intents": secondary_intents,
            "summary": summary,
            "extracted_facts": extracted_facts,
            "urgency": {
                "level": urgency_level,
                "score": urgency_score,
                "reasoning": urgency_reason
            },
            "missing_information": missing_info
        }

    def generate_grounded_response(self, system_prompt: str, user_message: str, grounding_data: Dict[str, Any]) -> str:
        text_lower = user_message.lower().strip()
        if "python" in text_lower or "pythn" in text_lower:
            return "Python is a high-level, general-purpose programming language known for its readable syntax, clean code structure, and extensive library ecosystem used in web development, data science, automation, and AI."
        elif "api" in text_lower:
            return "An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate and exchange data with each other seamlessly."
        elif "open source" in text_lower:
            return "Open source software refers to code that is publicly accessible, allowing anyone to view, modify, enhance, and distribute the source code freely under an open-source license."
        elif "internship" in text_lower or "intership" in text_lower:
            return "An internship is a professional learning experience that offers meaningful, practical work related to a student's field of study or career interest, helping build practical skills and network connections."
        elif "machine learning" in text_lower or "ai" in text_lower:
            return "Artificial Intelligence and Machine Learning enable computers to analyze data, learn patterns, and make intelligent predictions or decisions without being explicitly programmed for every scenario."
        
        summary = grounding_data.get("summary")
        if summary and not summary.startswith("Here is"):
            return summary
        return f"{user_message.strip().capitalize()} is a fundamental concept. You can explore structured documentation and learning resources for further details."


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI / OpenRouter API Provider supporting structured output.
    Falls back gracefully to MockLLMProvider if API key is missing or request fails.
    """
    def __init__(self, model_name: str = "openai/gpt-4o-mini"):
        self.model_name = os.getenv("LLM_MODEL", settings.LLM_MODEL)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")

    def generate_situation_analysis(self, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "mock_key":
            logger.info("OPENAI_API_KEY missing or mock_key set. Using MockLLMProvider fallback.")
            return MockLLMProvider().generate_situation_analysis(user_message, user_context)

        try:
            import httpx
            system_prompt = (
                "You are Sahay's Situation Analyzer. Analyze the user's message and return a JSON object with: "
                "flow (CRISIS, PUBLIC_SERVICE, ELIGIBILITY_CHECK), primary_intent, secondary_intents (list), summary, "
                "extracted_facts (dictionary), urgency (object), missing_information (list)."
            )
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.1
            }
            resp = httpx.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=15.0)
            resp.raise_for_status()
            result_json = resp.json()["choices"][0]["message"]["content"]
            return json.loads(result_json)
        except Exception as err:
            logger.warning(f"Live LLM provider call failed: {str(err)}. Falling back to MockLLMProvider.")
            return MockLLMProvider().generate_situation_analysis(user_message, user_context)

    def generate_grounded_response(self, system_prompt: str, user_message: str, grounding_data: Dict[str, Any]) -> str:
        if not self.api_key or self.api_key == "mock_key":
            return MockLLMProvider().generate_grounded_response(system_prompt, user_message, grounding_data)

        try:
            import httpx
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {user_message}\nGrounding:\n{json.dumps(grounding_data, indent=2)}"}
                ],
                "temperature": 0.2
            }
            resp = httpx.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=15.0)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as err:
            logger.warning(f"OpenAI response generation failed: {str(err)}. Using Mock fallback.")
            return MockLLMProvider().generate_grounded_response(system_prompt, user_message, grounding_data)


def get_llm_provider() -> BaseLLMProvider:
    provider_name = os.getenv("LLM_PROVIDER", settings.LLM_PROVIDER).lower()
    if provider_name == "ollama":
        provider = OllamaProvider()
        if provider.is_reachable():
            return provider
        logger.info("Ollama provider selected but unreachable. Falling back to OpenAI or Mock.")
        if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "mock_key":
            return OpenAIProvider()
        return MockLLMProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    return MockLLMProvider()
