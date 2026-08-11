import sys
from pathlib import Path

# Paths for both Vercel Serverless Function (frontend/ root) and local dev (Sahay/ root)
FRONTEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = FRONTEND_DIR.parent
BACKEND_DIR = ROOT_DIR / "backend"

if (FRONTEND_DIR / "app").exists() and str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))
if BACKEND_DIR.exists() and str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app as fastapi_app

async def app(scope, receive, send):
    await fastapi_app(scope, receive, send)
