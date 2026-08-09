import re
import os
import json
import logging
from typing import Dict, Any, Tuple, List, Optional
from app.models.schemas import FlowType, UrgencyLevel, Urgency, Situation, MissingInfoItem

logger = logging.getLogger(__name__)

class SemanticQueryResult:
    def __init__(
        self,
        raw_query: str,
        normalized_query: str,
        flow: FlowType,
        primary_intent: str,
        secondary_intents: List[str],
        confidence: float,
        entities: Dict[str, Any],
        urgency: Urgency,
        missing_information: List[MissingInfoItem],
        temporal_requirement: str = "NONE",
        domain: Optional[str] = None
    ):
        self.raw_query = raw_query
        self.normalized_query = normalized_query
        self.flow = flow
        self.primary_intent = primary_intent
        self.secondary_intents = secondary_intents
        self.confidence = confidence
        self.entities = entities
        self.urgency = urgency
        self.missing_information = missing_information
        self.temporal_requirement = temporal_requirement
        self.domain = domain

class SemanticUnderstandingEngine:
    """
    Sahay Semantic Understanding & Query Normalization Layer.
    Executes BEFORE any RAG or database retrieval to ensure robust human-language understanding:
    - Crisis & Safety First (Priority #1)
    - Context-Aware Multi-Turn Follow-Up Resolution (distinguishes active weather context from general topics)
    - Ambiguity Protection (Never forces unknown queries into PUBLIC_SERVICE)
    - Typo & Spelling Tolerance (tomorow, wether, wheather, scholrship, eligble, intership, etc.)
    - Multilingual & Transliterated Indian Input ('kal barish hogi?', 'ration kaise milega', 'ghar flood damage')
    """

    WEATHER_PATTERNS = [
        r"\b(weather|wether|weathe|wheather|climate|mausam)\b",
        r"\b(rain|rainy|raining|barish|baarish|baaris|barsat|varsha)\b",
        r"\b(forecast|temperature|temp|humidity|hot|cold)\b",
        r"will.*rain", r"tomorrow.*rain", r"rain.*tomorrow", r"is.*it.*going.*to.*rain",
        r"kal.*barish", r"barish.*hogi", r"baarish.*padegi"
    ]

    CRISIS_PATTERNS = [
        r"\b(flood|flooded|flooding|floodwater|waterlogging|floodwave)\b",
        r"\b(disaster|emergency|shelter|homeless|evicted|eviction)\b",
        r"\b(fire|earthquake|landslide|cyclone|tsunami|storm)\b",
        r"\b(chest pain|heart attack|bleeding|unconscious|starving)\b",
        r"nowhere to stay", r"house.*damaged", r"floodwater.*damaged", r"ghar.*flood", r"safety threat"
    ]

    FOOD_PATTERNS = [
        r"\b(food|grocery|groceries|ration|rations|khana|bhojan|pds|eat|feed)\b",
        r"grocery support", r"food for kids", r"food for children", r"ration card", r"ration crd", r"ration kaise", r"ration kaha"
    ]

    ELIGIBILITY_PATTERNS = [
        r"\b(eligible|eligble|eligibility|qualify|qualification|can i get|milega|milega kya)\b",
        r"what government support might i qualify for", r"am i eligible"
    ]

    PUBLIC_SERVICE_PATTERNS = [
        r"\b(scheme|schemes|government support|government assistance|financial assistance|welfare|pension|scholarship|scholarships|scholrship|ration|pmay|housing|caste certificate|unemployed|unemployment|job support)\b",
        r"apply for a government", r"government education", r"financial assistance programs"
    ]

    DOCUMENT_PATTERNS = [
        r"\b(document|documents|documnts|docs|paperwork|proof)\b"
    ]

    KNOWN_CITIES = ["patna", "gaya", "supaul", "muzaffarpur", "bhagalpur", "delhi", "mumbai", "kolkata", "chennai", "bengaluru", "new york", "london"]

    def understand_and_normalize(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> SemanticQueryResult:
        user_context = user_context or {}
        conversation_history = conversation_history or []
        text_raw = user_message.strip()
        text_lower = text_raw.lower()

        # -------------------------------------------------------------------
        # 1. PRIORITY #1: SAFETY & CRISIS INTENT (Overrides all other routes)
        # -------------------------------------------------------------------
        if any(re.search(pat, text_lower) for pat in self.CRISIS_PATTERNS):
            norm_query = "My house was damaged by flooding and we need emergency shelter."
            extracted_facts = dict(user_context)
            extracted_facts["disaster_impact"] = "flood"
            if any(w in text_lower for w in ["nowhere to stay", "evicted", "homeless", "need shelter"]):
                extracted_facts["displacement"] = True
            urgency = Urgency(level=UrgencyLevel.CRISIS, score=0.98, reasoning="Urgent displacement or physical safety crisis.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.CRISIS,
                primary_intent="CRISIS",
                secondary_intents=["EMERGENCY_SHELTER"],
                confidence=0.99,
                entities=extracted_facts,
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="CRISIS"
            )

        # -------------------------------------------------------------------
        # 2. FOLLOW-UP CONTEXT RESOLUTION (Multi-Turn Conversation Memory)
        # -------------------------------------------------------------------
        last_bot_msg = ""
        last_user_msg = ""
        if conversation_history:
            for msg in reversed(conversation_history):
                if msg.get("sender") == "SAHAY" and not last_bot_msg:
                    last_bot_msg = msg.get("text", "").lower()
                elif msg.get("sender") == "USER" and not last_user_msg:
                    last_user_msg = msg.get("text", "").lower()

        has_active_weather_context = (
            "weather" in last_bot_msg or "rain" in last_bot_msg or "forecast" in last_bot_msg or
            "weather" in last_user_msg or "rain" in last_user_msg or "barish" in last_user_msg
        )

        # Context Case A: City Single-Word Follow-Up ("Patna", "Delhi") after Weather Query
        if text_lower in self.KNOWN_CITIES or (len(text_lower.split()) <= 2 and any(c in text_lower for c in self.KNOWN_CITIES)):
            if has_active_weather_context or "city" in last_bot_msg or "location" in last_bot_msg:
                city = text_raw.capitalize()
                norm_query = f"Will it rain tomorrow in {city}?"
                urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="City follow-up for weather query.")
                return SemanticQueryResult(
                    raw_query=text_raw,
                    normalized_query=norm_query,
                    flow=FlowType.WEB_SEARCH_REQUIRED,
                    primary_intent="WEATHER",
                    secondary_intents=[],
                    confidence=0.98,
                    entities={"location": city, "time": "tomorrow", "city": city},
                    urgency=urgency,
                    missing_information=[],
                    temporal_requirement="CURRENT",
                    domain="WEATHER"
                )

        # Context Case B: Time-Period Follow-Up ("what about evening?", "and at night?", "what about morning?")
        if any(w in text_lower for w in ["evening", "night", "morning", "afternoon", "temperature", "pm", "am"]):
            if has_active_weather_context:
                city = user_context.get("city")
                if not city:
                    for c in self.KNOWN_CITIES:
                        if c in last_user_msg or c in last_bot_msg:
                            city = c.capitalize()
                            break
                city = city or "Patna"
                
                time_period = "evening"
                if "morning" in text_lower:
                    time_period = "morning"
                elif "afternoon" in text_lower:
                    time_period = "afternoon"
                elif "night" in text_lower:
                    time_period = "night"
                elif "evening" in text_lower:
                    time_period = "evening"

                norm_query = f"What will the weather be like tomorrow {time_period} in {city}?"
                urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="Weather time-period follow-up query.")
                return SemanticQueryResult(
                    raw_query=text_raw,
                    normalized_query=norm_query,
                    flow=FlowType.WEB_SEARCH_REQUIRED,
                    primary_intent="WEATHER",
                    secondary_intents=[],
                    confidence=0.98,
                    entities={"location": city, "time": "tomorrow", "city": city, "time_period": time_period},
                    urgency=urgency,
                    missing_information=[],
                    temporal_requirement="CURRENT",
                    domain="WEATHER"
                )
            elif not any(re.search(pat, text_lower) for pat in self.WEATHER_PATTERNS) and not any(c in text_lower for c in self.KNOWN_CITIES) and not any(re.search(pat, text_lower) for pat in self.PUBLIC_SERVICE_PATTERNS):
                # NO weather context exists! Classify as AMBIGUOUS (Never PUBLIC_SERVICE!)
                urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.20, reasoning="Generic follow-up without active domain context.")
                clarification = "Sure — evening for what? If you mean the weather, tell me the city."
                return SemanticQueryResult(
                    raw_query=text_raw,
                    normalized_query=clarification,
                    flow=FlowType.AMBIGUOUS,
                    primary_intent="AMBIGUOUS",
                    secondary_intents=[],
                    confidence=0.30,
                    entities={},
                    urgency=urgency,
                    missing_information=[
                        MissingInfoItem(
                            field="followup_context",
                            question=clarification,
                            importance="high"
                        )
                    ],
                    temporal_requirement="NONE",
                    domain="GENERAL"
                )

        # Context Case C: Location + Time Without Domain ("tomorrow + Patna + evening", "tomorrow patna evening")
        has_city = any(c in text_lower for c in self.KNOWN_CITIES)
        has_time = any(w in text_lower for w in ["tomorrow", "today", "tonight", "kal"])
        has_period = any(w in text_lower for w in ["evening", "morning", "afternoon", "night", "shaam"])
        has_weather_kw = any(re.search(pat, text_lower) for pat in self.WEATHER_PATTERNS)

        if has_city and (has_time or has_period) and not has_weather_kw:
            city_name = next(c.capitalize() for c in self.KNOWN_CITIES if c in text_lower)
            clarification = f"Are you asking about tomorrow evening's weather in {city_name}?"
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.40, reasoning="Location and time specified without explicit weather intent.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=clarification,
                flow=FlowType.AMBIGUOUS,
                primary_intent="WEATHER_CLARIFICATION",
                secondary_intents=[],
                confidence=0.50,
                entities={"city": city_name, "time": "tomorrow", "time_period": "evening"},
                urgency=urgency,
                missing_information=[
                    MissingInfoItem(
                        field="weather_confirm",
                        question=clarification,
                        importance="high"
                    )
                ],
                temporal_requirement="CURRENT",
                domain="WEATHER"
            )

        # Context Case D: Field Selection for Current Internship/Scholarship Query ("AI", "Data Science")
        if text_lower in ["ai", "data science", "software", "python", "machine learning", "cs", "computer science"]:
            if "internship" in last_bot_msg or "internship" in last_user_msg or "scholrship" in last_user_msg or "scholarship" in last_bot_msg:
                field = text_raw.upper() if len(text_raw) <= 3 else text_raw.title()
                norm_query = f"Currently available {field} internships in India 2026"
                urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.30, reasoning="Field refinement for live internship search.")
                return SemanticQueryResult(
                    raw_query=text_raw,
                    normalized_query=norm_query,
                    flow=FlowType.WEB_SEARCH_REQUIRED,
                    primary_intent="WEB_SEARCH_REQUIRED",
                    secondary_intents=[],
                    confidence=0.96,
                    entities={"topic": "internships", "field": field},
                    urgency=urgency,
                    missing_information=[],
                    temporal_requirement="CURRENT",
                    domain="GENERAL"
                )

        # Context Case E: Assistance Type Follow-Up ("food", "grocery", "job")
        if text_lower in ["food", "grocery", "rations", "ration", "unemployment", "job"]:
            if "lost my job" in last_user_msg or "unemployed" in last_user_msg or "assistance" in last_bot_msg:
                norm_query = f"I need {text_lower} assistance for my situation."
                urgency = Urgency(level=UrgencyLevel.HIGH, score=0.75, reasoning="Follow-up request for food/grocery support.")
                return SemanticQueryResult(
                    raw_query=text_raw,
                    normalized_query=norm_query,
                    flow=FlowType.PUBLIC_SERVICE,
                    primary_intent="FOOD_ASSISTANCE" if text_lower in ["food", "grocery", "rations", "ration"] else "UNEMPLOYMENT_SUPPORT",
                    secondary_intents=["UNEMPLOYMENT_SUPPORT"],
                    confidence=0.95,
                    entities={"need": text_lower},
                    urgency=urgency,
                    missing_information=[],
                    temporal_requirement="NONE",
                    domain="PUBLIC_SERVICE"
                )

        # -------------------------------------------------------------------
        # 3. WEATHER INTENT (Open-Meteo Integration)
        # -------------------------------------------------------------------
        if any(re.search(pat, text_lower) for pat in self.WEATHER_PATTERNS):
            city = None
            for c in self.KNOWN_CITIES:
                if c in text_lower:
                    city = c.capitalize()
                    break

            state = user_context.get("state", "Bihar")
            time_period = "evening" if "evening" in text_lower or "shaam" in text_lower else ("morning" if "morning" in text_lower else ("night" if "night" in text_lower else None))
            
            if city:
                norm_query = f"Will it rain tomorrow in {city}?" if not time_period else f"What will the weather be like tomorrow {time_period} in {city}?"
                missing_info = []
            else:
                norm_query = f"Will it rain tomorrow in {state}?"
                missing_info = [
                    MissingInfoItem(
                        field="city",
                        question=f"Which city in {state} should I check for tomorrow's weather forecast?",
                        importance="high"
                    )
                ]

            urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="Weather forecast inquiry.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.WEB_SEARCH_REQUIRED,
                primary_intent="WEATHER",
                secondary_intents=[],
                confidence=0.97,
                entities={"location": city or state, "city": city, "time": "tomorrow", "time_period": time_period},
                urgency=urgency,
                missing_information=missing_info,
                temporal_requirement="CURRENT",
                domain="WEATHER"
            )

        # -------------------------------------------------------------------
        # 4. PUBLIC SERVICE / ELIGIBILITY / DOCUMENT / SCHEME INTENTS
        # -------------------------------------------------------------------

        # A. Explicit Deterministic Eligibility Inquiry ("Am I eligible for ration?", "pmay milega kya", "qualify for")
        if any(re.search(pat, text_lower) for pat in self.ELIGIBILITY_PATTERNS) and not any(w in text_lower for w in ["internship", "intership", "scholarship", "scholrship", "python", "version"]):
            scheme_name = "PMAY" if "pmay" in text_lower else ("Ration Card" if "ration" in text_lower else "public welfare programs")
            norm_query = f"Am I eligible for {scheme_name}?"
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.40, reasoning="Eligibility criteria evaluation query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.ELIGIBILITY_CHECK,
                primary_intent="ELIGIBILITY_CHECK",
                secondary_intents=[],
                confidence=0.95,
                entities={"scheme": scheme_name},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # B. Public Service Food / Ration ("ration kaise milega", "ration kaha milega")
        if any(re.search(pat, text_lower) for pat in self.FOOD_PATTERNS) or "ration" in text_lower or ("food" in text_lower and "kids" in text_lower):
            urgency = Urgency(level=UrgencyLevel.HIGH, score=0.75, reasoning="Public service food and ration support query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query="I need food assistance and grocery support for my family.",
                flow=FlowType.PUBLIC_SERVICE,
                primary_intent="FOOD_ASSISTANCE",
                secondary_intents=["UNEMPLOYMENT_SUPPORT"],
                confidence=0.95,
                entities={"country": user_context.get("country", "IN"), "state": user_context.get("state")},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # C. Document Guidance
        if any(re.search(pat, text_lower) for pat in self.DOCUMENT_PATTERNS):
            scheme_name = "PMAY" if "pmay" in text_lower else "public welfare programs"
            norm_query = f"What documents are required for {scheme_name}?"
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.35, reasoning="Document requirements query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.DOCUMENT_GUIDANCE,
                primary_intent="DOCUMENT_GUIDANCE",
                secondary_intents=[],
                confidence=0.95,
                entities={"scheme": scheme_name},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # D. General Public Service / Scheme / Government Assistance
        if any(re.search(pat, text_lower) for pat in self.PUBLIC_SERVICE_PATTERNS):
            missing_info = []
            if "state" not in user_context and "location" not in user_context:
                missing_info.append(
                    MissingInfoItem(
                        field="location",
                        question="Which state and district are you currently located in?",
                        importance="high"
                    )
                )

            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=text_raw.capitalize(),
                flow=FlowType.PUBLIC_SERVICE,
                primary_intent="GENERAL_PUBLIC_SERVICE",
                secondary_intents=[],
                confidence=0.90,
                entities={"country": user_context.get("country", "IN"), "state": user_context.get("state")},
                urgency=Urgency(level=UrgencyLevel.NORMAL, score=0.30, reasoning="General public service inquiry."),
                missing_information=missing_info,
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # -------------------------------------------------------------------
        # 5. CONTEXTUAL CURRENT-INFORMATION VS. GENERAL INFORMATION DISCOVERY
        # -------------------------------------------------------------------
        
        # Definitional / Conceptual Questions (GENERAL_INFORMATION)
        is_concept_def = (
            text_lower.startswith("what is ") or
            text_lower.startswith("explain ") or
            text_lower.startswith("how does ") or
            text_lower.startswith("what does ") or
            "how do " in text_lower or
            "meaning of " in text_lower
        )
        
        # Check if query specifically asks for CURRENT/LIVE listings or recent time-sensitive data
        is_live_request = (
            any(w in text_lower for w in ["ongoing", "abhi", "open hai", "open h", "available now", "open now", "latest", "current", "recent", "2026", "right now", "mil raha hai", "kaha milengi", "kaha milegi"]) or
            ("which" in text_lower and ("open" in text_lower or "available" in text_lower)) or
            ("where" in text_lower and ("find" in text_lower or "get" in text_lower) and ("internship" in text_lower or "scholarship" in text_lower))
        )

        if is_live_request and not ("what is an open internship" in text_lower or "how does internship availability work" in text_lower or "what does open source" in text_lower):
            if any(w in text_lower for w in ["intership", "internship", "internhsip", "intenship"]):
                topic = "internships"
                norm_query = "Where can I find currently available internships?"
                rewrite_search = "currently available internships India 2026"
                domain = "GENERAL"
            elif any(w in text_lower for w in ["scholrship", "scholarship", "scholarshp"]):
                topic = "scholarships"
                norm_query = "Which scholarships are currently open?"
                rewrite_search = "currently open scholarships India 2026"
                domain = "PUBLIC_SERVICE"
            elif "pmay" in text_lower:
                topic = "PMAY"
                norm_query = "What are the current PMAY rules and guidelines?"
                rewrite_search = "current PMAY rules government India 2026"
                domain = "PUBLIC_SERVICE"
            elif "python" in text_lower:
                topic = "python"
                norm_query = "What is the latest Python version?"
                rewrite_search = "latest Python release version 2026"
                domain = "GENERAL"
            elif "job" in text_lower or "jobs" in text_lower:
                topic = "government jobs"
                norm_query = "Which government jobs are currently open?"
                rewrite_search = "latest government job openings India 2026"
                domain = "PUBLIC_SERVICE"
            else:
                topic = text_raw
                norm_query = f"Latest current information for: {text_raw}"
                rewrite_search = f"latest {text_raw} 2026"
                domain = "GENERAL"

            urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.30, reasoning="Current live information inquiry.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.WEB_SEARCH_REQUIRED,
                primary_intent="WEB_SEARCH_REQUIRED",
                secondary_intents=[],
                confidence=0.96,
                entities={"topic": topic, "search_rewrite": rewrite_search},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="CURRENT",
                domain=domain
            )

        # Standard General Information (Concepts, Definitions, Explanations)
        if is_concept_def or any(w in text_lower for w in ["python", "pythn", "ai", "api", "machine learning", "open source"]):
            if "python" in text_lower or "pythn" in text_lower:
                norm_query = "What is Python?"
            elif "api" in text_lower:
                norm_query = "What is an API (Application Programming Interface) and how does it work?"
            elif "open source" in text_lower:
                norm_query = "What does open source mean?"
            elif "internship" in text_lower or "intership" in text_lower:
                norm_query = "What is an internship and how does internship availability work?"
            else:
                norm_query = text_raw.capitalize()

            urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.10, reasoning="General knowledge educational query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.GENERAL_INFORMATION,
                primary_intent="GENERAL_INFORMATION",
                secondary_intents=[],
                confidence=0.98,
                entities={"topic": norm_query},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="GENERAL"
            )

        # -------------------------------------------------------------------
        # 6. UNRECOGNIZED / AMBIGUOUS QUERY FALLBACK PROTECTION (Never PUBLIC_SERVICE!)
        # -------------------------------------------------------------------
        urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.30, reasoning="Unrecognized or ambiguous query requiring user clarification.")
        clarification = f"Sure — what details would you like to know about '{text_raw}'?"
        
        return SemanticQueryResult(
            raw_query=text_raw,
            normalized_query=clarification,
            flow=FlowType.AMBIGUOUS,
            primary_intent="AMBIGUOUS",
            secondary_intents=[],
            confidence=0.40,
            entities={},
            urgency=urgency,
            missing_information=[
                MissingInfoItem(
                    field="query_clarification",
                    question=clarification,
                    importance="high"
                )
            ],
            temporal_requirement="NONE",
            domain="GENERAL"
        )

semantic_engine = SemanticUnderstandingEngine()
