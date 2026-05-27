"use client";

import { useState, useRef, useCallback, useMemo } from "react";
import clsx from "clsx";
import { Example, Neighbor, SafetyBand, BAND_META, DOMAIN_LABELS, FRAMING_LABELS } from "@/lib/types";

interface Props {
  examples: Example[];
  neighbors: Record<string, Neighbor[]>;
}

const ALL_BANDS: SafetyBand[] = [
  "benign",
  "capability_building",
  "ambiguous",
  "policy_relevant_sanitized",
  "abstract_risk_placeholder",
];

const SVG_W = 680;
const SVG_H = 480;
const PAD = 36;

function scaleCoords(examples: Example[]) {
  const xs = examples.map((e) => e.x);
  const ys = examples.map((e) => e.y);
  const xMin = Math.min(...xs), xMax = Math.max(...xs);
  const yMin = Math.min(...ys), yMax = Math.max(...ys);
  const xRange = xMax - xMin || 1;
  const yRange = yMax - yMin || 1;

  return examples.map((e) => ({
    ...e,
    sx: PAD + ((e.x - xMin) / xRange) * (SVG_W - PAD * 2),
    sy: SVG_H - PAD - ((e.y - yMin) / yRange) * (SVG_H - PAD * 2),
  }));
}

function BandPill({ band }: { band: SafetyBand }) {
  const m = BAND_META[band];
  return (
    <span
      className={`inline-block text-[11px] font-semibold px-2 py-0.5 band-${band.replace(/_/g, "-")}`}
      style={{ background: m.bg, color: m.text, border: `1px solid ${m.border}` }}
    >
      {m.short}
    </span>
  );
}

function SimBar({ value }: { value: number }) {
  return (
    <div className="flex items-center gap-2 w-full">
      <div className="flex-1 h-1.5 bg-[#E8E4DC] overflow-hidden">
        <div
          className="h-full bg-[#1D4ED8]"
          style={{ width: `${Math.round(value * 100)}%` }}
        />
      </div>
      <span className="text-[11px] text-[#5C5751] w-10 text-right shrink-0">
        {value.toFixed(3)}
      </span>
    </div>
  );
}

