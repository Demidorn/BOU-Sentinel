"""
Real-time data ingestion from external APIs.
Run via Celery tasks on schedule.
"""
import httpx
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.db.models import TimeSeries
from app.core.config import settings


async def fetch_fx_rates() -> dict:
    """Fetch USD/UGX from OpenExchangeRates (or fallback)."""
    try:
        url = (
            f"https://openexchangerates.org/api/latest.json"
            f"?app_id={settings.OPENEXCHANGERATES_APP_ID}"
            f"&symbols=UGX"
        )
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            rate = data["rates"]["UGX"]
            return {"usd_ugx": rate}
    except Exception as e:
        print(f"⚠️  FX fetch failed ({e}), using fallback rate")
        return {"usd_ugx": 3750.0}


async def fetch_weather_kampala() -> dict:
    """Fetch temperature + rainfall for Kampala as weather proxy."""
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q=Kampala,UG"
            f"&appid={settings.OPENWEATHERMAP_API_KEY}"
            f"&units=metric"
        )
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "rain": data.get("rain", {}).get("1h", 0),
            }
    except Exception:
        print("⚠️  Weather fetch failed, using defaults")
        return {"temp": 25.0, "humidity": 60.0, "rain": 0.0}


async def ingest_single_point(metric: str, value: float, source: str, region: str = None):
    """Insert one data point into DB."""
    async with async_session() as db:
        row = TimeSeries(
            metric=metric,
            ts=datetime.now(timezone.utc),
            value=value,
            source=source,
            region=region,
        )
        db.add(row)
        await db.commit()


async def run_all_ingestors():
    """Main entry point called by Celery beat."""
    now = datetime.now(timezone.utc)

    # 1. FX
    fx = await fetch_fx_rates()
    await ingest_single_point("fx_usd_ugx", fx["usd_ugx"], "openexchangerates")

    # 2. Weather
    weather = await fetch_weather_kampala()
    await ingest_single_point("weather_temp_kampala", weather["temp"], "openweathermap")
    await ingest_single_point("weather_humidity_kampala", weather["humidity"], "openweathermap")
    await ingest_single_point("weather_rainfall_kampala", weather["rain"], "openweathermap")
    # 3. Synthetic commodities (MVP: generated locally)
    import random
    commodities = {
        "commodity_maize": round(3500 + random.gauss(0, 200), 0),    # UGX/kg
        "commodity_beans": round(5000 + random.gauss(0, 300), 0),    # UGX/kg
        "commodity_coffee": round(12000 + random.gauss(0, 500), 0),  # UGX/kg
        "fuel_petrol": round(5200 + random.gauss(0, 100), 0),        # UGX/L
    }
    for metric, val in commodities.items():
        await ingest_single_point(metric, val, "synthetic_daily")

    # 4. Synthetic bank aggregates
    import random
    bank_aggs = {
        "agg_total_deposits": round(45_000_000_000 + random.gauss(0, 500_000_000), 0),
        "agg_total_withdrawals": round(38_000_000_000 + random.gauss(0, 400_000_000), 0),
        "agg_total_transfers": round(22_000_000_000 + random.gauss(0, 300_000_000), 0),
        "agg_forex_demand": round(800_000_000 + random.gauss(0, 50_000_000), 0),
        "agg_crossborder_outflow": round(250_000_000 + random.gauss(0, 20_000_000), 0),
    }
    for metric, val in bank_aggs.items():
        await ingest_single_point(metric, val, "bank_aggregates")

    print(f"✅ Ingestion complete at {now.isoformat()}")