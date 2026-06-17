import socketio
from app.core.config import settings

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.cors_origin_list,
    logger=False,
    engineio_logger=False,
)

@sio.event
async def connect(sid, environ):
    print(f"🔌 Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"🔌 Client disconnected: {sid}")

async def emit_alert(alert_data: dict):
    """Push new alert to all connected dashboard clients."""
    await sio.emit("alert:new", alert_data, namespace="/")