export default function OverlapMap({ examples, neighbors }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number } | null>(null);
  const [activeBands, setActiveBands] = useState<Set<SafetyBand>>(new Set(ALL_BANDS));
  const [showOnlyHighOverlap, setShowOnlyHighOverlap] = useState(false);
  const svgRef = useRef<SVGSVGElement>(null);

  const scaled = useMemo(() => scaleCoords(examples), [examples]);

  const filtered = useMemo(
    () =>
      scaled.filter(
        (e) =>
          activeBands.has(e.safety_band) &&
          (!showOnlyHighOverlap || e.is_high_overlap === 1)
      ),
    [scaled, activeBands, showOnlyHighOverlap]
  );

  const selectedEx = useMemo(
    () => (selected ? examples.find((e) => e.id === selected) : null),
    [selected, examples]
  );

  const hoveredEx = useMemo(
    () => (hovered ? scaled.find((e) => e.id === hovered) : null),
    [hovered, scaled]
  );

  const toggleBand = useCallback((band: SafetyBand) => {
    setActiveBands((prev) => {
      const next = new Set(prev);
      if (next.has(band)) {
        if (next.size === 1) return prev;
        next.delete(band);
      } else {
        next.add(band);
      }
      return next;
    });
  }, []);

  const handlePointEnter = useCallback(
    (id: string, svgX: number, svgY: number) => {
      setHovered(id);
      if (svgRef.current) {
        const rect = svgRef.current.getBoundingClientRect();
        const scaleX = rect.width / SVG_W;
        const scaleY = rect.height / SVG_H;
        setTooltip({
          x: svgX * scaleX,
          y: svgY * scaleY,
        });
      }
    },
    []
  );

  const handlePointLeave = useCallback(() => {
    setHovered(null);
    setTooltip(null);
  }, []);

  const neighborList = selectedEx ? (neighbors[selectedEx.id] || []) : [];
  const crossBandNeighbors = neighborList.filter(
    (n) => n.band !== selectedEx?.safety_band
  );

  return (
    <div>
      {/* Filter row */}
      <div className="flex flex-wrap gap-3 mb-6 items-center">
        <span className="text-[11px] font-semibold uppercase tracking-wider text-[#79746E]">
          Filter:
        </span>
        {ALL_BANDS.map((band) => {
          const m = BAND_META[band];
          const active = activeBands.has(band);
          return (
            <button
              key={band}
              onClick={() => toggleBand(band)}
              className="flex items-center gap-1.5 px-3 py-1 text-[11px] font-medium border transition-all"
              style={{
                background: active ? m.bg : "transparent",
                color: active ? m.text : "#79746E",
                borderColor: active ? m.border : "#DDD9D1",
                opacity: active ? 1 : 0.55,
              }}
            >
              <span
                className="w-2 h-2 rounded-full inline-block"
                style={{ background: m.color }}
              />
              {m.short}
            </button>
          );
        })}
        <label className="flex items-center gap-1.5 text-[11px] text-[#5C5751] cursor-pointer ml-2">
          <input
            type="checkbox"
            checked={showOnlyHighOverlap}
            onChange={(e) => setShowOnlyHighOverlap(e.target.checked)}
          />
          High-overlap only
        </label>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Map panel */}
        <div className="flex-1 min-w-0">
          <div className="map-figure relative overflow-hidden">
            <svg
              ref={svgRef}
              viewBox={`0 0 ${SVG_W} ${SVG_H}`}
              className="w-full h-auto"
              style={{ maxHeight: 480 }}
            >
              {filtered.map((e) => {
                const m = BAND_META[e.safety_band];
                const isSel = e.id === selected;
                const isHov = e.id === hovered;
                const r = isSel ? 8 : isHov ? 7 : e.is_high_overlap ? 6.5 : 5.5;
                return (
                  <g key={e.id}>
                    {isSel && (
                      <circle
                        cx={e.sx}
                        cy={e.sy}
                        r={r + 6}
                        fill="none"
                        stroke="#1A1917"
                        strokeWidth="1.5"
                        opacity="0.2"
                        style={{ pointerEvents: "none" }}
                      />
                    )}
                    <circle
                      cx={e.sx}
                      cy={e.sy}
                      r={r}
                      fill={m.color}
                      fillOpacity={isSel ? 1 : isHov ? 0.95 : 0.75}
                      stroke={isSel ? "#1A1917" : isHov ? m.color : "white"}
                      strokeWidth={isSel ? 1.5 : isHov ? 0 : 1}
                      style={{ cursor: "pointer", transition: "r 0.1s, fill-opacity 0.1s" }}
                      onClick={() => setSelected(isSel ? null : e.id)}
                      onMouseEnter={() => handlePointEnter(e.id, e.sx, e.sy)}
                      onMouseLeave={handlePointLeave}
                    />
                  </g>
                );
              })}
            </svg>

            {/* Hover tooltip */}
            {hoveredEx && tooltip && (
              <div
                className="map-tooltip"
                style={{
                  left: tooltip.x + 14,
                  top: tooltip.y - 30,
                  transform:
                    tooltip.x > svgRef.current!.getBoundingClientRect().width * 0.65
                      ? "translateX(-105%)"
                      : "none",
                }}
              >
                <BandPill band={hoveredEx.safety_band} />
                <p className="font-semibold text-[#1A1917] mt-1.5 mb-0.5 text-[13px] leading-snug">
                  {hoveredEx.topic}
                </p>
                <p className="text-[11px] text-[#5C5751]">
                  {DOMAIN_LABELS[hoveredEx.domain] || hoveredEx.domain}
                </p>
                <p className="text-[11px] text-[#79746E] mt-1">
                  Overlap: {hoveredEx.overlap_score.toFixed(2)}
                </p>
              </div>
            )}
          </div>

          {/* Caption */}
          <p className="fig-caption mt-2 text-center">
            Distance is a teaching aid, not ground truth. Click any point to explore.
          </p>

          {/* Legend */}
          <div className="mt-4 flex flex-wrap gap-4 justify-center">
            {ALL_BANDS.map((band) => {
              const m = BAND_META[band];
              return (
                <div key={band} className="flex items-center gap-1.5">
                  <span
                    className="w-2.5 h-2.5 rounded-full inline-block"
                    style={{ background: m.color }}
                  />
                  <span className="text-[11px] text-[#5C5751]">{m.label}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Detail panel */}
        <div className="lg:w-80 shrink-0">
          {selectedEx ? (
            <div className="border border-[#DDD9D1] bg-white p-5 h-full">
              <div className="flex items-start justify-between mb-3">
                <BandPill band={selectedEx.safety_band} />
                <button
                  onClick={() => setSelected(null)}
                  className="text-[#79746E] hover:text-[#1A1917] transition-colors text-lg leading-none"
                  aria-label="Close"
                >
                  &times;
                </button>
              </div>

              <h3 className="font-bold text-[#1A1917] text-[15px] leading-snug mb-1">
                {selectedEx.title}
              </h3>
              <p className="text-[12px] text-[#5C5751] mb-3">
                {DOMAIN_LABELS[selectedEx.domain] || selectedEx.domain}
                {" · "}
                {FRAMING_LABELS[selectedEx.framing] || selectedEx.framing}
              </p>

              <p className="text-[13px] text-[#1A1917] leading-relaxed mb-4 line-clamp-4">
                {selectedEx.safe_summary || selectedEx.content_text.slice(0, 160) + "..."}
              </p>

              {selectedEx.why_interesting && (
                <div className="border-l-2 border-[#DDD9D1] pl-3 mb-4">
                  <p className="text-[11px] font-semibold text-[#5C5751] uppercase tracking-wider mb-1">
                    Why interesting
                  </p>
                  <p className="text-[12px] text-[#5C5751] leading-relaxed">
                    {selectedEx.why_interesting}
                  </p>
                </div>
              )}

              {/* Scores */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="bg-[#F0EDE6] p-2.5 text-center">
                  <p className="text-[11px] text-[#79746E] mb-0.5">Overlap</p>
                  <p className="font-bold text-[#1A1917] text-[16px]">
                    {selectedEx.overlap_score.toFixed(2)}
                  </p>
                </div>
                <div className="bg-[#F0EDE6] p-2.5 text-center">
                  <p className="text-[11px] text-[#79746E] mb-0.5">Blur</p>
                  <p className="font-bold text-[#1A1917] text-[16px]">
                    {selectedEx.boundary_blur_score.toFixed(2)}
                  </p>
                </div>
              </div>

              {/* Cross-band neighbors */}
              {crossBandNeighbors.length > 0 && (
                <div>
                  <p className="text-[11px] font-semibold text-[#5C5751] uppercase tracking-wider mb-2">
                    Cross-band neighbors
                  </p>
                  <div className="space-y-2">
                    {crossBandNeighbors.slice(0, 5).map((nb) => (
                      <div key={nb.id} className="flex flex-col gap-1">
                        <div className="flex items-center justify-between">
                          <span className="text-[12px] text-[#1A1917] font-medium truncate flex-1 mr-2">
                            {nb.topic}
                          </span>
                          <BandPill band={nb.band} />
                        </div>
                        <SimBar value={nb.sim} />
                      </div>
                    ))}
                  </div>
                  <p className="text-[11px] text-[#79746E] mt-2">
                    These examples are from different safety bands but sit close in embedding
                    space.
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="border border-[#DDD9D1] bg-white p-5 h-full flex flex-col justify-center">
              <div className="text-center text-[#79746E]">
                <div className="text-3xl mb-3">&#8982;</div>
                <p className="text-[14px] font-medium text-[#5C5751] mb-1">
                  Click any point
                </p>
                <p className="text-[13px] text-[#79746E]">
                  to explore its safety band, domain, framing, and nearest
                  cross-band neighbors.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Stats row */}
      <div className="mt-6 flex flex-wrap gap-4 text-[13px] text-[#5C5751]">
        <span>
          <strong className="text-[#1A1917]">{filtered.length}</strong> of{" "}
          {examples.length} concepts shown
        </span>
        <span>&middot;</span>
        <span>
          <strong className="text-[#1A1917]">
            {filtered.filter((e) => e.is_high_overlap).length}
          </strong>{" "}
          high-overlap (&ge;0.6)
        </span>
      </div>
    </div>
  );
}
