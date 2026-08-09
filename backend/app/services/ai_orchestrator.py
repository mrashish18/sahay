import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    SahayResponse, FlowType, UrgencyLevel, ChatRequest,
    RecommendationItem, DocumentItem, ActionStep, SourceItem,
    EligibilityItem, Situation, Urgency
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
            conversation_history=session.messages[:-1]
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
        # ROUTE A: WEB_SEARCH_REQUIRED (Weather & Live Current Information)
        # -------------------------------------------------------------------
        if flow == FlowType.WEB_SEARCH_REQUIRED:
            query_to_search = sem_res.entities.get("search_rewrite") or sem_res.normalized_query or request.message
            summary, web_sources, web_missing, weather_payload = web_search_service.process_web_or_weather_query(
                query=query_to_search,
                user_context=request.user_context
            )
            situation = Situation(summary=summary, extracted_facts=extracted_facts, primary_intent="WEB_SEARCH_REQUIRED", weather_data=weather_payload)
            sources = web_sources
            missing_info.extend(web_missing)
            session.update_context(active_topic="weather", location=weather_payload.get("city") if weather_payload else None, tool_used="Open-Meteo Weather API")

            return SahayResponse(
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
                disclaimer="Live web search result. Powered by Sahay AI Assistant."
            )

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
            # Topic Reset: Clear weather location context when topic switches to General Information
            session.active_topic = "GENERAL_INFORMATION"
            session.active_location = None

            return SahayResponse(
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
                disclaimer="General information provided by Sahay AI Assistant."
            )

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
            session.active_topic = "AMBIGUOUS"

            return SahayResponse(
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
                disclaimer="Clarification requested. Powered by Sahay AI Assistant."
            )

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
            
            target_scheme_id = "SCH-IN-003" if (country == "IN" and state == "Bihar") else ("SCH-IN-001" if country == "IN" else "SCH-GOV-001")
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
                eligibility.append(el_res)
                documents = knowledge_base_service.get_documents_for_scheme(target_scheme_id)
                sources = crisis_eval.sources

            action_plan = crisis_eval.action_plan
            session.update_context(active_topic="crisis", tool_used="Crisis Navigator")

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

            # Search Knowledge Base Schemes with Intent Boosting
            all_recs = knowledge_base_service.search_schemes(
                query=request.message,
                country=country,
                state=state,
                primary_intent=situation.primary_intent
            )

            # MAX 3 RECOMMENDATIONS RULE (1 Primary + up to 2 Relevant Alternatives)
            recommendations = all_recs[:3]

            target_scheme_id = None
            if recommendations:
                target_scheme_id = recommendations[0].scheme_id
                scheme_data = knowledge_base_service.get_scheme(target_scheme_id)
                
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
                        flow in [FlowType.DOCUMENT_GUIDANCE, FlowType.ELIGIBILITY_CHECK] or
                        any(w in request.message.lower() for w in ["document", "documents", "paperwork", "proof", "docs"])
                    )
                    if is_doc_requested:
                        documents = knowledge_base_service.get_documents_for_scheme(target_scheme_id)

                    source_item = knowledge_base_service.get_source_for_scheme(target_scheme_id)
                    if source_item:
                        sources.append(source_item)

            # Build Tailored Action Plan for matched scheme
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
                    ActionStep(step_number=1, title="Collect Required Supporting Documentation", description="Gather income slips, photo identification, and separation/status certificates.", estimated_time="1-2 days"),
                    ActionStep(step_number=2, title="Submit Application via Official Portal", description="Complete online benefit enrollment form on the official issuing authority portal.", estimated_time="45 mins"),
                    ActionStep(step_number=3, title="Track Benefit Processing & Verification", description="Check application portal weekly using your confirmation tracking ID.", estimated_time="5-7 business days")
                ]

            session.update_context(active_topic=situation.primary_intent, tool_used="Sahay RAG & Eligibility Engine")

        return SahayResponse(
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
            disclaimer="DISCLAIMER: Sahay is an independent public-service navigator and does not guarantee official legal eligibility. Please verify all requirements directly with the issuing government authority."
        )

ai_orchestrator = AIOrchestrator()
