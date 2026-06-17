"use client";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from "recharts";
import type { Forecast } from "@/lib/types";

export default function ForecastChart({ forecast }: { forecast: Forecast }) {
  const data = forecast.points.map((p) => ({
    date: new Date(p.ts).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    forecast: p.yhat,
    upper: p.yhat_upper,
    lower: p.yhat_lower,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
        <defs>
          <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#C41E3A" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#C41E3A" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorBand" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#C41E3A" stopOpacity={0.1} />
            <stop offset="95%" stopColor="#C41E3A" stopOpacity={0.02} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis dataKey="date" tick={{ fill: "#94a3b8", fontSize: 10 }} interval="preserveStartEnd" />
        <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} domain={["dataMin - 5", "dataMax + 5"]} />
        <Tooltip
          contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: "8px" }}
          labelStyle={{ color: "#94a3b8" }}
        />
        <ReferenceLine y={50} stroke="#475569" strokeDasharray="3 3" label={{ value: "baseline", fill: "#475569", fontSize: 10 }} />
        <Area type="monotone" dataKey="upper" stroke="none" fill="url(#colorBand)" />
        <Area type="monotone" dataKey="lower" stroke="none" fill="#0F172A" />
        <Area
          type="monotone" dataKey="forecast"
          stroke="#C41E3A" strokeWidth={2}
          fill="url(#colorForecast)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}