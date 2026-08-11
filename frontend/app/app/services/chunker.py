from typing import List, Dict, Any

class SchemeChunker:
    """
    Logical section-based document chunker for public welfare schemes.
    Ensures deterministic chunk creation and preserves full parent metadata.
    """
    
    @staticmethod
    def chunk_scheme(scheme: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []
        scheme_id = scheme.get("id", "UNKNOWN")
        title = scheme.get("title", "")
        category = scheme.get("category", "")
        jurisdiction = scheme.get("jurisdiction", "")
        country = scheme.get("country", "IN")
        jurisdiction_level = scheme.get("jurisdiction_level", "NATIONAL")
        region = scheme.get("region")
        issuing_authority = scheme.get("issuing_authority", "")
        source_url = scheme.get("source_url", "")
        effective_date = scheme.get("effective_date")
        last_verified = scheme.get("last_verified")

        base_metadata = {
            "scheme_id": scheme_id,
            "title": title,
            "category": category,
            "jurisdiction": jurisdiction,
            "country": country,
            "jurisdiction_level": jurisdiction_level,
            "region": region,
            "issuing_authority": issuing_authority,
            "source_url": source_url,
            "effective_date": effective_date,
            "last_verified": last_verified,
        }

        # 1. Section: OVERVIEW
        if scheme.get("summary"):
            chunks.append({
                "chunk_id": f"chk-{scheme_id}-overview",
                "scheme_id": scheme_id,
                "section_type": "OVERVIEW",
                "content": f"Program Overview for {title}: {scheme['summary']}",
                "metadata": {**base_metadata, "section_type": "OVERVIEW"}
            })

        # 2. Section: BENEFITS
        if scheme.get("description"):
            chunks.append({
                "chunk_id": f"chk-{scheme_id}-benefits",
                "scheme_id": scheme_id,
                "section_type": "BENEFITS",
                "content": f"Program Benefits and Details for {title}: {scheme['description']}",
                "metadata": {**base_metadata, "section_type": "BENEFITS"}
            })

        # 3. Section: ELIGIBILITY
        if scheme.get("eligibility_rules"):
            rules_str = ", ".join([f"{k}: {v}" for k, v in scheme["eligibility_rules"].items()])
            chunks.append({
                "chunk_id": f"chk-{scheme_id}-eligibility",
                "scheme_id": scheme_id,
                "section_type": "ELIGIBILITY",
                "content": f"Eligibility Criteria for {title}: Criteria requirements include {rules_str}.",
                "metadata": {**base_metadata, "section_type": "ELIGIBILITY"}
            })

        # 4. Section: DOCUMENTS
        if scheme.get("document_requirements"):
            doc_names = [d.get("document_name", "") for d in scheme["document_requirements"] if d.get("document_name")]
            doc_str = "; ".join(doc_names)
            chunks.append({
                "chunk_id": f"chk-{scheme_id}-documents",
                "scheme_id": scheme_id,
                "section_type": "DOCUMENTS",
                "content": f"Required Documentation Checklist for {title}: Mandatory documents include {doc_str}.",
                "metadata": {**base_metadata, "section_type": "DOCUMENTS"}
            })

        # 5. Section: SOURCE
        chunks.append({
            "chunk_id": f"chk-{scheme_id}-source",
            "scheme_id": scheme_id,
            "section_type": "SOURCE",
            "content": f"Issuing Authority and Verification Source for {title}: Published by {issuing_authority}. Direct Portal: {source_url}.",
            "metadata": {**base_metadata, "section_type": "SOURCE"}
        })

        return chunks
