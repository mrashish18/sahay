import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class SchemeDB(Base):
    __tablename__ = "schemes"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    eligibility_rules: Mapped[dict] = mapped_column(JSON, default=dict)
    document_requirements: Mapped[dict] = mapped_column(JSON, default=list)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    effective_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_verified: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

class KnowledgeChunkDB(Base):
    __tablename__ = "knowledge_chunks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    scheme_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("schemes.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meta_data: Mapped[dict] = mapped_column(JSON, default=dict)
    # Embedding stored as serialized JSON list for compatibility before pgvector binding
    embedding_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class ToolRegistryDB(Base):
    __tablename__ = "tool_registry"
    
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    version: Mapped[str] = mapped_column(String(20), primary_key=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    input_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    permissions: Mapped[dict] = mapped_column(JSON, default=list)
    reliability_score: Mapped[float] = mapped_column(Float, default=1.0)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

class TTEProposalDB(Base):
    __tablename__ = "tte_proposals"
    
    proposal_id: Mapped[str] = mapped_column(String, primary_key=True)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    problem_context: Mapped[str] = mapped_column(Text, nullable=False)
    generated_code: Mapped[str] = mapped_column(Text, nullable=False)
    test_results: Mapped[dict] = mapped_column(JSON, default=dict)
    static_analysis_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    security_audit_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default="PROPOSED")

class ConversationDB(Base):
    __tablename__ = "conversations"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")

class MessageDB(Base):
    __tablename__ = "messages"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(String, ForeignKey("conversations.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
