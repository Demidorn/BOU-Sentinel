import type { Alert } from "@/lib/types";
import { severityColor, typeIcon } from "@/lib/utils";

interface Props {
  alerts: Alert[];
  onSelect: (alert: Alert) => void;
}

export default function AlertsFeed({ alerts, onSelect }: Props) {
  if (alerts.length === 0) {
    return <p className="text-slate-500 text-sm py-8 text-center">No active alerts 🎉</p>;
  }

  return (
    <div className="space-y-2 max-h-[300px] overflow-y-auto pr-2">
      {alerts.map((alert) => (
        <button
          key={alert.id}
          onClick={() => onSelect(alert)}
          className="w-full text-left flex items-center gap-3 p-3 rounded-lg bg-bou-dark/50 hover:bg-white/5 border border-bou-border/50 transition-colors"
        >
          <span className="text-xl flex-shrink-0">{typeIcon(alert.type)}</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-white truncate">{alert.title}</p>
            <p className="text-xs text-slate-500">
              {new Date(alert.created_at).toLocaleString()} · {alert.type}
            </p>
          </div>
          <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium flex-shrink-0 ${severityColor(alert.severity)}`}>
            Sev {alert.severity}
          </span>
        </button>
      ))}
    </div>
  );
}