"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { StressRegion } from "@/lib/types";

// We'll render a simple visual map since Leaflet requires client-side only
export default function MapPage() {
  const [regions, setRegions] = useState<StressRegion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.stressMap().then(setRegions).finally(() => setLoading(false));
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 70) return "#ef4444";
    if (score >= 50) return "#f59e0b";
    if (score >= 30) return "#eab308";
    return "#22c55e";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 70) return "Critical";
    if (score >= 50) return "High";
    if (score >= 30) return "Moderate";
    return "Low";
  };

  if (loading) {
    return <div className="flex items-center justify-center h-[80vh]"><p className="text-slate-400">Loading map...</p></div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Economic Stress Map</h1>
        <p className="text-sm text-slate-400">Composite risk scores by region</p>
      </div>

      {/* Simplified visual map layout */}
      <div className="bg-bou-card rounded-xl border border-bou-border p-6">
        {/* Uganda outline (simplified SVG representation) */}
        <div className="relative w-full max-w-2xl mx-auto aspect-[4/3]">
          {/* Map container */}
          <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 gap-4">
            {regions.map((region) => {
              const positions: Record<string, string> = {
                "Central": "col-start-2 row-start-2",
                "Eastern": "col-start-2 row-start-1",
                "Northern": "col-start-1 row-start-1",
                "Western": "col-start-1 row-start-2",
              };
              return (
                <div
                  key={region.region}
                  className={`${positions[region.region]} rounded-xl p-6 flex flex-col items-center justify-center border-2 transition-all hover:scale-105 cursor-pointer`}
                  style={{
                    borderColor: getScoreColor(region.score),
                    backgroundColor: `${getScoreColor(region.score)}15`,
                  }}
                >
                  <h3 className="text-white font-bold text-lg">{region.region}</h3>
                  <div
                    className="text-3xl font-black my-2"
                    style={{ color: getScoreColor(region.score) }}
                  >
                    {region.score.toFixed(1)}
                  </div>
                  <span
                    className="text-xs font-medium px-3 py-1 rounded-full"
                    style={{
                      color: getScoreColor(region.score),
                      backgroundColor: `${getScoreColor(region.score)}20`,
                    }}
                  >
                    {getScoreLabel(region.score)}
                  </span>
                  <p className="text-[10px] text-slate-500 mt-2">
                    Top: {region.top_driver.replace(/_/g, " ")}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-6 mt-8">
          {[
            { label: "Low", color: "#22c55e" },
            { label: "Moderate", color: "#eab308" },
            { label: "High", color: "#f59e0b" },
            { label: "Critical", color: "#ef4444" },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-2">
              <div className="w-3 h-3 rounded" style={{ backgroundColor: item.color }} />
              <span className="text-xs text-slate-400">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Region details table */}
      <div className="bg-bou-card rounded-xl border border-bou-border p-5">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Regional Breakdown</h2>
        <table className="w-full">
          <thead>
            <tr className="text-xs text-slate-500 border-b border-bou-border">
              <th className="text-left py-2">Region</th>
              <th className="text-left py-2">Score</th>
              <th className="text-left py-2">Status</th>
              <th className="text-left py-2">Top Driver</th>
            </tr>
          </thead>
          <tbody>
            {regions.map((r) => (
              <tr key={r.region} className="border-b border-bou-border/50">
                <td className="py-3 text-sm text-white">{r.region}</td>
                <td className="py-3">
                  <span className="text-sm font-mono" style={{ color: getScoreColor(r.score) }}>
                    {r.score.toFixed(1)}
                  </span>
                </td>
                <td className="py-3">
                  <span
                    className="text-xs px-2 py-1 rounded-full"
                    style={{ color: getScoreColor(r.score), backgroundColor: `${getScoreColor(r.score)}20` }}
                  >
                    {getScoreLabel(r.score)}
                  </span>
                </td>
                <td className="py-3 text-sm text-slate-400">{r.top_driver.replace(/_/g, " ")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}