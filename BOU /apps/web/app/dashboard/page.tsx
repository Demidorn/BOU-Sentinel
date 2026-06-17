"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getSocket } from "@/lib/socket";
import type { DashboardSummary, Alert, Forecast, TSPoint } from "@/lib/types";
import KPICard from "@/components/KPICard";
import ForecastChart from "@/components/ForecastChart";
import AlertsFeed from "@/components/AlertsFeed";
import AlertDrawer from "@/components/AlertDrawer";
import TrendChart from "@/components/TrendChart";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [forecast, setForecast] = useState<Forecast | null>(null);
  const [fxSeries, setFxSeries] = useState<TSPoint[]>([]);
  const [ipiSeries, setIpiSeries] = useState<TSPoint[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [loading, setLoading] = useState(true);

  // Initial fetch for dashboard data
  useEffect(() => {
    async function load() {
      try {
        const [s, a, f, fx, ipi] = await Promise.all([
          api.summary(),
          api.alerts(),
          api.forecast(30),
          api.timeseries("fx_usd_ugx", 60),
          api.timeseries("inflation_pressure_index", 60),
        ]);
        setSummary(s);
        setAlerts(a);
        setForecast(f);
        setFxSeries(fx);
        setIpiSeries(ipi);
      } catch (err) {
        console.error("Failed to load dashboard:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Real-time alerts via Socket.IO 
  useEffect(() => {
    const socket = getSocket();
    socket.on("alert:new", (data: Alert) => {
      setAlerts((prev) => [data, ...prev]);
      setSummary((prev) =>
        prev ? { ...prev, open_alerts_count: prev.open_alerts_count + 1 } : prev
      );
    });
    return () => { socket.off("alert:new"); };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[80vh]">
        <div className="text-center">
          <div className="text-4xl mb-4 animate-pulse">🛡️</div>
          <p className="text-slate-400">Loading BOU Sentinel...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Command Center</h1>
          <p className="text-sm text-slate-400">
            Last updated: {summary?.last_updated ? new Date(summary.last_updated).toLocaleString() : "N/A"}
          </p>
        </div>
        <div className="flex items-center gap-2 bg-bou-card px-4 py-2 rounded-lg border border-bou-border">
          <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          <span className="text-sm text-slate-300">Live Monitoring</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="USD/UGX Rate"
          value={summary?.fx_rate?.toLocaleString() || "N/A"}
          change={summary?.fx_change_7d}
          changeLabel="7d change"
          icon="💱"
        />
        <KPICard
          title="Inflation Pressure Index"
          value={summary?.inflation_pressure_index?.toFixed(1) || "N/A"}
          trend={summary?.ipi_trend}
          changeLabel="trend"
          icon="📈"
          trendColor={summary?.ipi_trend === "rising" ? "text-red-400" : summary?.ipi_trend === "falling" ? "text-emerald-400" : "text-slate-400"}
        />
        <KPICard
          title="30-Day Forecast"
          value={summary?.forecast_direction === "up" ? "▲ Rising" : summary?.forecast_direction === "down" ? "▼ Falling" : "● Flat"}
          change={summary?.forecast_change_pct}
          changeLabel="projected"
          icon="🔮"
        />
        <KPICard
          title="Open Alerts"
          value={String(summary?.open_alerts_count || 0)}
          icon="🚨"
          valueColor={summary?.open_alerts_count && summary.open_alerts_count > 0 ? "text-red-400" : "text-emerald-400"}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-bou-card rounded-xl border border-bou-border p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Inflation Pressure Forecast (30d)</h2>
          {forecast ? (
            <ForecastChart forecast={forecast} />
          ) : (
            <p className="text-slate-500 text-sm">No forecast available</p>
          )}
        </div>
        <div className="bg-bou-card rounded-xl border border-bou-border p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">USD/UGX Trend (60d)</h2>
          <TrendChart data={fxSeries} color="#D4AF37" label="USD/UGX" />
        </div>
      </div>

      {/* IPI Trend + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-bou-card rounded-xl border border-bou-border p-5 lg:col-span-1">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Inflation Pressure Trend</h2>
          <TrendChart data={ipiSeries} color="#C41E3A" label="IPI" />
        </div>
        <div className="bg-bou-card rounded-xl border border-bou-border p-5 lg:col-span-2">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Live Alerts Feed</h2>
          <AlertsFeed alerts={alerts} onSelect={setSelectedAlert} />
        </div>
      </div>

      {/* Alert Detail Drawer */}
      {selectedAlert && (
        <AlertDrawer alert={selectedAlert} onClose={() => setSelectedAlert(null)} />
      )}
    </div>
  );
}