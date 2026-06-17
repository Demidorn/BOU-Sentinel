"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { TSPoint } from "@/lib/types";

export default function TrendChart({ data, color, label }: { data: TSPoint[]; color: string; label: string }) {
  const chartData = data.map((p) => ({
    date: new Date(p.ts).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    value: p.value,
  }));

  if (chartData.length === 0) {
    return <p className="text-slate-500 text-sm">No data available</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis dataKey="date" tick={{ fill: "#94a3b8", fontSize: 10 }} interval="preserveStartEnd" />
        <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} domain={["dataMin - 50", "dataMax + 50"]} />
        <Tooltip
          contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: "8px" }}
          labelStyle={{ color: "#94a3b8" }}
        />
        <Line
          type="monotone" dataKey="value"
          stroke={color} strokeWidth={2}
          dot={false} activeDot={{ r: 4, fill: color }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}