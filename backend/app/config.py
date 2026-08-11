import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sahay Backend"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sahay-cyan.vercel.app",
        "*"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./sahayai_dev.db" # Default fallback for local testing without postgres container
    
    # Security & Auth
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    
    # AI & Tools
    LLM_PROVIDER: str = "mock"
    LLM_MODEL: str = "openai/gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:8b"
    EMBEDDING_PROVIDER: str = "mock"
    TTE_ALLOW_UNAPPROVED_EXECUTION: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
