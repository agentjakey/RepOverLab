"use client";

import { useState, useMemo } from "react";
import { Example, Neighbor, BAND_META, DOMAIN_LABELS, FRAMING_LABELS } from "@/lib/types";

interface Props {
  examples: Example[];
  neighbors: Record<string, Neighbor[]>;
}

function ExCard({ ex }: { ex: Example }) {
  const m = BAND_META[ex.safety_band];
  return (
    <div className="border border-[#DDD9D1] bg-white p-5 h-full">
      <span
        className="inline-block text-[11px] font-semibold px-2 py-0.5 mb-3"
        style={{ background: m.bg, color: m.text, border: `1px solid ${m.border}` }}
      >
        {m.label}
      </span>
      <h4 className="font-bold text-[#1A1917] text-[15px] leading-snug mb-1">
        {ex.title}
      </h4>
      <p className="text-[12px] text-[#5C5751] mb-3">
        {DOMAIN_LABELS[ex.domain] || ex.domain}
        {" · "}
        {FRAMING_LABELS[ex.framing] || ex.framing}
      </p>
      <p className="text-[13px] text-[#5C5751] leading-relaxed">
        {ex.safe_summary || ex.content_text.slice(0, 200) + "..."}
      </p>

      <div className="mt-4 pt-4 border-t border-[#EAE7E0] grid grid-cols-2 gap-2 text-center">
        <div>
          <p className="text-[11px] text-[#79746E]">Overlap</p>
          <p className="font-bold text-[#1A1917]">{ex.overlap_score.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-[11px] text-[#79746E]">Blur</p>
          <p className="font-bold text-[#1A1917]">{ex.boundary_blur_score.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
}

function simBetween(a: Example, b: Example, neighbors: Record<string, Neighbor[]>): number | null {
  const nbList = neighbors[a.id];
  if (!nbList) return null;
  const found = nbList.find((n) => n.id === b.id);
  return found ? found.sim : null;
}

function interpText(sim: number, sameBand: boolean): string {
  if (sameBand) {
    return "These examples share a safety band. High similarity between same-band examples is expected.";
  }
  if (sim >= 0.7) {
    return "High similarity across bands. A threshold-based system would need a very fine boundary to separate these.";
  }
  if (sim >= 0.45) {
    return "Moderate similarity. These examples share vocabulary or conceptual territory despite different safety classifications.";
  }
  return "Lower similarity. The embedding model distinguishes these reasonably well, assuming similar phrasing.";
}

export default function ComparePanel({ examples, neighbors }: Props) {
  const [idA, setIdA] = useState(examples[0]?.id ?? "");
  const [idB, setIdB] = useState(examples[5]?.id ?? "");

  const exA = useMemo(() => examples.find((e) => e.id === idA), [examples, idA]);
  const exB = useMemo(() => examples.find((e) => e.id === idB), [examples, idB]);

  const sim = useMemo(
    () => (exA && exB ? simBetween(exA, exB, neighbors) : null),
    [exA, exB, neighbors]
  );

  const sameBand = exA?.safety_band === exB?.safety_band;

  return (
    <div>
      <div className="essay-prose mb-8">
        <p>
          Select any two examples to see their cosine similarity in full embedding space.
          Similarity here is a measurement of how the model represents them &mdash; not a
          judgment about whether they should be treated the same way.
        </p>
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-[11px] font-semibold text-[#5C5751] uppercase tracking-wider mb-2">
            Example A
          </label>
          <select
            value={idA}
            onChange={(e) => setIdA(e.target.value)}
            className="w-full px-3 py-2 bg-white border border-[#DDD9D1] text-[13px] text-[#1A1917] focus:outline-none focus:border-[#1A1917]"
          >
            {examples.map((ex) => (
              <option key={ex.id} value={ex.id}>
                {ex.topic} ({BAND_META[ex.safety_band]?.short})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-[11px] font-semibold text-[#5C5751] uppercase tracking-wider mb-2">
            Example B
          </label>
          <select
            value={idB}
            onChange={(e) => setIdB(e.target.value)}
            className="w-full px-3 py-2 bg-white border border-[#DDD9D1] text-[13px] text-[#1A1917] focus:outline-none focus:border-[#1A1917]"
          >
            {examples.map((ex) => (
              <option key={ex.id} value={ex.id} disabled={ex.id === idA}>
                {ex.topic} ({BAND_META[ex.safety_band]?.short})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Similarity result */}
      {sim !== null && exA && exB && (
        <div
          className={`mb-6 px-5 py-4 border-l-2 ${
            sameBand
              ? "border-[#16A34A] bg-[#F0FDF4] text-[#14532D]"
              : sim >= 0.6
              ? "border-[#B91C1C] bg-[#FEF2F2] text-[#7F1D1D]"
              : "border-[#B45309] bg-[#FFFBEB] text-[#78350F]"
          }`}
        >
          <p className="text-[13px] font-semibold mb-1">
            Cosine similarity:{" "}
            <span className="text-[20px] font-bold">{sim.toFixed(4)}</span>
          </p>
          <p className="text-[13px] leading-relaxed">
            {interpText(sim, sameBand)}
          </p>
        </div>
      )}

      {sim === null && exA && exB && (
        <div className="mb-6 px-5 py-4 border-l-2 border-[#DDD9D1] bg-[#F7F5F0] text-[#5C5751]">
          <p className="text-[13px]">
            These two examples are beyond the stored top-10 neighbor range. Their similarity is
            low &mdash; likely below 0.3.
          </p>
        </div>
      )}

      {/* Side-by-side cards */}
      {exA && exB && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <ExCard ex={exA} />
          <ExCard ex={exB} />
        </div>
      )}
    </div>
  );
}
