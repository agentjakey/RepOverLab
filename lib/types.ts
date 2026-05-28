export type SafetyBand =
  | "benign"
  | "capability_building"
  | "ambiguous"
  | "policy_relevant_sanitized"
  | "abstract_risk_placeholder";

export interface Example {
  id: string;
  title: string;
  topic: string;
  content_text: string;
  domain: string;
  safety_band: SafetyBand;
  framing: string;
  safe_summary: string;
  why_interesting: string;
  x: number;
  y: number;
  overlap_score: number;
  is_high_overlap: number;
  nearest_cross_band_sim: number;
  sim_to_benign: number;
  sim_to_ambiguous: number;
  sim_to_policy_relevant_sanitized: number;
  boundary_blur_score: number;
}

export interface Neighbor {
  id: string;
  sim: number;
  band: SafetyBand;
  topic: string;
}

export type Neighbors = Record<string, Neighbor[]>;

export const BAND_META: Record<
  SafetyBand,
  { label: string; short: string; color: string; bg: string; border: string; text: string }
> = {
  benign: {
    label: "Benign",
    short: "Benign",
    color: "#1D4ED8",
    bg: "#DBEAFE",
    border: "#BFDBFE",
    text: "#1E40AF",
  },
  capability_building: {
    label: "Capability-Building",
    short: "Capability",
    color: "#6D28D9",
    bg: "#EDE9FE",
    border: "#DDD6FE",
    text: "#5B21B6",
  },
  ambiguous: {
    label: "Ambiguous",
    short: "Ambiguous",
    color: "#B45309",
    bg: "#FEF3C7",
    border: "#FDE68A",
    text: "#92400E",
  },
  policy_relevant_sanitized: {
    label: "Policy-Relevant",
    short: "Policy",
    color: "#B91C1C",
    bg: "#FEE2E2",
    border: "#FECACA",
    text: "#991B1B",
  },
  abstract_risk_placeholder: {
    label: "Abstract Placeholder",
    short: "Abstract",
    color: "#57534E",
    bg: "#F3F4F6",
    border: "#D1D5DB",
    text: "#374151",
  },
};

export const DOMAIN_LABELS: Record<string, string> = {
  biology: "Biology",
  cybersecurity: "Cybersecurity",
  persuasion: "Persuasion",
  physics: "Physics",
  AI_agents: "AI Agents",
  governance: "Governance",
  education: "Education",
  medicine: "Medicine",
  climate: "Climate",
  law_policy: "Law & Policy",
};

export const FRAMING_LABELS: Record<string, string> = {
  educational: "Educational",
  technical: "Technical",
  casual: "Casual",
  fictional: "Fictional",
  policy: "Policy",
  reflective: "Reflective",
  abstract_placeholder: "Abstract",
};
