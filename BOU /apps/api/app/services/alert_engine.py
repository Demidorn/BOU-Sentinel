"""
Rule-based + statistical alert generation.
Runs on schedule via Celery.
"""
import json
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import async_session
from app.db.models import Alert
from app.realtime.socketio_server import emit_alert


async def _get_latest(metric: str, hours: int = 168) -> float | None:
    """Get latest value for a metric within given hours."""
    async with async_session() as db:
        result = await db.execute(
            text("""
                SELECT value FROM ts_metrics
                WHERE metric = :metric AND ts >= NOW() - (:hours || ' hours')::interval
                ORDER BY ts DESC LIMIT 1
            """),
            {"metric": metric, "hours": hours},
        )
        row = result.first()
        return row[0] if row else None


async def _get_rolling_stats(metric: str, days: int = 7):
    """Get mean and std of a metric over N days."""
    async with async_session() as db:
        result = await db.execute(
            text("""
                SELECT AVG(value), STDDEV(value) FROM ts_metrics
                WHERE metric = :metric AND ts >= NOW() - (:days || ' days')::interval
            """),
            {"metric": metric, "days": days},
        )
        row = result.first()
        return {"mean": row[0], "std": row[1]} if row[0] else {"mean": 0, "std": 1}


async def _create_alert(db: AsyncSession, **kwargs) -> Alert:
    """Create alert + emit via Socket.IO."""
    alert = Alert(**kwargs)
    db.add(alert)
    await db.flush()
    await db.commit()

    # Push to dashboard
    await emit_alert({
        "id": str(alert.id),
        "type": alert.type,
        "severity": alert.severity,
        "title": alert.title,
        "description": alert.description,
        "region": alert.region,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    })
    return alert


async def check_fx_pressure():
    """Alert if USD/UGX moves sharply."""
    fx = await _get_latest("fx_usd_ugx")
    stats = await _get_rolling_stats("fx_usd_ugx", days=30)

    if fx and stats["std"] and stats["std"] > 0:
        z_score = (fx - stats["mean"]) / stats["std"]
        if abs(z_score) > 2.0:
            severity = 4 if abs(z_score) > 3 else 3
            direction = "depreciated" if z_score > 0 else "appreciated"
            async with async_session() as db:
                await _create_alert(
                    db,
                    type="FX_PRESSURE",
                    severity=severity,
                    title=f"UGX {direction} sharply — USD/UGX at {fx:.0f}",
                    description=f"Z-score: {z_score:.2f}, rolling mean: {stats['mean']:.0f}",
                    region=None,
                    evidence={"fx_rate": fx, "z_score": round(z_score, 2), "mean": stats["mean"]},
                )
            print(f"🚨 FX alert: {direction} (z={z_score:.2f})")


async def check_liquidity_stress():
    """Alert if withdrawals spike relative to deposits."""
    deposits = await _get_latest("agg_total_deposits")
    withdrawals = await _get_latest("agg_total_withdrawals")

    if deposits and withdrawals and deposits > 0:
        ratio = withdrawals / deposits
        if ratio > 1.1:  # withdrawals exceed deposits by >10%
            async with async_session() as db:
                await _create_alert(
                    db,
                    type="LIQUIDITY_STRESS",
                    severity=4 if ratio > 1.3 else 3,
                    title=f"Liquidity stress: withdrawals exceed deposits (ratio {ratio:.2f})",
                    description=f"Deposits: {deposits/1e9:.1f}B, Withdrawals: {withdrawals/1e9:.1f}B",
                    region=None,
                    evidence={"deposits": deposits, "withdrawals": withdrawals, "ratio": round(ratio, 3)},
                )
            print(f"🚨 Liquidity alert: ratio={ratio:.2f}")


