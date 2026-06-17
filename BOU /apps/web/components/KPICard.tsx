interface KPICardProps {
  title: string;
  value: string;
  change?: number | null;
  changeLabel?: string;
  icon: string;
  valueColor?: string;
  trend?: string | null;
  trendColor?: string;
}

export default function KPICard({
  title, value, change, changeLabel, icon, valueColor, trend, trendColor,
}: KPICardProps) {
  return (
    <div className="bg-bou-card rounded-xl border border-bou-border p-4 hover:border-bou-gold/30 transition-colors">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-slate-400 uppercase tracking-wider">{title}</span>
        <span className="text-xl">{icon}</span>
      </div>
      <div className={`text-2xl font-bold ${valueColor || "text-white"}`}>{value}</div>
      <div className="mt-2 flex items-center gap-2">
        {trend && (
          <span className={`text-xs font-medium ${trendColor || "text-slate-400"}`}>
            {trend}
          </span>
        )}
        {change !== undefined && change !== null && (
          <span className={`text-xs ${change >= 0 ? "text-red-400" : "text-emerald-400"}`}>
            {change >= 0 ? "+" : ""}{change.toFixed(2)}%
          </span>
        )}
        {changeLabel && (
          <span className="text-xs text-slate-500">{changeLabel}</span>
        )}
      </div>
    </div>
  );
}