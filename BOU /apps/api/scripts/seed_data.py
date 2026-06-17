"""
Seed historical data to make dashboard look populated on first load.
Run once: python /app/scripts/seed_data.py
"""
import sys, os, random
sys.path.insert(0, "/app")

from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from app.db.session import engine, async_session


async def seed():
    """Generate 90 days of historical data for all metrics."""
    now = datetime.now(timezone.utc)
    days = 90

    async with engine.begin() as conn:
        # Ensure tables exist
        from app.db.session import Base
        from app.db.models import TimeSeries, Alert, Forecast
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Check if already seeded
        result = await db.execute(text("SELECT COUNT(*) FROM ts_metrics"))
        count = result.scalar()
        if count > 100:
            print(f"ℹ️  Database already has {count} rows — skipping seed")
            return

        print("🌱 Seeding historical data...")

        # Generate base curves with realistic trends
        base_fx = 3700
        base_maize = 3500
        base_beans = 5000
        base_coffee = 12000
        base_fuel = 5100
        base_temp = 25

        for d in range(days):
            ts = now - timedelta(days=days - d)
            trend = d / days  # 0 to 1

            # FX: gradual depreciation with noise
            fx = base_fx + trend * 150 + random.gauss(0, 30)
            # Add a "shock" around day 60-70
            if 60 <= d <= 70:
                fx += 120

            # Commodities: seasonal pattern + noise
            seasonal = 200 * (1 if 30 <= d <= 50 else -1 if 70 <= d <= 85 else 0)
            maize = base_maize + seasonal + random.gauss(0, 100)
            beans = base_beans + seasonal * 0.8 + random.gauss(0, 150)
            coffee = base_coffee + trend * 500 + random.gauss(0, 300)

            # Fuel: step change around day 40
            fuel = base_fuel + (200 if d > 40 else 0) + random.gauss(0, 50)

            # Weather
            temp = base_temp + 3 * (1 if d % 30 < 15 else -1) + random.gauss(0, 2)
            humidity = 60 + 10 * (1 if d % 30 < 15 else -1) + random.gauss(0, 5)

            # Bank aggregates
            deposits = 45e9 + trend * 2e9 + random.gauss(0, 500e6)
            withdrawals = 38e9 + trend * 3e9 + random.gauss(0, 400e6)  # growing faster = stress
            transfers = 22e9 + random.gauss(0, 300e6)
            forex_demand = 800e6 + trend * 200e6 + random.gauss(0, 50e6)
            outflow = 250e6 + trend * 100e6 + random.gauss(0, 20e6)

            points = [
                ("fx_usd_ugx", fx, "seed", None),
                ("commodity_maize", maize, "seed", None),
                ("commodity_beans", beans, "seed", None),
                ("commodity_coffee", coffee, "seed", None),
                ("fuel_petrol", fuel, "seed", None),
                ("weather_temp_kampala", temp, "seed", "Central"),
                ("weather_humidity_kampala", humidity, "seed", "Central"),
                ("agg_total_deposits", deposits, "seed", None),
                ("agg_total_withdrawals", withdrawals, "seed", None),
                ("agg_total_transfers", transfers, "seed", None),
                ("agg_forex_demand", forex_demand, "seed", None),
                ("agg_crossborder_outflow", outflow, "seed", None),
            ]

            for metric, value, source, region in points:
                await db.execute(
                    text("""
                        INSERT INTO ts_metrics (metric, ts, value, source, region)
                        VALUES (:metric, :ts, :value, :source, :region)
                    """),
                    {"metric": metric, "ts": ts, "value": round(value, 2), "source": source, "region": region},
                )

        # Add regional stress scores for the last 30 days
        regions = ["Central", "Eastern", "Northern", "Western"]
        for d in range(30):
            ts = now - timedelta(days=30 - d)
            for region in regions:
                base = {"Central": 55, "Eastern": 40, "Northern": 45, "Western": 35}[region]
                score = base + random.gauss(0, 8) + (10 if 10 <= d <= 20 else 0)
                score = max(0, min(100, score))
                await db.execute(
                    text("""
                        INSERT INTO ts_metrics (metric, ts, value, source, region)
                        VALUES ('stress_score', :ts, :value, 'seed', :region)
                    """),
                    {"ts": ts, "value": round(score, 2), "region": region},
                )

        # Add sample alerts
        alert_samples = [
            ("FX_PRESSURE", 3, "UGX depreciated sharply — USD/UGX at 3890", "Z-score: 2.3, rolling mean: 3750", None, {"fx_rate": 3890, "z_score": 2.3}),
            ("LIQUIDITY_STRESS", 3, "Liquidity stress: withdrawals exceed deposits (ratio 1.15)", "Deposits: 46.2B, Withdrawals: 53.1B", None, {"ratio": 1.15}),
            ("INFLATION_RISK", 4, "Maize spiked: 4,200 UGX/kg", "Z-score: 2.8, mean: 3,500", None, {"value": 4200, "z_score": 2.8}),
            ("CAPITAL_FLIGHT", 3, "Capital flight risk: cross-border outflows elevated", "Outflow Z-score: 2.1", None, {"z_score": 2.1}),
            ("FX_PRESSURE", 2, "Minor FX volatility detected", "Within normal range but trending", None, {}),
        ]

        for type_, sev, title, desc, region, evidence in alert_samples:
            await db.execute(
                text("""
                    INSERT INTO alerts (id, type, severity, title, description, region, evidence, status)
                    VALUES (gen_random_uuid(), :type, :sev, :title, :desc, :region, :evidence, 'open')
                """),
                {"type": type_, "sev": sev, "title": title, "desc": desc, "region": region, "evidence": json.dumps(evidence)},
            )

        await db.commit()
        print(f"✅ Seeded {days} days of data + 5 alerts")


import json

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())