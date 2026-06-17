import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Text, JSON, Boolean, Index, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column


class TimeSeries(Base):
    """All numeric time-series data (FX, commodities, aggregates, indices)."""
    __tablename__ = "ts_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    metric = Column(String(128), nullable=False, index=True)
    ts = Column(DateTime(timezone=True), nullable=False, index=True)
    value = Column(Float, nullable=False)
    region = Column(String(64), nullable=True, index=True)
    source = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_ts_metric_ts", "metric", "ts"),
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    type = Column(String(64), nullable=False, index=True)   # INFLATION_RISK, CAPITAL_FLIGHT, etc.
    severity = Column(Integer, default=3)                    # 1-5
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    region = Column(String(64), nullable=True)
    evidence = Column(JSON, nullable=True)
    status = Column(String(20), default="open")              # open | ack | closed


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric = Column(String(128), nullable=False, index=True)
    horizon_days = Column(Integer, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    points = Column(JSON, nullable=False)                    # [{ts, yhat, yhat_lower, yhat_upper}]
    model_version = Column(String(32), default="1.0")
    metrics = Column(JSON, nullable=True)                    # {mape, rmse, etc.}