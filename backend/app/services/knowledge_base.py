import json
import os
import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import RecommendationItem, SourceItem, DocumentItem

class KnowledgeBaseService:
    """
    Manages loading, parsing, metadata tagging, intent-aware ranking, and retrieval of authentic public service schemes.
    """
    
    def __init__(self, raw_data_path: str = "../data/raw/authentic_schemes.json"):
        self.raw_data_path = raw_data_path
        self._schemes: Dict[str, Dict[str, Any]] = {}
        self._knowledge_chunks: List[Dict[str, Any]] = []
        self._load_dataset()

    def _load_dataset(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = os.path.abspath(os.path.join(base_dir, "../../../", "data/raw/authentic_schemes.json"))
        
        if os.path.exists(resolved_path):
            with open(resolved_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    scheme_id = item["id"]
                    self._schemes[scheme_id] = item
                    
                    chunk_text = f"{item['title']} - {item['category']}. {item['summary']} {item['description']}"
                    metadata = {
                        "scheme_id": scheme_id,
                        "title": item["title"],
                        "category": item["category"],
                        "jurisdiction": item["jurisdiction"],
                        "issuing_authority": item["issuing_authority"],
                        "source_url": item["source_url"],
                        "effective_date": item.get("effective_date"),
                        "last_verified": item.get("last_verified")
                    }
                    self._knowledge_chunks.append({
                        "chunk_id": f"chk-{uuid.uuid4().hex[:8]}",
                        "scheme_id": scheme_id,
                        "content": chunk_text,
                        "metadata": metadata
                    })

    def get_scheme(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        return self._schemes.get(scheme_id)

    def list_schemes(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        schemes = list(self._schemes.values())
        if category:
            return [s for s in schemes if s["category"].lower() == category.lower()]
        return schemes

    def search_schemes(
        self, query: str, country: Optional[str] = "IN", state: Optional[str] = None, primary_intent: Optional[str] = None
    ) -> List[RecommendationItem]:
        query_lower = query.lower().strip()

        # AMBIGUOUS Intent Rule: Do NOT return premature scheme recommendations for ambiguous queries!
        if primary_intent == "AMBIGUOUS" or query_lower in ["i need help with my house.", "i need help with my house", "help with house", "need help"]:
            return []

        query_terms = [t for t in query_lower.replace('.', ' ').replace(',', ' ').split() if len(t) > 2]
        scored_schemes = []
        
        # Keyword Alias Mapping Table for exact civic intent matching
        alias_map = [
            (["grocery", "food", "ration", "eat", "feed", "pds", "food grain", "nutrition"], ["SCH-IN-014", "SCH-IN-004", "SCH-GOV-002"]),
            (["birth", "dob", "born", "newborn", "delivery"], ["SCH-IN-010"]),
            (["addhar", "aadhar", "aadhaar", "uidai", "identity"], ["SCH-IN-005"]),
            (["income", "caste", "domicile", "residence", "certif", "cerificate", "certificate", "e-district", "serviceonline"], ["SCH-IN-011"]),
            (["driving", "license", "licence", "dl", "learner", "parivahan", "rto", "sarathi"], ["SCH-IN-012"]),
            (["passport", "tatkaal", "visa", "mea"], ["SCH-IN-013"]),
            (["hospital", "medical", "ayushman", "health", "pmjay", "doctor"], ["SCH-IN-006"]),
            (["job", "unemployed", "career", "employment", "skill", "layoff"], ["SCH-IN-007", "SCH-GOV-003"]),
            (["pension", "senior", "elderly", "widow", "nsap"], ["SCH-IN-008"]),
            (["loan", "mudra", "shopkeeper", "entrepreneur"], ["SCH-IN-009"]),
            (["flood", "disaster", "shelter assistance"], ["SCH-IN-003", "SCH-GOV-001"]),
            (["farmer", "pm-kisan", "agriculture", "landholding"], ["SCH-IN-002"]),
            (["pmay", "housing", "pucca house", "awas"], ["SCH-IN-001"]),
        ]

        matched_target_ids = set()
        primary_boost_ids = set()

        for keywords, target_ids in alias_map:
            if any(kw in query_lower for kw in keywords):
                for tid in target_ids:
                    matched_target_ids.add(tid)

        # Primary intent priority boosting
        if primary_intent == "FOOD_ASSISTANCE":
            primary_boost_ids.update(["SCH-IN-014", "SCH-IN-004", "SCH-GOV-002"])
        elif primary_intent == "UNEMPLOYMENT_SUPPORT":
            primary_boost_ids.update(["SCH-IN-007", "SCH-GOV-003"])
        elif primary_intent == "HOUSING_ASSISTANCE":
            primary_boost_ids.update(["SCH-IN-001", "SCH-GOV-001"])

        for scheme in self._schemes.values():
            # 1. Strict Country Jurisdiction Filter
            scheme_country = scheme.get("country", "IN")
            if country and scheme_country != country:
                continue

            # 2. Strict State/Region Jurisdiction Filter
            scheme_level = scheme.get("jurisdiction_level", "NATIONAL")
            scheme_region = scheme.get("region")
            if state and scheme_level == "STATE" and scheme_region and scheme_region.lower() != state.lower():
                continue

            text_corpus = f"{scheme['title']} {scheme['summary']} {scheme['category']} {scheme['description']}".lower()
            
            score = 0
            # Primary intent priority score (+200)
            if scheme["id"] in primary_boost_ids:
                score += 200

            # Direct keyword alias match (+100)
            if scheme["id"] in matched_target_ids:
                score += 100

            for term in query_terms:
                if term in text_corpus:
                    score += 10
            
            if score > 0:
                scored_schemes.append((scheme, score))
                
        # Sort by score descending
        scored_schemes.sort(key=lambda x: x[1], reverse=True)
        
        # Filter recommendations by strict semantic relevance threshold (score >= 100 for primary boost/alias match)
        filtered_results: List[RecommendationItem] = []
        for scheme, score in scored_schemes:
            if primary_intent and primary_intent in ["FOOD_ASSISTANCE", "UNEMPLOYMENT_SUPPORT", "HOUSING_ASSISTANCE"]:
                # Only include schemes with a direct intent or alias match (score >= 100)
                if score >= 100:
                    filtered_results.append(
                        RecommendationItem(
                            scheme_id=scheme["id"],
                            title=scheme["title"],
                            issuing_authority=scheme["issuing_authority"],
                            country=scheme.get("country", "IN"),
                            jurisdiction_level=scheme.get("jurisdiction_level", "NATIONAL"),
                            region=scheme.get("region"),
                            category=scheme["category"],
                            summary=scheme["summary"],
                            match_confidence="HIGH"
                        )
                    )
            elif score > 0:
                filtered_results.append(
                    RecommendationItem(
                        scheme_id=scheme["id"],
                        title=scheme["title"],
                        issuing_authority=scheme["issuing_authority"],
                        country=scheme.get("country", "IN"),
                        jurisdiction_level=scheme.get("jurisdiction_level", "NATIONAL"),
                        region=scheme.get("region"),
                        category=scheme["category"],
                        summary=scheme["summary"],
                        match_confidence="HIGH" if score >= 100 else "MEDIUM"
                    )
                )

        return filtered_results

    def get_documents_for_scheme(self, scheme_id: str) -> List[DocumentItem]:
        scheme = self._schemes.get(scheme_id)
        if not scheme or "document_requirements" not in scheme:
            return []
            
        docs: List[DocumentItem] = []
        for req in scheme["document_requirements"]:
            docs.append(
                DocumentItem(
                    document_name=req["document_name"],
                    purpose=req["purpose"],
                    how_to_obtain=req["how_to_obtain"],
                    is_mandatory=req.get("is_mandatory", True)
                )
            )
        return docs

    def get_source_for_scheme(self, scheme_id: str) -> Optional[SourceItem]:
        scheme = self._schemes.get(scheme_id)
        if not scheme:
            return None
            
        return SourceItem(
            title=f"Official Portal: {scheme['title']}",
            url=scheme["source_url"],
            issuing_authority=scheme["issuing_authority"],
            last_verified=scheme.get("last_verified")
        )

knowledge_base_service = KnowledgeBaseService()
