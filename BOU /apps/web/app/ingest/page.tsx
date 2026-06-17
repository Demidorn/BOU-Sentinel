"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";

declare const process: { env: { NEXT_PUBLIC_API_URL?: string } };

interface IngestRecord {
  metric: string;
  ts: string;
  source: string;
}

export default function IngestPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ ingested: number; file: string } | null>(null);
  const [lastIngested, setLastIngested] = useState<IngestRecord[]>([]);

  useEffect(() => {
    fetchLast();
  }, []);

  async function fetchLast() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/v1/ingest/last`);
      if (res.ok) setLastIngested(await res.json());
    } catch {}
  }

  async function handleUpload() {
    if (!file) return;
    setUploading(true);
    try {
      const result = await api.uploadCSV(file);
      setUploadResult(result);
      fetchLast();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Data Ingestion</h1>
        <p className="text-sm text-slate-400">Upload CSV files or monitor the latest ingested data</p>
      </div>

      {/* Upload Card */}
      <div className="bg-bou-card rounded-xl border border-bou-border p-6 max-w-xl">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Upload CSV</h2>
        <p className="text-xs text-slate-500 mb-4">
          CSV format: <code className="bg-bou-dark px-1 rounded">metric, ts, value, region, source</code>
        </p>
        <div className="space-y-4">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-bou-gold file:text-black hover:file:bg-bou-gold/80 cursor-pointer"
          />
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="px-4 py-2 bg-bou-gold text-black rounded-lg font-semibold text-sm hover:bg-bou-gold/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? "Uploading..." : "Upload & Ingest"}
          </button>
          {uploadResult && (
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3">
              <p className="text-sm text-emerald-400">
                ✅ Ingested {uploadResult.ingested} rows from {uploadResult.file}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Last Ingested */}
      <div className="bg-bou-card rounded-xl border border-bou-border p-6">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Latest Ingested Metrics</h2>
        {lastIngested.length === 0 ? (
          <p className="text-slate-500 text-sm">No data ingested yet. Run the seed script or upload a CSV.</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="text-xs text-slate-500 border-b border-bou-border">
                <th className="text-left py-2">Metric</th>
                <th className="text-left py-2">Last Timestamp</th>
                <th className="text-left py-2">Source</th>
              </tr>
            </thead>
            <tbody>
              {lastIngested.map((r, i) => (
                <tr key={i} className="border-b border-bou-border/50">
                  <td className="py-2 text-sm text-white font-mono">{r.metric}</td>
                  <td className="py-2 text-sm text-slate-400">{new Date(r.ts).toLocaleString()}</td>
                  <td className="py-2 text-sm text-slate-400">{r.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}