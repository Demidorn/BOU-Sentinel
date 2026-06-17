"use client";
import type { Alert } from "@/lib/types";
import { severityColor, typeIcon } from "@/lib/utils";

interface Props {
  alert: Alert;
  onClose: () => void;
}

export default function AlertDrawer({ alert, onClose }: Props) {
  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50 z-40" onClick={onClose} />
      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-[420px] bg-bou-black border-l border-bou-border z-50 p-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-bold text-white">Alert Details</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl">✕</button>
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{typeIcon(alert.type)}</span>
            <div>
              <p className="text-white font-semibold">{alert.title}</p>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${severityColor(alert.severity)}`}>
                Severity {alert.severity}
              </span>
            </div>
          </div>

          <div className="bg-bou-card rounded-lg p-4 border border-bou-border space-y-2">
            <div>
              <span className="text-xs text-slate-500">Type</span>
              <p className="text-sm text-white">{alert.type}</p>
            </div>
            <div>
              <span className="text-xs text-slate-500">Time</span>
              <p className="text-sm text-white">{new Date(alert.created_at).toLocaleString()}</p>
            </div>
            {alert.region && (
              <div>
                <span className="text-xs text-slate-500">Region</span>
                <p className="text-sm text-white">{alert.region}</p>
              </div>
            )}
          </div>

          {alert.description && (
            <div className="bg-bou-card rounded-lg p-4 border border-bou-border">
              <span className="text-xs text-slate-500">Description</span>
              <p className="text-sm text-slate-300 mt-1">{alert.description}</p>
            </div>
          )}

          {alert.evidence && Object.keys(alert.evidence).length > 0 && (
            <div className="bg-bou-card rounded-lg p-4 border border-bou-border">
              <span className="text-xs text-slate-500">Evidence (AI)</span>
              <pre className="text-xs text-emerald-400 mt-2 overflow-x-auto">
                {JSON.stringify(alert.evidence, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </>
  );
}