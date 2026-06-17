export interface DashboardSummary {
  fx_rate: number | null;
  fx_change_7d: number | null;
  inflation_pressure_index: number | null;
  ipi_trend: string | null;
  forecast_direction: string | null;
  forecast_change_pct: number | null;
  open_alerts_count: number;
  last_updated: string | null;
}

export interface Alert {
  id: string;
  created_at: string;
  type: string;
  severity: number;
  title: string;
  description: string | null;
  region: string | null;
  evidence: Record<string, unknown> | null;
  status: string;
}

export interface ForecastPoint {
  ts: string;
  yhat: number;
  yhat_lower: number;
  yhat_upper: number;
}

export interface Forecast {
  id: string;
  metric: string;
  horizon_days: number;
  generated_at: string;
  points: ForecastPoint[];
  model_version: string;
  metrics: { mape?: number } | null;
}

export interface StressRegion {
  region: string;
  score: number;
  top_driver: string;
}

export interface TSPoint {
  ts: string;
  value: number;
  region: string | null;
}
