"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const links = [
  { href: "/dashboard", label: "Command Center", icon: "📊" },
  { href: "/map",       label: "Risk Map",       icon: "🗺️" },
  { href: "/ingest",    label: "Data Ingest",    icon: "📥" },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-bou-black border-r border-bou-border p-4 z-50">
      {/* Logo */}
      <div className="mb-8">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🛡️</span>
          <div>
            <h1 className="text-lg font-bold text-bou-gold">BOU SENTINEL</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-wider">Economic Early Warning</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="space-y-1">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors",
              pathname === link.href
                ? "bg-bou-gold/10 text-bou-gold border border-bou-gold/20"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            )}
          >
            <span className="text-lg">{link.icon}</span>
            {link.label}
          </Link>
        ))}
      </nav>

      {/* Status */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="bg-bou-card rounded-lg p-3 border border-bou-border">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            <span className="text-xs text-slate-400">System Online</span>
          </div>
          <p className="text-[10px] text-slate-500">v0.1.0 — MVP</p>
        </div>
      </div>
    </aside>
  );
}