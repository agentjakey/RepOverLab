import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "monospace"],
      },
      colors: {
        bg: "#F8F6F1",
        surface: "#FFFFFF",
        "surface-muted": "#F2EFE9",
        text: "#1C1917",
        muted: "#57534E",
        border: "#E2DDD6",
        accent: "#B91C1C",
        "accent-soft": "#FEF2F2",
        "blue-soft": "#EFF6FF",
        "amber-soft": "#FFFBEB",
        "green-soft": "#F0FDF4",
        "violet-soft": "#F5F3FF",
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
      typography: {
        DEFAULT: {
          css: {
            color: "#1C1917",
            lineHeight: "1.75",
            fontSize: "1.0625rem",
          },
        },
      },
    },
  },
  plugins: [],
};

export default config;
