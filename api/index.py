import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.main import app as fastapi_app
except ImportError:
    from backend.app.main import app as fastapi_app

async def app(scope, receive, send):
    await fastapi_app(scope, receive, send)