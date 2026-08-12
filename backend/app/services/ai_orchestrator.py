import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    SahayResponse, FlowType, UrgencyLevel, ChatRequest,
    RecommendationItem, DocumentItem, ActionStep, SourceItem,
    EligibilityItem, EligibilityStatus, Situation, Urgency,
    ConversationDecision, EntityProvenance
)
from app.services.conversation_router import conversation_router
from app.services.web_search_service import web_search_service
from app.services.situation_analyzer import situation_analyzer
from app.services.eligibility_engine import eligibility_engine
from app.services.knowledge_base import knowledge_base_service
from app.services.rag_service import rag_service
from app.services.crisis_navigator import crisis_navigator
from app.services.llm_provider import get_llm_provider
from app.services.conversation_memory import conversation_memory

class AIOrchestrator:
    """
    Main AI Orchestrator with Conversational AI 2.0.
    Integrates Semantic Understanding, Ollama/OpenAI Grounded Generation,
    Multi-Turn Memory, Max 3 Scheme Recommendations, and Open-Meteo Weather.
    """
    
    def process_request(self, request: ChatRequest) -> SahayResponse:
        req_id = f"req-{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        
        cid = getattr(request, "conversation_id", None) or "default_session"
        session = conversation_memory.get_or_create_session(cid)
        session.add_message("USER", request.message)

        # 1. Intent & Flow Classification via Semantic Router
        flow, primary_intent, extracted_facts, urgency, sem_res = conversation_router.route(
            user_message=request.message,
            user_context=request.user_context,
            conversation_history=session.messages[:-1],
            session=session
        )

        country = extracted_facts.get("country") or (request.user_context or {}).get("country", "IN")
        state = extracted_facts.get("state") or (request.user_context or {}).get("state")

        recommendations: List[RecommendationItem] = []
        eligibility: List[EligibilityItem] = []
        documents: List[DocumentItem] = []
        action_plan: List[ActionStep] = []
        sources: List[SourceItem] = []
        missing_info = list(sem_res.missing_information)
        evidence = []

        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # ROUTE A: WEB_SEARCH_REQUIRED (Weather & Live Current Information)
        # -------------------------------------------------------------------
        if flow == FlowType.WEB_SEARCH_REQUIRED:
            query_to_search = sem_res.entities.get("search_rewrite") or sem_res.normalized_query or request.message
            req_time_period = sem_res.entities.get("time_period")
            requested_location = sem_res.entities.get("city") or sem_res.entities.get("location")
            summary, web_sources, web_missing, weather_payload = web_search_service.process_web_or_weather_query(
                query=query_to_search,
                user_context=request.user_context,
                time_period=req_time_period,
                location=requested_location
            )

            # TOOL VALIDATION RULE:
            # For every weather request, verify requested_location vs tool_location
            val_status = "PASSED"
            tool_city = weather_payload.get("city") if weather_payload else None
            if requested_location and tool_city:
                req_norm = requested_location.lower().replace(" ", "")
                tool_norm = tool_city.lower().replace(" ", "")
                if req_norm not in tool_norm and tool_norm not in req_norm:
                    val_status = "FAILED"
                    summary = f"Could not retrieve verified weather forecast for '{requested_location}'."
                    weather_payload = None

            situation = Situation(summary=summary, extracted_facts=extracted_facts, primary_intent=primary_intent, weather_data=weather_payload)
            sources = web_sources
            if web_missing:
                val_status = "FAILED" if not weather_payload else val_status
                existing_fields = {m.field for m in missing_info}
                for wm in web_missing:
                    if wm.field not in existing_fields:
                        missing_info.append(wm)
                        existing_fields.add(wm.field)

            if weather_payload and weather_payload.get("city"):
                session.update_context(
                    active_topic="WEATHER",
                    active_intent="WEATHER",
                    active_domain="WEATHER",
                    location=weather_payload.get("city"),
                    time_period=sem_res.entities.get("time_period"),
                    tool_used="Open-Meteo Weather API"
                )
            else:
                session.update_context(
                    active_topic=primary_intent,
                    active_domain=sem_res.domain or "GENERAL",
                    tool_used="Live Web Search"
                )

            selected_tool = "weather_forecast" if (weather_payload and weather_payload.get("city")) else "live_web_search"
            tool_args = {
                "requested_location": requested_location,
                "resolved_location": weather_payload.get("city") if weather_payload else requested_location,
                "time_period": req_time_period,
                "query": query_to_search
            }

            entity_prov = dict(getattr(sem_res, "entity_provenance", {}))
            for k in sem_res.entities:
                if k not in entity_prov:
                    if sem_res.entities.get(k) and sem_res.entities.get(k) != getattr(session, k, None):
                        entity_prov[k] = EntityProvenance.CURRENT_MESSAGE
                    else:
                        entity_prov[k] = EntityProvenance.CONVERSATION_CONTEXT

            decision = ConversationDecision(
                intent=primary_intent,
                sub_intent=getattr(sem_res, "sub_intent", None) or primary_intent,
                entities=sem_res.entities,
                entity_provenance=entity_prov,
                temporal_context={"date": sem_res.entities.get("time") or "today", "time_period": req_time_period},
                jurisdiction={"country": country, "state": state},
                conversation_context_used={
                    "active_topic": getattr(session, "active_topic", None),
                    "weather_location": session.weather_context.get("location")
                },
                missing_information=missing_info,
                action_required="FETCH_WEATHER" if selected_tool == "weather_forecast" else "SEARCH_WEB",
                selected_tool=selected_tool,
                tool_arguments=tool_args,
                confidence=sem_res.confidence,
                validation_status=val_status
            )

            resp = SahayResponse(
                request_id=req_id,
                timestamp=now_iso,
                flow=flow,
                situation=situation,
                urgency=urgency,
                missing_information=missing_info,
                recommendations=[],  # ZERO government schemes for weather/current info!
                eligibility=[],
                documents=[],
                action_plan=[],
                sources=sources,
                evidence=[],
                disclaimer="Live web search result. Powered by Sahay AI Assistant.",
                decision_metadata=decision
            )
            session.add_message("SAHAY", summary)
            return resp

        # -------------------------------------------------------------------
        # ROUTE B: GENERAL_INFORMATION (Programming, Math, Definitions)
        # -------------------------------------------------------------------
        elif flow == FlowType.GENERAL_INFORMATION:
            provider = get_llm_provider()
            summary = provider.generate_grounded_response(
                system_prompt="You are Sahay AI, a helpful, natural conversational AI assistant. Answer general knowledge questions clearly and conversationally.",
                user_message=request.message,
                grounding_data={"query": request.message}
            )

            situation = Situation(summary=summary, extracted_facts=extracted_facts, primary_intent="GENERAL_INFORMATION")
            session.reset_topic("GENERAL_INFORMATION", new_domain="GENERAL")

            decision = ConversationDecision(
                intent="GENERAL_INFORMATION",
                sub_intent="GENERAL_KNOWLEDGE",
                entities=sem_res.entities,
                temporal_context={"date": "none"},
                jurisdiction={"country": country, "state": state},
                conversation_context_used={"active_topic": "GENERAL_INFORMATION"},
                missing_information=[],
                action_required="GENERATE_GROUNDED_RESPONSE",
                selected_tool="llm_grounded_provider",
                tool_arguments={"query": request.message},
                confidence=sem_res.confidence,
                validation_status="PASSED"
            )

            resp = SahayResponse(
                request_id=req_id,
                timestamp=now_iso,
                flow=flow,
                situation=situation,
                urgency=urgency,
                missing_information=[],
                recommendations=[],  # ZERO government schemes for general questions!
                eligibility=[],
                documents=[],
                action_plan=[],
                sources=[],
                evidence=[],
                disclaimer="General information provided by Sahay AI Assistant.",
                decision_metadata=decision
            )
            session.add_message("SAHAY", summary)
            return resp

        # -------------------------------------------------------------------
        # ROUTE C: AMBIGUOUS Intent (Clarification Required - ZERO Scheme Cards!)
        # -------------------------------------------------------------------
        elif flow == FlowType.AMBIGUOUS:
            summary = sem_res.normalized_query or "Could you please specify more details so I can assist you better?"
            missing_items = list(sem_res.missing_information)
            if not missing_items:
                missing_items.append(
                    MissingInfoItem(
                        field="query_clarification",
                        question=summary,
                        importance="high"
                    )
                )

            situation = Situation(summary=summary, extracted_facts=extracted_facts, primary_intent=sem_res.primary_intent or "AMBIGUOUS")
            session.update_context(active_topic="AMBIGUOUS", active_domain="GENERAL")

            decision = ConversationDecision(
                intent="AMBIGUOUS",
                sub_intent="CLARIFICATION_REQUIRED",
                entities=sem_res.entities,
                temporal_context={"date": "none"},
                jurisdiction={"country": country, "state": state},
                conversation_context_used={"active_topic": "AMBIGUOUS"},
                missing_information=missing_items,
                action_required="ASK_CLARIFICATION",
                selected_tool=None,
                tool_arguments={},
                confidence=sem_res.confidence,
                validation_status="PASSED"
            )

            resp = SahayResponse(
                request_id=req_id,
                timestamp=now_iso,
                flow=flow,
                situation=situation,
                urgency=urgency,
                missing_information=missing_items,
                recommendations=[],  # ZERO premature schemes!
                eligibility=[],
                documents=[],
                action_plan=[],
                sources=[],
                evidence=[],
                disclaimer="Clarification requested. Powered by Sahay AI Assistant.",
                decision_metadata=decision
            )
            session.add_message("SAHAY", summary)
            return resp

        # -------------------------------------------------------------------
        # ROUTE D: CRISIS Navigator Workflow
        # -------------------------------------------------------------------
        elif flow == FlowType.CRISIS:
            situation, urgency, missing_info, _ = situation_analyzer.analyze(
                user_message=request.message,
                user_context=request.user_context
            )
            crisis_eval = crisis_navigator.process_crisis(
                situation=situation,
                urgency=urgency,
                missing_info=missing_info,
                message=request.message
            )
            
            situation.summary = "EMERGENCY ASSISTANCE: Your safety is the top priority. Please move to higher ground or a designated shelter immediately. Below are emergency relief steps and official disaster assistance resources."
            target_scheme_id = "SCH-IN-003" if country == "IN" else "SCH-GOV-001"
            scheme_data = knowledge_base_service.get_scheme(target_scheme_id)
            
            if scheme_data:
                recommendations = [
                    RecommendationItem(
                        scheme_id=scheme_data["id"],
                        title=scheme_data["title"],
                        issuing_authority=scheme_data["issuing_authority"],
                        country=scheme_data.get("country", "IN"),
                        jurisdiction_level=scheme_data.get("jurisdiction_level", "NATIONAL"),
                        region=scheme_data.get("region"),
                        category=scheme_data["category"],
                        summary=scheme_data["summary"],
                        match_confidence="HIGH"
                    )
                ]
                el_res = eligibility_engine.evaluate_scheme(
                    scheme_id=target_scheme_id,
                    rules=scheme_data.get("eligibility_rules", {}),
                    user_facts=situation.extracted_facts
                )
                if el_res.status == EligibilityStatus.LIKELY_ELIGIBLE:
                    el_res.status = EligibilityStatus.POTENTIALLY_ELIGIBLE
                    el_res.reasoning = "Potentially Relevant: Disaster relief assistance may apply based on reported flood damage, but official district registration and verification remain required."
                eligibility.append(el_res)
                documents = knowledge_base_service.get_documents_for_scheme(target_scheme_id)
                sources = crisis_eval.sources

            action_plan = crisis_eval.action_plan
            session.reset_topic("CRISIS", new_domain="CRISIS")

        # -------------------------------------------------------------------
        # ROUTE E: PUBLIC_SERVICE, ELIGIBILITY_CHECK, DOCUMENT_GUIDANCE
        # -------------------------------------------------------------------
        else:
            situation, urgency, missing_info_analyzer, _ = situation_analyzer.analyze(
                user_message=request.message,
                user_context=request.user_context
            )
            if sem_res.primary_intent and sem_res.primary_intent != "GENERAL_PUBLIC_SERVICE":
                situation.primary_intent = sem_res.primary_intent
            missing_info.extend(missing_info_analyzer)

            # Perform RAG Evidence Tracing
            evidence = rag_service.search_knowledge(
                query=request.message,
                country=country,
                state=state,
                top_k=4
            )

            # Target Scheme Determination & Context Lock (Section 1)
            # HARD RULE: Explicit entity/scheme references in current query ("pmay", "ayushman", "scholarship")
            # have HIGHER priority than pronoun references or previous active_scheme!
            has_explicit_scheme = any(w in request.message.lower() for w in ["pmay", "housing", "awas", "ayushman", "health card", "pmjay", "ration", "kisan", "pm-kisan"])
            has_pronoun_ref = any(w in request.message.lower() for w in ["it", "this", "that", "for it", "the scheme", "this scheme", "that scheme", "the ration", "uske liye", "iske liye", "isme", "usme"])
            
            if has_explicit_scheme and sem_res.entities.get("scheme"):
                target_scheme_id = sem_res.entities.get("scheme")
            elif has_pronoun_ref and getattr(session, "active_scheme", None):
                target_scheme_id = session.active_scheme
            else:
                target_scheme_id = sem_res.entities.get("scheme") or getattr(session, "active_scheme", None)
            
            if not target_scheme_id and situation.primary_intent == "FOOD_ASSISTANCE":
                target_scheme_id = "SCH-IN-014"

            # STRICT SCHEME LOCK RULE:
            # If flow is ELIGIBILITY_CHECK, DOCUMENT_GUIDANCE, or target_scheme_id is locked from prior turn,
            # return ONLY the referenced target scheme (Max recommendations = 1). NEVER run broad search.
            if flow in [FlowType.ELIGIBILITY_CHECK, FlowType.DOCUMENT_GUIDANCE] or has_pronoun_ref or any(w in request.message.lower() for w in ["eligible", "eligibility", "qualify", "document", "documents"]):
                target_scheme_id = target_scheme_id or "SCH-IN-014"
                scheme_data = knowledge_base_service.get_scheme(target_scheme_id)
                if scheme_data:
                    recommendations = [
                        RecommendationItem(
                            scheme_id=scheme_data["id"],
                            title=scheme_data["title"],
                            issuing_authority=scheme_data["issuing_authority"],
                            country=scheme_data.get("country", "IN"),
                            jurisdiction_level=scheme_data.get("jurisdiction_level", "NATIONAL"),
                            region=scheme_data.get("region"),
                            category=scheme_data["category"],
                            summary=scheme_data["summary"],
                            match_confidence="HIGH"
                        )
                    ]
                else:
                    recommendations = []
            else:
                # General Search: Max 3 Recommendations (1 Primary + up to 2 Alternatives)
                all_recs = knowledge_base_service.search_schemes(
                    query=request.message,
                    country=country,
                    state=state,
                    primary_intent=situation.primary_intent
                )
                recommendations = all_recs[:3]
                if not target_scheme_id and recommendations:
                    target_scheme_id = recommendations[0].scheme_id

            if target_scheme_id:
                scheme_data = knowledge_base_service.get_scheme(target_scheme_id)
                session.update_context(
                    active_topic=situation.primary_intent or "PUBLIC_SERVICE",
                    active_intent=flow.value,
                    active_domain="PUBLIC_SERVICE",
                    active_scheme=target_scheme_id
                )
                
                if scheme_data:
                    # Contextual Eligibility Card Rule: ONLY display if user explicitly asked or flow is ELIGIBILITY_CHECK
                    is_eligibility_requested = (
                        flow == FlowType.ELIGIBILITY_CHECK or
                        any(w in request.message.lower() for w in ["eligible", "eligibility", "qualify", "can i get", "milega kya"])
                    )
                    if is_eligibility_requested:
                        el_res = eligibility_engine.evaluate_scheme(
                            scheme_id=target_scheme_id,
                            rules=scheme_data.get("eligibility_rules", {}),
                            user_facts=situation.extracted_facts
                        )
                        eligibility.append(el_res)

                    # Contextual Document Checklist Card Rule: ONLY display if user explicitly asked or flow is DOCUMENT_GUIDANCE
                    is_doc_requested = (
                        flow in [FlowType.DOCUMENT_GUIDANCE] or
                        any(w in request.message.lower() for w in ["document", "documents", "paperwork", "proof", "docs"])
                    )
                    if is_doc_requested:
                        documents = knowledge_base_service.get_documents_for_scheme(target_scheme_id)

                    source_item = knowledge_base_service.get_source_for_scheme(target_scheme_id)
                    if source_item:
                        sources.append(source_item)

            # Conversational Response Hierarchy Formatter (Section 2 & 8)
            if flow == FlowType.ELIGIBILITY_CHECK or any(w in request.message.lower() for w in ["eligible", "eligibility", "for it"]):
                if target_scheme_id == "SCH-IN-014":
                    situation.summary = (
                        "I can help check your eligibility for NFSA food assistance.\n\n"
                        "Income eligibility criteria could not be verified from the current trusted dataset.\n\n"
                        "Do you currently hold an active Priority Household (PHH) or Antyodaya Anna Yojana (AAY) Ration Card?"
                    )
                else:
                    situation.summary = (
                        "I can help check whether you may qualify for this assistance.\n\n"
                        "I need a couple of details to evaluate official requirements.\n\n"
                        "What is your current location and household situation?"
                    )
            elif situation.primary_intent == "FOOD_ASSISTANCE" and not any(w in request.message.lower() for w in ["eligible", "document"]):
                situation.summary = (
                    "Yes — I can help with that.\n\n"
                    "The most relevant program I found is NFSA/PMGKAY food assistance.\n\n"
                    "If your family has an eligible ration card, you may be able to receive food-grain entitlements through your Fair Price Shop.\n\n"
                    "Do you already have a ration card?"
                )

            # Action Plan reduction for simple queries
            is_action_plan_requested = (
                flow == FlowType.DOCUMENT_GUIDANCE or
                any(w in request.message.lower() for w in ["how to apply", "where to apply", "procedure", "steps", "application process"])
            )
            if is_action_plan_requested and target_scheme_id:
                if target_scheme_id == "SCH-IN-011":
                    action_plan = [
                        ActionStep(step_number=1, title="Download & Complete e-District Self-Declaration Form", description="Download prescribed income/caste declaration form from State ServicePlus portal & attach photo.", estimated_time="20 mins"),
                        ActionStep(step_number=2, title="Submit Online Application on State e-District Portal", description="Log into State ServicePlus portal (serviceonline.bihar.gov.in), upload Aadhaar & salary/land proof.", estimated_time="30 mins"),
                        ActionStep(step_number=3, title="Revenue Officer Verification & Certificate Issue", description="Track application status; BDO/Circle Officer verifies record and issues digitally signed certificate.", estimated_time="7-14 business days")
                    ]
                elif target_scheme_id == "SCH-IN-014":
                    action_plan = [
                        ActionStep(step_number=1, title="Check Ration Card Entitlement at Fair Price Shop (FPS)", description="Visit local FPS with Ration Card or Aadhaar number for biometric e-POS verification.", estimated_time="15 mins"),
                        ActionStep(step_number=2, title="Collect Monthly Free Ration & Grocery Allocation", description="Receive 5 kg free food grains (rice/wheat) per person per month under PMGKAY.", estimated_time="30 mins"),
                        ActionStep(step_number=3, title="Apply for Ration Card Migration / One Nation One Ration Card", description="If relocated, register for ONORC portability at any local ration center.", estimated_time="1 day")
                    ]
                else:
                    action_plan = [
                        ActionStep(step_number=1, title="Collect Required Supporting Documentation", description="Gather income slips, photo identification, and status certificates.", estimated_time="1-2 days"),
                        ActionStep(step_number=2, title="Submit Application via Official Portal", description="Complete online benefit enrollment form on the official issuing authority portal.", estimated_time="45 mins"),
                        ActionStep(step_number=3, title="Track Benefit Processing & Verification", description="Check application portal weekly using your confirmation tracking ID.", estimated_time="5-7 business days")
                    ]
            else:
                action_plan = []

            session.update_context(
                active_topic=situation.primary_intent or "PUBLIC_SERVICE",
                active_scheme=target_scheme_id,
                tool_used="Sahay RAG & Eligibility Engine"
            )

        # -------------------------------------------------------------------
        # FINAL JURISDICTION PROTECTION GATE
        # -------------------------------------------------------------------
        if country == "IN":
            recommendations = [r for r in recommendations if r.country == "IN"]
            sources = [
                s for s in sources
                if not any(us_kw in (s.url or "").lower() or us_kw in (s.title or "").lower() or us_kw in (s.issuing_authority or "").lower()
                           for us_kw in ["fema", "hhs.gov", "usa.gov", "snap", "us department", "us emergency"])
            ]
        elif country == "US":
            recommendations = [r for r in recommendations if r.country == "US"]

        decision = ConversationDecision(
            intent=primary_intent,
            sub_intent=getattr(sem_res, "sub_intent", None) or primary_intent,
            entities=sem_res.entities,
            entity_provenance={
                k: (EntityProvenance.CURRENT_MESSAGE if sem_res.entities.get(k) and sem_res.entities.get(k) != getattr(session, k, None) else EntityProvenance.CONVERSATION_CONTEXT)
                for k in sem_res.entities
            },
            temporal_context={"date": sem_res.entities.get("time") or "none"},
            jurisdiction={"country": country, "state": state},
            conversation_context_used={
                "active_topic": getattr(session, "active_topic", None),
                "service_scheme": getattr(session.service_context, "get", lambda k: None)("scheme_id")
            },
            missing_information=missing_info,
            action_required="EVALUATE_ELIGIBILITY" if flow == FlowType.ELIGIBILITY_CHECK else ("CRISIS_RESPONSE" if flow == FlowType.CRISIS else "SEARCH_KNOWLEDGE_BASE"),
            selected_tool="eligibility_evaluator" if flow == FlowType.ELIGIBILITY_CHECK else ("crisis_navigator" if flow == FlowType.CRISIS else "rag_knowledge_base"),
            tool_arguments={"country": country, "state": state, "primary_intent": primary_intent},
            confidence=sem_res.confidence,
            validation_status="PASSED"
        )

        resp = SahayResponse(
            request_id=req_id,
            timestamp=now_iso,
            flow=flow,
            situation=situation,
            urgency=urgency,
            missing_information=missing_info,
            recommendations=recommendations,
            eligibility=eligibility,
            documents=documents,
            action_plan=action_plan,
            sources=sources,
            evidence=evidence,
            disclaimer="DISCLAIMER: Sahay is an independent public-service navigator and does not guarantee official legal eligibility. Please verify all requirements directly with the issuing government authority.",
            decision_metadata=decision
        )
        session.add_message("SAHAY", situation.summary)
        return resp

ai_orchestrator = AIOrchestrator()
