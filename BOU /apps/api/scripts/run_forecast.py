"""Manual forecast trigger for demo."""
import sys
sys.path.insert(0, "/app")

import asyncio
from app.services.forecasting import compute_inflation_pressure_index, run_prophet_forecast
from app.services.alert_engine import run_all_alert_checks, compute_stress_scores


async def main():
    print("📊 Computing IPI...")
    await compute_inflation_pressure_index()
    print("🔮 Running Prophet forecast...")
    await run_prophet_forecast()
    print("🚨 Running alert checks...")
    await run_all_alert_checks()
    print("🗺️  Computing stress scores...")
    await compute_stress_scores()
    print("\n✅ All jobs complete!")


if __name__ == "__main__":
    asyncio.run(main())