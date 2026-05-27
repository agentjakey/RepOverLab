"use client";

import { useState } from "react";

type Mode = "non-technical" | "technical" | "researcher";

const MODE_LABELS: Record<Mode, string> = {
  "non-technical": "Non-technical",
  technical: "Technical",
  researcher: "Researcher",
};

const MODE_DESCRIPTIONS: Record<Mode, string> = {
  "non-technical": "Plain language. Technical terms explained inline.",
  technical:
    "Assumes familiarity with embeddings, cosine similarity, and dimensionality reduction.",
  researcher:
    "Includes methodology details and links for deeper exploration.",
};

export default function Hero() {
  const [mode, setMode] = useState<Mode>("non-technical");

  return (
    <section id="top" className="border-b border-[#E4E2DB] pt-36 pb-28 px-6">
      <div className="prose-col">
        <p className="section-num mb-6">
          Latent Space Lab &mdash; An Interactive Essay
        </p>

        <p
          className="text-[1.2rem] italic leading-relaxed text-[#5C5751] mb-6"
          style={{
            fontFamily: "Georgia, Cambria, 'Times New Roman', Times, serif",
          }}
        >
          The hard cases in AI safety rarely live in clean boxes.
        </p>

        <h1 className="text-5xl sm:text-6xl font-bold text-[#1A1917] leading-[1.08] tracking-tight mb-4">
          Representation
          <br />
          Overlap
        </h1>

        <p className="text-[1.0625rem] text-[#5C5751] leading-relaxed mb-12">
          Why safety boundaries are not always cleanly separable.
        </p>

        <div className="mb-10">
          <div className="flex flex-wrap items-center gap-x-1 text-[12px] text-[#79746E] mb-2">
            <span className="mr-1">Reading mode:</span>
            {(["non-technical", "technical", "researcher"] as Mode[]).map(
              (m, i) => (
                <span key={m} className="flex items-center gap-x-1">
                  {i > 0 && <span className="mx-1 text-[#C4C0BB]">/</span>}
                  <button
                    onClick={() => setMode(m)}
                    className={`transition-colors ${
                      mode === m
                        ? "text-[#1A1917] font-semibold"
                        : "hover:text-[#1A1917]"
                    }`}
                  >
                    {MODE_LABELS[m]}
                  </button>
                </span>
              )
            )}
          </div>
          <p className="text-[12px] text-[#79746E]">{MODE_DESCRIPTIONS[mode]}</p>
        </div>

        <p className="text-[12px] text-[#79746E] mb-10">
          ~8 min read &middot; includes interactive map and comparisons
        </p>

        <a
          href="#idea"
          className="inline-flex items-center gap-2 text-[13px] text-[#5C5751] hover:text-[#1A1917] transition-colors"
        >
          Begin reading
          <svg
            width="14"
            height="14"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <polyline points="19 12 12 19 5 12" />
          </svg>
        </a>
      </div>
    </section>
  );
}
