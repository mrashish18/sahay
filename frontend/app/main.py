from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.v1.endpoints import health, chat, tools, services

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None,
    openapi_url=None,
    redoc_url=None,
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

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/docs", include_in_schema=False)
@app.get("/api/docs", include_in_schema=False)
@app.get("/api/v1/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - Swagger UI"
    )

@app.get("/redoc", include_in_schema=False)
@app.get("/api/redoc", include_in_schema=False)
@app.get("/api/v1/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - ReDoc"
    )

@app.get("/openapi.json", include_in_schema=False)
@app.get("/api/openapi.json", include_in_schema=False)
@app.get("/api/v1/openapi.json", include_in_schema=False)
async def custom_openapi():
    return JSONResponse(app.openapi())

@app.get("/")
@app.get("/api")
async def root():
    return {
        "message": "Welcome to Sahay Backend API",
        "health": "/api/health",
        "docs": "/api/docs",
        "openapi": "/api/openapi.json",
        "redoc": "/api/redoc"
    }
