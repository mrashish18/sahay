from typing import Dict, Any, List, Tuple, Optional
from app.models.schemas import Situation, Urgency, UrgencyLevel, ActionStep, SourceItem, MissingInfoItem
from app.models.crisis import CrisisType, ResourceType, SafetyStep, CrisisResource, CrisisAssessment
from app.services.knowledge_base import knowledge_base_service
from app.services.rag_service import rag_service

class CrisisNavigator:
    """
    First-Class Crisis Navigator for Sahay.
    Enforces deterministic priority ordering:
    1. Immediate Safety Steps
    2. Emergency & Crisis Resources
    3. Immediate Assistance (Shelter/Food/Medical)
    4. Public Service Assistance
    5. Action Plan & Verified Traceable Sources
    
    Zero LLM interference in emergency priority ordering. Zero fabricated contact numbers.
    """

    def classify_crisis_type(self, message: str, facts: Dict[str, Any]) -> Tuple[CrisisType, Dict[str, Any]]:
        text_lower = message.lower()
        signals: Dict[str, Any] = {}

        # 1. Fact Signal Extraction (Preserve explicit vs inferred distinction)
        if facts.get("disaster_impact") == "flood" or "flood" in text_lower or "flooding" in text_lower:
            signals["disaster_impact"] = "flood"
        if facts.get("displacement") is True or "nowhere to stay" in text_lower or "shelter" in text_lower:
            signals["displacement"] = True
        if "chest pain" in text_lower or "medical emergency" in text_lower or "hospital" in text_lower:
            signals["medical_emergency"] = True
        if "don't feel safe" in text_lower or "safety threat" in text_lower or "abuse" in text_lower:
            signals["safety_threat"] = True
        if "no food" in text_lower or "starving" in text_lower:
            signals["lack_of_food"] = True

        # 2. Crisis Category Assignment
        if signals.get("medical_emergency"):
            return CrisisType.MEDICAL_EMERGENCY, signals
        elif signals.get("safety_threat"):
            return CrisisType.SAFETY_THREAT, signals
        elif signals.get("disaster_impact") == "flood":
            if signals.get("displacement"):
                return CrisisType.DISPLACEMENT, signals
            return CrisisType.FLOOD, signals
        elif "fire" in text_lower:
            return CrisisType.FIRE, signals
        elif signals.get("lack_of_food"):
            return CrisisType.FOOD_INSECURITY, signals
        elif signals.get("displacement"):
            return CrisisType.HOMELESSNESS, signals
        elif any(k in text_lower for k in ["disaster", "storm", "earthquake", "cyclone"]):
            return CrisisType.DISASTER, signals

        return CrisisType.OTHER, signals

    def generate_safety_steps(self, crisis_type: CrisisType, signals: Dict[str, Any]) -> List[SafetyStep]:
        steps: List[SafetyStep] = []

        if crisis_type == CrisisType.MEDICAL_EMERGENCY:
            steps.append(SafetyStep(
                priority=1,
                title="Seek Immediate Medical Emergency Care",
                description="Immediately contact your local medical emergency service or proceed to the nearest emergency room.",
                reason="Acute health emergencies require professional medical evaluation without delay."
            ))
            steps.append(SafetyStep(
                priority=2,
                title="Do Not Delay Care for Documentation",
                description="Hospital emergency departments are obligated to provide urgent stabilization regardless of documentation.",
                reason="Physical health and safety take absolute priority over administrative paperwork."
            ))
        elif crisis_type == CrisisType.SAFETY_THREAT:
            steps.append(SafetyStep(
                priority=1,
                title="Move to a Safe Public or Sheltered Location",
                description="If you feel threatened at home, relocate to a well-lit public space, shelter, or trusted community center immediately.",
                reason="Physical safety is the paramount priority."
            ))
            steps.append(SafetyStep(
                priority=2,
                title="Contact Municipal Safety Authorities",
                description="Call your local municipal safety helpline or law enforcement if you are in immediate danger.",
                reason="Official intervention provides protective escalation."
            ))
        elif crisis_type in (CrisisType.FLOOD, CrisisType.DISASTER, CrisisType.DISPLACEMENT):
            steps.append(SafetyStep(
                priority=1,
                title="Move to Higher Ground & Safe Evacuation Shelter",
                description="Avoid standing or moving floodwaters and move immediately to designated municipal emergency lodging.",
                reason="Floodwaters pose severe structural, electrical, and submersion risks."
            ))
            steps.append(SafetyStep(
                priority=2,
                title="Avoid Damaged Structures & Power Lines",
                description="Do not re-enter flood-damaged buildings until cleared by disaster emergency inspectors.",
                reason="Unseen structural weakening and electrical hazards present severe physical danger."
            ))
        elif crisis_type == CrisisType.FOOD_INSECURITY:
            steps.append(SafetyStep(
                priority=1,
                title="Access Community Emergency Food Pantries",
                description="Locate local emergency food distribution hubs or community nutrition centers for immediate meal supply.",
                reason="Immediate nutrition support prevents acute health deterioration."
            ))

        return steps

    def get_verified_emergency_resources(self, crisis_type: CrisisType, state: Optional[str], country: Optional[str] = "IN") -> List[CrisisResource]:
        resources: List[CrisisResource] = []
        jurisdiction = f"{state}, India" if country == "IN" and state else ("India (National)" if country == "IN" else "United States")

        target_scheme_id = "SCH-IN-003" if (country == "IN" and (state == "Bihar" or crisis_type in (CrisisType.FLOOD, CrisisType.DISASTER, CrisisType.DISPLACEMENT))) else ("SCH-GOV-001" if country == "US" else "SCH-IN-001")
        disaster_scheme = knowledge_base_service.get_scheme(target_scheme_id)
        if disaster_scheme and disaster_scheme.get("country") == country:
            resources.append(CrisisResource(
                name=disaster_scheme["title"],
                resource_type=ResourceType.SHELTER if crisis_type in (CrisisType.FLOOD, CrisisType.DISPLACEMENT) else ResourceType.EMERGENCY,
                description=disaster_scheme["summary"],
                jurisdiction=disaster_scheme["jurisdiction"],
                availability="24/7 Intake",
                source_url=disaster_scheme["source_url"],
                issuing_authority=disaster_scheme["issuing_authority"],
                last_verified=disaster_scheme.get("last_verified"),
                verified=True
            ))

        # Check for food support if food crisis
        if crisis_type == CrisisType.FOOD_INSECURITY:
            food_scheme_id = "SCH-IN-014" if country == "IN" else "SCH-GOV-002"
            food_scheme = knowledge_base_service.get_scheme(food_scheme_id)
            if food_scheme:
                resources.append(CrisisResource(
                    name=food_scheme["title"],
                    resource_type=ResourceType.FOOD,
                    description=food_scheme["summary"],
                    jurisdiction=food_scheme["jurisdiction"],
                    availability="Business Hours Intake",
                    source_url=food_scheme["source_url"],
                    issuing_authority=food_scheme["issuing_authority"],
                    last_verified=food_scheme.get("last_verified"),
                    verified=True
                ))

        # NO FAKE DATA POLICY: If no specific local resource is in DB, return transparent official advisory
        if not resources:
            resources.append(CrisisResource(
                name="Municipal Emergency Services",
                resource_type=ResourceType.EMERGENCY,
                description="For immediate local emergency support, please contact your designated local municipal hotline or emergency dispatch center.",
                jurisdiction=jurisdiction,
                availability="24/7",
                source_url="https://disastermanagement.gov.in" if country == "IN" else "https://www.fema.gov",
                issuing_authority="National Disaster Management Authority" if country == "IN" else "FEMA",
                last_verified="2026-01-15",
                verified=True
            ))

        return resources

    def process_crisis(
        self, situation: Situation, urgency: Urgency, missing_info: List[MissingInfoItem], message: str
    ) -> CrisisAssessment:
        facts = situation.extracted_facts
        crisis_type, signals = self.classify_crisis_type(message, facts)

        # 1. Deterministic Priority: Immediate Safety
        safety_steps = self.generate_safety_steps(crisis_type, signals)

        # 2. Verified Crisis Resources
        state = facts.get("state")
        country = facts.get("country", "IN")
        resources = self.get_verified_emergency_resources(crisis_type, state, country)

        # 3. Action Plan Generation
        action_plan: List[ActionStep] = [
            ActionStep(
                step_number=1,
                title="Ensure Immediate Physical Safety",
                description="Follow the top safety instructions above. Move to safe shelter or seek care if in danger.",
                estimated_time="IMMEDIATE"
            ),
            ActionStep(
                step_number=2,
                title="Contact Emergency Intake & Housing Services",
                description="Reach out to verified emergency shelter intake services or municipal response centers.",
                estimated_time="30 mins"
            ),
            ActionStep(
                step_number=3,
                title="File Emergency Financial & Housing Claim",
                description="Submit disaster assistance application on the official government disaster relief portal.",
                estimated_time="1 hour"
            )
        ]

        # 4. Sources
        sources: List[SourceItem] = []
        for r in resources:
            sources.append(SourceItem(
                title=r.name,
                url=r.source_url,
                issuing_authority=r.issuing_authority,
                last_verified=r.last_verified
            ))

        return CrisisAssessment(
            crisis_detected=True,
            crisis_type=crisis_type,
            severity=urgency.level,
            signals=signals,
            immediate_safety_steps=safety_steps,
            emergency_resources=resources,
            missing_information=missing_info,
            action_plan=action_plan,
            sources=sources
        )

crisis_navigator = CrisisNavigator()
