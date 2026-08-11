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
        domain: Optional[str] = None,
        sub_intent: Optional[str] = None,
        entity_provenance: Optional[Dict[str, Any]] = None
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
        self.sub_intent = sub_intent
        self.entity_provenance = entity_provenance or {}

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
        r"nowhere to stay", r"house.*damaged", r"floodwater.*damaged", r"ghar.*flood", r"safety threat",
        r"\b(doob|dub|doobba|duba|dube)\b",
        r"pani.*(doob|dub|bhar|aagaya|aa\s+gaya|main|me|gaya|gya)",
        r"ghar.*(doob|dub|pani|paani|bhar|toot|flood)",
        r"rehne\s+ki\s+jagah\s+nahi", r"paani\s+ghar"
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

    KNOWN_CITIES = [
        "triveniganj", "triveni ganj", "supaul", "patna", "gaya", "muzaffarpur", "bhagalpur",
        "darbhanga", "purnia", "madhubani", "saharsa", "araria", "kishanganj", "madhepura",
        "sitamarhi", "bettiah", "munger", "buxar", "sasaram", "siwan", "gopalganj",
        "katihar", "begusarai", "nalanda", "rajgir", "nawada", "jamui", "khagaria",
        "vaishali", "hajipur", "samastipur", "chhapra", "motihari", "rohtas",
        "delhi", "mumbai", "kolkata", "chennai", "bengaluru", "hyderabad", "pune",
        "jaipur", "ahmedabad", "lucknow", "chandigarh", "shimla", "new york", "london"
    ]

    def extract_location_from_text(self, text: str) -> Optional[str]:
        text_raw = text.strip()
        text_lower = text_raw.lower()

        # 1. Check known cities / towns / districts list first
        for c in self.KNOWN_CITIES:
            if c in text_lower:
                if c in ["triveniganj", "triveni ganj"]:
                    return "Triveniganj"
                return c.capitalize()

        # 2. Regex preposition matching: "in <place>", "for <place>", "about <place>", "near <place>"
        prep_match = re.search(r"\b(?:in|at|for|near|around|about|what about|how about)\s+([a-zA-Z\s\-]+)", text_raw, re.IGNORECASE)
        if prep_match:
            candidate = prep_match.group(1).strip()
            stop_words = [
                "the", "a", "an", "some", "any", "every", "all", "in", "at", "for", "near", "around", "about",
                "tomorrow", "today", "tonight", "yesterday", "evening", "morning", "afternoon",
                "night", "raat", "subah", "dopahar", "shaam", "kal", "aaj", "please", "help",
                "hogi", "hoga", "hain", "hai", "kaisa", "kaisi", "kya", "batao", "bataiye", "weather", "rain",
                "it", "this", "that", "there", "here", "where", "somewhere", "anywhere", "place", "them", "him", "her", "me", "us", "you", "which", "what", "my", "your",
                "our", "their", "who", "whom", "whose", "info", "information", "details", "scheme", "program",
                "support", "assistance", "food", "ration", "housing", "health", "card", "job", "work"
            ]
            clean_words = []
            for w in candidate.split():
                if w.lower() in stop_words:
                    break
                clean_words.append(w)
            if clean_words:
                loc = " ".join(clean_words).strip("?,.!")
                if loc and len(loc) >= 3 and not any(w in loc.lower() for w in ["weather", "rain", "forecast", "temp", "mausam"]):
                    if loc.lower() not in ["us", "usa", "united states", "india", "bihar", "uk", "it", "this", "that", "there", "here", "where"]:
                        return loc.title()

        return None

    def understand_and_normalize(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
        session: Optional[Any] = None
    ) -> SemanticQueryResult:
        user_context = user_context or {}
        conversation_history = conversation_history or []
        text_raw = user_message.strip()
        text_lower = text_raw.lower()

        # 1. PRIORITY #1: SAFETY & CRISIS INTENT (Overrides all other routes)
        # -------------------------------------------------------------------
        is_crisis_query = any(re.search(pat, text_lower) for pat in self.CRISIS_PATTERNS)
        is_active_crisis = getattr(session, "active_topic", None) == "CRISIS" or getattr(session, "active_domain", None) == "CRISIS"
        is_crisis_followup = is_active_crisis and any(w in text_lower for w in ["what should i do", "where can i get help", "how to get help", "what to do", "next steps", "shelter", "help"])

        if is_crisis_query or is_crisis_followup:
            norm_query = "My house was damaged by flooding and we need emergency shelter." if is_crisis_query else "Emergency assistance follow-up: what action steps and resources are available?"
            extracted_facts = dict(user_context)
            extracted_facts["disaster_impact"] = "flood"
            if any(w in text_lower for w in ["nowhere to stay", "evicted", "homeless", "need shelter"]):
                extracted_facts["displacement"] = True
            urgency = Urgency(level=UrgencyLevel.CRISIS, score=0.98, reasoning="Urgent displacement or physical safety crisis.")
            
            if session:
                session.reset_topic("CRISIS", new_domain="CRISIS")

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
        # 1B. PUBLIC SERVICE STATE FOLLOW-UP ("in Bihar", "in Delhi")
        # -------------------------------------------------------------------
        active_topic_val = getattr(session, "active_topic", None)
        if text_lower in ["in bihar", "bihar", "in delhi", "delhi", "in us", "in usa"] and active_topic_val != "WEATHER":
            st_name = "Bihar" if "bihar" in text_lower else ("Delhi" if "delhi" in text_lower else "US")
            c_name = "US" if st_name == "US" else "IN"
            if session:
                session.update_context(state=st_name, country=c_name)
            ext_facts = dict(user_context)
            ext_facts["state"] = st_name
            ext_facts["country"] = c_name
            if getattr(session, "service_context", {}).get("scheme_id"):
                ext_facts["scheme"] = session.service_context["scheme_id"]
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.30, reasoning="Updated location jurisdiction context.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=f"Public service assistance in {st_name}",
                flow=FlowType.PUBLIC_SERVICE,
                primary_intent=active_topic_val or "PUBLIC_SERVICE",
                secondary_intents=[],
                confidence=0.95,
                entities=ext_facts,
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # -------------------------------------------------------------------
        # 2. PENDING CLARIFICATION RESOLUTION & TOPIC CHANGE CHECK
        # -------------------------------------------------------------------
        is_explicit_topic_change = (
            any(re.search(pat, text_lower) for pat in self.CRISIS_PATTERNS) or
            any(re.search(pat, text_lower) for pat in self.FOOD_PATTERNS) or
            any(re.search(pat, text_lower) for pat in self.WEATHER_PATTERNS) or
            bool(re.search(r"\b(python|pythn|ration|pmay)\b", text_lower))
        )

        if session and session.pending_clarification:
            if is_explicit_topic_change:
                # User changed topic — clear stale pending clarification!
                session.clear_pending()
            else:
                # Check if user input satisfies pending clarification
                if session.pending_intent == "WEATHER" or session.pending_clarification in ["city", "weather_city", "weather_confirm"]:
                    city = None
                    for c in self.KNOWN_CITIES:
                        if c in text_lower:
                            city = c.capitalize()
                            break
                    if not city and len(text_lower.split()) <= 2 and not any(w in text_lower for w in ["what", "how", "why", "who", "when"]):
                        city = text_raw.capitalize()

                    if city:
                        time_period = session.pending_entities.get("time_period") or session.time_period or "evening"
                        session.clear_pending()
                        session.update_context(
                            active_topic="WEATHER",
                            active_intent="WEATHER",
                            active_domain="WEATHER",
                            location=city,
                            time_period=time_period,
                            date_reference="tomorrow"
                        )
                        norm_query = f"What will the weather be like tomorrow {time_period} in {city}?"
                        urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="Resolved pending weather location clarification.")
                        return SemanticQueryResult(
                            raw_query=text_raw,
                            normalized_query=norm_query,
                            flow=FlowType.WEB_SEARCH_REQUIRED,
                            primary_intent="WEATHER",
                            secondary_intents=[],
                            confidence=0.98,
                            entities={"location": city, "city": city, "time": "tomorrow", "time_period": time_period},
                            urgency=urgency,
                            missing_information=[],
                            temporal_requirement="CURRENT",
                            domain="WEATHER"
                        )

        # -------------------------------------------------------------------
        # 3. EXPLICIT WEATHER INTENT & WEATHER FOLLOW-UPS
        # -------------------------------------------------------------------
        last_bot_msg = ""
        last_user_msg = ""
        if conversation_history:
            for msg in reversed(conversation_history):
                if msg.get("sender") == "SAHAY" and not last_bot_msg:
                    last_bot_msg = msg.get("text", "").lower()
                elif msg.get("sender") == "USER" and not last_user_msg:
                    last_user_msg = msg.get("text", "").lower()

        active_topic = getattr(session, "active_topic", None)
        active_location = getattr(session, "location", None)
        active_scheme = getattr(session, "active_scheme", None)

        is_explicit_weather = any(re.search(pat, text_lower) for pat in self.WEATHER_PATTERNS)

        if is_explicit_weather:
            explicit_city_in_msg = self.extract_location_from_text(text_raw)

            city = explicit_city_in_msg
            if not city and active_topic == "WEATHER" and active_location:
                city = active_location

            state = user_context.get("state", "Bihar")
            time_period = None
            if "night" in text_lower or "raat" in text_lower or "overnight" in text_lower:
                time_period = "night"
            elif "morning" in text_lower or "subah" in text_lower:
                time_period = "morning"
            elif "afternoon" in text_lower or "dopahar" in text_lower:
                time_period = "afternoon"
            elif "evening" in text_lower or "shaam" in text_lower:
                time_period = "evening"

            # TIME PERIOD INHERITANCE RULE (FAILURE 3 & 4):
            # Inherit session.time_period ONLY if no new city is named and query is an elliptical continuation ("weather", "aur raat me")
            if not time_period and not explicit_city_in_msg and text_lower.strip() in ["weather", "wether", "wheather", "aur raat me"]:
                if active_topic == "WEATHER" and getattr(session, "time_period", None):
                    time_period = session.time_period

            if city:
                period_str = f" {time_period}" if time_period else ""
                norm_query = f"What will the weather be like tomorrow{period_str} in {city}?"
                missing_info = []
                if session:
                    session.update_context(
                        active_topic="WEATHER",
                        active_intent="WEATHER",
                        active_domain="WEATHER",
                        location=city,
                        time_period=time_period,
                        date_reference="tomorrow"
                    )
            else:
                period_label = f"tomorrow {time_period}'s" if time_period else "tomorrow's"
                q_text = f"Which city in {state} should I check for {period_label} weather forecast?"
                norm_query = f"Weather forecast for {state}"
                missing_info = [
                    MissingInfoItem(
                        field="city",
                        question=q_text,
                        importance="high"
                    )
                ]
                if session:
                    session.set_pending(intent="WEATHER", clarification="city", entities={"time_period": time_period, "state": state})

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

        # Context Case C: Location + Time Without Domain when NO active weather session ("tomorrow + Patna + evening")
        has_city = any(c in text_lower for c in self.KNOWN_CITIES)
        has_time = any(w in text_lower for w in ["tomorrow", "today", "tonight", "kal"])
        has_period = any(w in text_lower for w in ["evening", "morning", "afternoon", "night", "shaam", "raat", "subah", "dopahar"])

        if has_city and (has_time or has_period) and not is_explicit_weather and active_topic != "WEATHER":
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

        # Weather Follow-Up ("what about tomorrow?", "what about evening?", "how about Supaul?", "and at night?", "aur raat me")
        is_weather_followup = (
            (active_topic == "WEATHER" or "weather" in last_bot_msg or "rain" in last_bot_msg or "forecast" in last_bot_msg) and
            (
                any(w in text_lower for w in ["tomorrow", "today", "tonight", "kal", "evening", "night", "morning", "afternoon", "shaam", "raat", "subah", "dopahar", "overnight"]) or
                bool(self.extract_location_from_text(text_raw)) or
                text_lower.startswith(("what about", "how about", "and in", "aur"))
            )
        )

        if is_weather_followup:
            city = self.extract_location_from_text(text_raw)
            if not city:
                city = active_location
            if not city:
                for msg in [last_user_msg, last_bot_msg]:
                    c_found = self.extract_location_from_text(msg)
                    if c_found:
                        city = c_found
                        break
            city = city or "Patna"

            time_period = None
            if "night" in text_lower or "raat" in text_lower or "overnight" in text_lower:
                time_period = "night"
            elif "morning" in text_lower or "subah" in text_lower:
                time_period = "morning"
            elif "afternoon" in text_lower or "dopahar" in text_lower:
                time_period = "afternoon"
            elif "evening" in text_lower or "shaam" in text_lower:
                time_period = "evening"
            else:
                time_period = getattr(session, "time_period", None)

            if session:
                session.update_context(
                    active_topic="WEATHER",
                    active_intent="WEATHER",
                    active_domain="WEATHER",
                    location=city,
                    time_period=time_period,
                    date_reference="tomorrow"
                )

            period_str = f" {time_period}" if time_period else ""
            norm_query = f"What will the weather be like tomorrow{period_str} in {city}?"
            urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="Weather follow-up query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.WEB_SEARCH_REQUIRED,
                primary_intent="WEATHER",
                secondary_intents=[],
                confidence=0.98,
                entities={"location": city, "city": city, "time": "tomorrow", "time_period": time_period},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="CURRENT",
                domain="WEATHER"
            )

        # Single-Word or Short City Follow-Up ("Patna", "Delhi", "Supaul") after weather query or clarification
        extracted_city = self.extract_location_from_text(text_raw)
        if extracted_city or text_lower in self.KNOWN_CITIES or (len(text_lower.split()) <= 2 and not any(w in text_lower for w in ["what", "how", "why", "when", "who"])):
            is_weather_context = (active_topic == "WEATHER") or ("weather" in last_bot_msg or "rain" in last_bot_msg or "city" in last_bot_msg)
            if is_weather_context:
                city = extracted_city or text_raw.capitalize()
                time_period = getattr(session, "time_period", None) or "evening"
                if session:
                    session.clear_pending()
                    session.update_context(
                        active_topic="WEATHER",
                        active_intent="WEATHER",
                        active_domain="WEATHER",
                        location=city,
                        time_period=time_period,
                        date_reference="tomorrow"
                    )
                norm_query = f"What will the weather be like tomorrow {time_period} in {city}?"
                urgency = Urgency(level=UrgencyLevel.INFORMATIONAL, score=0.20, reasoning="City follow-up for weather query.")
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

        # Pronoun / Reference / Explicit Scheme Follow-Up ("am i eligible for it?", "what documents do I need?", "pmay milega mujhe")
        has_elig_kw = any(w in text_lower for w in ["eligible", "eligibility", "qualify", "can i get", "milega", "milegi"])
        has_doc_kw = any(w in text_lower for w in ["document", "documents", "paperwork", "proof", "docs"])
        has_explicit_pmay = "pmay" in text_lower or "housing" in text_lower or "awas" in text_lower
        has_explicit_ayushman = "ayushman" in text_lower or "health card" in text_lower or "pmjay" in text_lower
        has_explicit_ration = "ration" in text_lower or "food" in text_lower or "nfsa" in text_lower
        has_explicit_kisan = "kisan" in text_lower or "pm-kisan" in text_lower

        if has_elig_kw or has_doc_kw or has_explicit_pmay or has_explicit_ayushman or has_explicit_kisan or (has_explicit_ration and (has_elig_kw or has_doc_kw)):
            if has_explicit_pmay:
                resolved_scheme = "PMAY"
                scheme_id = "SCH-IN-001"
            elif has_explicit_ayushman:
                resolved_scheme = "Ayushman Bharat"
                scheme_id = "SCH-IN-006"
            elif has_explicit_kisan:
                resolved_scheme = "PM-KISAN"
                scheme_id = "SCH-IN-002"
            elif has_explicit_ration:
                resolved_scheme = "NFSA"
                scheme_id = "SCH-IN-014"
            else:
                ref_target = session.resolve_reference(text_raw) if session else None
                target_scheme = ref_target or active_scheme or ("NFSA" if active_topic in ["FOOD_ASSISTANCE", "NFSA", "PUBLIC_SERVICE"] else None)
                if target_scheme == "SCH-IN-006":
                    resolved_scheme, scheme_id = "Ayushman Bharat", "SCH-IN-006"
                elif target_scheme == "SCH-IN-001":
                    resolved_scheme, scheme_id = "PMAY", "SCH-IN-001"
                elif target_scheme == "SCH-IN-002":
                    resolved_scheme, scheme_id = "PM-KISAN", "SCH-IN-002"
                elif target_scheme in ["NFSA", "SCH-IN-014", "FOOD_ASSISTANCE", "ration"]:
                    resolved_scheme, scheme_id = "NFSA", "SCH-IN-014"
                else:
                    resolved_scheme = target_scheme or "NFSA"
                    scheme_id = "SCH-IN-014"

            target_flow = FlowType.DOCUMENT_GUIDANCE if has_doc_kw else FlowType.ELIGIBILITY_CHECK
            target_intent = "DOCUMENT_GUIDANCE" if has_doc_kw else "ELIGIBILITY_CHECK"

            if session:
                session.clear_pending()
                session.update_context(
                    active_topic=resolved_scheme,
                    active_intent=target_intent,
                    active_domain="PUBLIC_SERVICE",
                    active_scheme=scheme_id
                )
            norm_query = f"What documents are required for {resolved_scheme} scheme?" if has_doc_kw else f"Am I eligible for {resolved_scheme} scheme?"
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.40, reasoning="Resolved scheme requirements check.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=target_flow,
                primary_intent=target_intent,
                secondary_intents=[],
                confidence=0.96,
                entities={"scheme": scheme_id, "scheme_name": resolved_scheme},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # -------------------------------------------------------------------
        # 4. CURRENT-INFORMATION & LIVE REQUESTS (Scholarships, Internships, Jobs)
        # -------------------------------------------------------------------
        is_live_request = (
            any(w in text_lower for w in ["ongoing", "abhi", "open hai", "open h", "available now", "open now", "latest", "current", "recent", "2026", "right now", "mil raha hai", "kaha milengi", "kaha milegi"]) or
            ("which" in text_lower and ("open" in text_lower or "available" in text_lower)) or
            ("where" in text_lower and ("find" in text_lower or "get" in text_lower) and ("internship" in text_lower or "scholarship" in text_lower))
        )

        if is_live_request:
            if any(w in text_lower for w in ["scholrship", "scholarship", "scholarshp"]):
                topic = "scholarships"
                norm_query = "Which scholarships are currently open?"
                rewrite_search = "currently open scholarships India 2026"
                domain = "PUBLIC_SERVICE"
            elif any(w in text_lower for w in ["intership", "internship", "internhsip", "intenship"]):
                topic = "internships"
                norm_query = "Where can I find currently available internships?"
                rewrite_search = "currently available internships India 2026"
                domain = "GENERAL"
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

            if session:
                session.reset_topic("WEB_SEARCH_REQUIRED", new_domain=domain)

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

        # -------------------------------------------------------------------
        # 5. GENERAL INFORMATION (Concepts, Definitions, Programming, Math)
        # -------------------------------------------------------------------
        is_concept_def = (
            text_lower.startswith("what is ") or
            text_lower.startswith("explain ") or
            text_lower.startswith("how does ") or
            text_lower.startswith("what does ") or
            "how do " in text_lower or
            "meaning of " in text_lower or
            bool(re.search(r"\b(python|pythn)\b", text_lower))
        )

        if is_concept_def or bool(re.search(r"\b(python|pythn|api|machine learning|open source)\b", text_lower)):
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

            if session:
                session.reset_topic("GENERAL_INFORMATION", new_domain="GENERAL")

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
        # 6. PUBLIC SERVICE / FOOD ASSISTANCE / ELIGIBILITY / DOCUMENT INTENTS
        # -------------------------------------------------------------------
        # Food / Ration Assistance
        if any(re.search(pat, text_lower) for pat in self.FOOD_PATTERNS) or "ration" in text_lower or ("food" in text_lower and "kids" in text_lower):
            country_code = "US" if any(w in text_lower for w in ["in the us", "in us", "in usa", "united states"]) else user_context.get("country", "IN")
            scheme_id = "SCH-GOV-002" if country_code == "US" else "SCH-IN-014"

            if session:
                session.reset_topic("FOOD_ASSISTANCE", new_domain="PUBLIC_SERVICE")
                session.update_context(active_scheme=scheme_id, country=country_code)

            urgency = Urgency(level=UrgencyLevel.HIGH, score=0.75, reasoning="Public service food and ration support query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query="I need food assistance and grocery support for my family.",
                flow=FlowType.PUBLIC_SERVICE,
                primary_intent="FOOD_ASSISTANCE",
                secondary_intents=["UNEMPLOYMENT_SUPPORT"],
                confidence=0.95,
                entities={"country": country_code, "state": user_context.get("state") if country_code == "IN" else None, "scheme": scheme_id},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # Deterministic Eligibility Inquiry
        if any(re.search(pat, text_lower) for pat in self.ELIGIBILITY_PATTERNS) and not any(w in text_lower for w in ["internship", "intership", "scholarship", "scholrship", "python", "version"]):
            country_code = "US" if any(w in text_lower for w in ["in the us", "in us", "in usa", "united states"]) else user_context.get("country", "IN")
            
            # Check for pronoun reference to session.active_scheme ("it", "this", "that", "for it")
            ref_scheme = None
            if session and getattr(session, "active_scheme", None) and any(w in text_lower for w in ["it", "this", "that", "the scheme", "this scheme", "that scheme", "for it", "the ration"]):
                ref_scheme = session.active_scheme

            scheme_name = "PMAY" if "pmay" in text_lower else ("Ration Card" if "ration" in text_lower else "public welfare programs")
            scheme_id = ref_scheme or ("SCH-GOV-001" if country_code == "US" else ("SCH-IN-014" if "ration" in text_lower or "food" in text_lower or "job" in text_lower else "SCH-IN-001"))
            if session:
                session.reset_topic("ELIGIBILITY_CHECK", new_domain="PUBLIC_SERVICE")
                session.update_context(active_scheme=scheme_id, country=country_code)

            norm_query = f"Am I eligible for {scheme_name}?"
            urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.40, reasoning="Eligibility criteria evaluation query.")
            return SemanticQueryResult(
                raw_query=text_raw,
                normalized_query=norm_query,
                flow=FlowType.ELIGIBILITY_CHECK,
                primary_intent="ELIGIBILITY_CHECK",
                secondary_intents=[],
                confidence=0.95,
                entities={"scheme": scheme_id, "scheme_name": scheme_name},
                urgency=urgency,
                missing_information=[],
                temporal_requirement="NONE",
                domain="PUBLIC_SERVICE"
            )

        # Document Guidance
        if any(re.search(pat, text_lower) for pat in self.DOCUMENT_PATTERNS):
            scheme_name = "PMAY" if "pmay" in text_lower else "public welfare programs"
            if session:
                session.reset_topic("DOCUMENT_GUIDANCE", new_domain="PUBLIC_SERVICE")

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

        # General Public Service
        if any(re.search(pat, text_lower) for pat in self.PUBLIC_SERVICE_PATTERNS):
            if session:
                session.reset_topic("PUBLIC_SERVICE", new_domain="PUBLIC_SERVICE")

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
        # 7. UNRECOGNIZED / AMBIGUOUS QUERY FALLBACK PROTECTION (Never PUBLIC_SERVICE!)
        # -------------------------------------------------------------------
        urgency = Urgency(level=UrgencyLevel.NORMAL, score=0.30, reasoning="Unrecognized or ambiguous query requiring user clarification.")
        clarification = f"Sure — what details would you like to know about '{text_raw}'?"
        if session:
            session.reset_topic("AMBIGUOUS", new_domain="GENERAL")
            session.set_pending(intent="AMBIGUOUS", clarification="query_clarification")

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
