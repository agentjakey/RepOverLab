"use client";

import { useState, useMemo } from "react";
import { Example, BAND_META, DOMAIN_LABELS } from "@/lib/types";

interface Props {
  examples: Example[];
}

function MiniBar({ value, label, color }: { value: number; label: string; color: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-[11px] text-[#5C5751] w-16 shrink-0">{label}</span>
      <div className="flex-1 h-1.5 bg-[#EAE7E0] overflow-hidden">
        <div
          className="h-full"
          style={{ width: `${Math.round(value * 100)}%`, background: color }}
        />
      </div>
      <span className="text-[11px] text-[#5C5751] w-10 text-right shrink-0">
        {value.toFixed(2)}
      </span>
    </div>
  );
}

export default function BoundaryBlur({ examples }: Props) {
  const [selected, setSelected] = useState<string | null>(null);

  const sorted = useMemo(
    () => [...examples].sort((a, b) => b.boundary_blur_score - a.boundary_blur_score),
    [examples]
  );

  const top30 = sorted.slice(0, 30);
  const selectedEx = selected ? examples.find((e) => e.id === selected) : null;

  return (
    <div>
      <div className="essay-prose mb-8 space-y-3">
        <p>
          The boundary blur score measures how evenly an example sits near multiple
          safety band centroids at once. A score near 1.0 means the concept does not
          anchor firmly within any single cluster. A score near 0.0 means it sits
          clearly within one band.
        </p>
        <p>
          High blur is not a danger signal. It is a geometric property. Many high-blur
          concepts are straightforwardly benign — they simply use language that crosses
          categorical boundaries.
        </p>
        <p className="text-[0.9rem] text-[#79746E] border-l-2 border-[#E4E2DB] pl-4 not-italic">
          Scores in this dataset cluster in the 0.99-1.00 range. This is expected:
          all-MiniLM-L6-v2 produces cosine similarities in a compressed range across
          general-topic text, and normalized Shannon entropy over three centroids
          saturates quickly. The ranking is meaningful even when absolute values are
          close. A concept scoring 0.994 is meaningfully less anchored than one scoring
          1.000. This is an exploration heuristic, not a calibrated risk score.
        </p>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Ranked list */}
        <div className="flex-1 min-w-0">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-[#79746E] mb-4">
            Top 30 by boundary blur
          </p>
          <div>
            {top30.map((ex, i) => {
              const m = BAND_META[ex.safety_band];
              const isSel = ex.id === selected;
              return (
                <button
                  key={ex.id}
                  onClick={() => setSelected(isSel ? null : ex.id)}
                  className={`w-full text-left flex items-center gap-3 py-2.5 border-b border-[#EAE7E0] transition-colors ${
                    isSel ? "bg-[#F0EDE6]" : "hover:bg-[#F7F5F0]"
                  }`}
                >
                  <span className="text-[12px] font-bold w-6 shrink-0 text-[#79746E]">
                    {i + 1}
                  </span>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span
                        className={`text-[13px] font-medium truncate ${
                          isSel ? "text-[#1A1917]" : "text-[#1A1917]"
                        }`}
                      >
                        {ex.topic}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div
                        className="h-1"
                        style={{
                          width: `${Math.round(ex.boundary_blur_score * 120)}px`,
                          background: m.color,
                          minWidth: "4px",
                          opacity: 0.7,
                        }}
                      />
                      <span className="text-[11px] text-[#79746E]">
                        {ex.boundary_blur_score.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  <span
                    className="shrink-0 text-[10px] font-semibold px-1.5 py-0.5"
                    style={{
                      background: m.bg,
                      color: m.text,
                    }}
                  >
                    {m.short}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Detail panel */}
        <div className="lg:w-72 shrink-0">
          {selectedEx ? (
            <div className="border border-[#DDD9D1] bg-white p-5 sticky top-16">
              <div className="flex items-center justify-between mb-3">
                <span
                  className="inline-block text-[11px] font-semibold px-2 py-0.5"
                  style={{
                    background: BAND_META[selectedEx.safety_band].bg,
                    color: BAND_META[selectedEx.safety_band].text,
                    border: `1px solid ${BAND_META[selectedEx.safety_band].border}`,
                  }}
                >
                  {BAND_META[selectedEx.safety_band].label}
                </span>
                <button
                  onClick={() => setSelected(null)}
                  className="text-[#79746E] hover:text-[#1A1917] text-lg leading-none"
                >
                  &times;
                </button>
              </div>

              <h4 className="font-bold text-[#1A1917] text-[14px] leading-snug mb-1">
                {selectedEx.title}
              </h4>
              <p className="text-[12px] text-[#5C5751] mb-4">
                {DOMAIN_LABELS[selectedEx.domain] || selectedEx.domain}
              </p>

              <p className="text-[13px] text-[#5C5751] leading-relaxed mb-4 line-clamp-4">
                {selectedEx.safe_summary}
              </p>

              <div className="space-y-2">
                <p className="text-[11px] font-semibold text-[#5C5751] uppercase tracking-wider mb-2">
                  Centroid similarities
                </p>
                <MiniBar value={selectedEx.sim_to_benign} label="Benign" color="#1D4ED8" />
                <MiniBar
                  value={selectedEx.sim_to_ambiguous}
                  label="Ambiguous"
                  color="#B45309"
                />
                <MiniBar
                  value={selectedEx.sim_to_policy_relevant_sanitized}
                  label="Policy"
                  color="#B91C1C"
                />
              </div>

              <div className="mt-4 pt-4 border-t border-[#EAE7E0] grid grid-cols-2 gap-2 text-center">
                <div>
                  <p className="text-[11px] text-[#79746E]">Blur score</p>
                  <p className="font-bold text-[#1A1917] text-[15px]">
                    {selectedEx.boundary_blur_score.toFixed(3)}
                  </p>
                </div>
                <div>
                  <p className="text-[11px] text-[#79746E]">Overlap</p>
                  <p className="font-bold text-[#1A1917] text-[15px]">
                    {selectedEx.overlap_score.toFixed(2)}
                  </p>
                </div>
              </div>

              <p className="text-[11px] text-[#79746E] mt-3 leading-relaxed">
                High blur means the concept sits near multiple safety clusters
                simultaneously &mdash; not that it is unsafe.
              </p>
            </div>
          ) : (
            <div className="border border-[#DDD9D1] bg-white p-5 text-center">
              <p className="text-[14px] font-medium text-[#5C5751] mb-1">Select a concept</p>
              <p className="text-[13px] text-[#79746E]">
                to see its centroid similarity breakdown.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
