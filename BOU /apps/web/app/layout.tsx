import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BOU Sentinel — Economic Early Warning System",
  description: "AI-Powered National Economic Early Warning System for Uganda",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-bou-dark">{children}</body>
    </html>
  );
}