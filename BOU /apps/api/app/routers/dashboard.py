from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta
from typing import Optional

from app.db.session import get_db
from app.db.models import TimeSeries, Alert, Forecast
from app.db.schemas import DashboardSummary, ForecastOut, StressMapRegion

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(db: AsyncSession = Depends(get_db)):
    """Single endpoint that powers all KPI tiles."""

    # Latest FX rate
    fx_q = (
        select(TimeSeries)
        .where(TimeSeries.metric == "fx_usd_ugx")
        .order_by(desc(TimeSeries.ts))
        .limit(1)
    )
    fx_result = await db.execute(fx_q)
    fx_latest = fx_result.scalar_one_or_none()

    # FX 7 days ago
    fx_7d_q = (
        select(TimeSeries)
        .where(TimeSeries.metric == "fx_usd_ugx")
        .where(TimeSeries.ts <= func.now() - timedelta(days=7))
        .order_by(desc(TimeSeries.ts))
        .limit(1)
    )
    fx_7d_result = await db.execute(fx_7d_q)
    fx_7d = fx_7d_result.scalar_one_or_none()

    # Latest IPI
    ipi_q = (
        select(TimeSeries)
        .where(TimeSeries.metric == "inflation_pressure_index")
        .order_by(desc(TimeSeries.ts))
        .limit(1)
    )
    ipi_result = await db.execute(ipi_q)
    ipi_latest = ipi_result.scalar_one_or_none()

    # IPI 7 days ago for trend
    ipi_7d_q = (
        select(TimeSeries)
        .where(TimeSeries.metric == "inflation_pressure_index")
        .where(TimeSeries.ts <= func.now() - timedelta(days=7))
        .order_by(desc(TimeSeries.ts))
        .limit(1)
    )
    ipi_7d_result = await db.execute(ipi_7d_q)
    ipi_7d = ipi_7d_result.scalar_one_or_none()

    # Open alerts count
    alerts_q = select(func.count(Alert.id)).where(Alert.status == "open")
    alerts_result = await db.execute(alerts_q)
    open_count = alerts_result.scalar() or 0

    # Latest forecast
    fc_q = (
        select(Forecast)
        .where(Forecast.metric == "inflation_pressure_index")
        .where(Forecast.horizon_days == 30)
        .order_by(desc(Forecast.generated_at))
        .limit(1)
    )
    fc_result = await db.execute(fc_q)
    fc_latest = fc_result.scalar_one_or_none()

    # Compute values
    fx_val = fx_latest.value if fx_latest else None
    fx_change = None
    if fx_latest and fx_7d:
        fx_change = round(((fx_latest.value - fx_7d.value) / fx_7d.value) * 100, 2)

    ipi_val = round(ipi_latest.value, 2) if ipi_latest else None
    ipi_trend = "stable"
    if ipi_latest and ipi_7d:
        diff = ipi_latest.value - ipi_7d.value
        ipi_trend = "rising" if diff > 0.5 else ("falling" if diff < -0.5 else "stable")

    forecast_dir = "flat"
    fc_change = None
    if fc_latest and fc_latest.points and ipi_val:
        first_pt = fc_latest.points[0]["yhat"]
        last_pt = fc_latest.points[-1]["yhat"]
        fc_change = round(((last_pt - first_pt) / first_pt) * 100, 2) if first_pt != 0 else 0
        forecast_dir = "up" if fc_change > 1 else ("down" if fc_change < -1 else "flat")

    return DashboardSummary(
        fx_rate=fx_val,
        fx_change_7d=fx_change,
        inflation_pressure_index=ipi_val,
        ipi_trend=ipi_trend,
        forecast_direction=forecast_dir,
        forecast_change_pct=fc_change,
        open_alerts_count=open_count,
        last_updated=fx_latest.ts if fx_latest else datetime.utcnow(),
    )


@router.get("/forecast", response_model=ForecastOut)
async def get_forecast(
    horizon: int = Query(30, ge=30, le=90),
    db: AsyncSession = Depends(get_db),
):
    """Latest forecast for a given horizon."""
    q = (
        select(Forecast)
        .where(Forecast.metric == "inflation_pressure_index")
        .where(Forecast.horizon_days == horizon)
        .order_by(desc(Forecast.generated_at))
        .limit(1)
    )
    result = await db.execute(q)
    fc = result.scalar_one_or_none()
    if not fc:
        return {"error": "No forecast available yet. Run the forecasting job."}
    return fc


@router.get("/stress-map", response_model=list[StressMapRegion])
async def get_stress_map(
    date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Latest stress scores per region for the choropleth."""
    regions = ["Central", "Eastern", "Northern", "Western"]
    results = []
    for region in regions:
        q = (
            select(TimeSeries)
            .where(TimeSeries.metric == "stress_score")
            .where(TimeSeries.region == region)
            .order_by(desc(TimeSeries.ts))
            .limit(1)
        )
        r = await db.execute(q)
        row = r.scalar_one_or_none()
        score = round(row.value, 2) if row else 0.0
        top_driver = "fx_pressure" if score > 60 else "commodity_prices" if score > 40 else "stable"
        results.append(StressMapRegion(region=region, score=score, top_driver=top_driver))
    return results


@router.get("/ts/{metric}")
async def get_timeseries(
    metric: str,
    days: int = Query(90, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """Raw time series for charts."""
    q = (
        select(TimeSeries)
        .where(TimeSeries.metric == metric)
        .where(TimeSeries.ts >= func.now() - timedelta(days=days))
        .order_by(TimeSeries.ts)
    )
    result = await db.execute(q)
    rows = result.scalars().all()
    return [{"ts": str(r.ts), "value": r.value, "region": r.region} for r in rows]