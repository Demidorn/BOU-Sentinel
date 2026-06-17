import socketio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import create_tables
from app.routers import dashboard, alerts, ingest, health
from app.realtime.socketio_server import sio

# ── Lifespan ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

# ── FastAPI ──────────────────────────────────────────
app = FastAPI(
    title="BOU Sentinel API",
    description="AI-Powered National Economic Early Warning System",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────
app.include_router(health.router,  prefix="/v1", tags=["health"])
app.include_router(dashboard.router, prefix="/v1/dashboard", tags=["dashboard"])
app.include_router(alerts.router,    prefix="/v1/alerts", tags=["alerts"])
app.include_router(ingest.router,    prefix="/v1/ingest", tags=["ingest"])

# ── Socket.IO (ASGI) ────────────────────────────────
# socket_app = socketio.ASGIApp(sio, other_app=app)
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)