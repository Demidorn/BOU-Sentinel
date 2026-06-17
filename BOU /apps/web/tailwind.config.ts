import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bou: {
          gold: "#D4AF37",
          red: "#C41E3A",
          black: "#1A1A1A",
          dark: "#0F172A",
          card: "#1E293B",
          border: "#334155",
        },
      },
    },
  },
  plugins: [],
};
export default config;