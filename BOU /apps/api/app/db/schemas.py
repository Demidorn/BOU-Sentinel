from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


# ── Time Series ──────────────────────────────────────
class TSPointIn(BaseModel):
    metric: str
    ts: datetime
    value: float
    region: Optional[str] = None
    source: Optional[str] = None


class TSPointOut(BaseModel):
    id: UUID
    metric: str
    ts: datetime
    value: float
    region: Optional[str]
    source: Optional[str]

    class Config:
        from_attributes = True


# ── Alerts ───────────────────────────────────────────
class AlertOut(BaseModel):
    id: UUID
    created_at: datetime
    type: str
    severity: int
    title: str
    description: Optional[str]
    region: Optional[str]
    evidence: Optional[Any]
    status: str

    class Config:
        from_attributes = True


# ── Forecasts ────────────────────────────────────────
class ForecastPoint(BaseModel):
    ts: str
    yhat: float
    yhat_lower: float
    yhat_upper: float


class ForecastOut(BaseModel):
    id: UUID
    metric: str
    horizon_days: int
    generated_at: datetime
    points: List[ForecastPoint]
    model_version: str
    metrics: Optional[Any]

    class Config:
        from_attributes = True


# ── Dashboard ────────────────────────────────────────
class DashboardSummary(BaseModel):
    fx_rate: Optional[float] = None
    fx_change_7d: Optional[float] = None
    inflation_pressure_index: Optional[float] = None
    ipi_trend: Optional[str] = None          # "rising" | "falling" | "stable"
    forecast_direction: Optional[str] = None  # "up" | "down" | "flat"
    forecast_change_pct: Optional[float] = None
    open_alerts_count: int = 0
    last_updated: Optional[datetime] = None


class StressMapRegion(BaseModel):
    region: str
    score: float
    top_driver: str


# ── Ingestion ────────────────────────────────────────
class IngestBatch(BaseModel):
    points: List[TSPointIn]


class BankAggregateUpload(BaseModel):
    """Expected shape from CSV upload."""
    date: str
    metric: str
    value: float
    region: Optional[str] = None