"use client";

import { useState, useMemo } from "react";
import { Example, BAND_META, DOMAIN_LABELS } from "@/lib/types";

interface Props {
  examples: Example[];
}

function MiniBar({ value, label, color }: { value: number; label: string; color: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-[11px] text-[#57534E] w-16 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-[#F2EFE9] rounded-full overflow-hidden">
        <div
          className="h-full rounded-full"
          style={{ width: `${Math.round(value * 100)}%`, background: color }}
        />
      </div>
      <span className="text-[11px] text-[#57534E] w-10 text-right shrink-0">
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
      <p className="text-[0.95rem] text-[#57534E] leading-relaxed mb-6 max-w-[60ch]">
        The boundary blur score measures how evenly an example sits near multiple safety
        band centroids at once. A score near 1.0 means the example does not sit firmly
        within any single cluster. A score near 0.0 means it sits clearly within one band.
      </p>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Ranked list */}
        <div className="flex-1 min-w-0">
          <p className="text-[12px] font-semibold uppercase tracking-wider text-[#57534E] mb-3">
            Top 30 by boundary blur
          </p>
          <div className="space-y-1">
            {top30.map((ex, i) => {
              const m = BAND_META[ex.safety_band];
              const isSel = ex.id === selected;
              return (
                <button
                  key={ex.id}
                  onClick={() => setSelected(isSel ? null : ex.id)}
                  className={`w-full text-left flex items-center gap-3 px-3 py-2 rounded-lg border transition-all ${
                    isSel
                      ? "bg-[#1C1917] text-white border-[#1C1917]"
                      : "bg-white border-[#E2DDD6] hover:border-[#1C1917] hover:bg-[#F8F6F1]"
                  }`}
                >
                  <span
                    className={`text-[12px] font-bold w-6 shrink-0 ${
                      isSel ? "text-[#A8A29E]" : "text-[#78716C]"
                    }`}
                  >
                    {i + 1}
                  </span>

                  {/* Blur bar */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span
                        className={`text-[13px] font-medium truncate ${
                          isSel ? "text-white" : "text-[#1C1917]"
                        }`}
                      >
                        {ex.topic}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div
                        className="h-1.5 rounded-full"
                        style={{
                          width: `${Math.round(ex.boundary_blur_score * 120)}px`,
                          background: isSel ? "#A8A29E" : m.color,
                          minWidth: "4px",
                        }}
                      />
                      <span
                        className={`text-[11px] ${isSel ? "text-[#A8A29E]" : "text-[#78716C]"}`}
                      >
                        {ex.boundary_blur_score.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  <span
                    className="shrink-0 text-[11px] font-semibold px-1.5 py-0.5 rounded-md"
                    style={{
                      background: isSel ? "rgba(255,255,255,0.15)" : m.bg,
                      color: isSel ? "white" : m.text,
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
            <div className="bg-white rounded-xl border border-[#E2DDD6] p-5 sticky top-20">
              <div className="flex items-center justify-between mb-3">
                <span
                  className="inline-block text-[11px] font-semibold px-2 py-0.5 rounded-full"
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
                  className="text-[#78716C] hover:text-[#1C1917] text-lg leading-none"
                >
                  &times;
                </button>
              </div>

              <h4 className="font-bold text-[#1C1917] text-[14px] leading-snug mb-1">
                {selectedEx.title}
              </h4>
              <p className="text-[12px] text-[#57534E] mb-4">
                {DOMAIN_LABELS[selectedEx.domain] || selectedEx.domain}
              </p>

              <p className="text-[13px] text-[#57534E] leading-relaxed mb-4 line-clamp-4">
                {selectedEx.safe_summary}
              </p>

              <div className="space-y-2">
                <p className="text-[11px] font-semibold text-[#57534E] uppercase tracking-wider mb-2">
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

              <div className="mt-4 pt-4 border-t border-[#E2DDD6] grid grid-cols-2 gap-2 text-center">
                <div>
                  <p className="text-[11px] text-[#78716C]">Blur score</p>
                  <p className="font-bold text-[#1C1917] text-[15px]">
                    {selectedEx.boundary_blur_score.toFixed(3)}
                  </p>
                </div>
                <div>
                  <p className="text-[11px] text-[#78716C]">Overlap</p>
                  <p className="font-bold text-[#1C1917] text-[15px]">
                    {selectedEx.overlap_score.toFixed(2)}
                  </p>
                </div>
              </div>

              <p className="text-[11px] text-[#78716C] mt-3">
                High blur does not mean unsafe. It means the concept sits near multiple
                safety clusters simultaneously.
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-[#E2DDD6] p-5 text-center">
              <p className="text-[14px] font-medium text-[#57534E] mb-1">Select a concept</p>
              <p className="text-[13px] text-[#78716C]">
                to see its centroid similarity breakdown.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
