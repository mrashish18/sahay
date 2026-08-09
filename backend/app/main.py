from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.endpoints import health, chat, tools, services

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Sahay — Public-Service & Crisis Assistance Navigator Backend"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routes
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat"])
app.include_router(tools.router, prefix=settings.API_V1_STR, tags=["Tools & TTE"])
app.include_router(services.router, prefix=settings.API_V1_STR, tags=["Services & Schemes"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Sahay Backend API",
        "health": "/health",
        "docs": "/docs"
    }
