const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  summary: () => fetchJSON<import("./types").DashboardSummary>("/v1/dashboard/summary"),
  forecast: (horizon = 30) =>
    fetchJSON<import("./types").Forecast>(`/v1/dashboard/forecast?horizon=${horizon}`),
  alerts: (status = "open", limit = 50) =>
    fetchJSON<import("./types").Alert[]>(`/v1/alerts/?status=${status}&limit=${limit}`),
  stressMap: () => fetchJSON<import("./types").StressRegion[]>("/v1/dashboard/stress-map"),
  timeseries: (metric: string, days = 90) =>
    fetchJSON<import("./types").TSPoint[]>(`/v1/dashboard/ts/${metric}?days=${days}`),
  uploadCSV: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BASE}/v1/ingest/csv`, { method: "POST", body: form });
    return res.json();
  },
};
