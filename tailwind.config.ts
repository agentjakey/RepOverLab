import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sora)", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ["var(--font-lora)", "Georgia", "Cambria", "Times New Roman", "serif"],
        mono: ["var(--font-dm-mono)", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      colors: {
        background: "#FAFAF8",
        primary: "#1A1915",
        secondary: "#5C5A54",
        accent: "#C2411C",
        border: "#E4E2DB",
        "surface-muted": "#F0EDE8",
        "accent-soft": "#FFF2EE",
        "blue-soft": "#EFF6FF",
        "amber-soft": "#FFFBEB",
        band: {
          benign: "#1D4ED8",
          capability: "#6D28D9",
          ambiguous: "#B45309",
          policy: "#B91C1C",
          abstract: "#57534E",
        },
      },
      maxWidth: {
        prose: "68ch",
        lab: "1100px",
      },
    },
  },
  plugins: [],
};

export default config;
