from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import csv
import io

from app.db.session import get_db
from app.db.models import TimeSeries
from app.db.schemas import TSPointIn, IngestBatch

router = APIRouter()


@router.post("/metrics")
async def ingest_metrics(batch: IngestBatch, db: AsyncSession = Depends(get_db)):
    """Bulk insert time-series points."""
    count = 0
    for p in batch.points:
        row = TimeSeries(
            metric=p.metric,
            ts=p.ts,
            value=p.value,
            region=p.region,
            source=p.source or "api_upload",
        )
        db.add(row)
        count += 1
    await db.commit()
    return {"ingested": count}


@router.post("/csv")
async def ingest_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Upload CSV: metric,ts,value,region,source"""
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    count = 0
    for row in reader:
        ts_row = TimeSeries(
            metric=row["metric"],
            ts=datetime.fromisoformat(row["ts"]),
            value=float(row["value"]),
            region=row.get("region") or None,
            source=row.get("source") or "csv_upload",
        )
        db.add(ts_row)
        count += 1
    await db.commit()
    return {"ingested": count, "file": file.filename}


@router.get("/last")
async def last_ingested(db: AsyncSession = Depends(get_db)):
    """Show the most recent row per metric (for the ingest page)."""
    q = (
        select(TimeSeries.metric, TimeSeries.ts, TimeSeries.source)
        .order_by(TimeSeries.ts.desc())
        .limit(10)
    )
    # Use a raw approach for simplicity
    from sqlalchemy import text
    raw = await db.execute(
        text("""
            SELECT DISTINCT ON (metric) metric, ts, source
            FROM ts_metrics
            ORDER BY metric, ts DESC
            LIMIT 20
        """)
    )
    rows = raw.fetchall()
    return [{"metric": r[0], "ts": str(r[1]), "source": r[2]} for r in rows]