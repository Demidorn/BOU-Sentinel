import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatUGX(value: number): string {
  return new Intl.NumberFormat("en-UG", {
    style: "currency",
    currency: "UGX",
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(value);
}

export function severityColor(severity: number): string {
  if (severity >= 4) return "text-red-400 bg-red-500/20 border-red-500/30";
  if (severity >= 3) return "text-amber-400 bg-amber-500/20 border-amber-500/30";
  return "text-blue-400 bg-blue-500/20 border-blue-500/30";
}

export function typeIcon(type: string): string {
  const map: Record<string, string> = {
    FX_PRESSURE: "💱",
    INFLATION_RISK: "📈",
    LIQUIDITY_STRESS: "💧",
    CAPITAL_FLIGHT: "✈️",
    FRAUD: "🚨",
  };
  return map[type] || "⚠️";
}
