"""
Inflation Pressure Index computation + Prophet forecasting.
"""
import json
from datetime import datetime, timezone
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import async_session


async def compute_inflation_pressure_index():
    """
    Compute IPI from ingested signals:
    IPI = weighted composite of normalized sub-indices.
    Store as a new time-series point.
    """
    async with async_session() as db:
        # Pull last 30 days of each component
        query = text("""
            SELECT metric, ts, value FROM ts_metrics
            WHERE ts >= NOW() - INTERVAL '30 days'
            ORDER BY ts
        """)
        result = await db.execute(query)
        rows = result.fetchall()

        if not rows:
            print("⚠️  No data to compute IPI")
            return

        df = pd.DataFrame(rows, columns=["metric", "ts", "value"])

        # Pivot: one column per metric
        pivot = df.pivot_table(index="ts", columns="metric", values="value", aggfunc="last")
        pivot = pivot.sort_index().ffill()

        # Compute daily returns for each metric
        returns = pivot.pct_change().dropna()

        if returns.empty:
            # Not enough data yet — just compute a simple average of latest values
            latest = pivot.iloc[-1] if not pivot.empty else pd.Series()
            ipi = 50.0  # neutral baseline
        else:
            # Weights (can be tuned)
            weights = {
                "fx_usd_ugx": 0.25,
                "commodity_maize": 0.20,
                "commodity_beans": 0.15,
                "commodity_coffee": 0.10,
                "fuel_petrol": 0.20,
                "weather_temp_kampala": 0.10,
            }

            # Normalize returns to 0-100 scale
            # Higher return = more inflationary pressure
            weighted = pd.Series(dtype=float)
            total_weight = 0
            for metric, w in weights.items():
                if metric in returns.columns:
                    col = returns[metric].dropna()
                    if len(col) > 0:
                        # Recent 7-day average return
                        recent = col.tail(7).mean()
                        # Map to 0-100: negative return = low pressure, positive = high
                        # IPI = 50 + (recent * 1000) scaled and clamped
                        score = 50 + (recent * 500)
                        score = max(0, min(100, score))
                        weighted[metric] = score * w
                        total_weight += w

            if total_weight > 0:
                ipi = weighted.sum() / total_weight * (100 / total_weight)
                ipi = max(0, min(100, ipi))
            else:
                ipi = 50.0

        # Store the computed IPI
        row = {
            "metric": "inflation_pressure_index",
            "ts": datetime.now(timezone.utc),
            "value": round(float(ipi), 2),
            "source": "ipi_compute",
            "region": None,
        }
        await db.execute(
            text("""
                INSERT INTO ts_metrics (metric, ts, value, source, region)
                VALUES (:metric, :ts, :value, :source, :region)
            """),
            row,
        )
        await db.commit()
        print(f"✅ IPI computed: {round(float(ipi), 2)}")


async def run_prophet_forecast():
    """
    Train Prophet on the IPI series and generate 30-day forecast.
    Save to forecasts table.
    """
    try:
        from prophet import Prophet
    except ImportError:
        print("⚠️  Prophet not installed — skipping forecast")
        return

    async with async_session() as db:
        query = text("""
            SELECT ts, value FROM ts_metrics
            WHERE metric = 'inflation_pressure_index'
            ORDER BY ts ASC
        """)
        result = await db.execute(query)
        rows = result.fetchall()

        if len(rows) < 10:
            print("⚠️  Not enough IPI data points for forecast (need >= 10)")
            return

        df = pd.DataFrame(rows, columns=["ds", "y"])
        df["ds"] = pd.to_datetime(df["ds"])
        df = df.dropna()

        # Train Prophet
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            interval_width=0.90,
        )
        model.fit(df)

        # Predict 30 days ahead
        future = model.make_future_dataframe(periods=30, freq="D")
        forecast = model.predict(future)

        # Take only the future portion
        future_fc = forecast[forecast["ds"] > df["ds"].max()].copy()

        # Build points
        points = []
        for _, row in future_fc.iterrows():
            points.append({
                "ts": row["ds"].isoformat(),
                "yhat": round(float(row["yhat"]), 2),
                "yhat_lower": round(float(row["yhat_lower"]), 2),
                "yhat_upper": round(float(row["yhat_upper"]), 2),
            })

        # Compute simple MAPE on training data
        merged = df.merge(forecast[["ds", "yhat"]], on="ds", how="inner")
        mape = round(float((abs(merged["y"] - merged["yhat"]) / merged["y"]).mean() * 100), 2)

        # Save
        await db.execute(
            text("""
                INSERT INTO forecasts (metric, horizon_days, points, model_version, metrics)
                VALUES (:metric, :horizon, :points, :version, :metrics)
            """),
            {
                "metric": "inflation_pressure_index",
                "horizon": 30,
                "points": json.dumps(points),
                "version": "1.0",
                "metrics": json.dumps({"mape": mape}),
            },
        )
        await db.commit()
        print(f"✅ Forecast generated: {len(points)} points, MAPE={mape}%")