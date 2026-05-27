"use client";

import { useState } from "react";
import clsx from "clsx";

type Mode = "non-technical" | "technical" | "researcher";

const MODE_DESCRIPTIONS: Record<Mode, string> = {
  "non-technical":
    "This page uses plain language. Technical terms are explained inline.",
  technical:
    "This page assumes familiarity with embeddings, cosine similarity, and dimensionality reduction.",
  researcher:
    "This page includes methodology details and links to underlying concepts for deeper exploration.",
};

export default function Hero() {
  const [mode, setMode] = useState<Mode>("non-technical");

  return (
    <section id="top" className="pt-32 pb-24 px-6">
      <div className="max-w-[68ch] mx-auto">
        {/* Eyebrow */}
        <p className="text-[11px] font-semibold tracking-widest uppercase text-[#57534E] mb-4">
          Latent Space Lab &mdash; An Interactive Essay
        </p>

        {/* Title */}
        <h1 className="text-4xl sm:text-5xl font-bold text-[#1C1917] leading-[1.15] mb-5 tracking-tight">
          Representation
          <br />
          Overlap
        </h1>

        {/* Subtitle */}
        <p className="text-xl sm:text-2xl font-medium text-[#57534E] mb-8 leading-snug">
          Why safety boundaries are not always cleanly separable.
        </p>

        {/* Opening line */}
        <p className="text-[1.125rem] text-[#1C1917] leading-relaxed mb-10 border-l-4 border-[#B91C1C] pl-5 font-medium">
          The hard cases in AI safety rarely live in clean boxes.
        </p>

        {/* Reading mode */}
        <div className="mb-2">
          <p className="text-[13px] text-[#57534E] mb-2 font-medium">
            How would you like to read this?
          </p>
          <div className="flex flex-wrap gap-2">
            {(["non-technical", "technical", "researcher"] as Mode[]).map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={clsx(
                  "px-4 py-1.5 rounded-full text-[13px] font-medium border transition-colors",
                  mode === m
                    ? "bg-[#1C1917] text-white border-[#1C1917]"
                    : "bg-transparent text-[#57534E] border-[#E2DDD6] hover:border-[#1C1917] hover:text-[#1C1917]"
                )}
              >
                {m === "non-technical"
                  ? "Non-technical"
                  : m === "technical"
                  ? "Technical"
                  : "Researcher"}
              </button>
            ))}
          </div>
          <p className="text-[13px] text-[#57534E] mt-3">{MODE_DESCRIPTIONS[mode]}</p>
        </div>

        {/* Read time */}
        <p className="text-[12px] text-[#78716C] mt-6">
          ~8 min read &middot; includes interactive map and comparisons
        </p>

        {/* Arrow down */}
        <a
          href="#idea"
          className="inline-flex items-center gap-2 mt-8 text-[13px] text-[#57534E] hover:text-[#1C1917] transition-colors"
        >
          Begin reading
          <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <line x1="12" y1="5" x2="12" y2="19" />
            <polyline points="19 12 12 19 5 12" />
          </svg>
        </a>
      </div>
    </section>
  );
}
