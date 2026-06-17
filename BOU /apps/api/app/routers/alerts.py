from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, desc
from typing import Optional

from app.db.session import get_db
from app.db.models import Alert
from app.db.schemas import AlertOut

router = APIRouter()


@router.get("/", response_model=list[AlertOut])
async def list_alerts(
    status: Optional[str] = Query("open"),
    alert_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    q = select(Alert)
    if status:
        q = q.where(Alert.status == status)
    if alert_type:
        q = q.where(Alert.type == alert_type)
    q = q.order_by(desc(Alert.created_at)).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.patch("/{alert_id}/ack")
async def ack_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    q = update(Alert).where(Alert.id == alert_id).values(status="ack")
    await db.execute(q)
    await db.commit()
    return {"status": "acknowledged"}


@router.patch("/{alert_id}/close")
async def close_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    q = update(Alert).where(Alert.id == alert_id).values(status="closed")
    await db.execute(q)
    await db.commit()
    return {"status": "closed"}