async def check_capital_flight():
    """Alert if cross-border outflows spike."""
    outflow = await _get_latest("agg_crossborder_outflow")
    stats = await _get_rolling_stats("agg_crossborder_outflow", days=14)

    if outflow and stats["std"] and stats["std"] > 0:
        z = (outflow - stats["mean"]) / stats["std"]
        if z > 2.0:
            async with async_session() as db:
                await _create_alert(
                    db,
                    type="CAPITAL_FLIGHT",
                    severity=4 if z > 3 else 3,
                    title=f"Capital flight risk: cross-border outflows elevated",
                    description=f"Outflow Z-score: {z:.2f}",
                    region=None,
                    evidence={"outflow": outflow, "z_score": round(z, 2), "mean": stats["mean"]},
                )
            print(f"🚨 Capital flight alert: z={z:.2f}")


async def check_commodity_shocks():
    """Alert on large commodity price moves."""
    for commodity in ["commodity_maize", "commodity_beans", "fuel_petrol"]:
        stats = await _get_rolling_stats(commodity, days=14)
        latest = await _get_latest(commodity)
        if latest and stats["mean"] and stats["std"] and stats["std"] > 0:
            z = (latest - stats["mean"]) / stats["std"]
            if abs(z) > 2.0:
                direction = "spiked" if z > 0 else "crashed"
                async with async_session() as db:
                    await _create_alert(
                        db,
                        type="INFLATION_RISK",
                        severity=3 if abs(z) < 3 else 4,
                        title=f"{commodity.replace('commodity_', '').replace('_', ' ').title()} {direction}: {latest:,.0f} UGX",
                        description=f"Z-score: {z:.2f}, mean: {stats['mean']:,.0f}",
                        region=None,
                        evidence={"metric": commodity, "value": latest, "z_score": round(z, 2)},
                    )
                print(f"🚨 Commodity alert: {commodity} {direction}")


async def run_all_alert_checks():
    """Run all alert rules. Called by Celery beat."""
    print("🔍 Running alert engine...")
    await check_fx_pressure()
    await check_liquidity_stress()
    await check_capital_flight()
    await check_commodity_shocks()
    print("✅ Alert engine complete")


async def compute_stress_scores():
    """Compute composite stress score for each region."""
    regions = ["Central", "Eastern", "Northern", "Western"]

    async with async_session() as db:
        # Get national-level signals (MVP: distribute with slight variations)
        latest_metrics = {}
        for metric in ["fx_usd_ugx", "commodity_maize", "fuel_petrol", "agg_total_withdrawals"]:
            result = await db.execute(
                text("""
                    SELECT value FROM ts_metrics
                    WHERE metric = :metric
                    ORDER BY ts DESC LIMIT 1
                """),
                {"metric": metric},
            )
            row = result.first()
            latest_metrics[metric] = row[0] if row else 0

        import random
        for region in regions:
            # Simple composite (MVP): weighted random-ish per region
            fx_component = min(100, max(0, (latest_metrics.get("fx_usd_ugx", 3750) - 3500) / 10))
            food_component = min(100, max(0, (latest_metrics.get("commodity_maize", 3500) - 3000) / 20))
            fuel_component = min(100, max(0, (latest_metrics.get("fuel_petrol", 5200) - 5000) / 5))
            liq_component = min(100, max(0, (latest_metrics.get("agg_total_withdrawals", 38e9) - 35e9) / 1e8))

            noise = random.gauss(0, 3)
            region_factor = {"Central": 1.1, "Eastern": 0.95, "Northern": 1.05, "Western": 0.9}.get(region, 1.0)
            score = (fx_component * 0.3 + food_component * 0.25 + fuel_component * 0.25 + liq_component * 0.2) * region_factor + noise
            score = max(0, min(100, round(score, 2)))

            await db.execute(
                text("""
                    INSERT INTO ts_metrics (metric, ts, value, source, region)
                    VALUES ('stress_score', NOW(), :value, 'stress_compute', :region)
                """),
                {"value": score, "region": region},
            )

        await db.commit()
        print("✅ Stress scores computed for all regions")