import { promises as fs } from "fs";
import path from "path";
import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import Section from "@/components/Section";
import CareNote from "@/components/CareNote";
import OverlapMap from "@/components/OverlapMap";
import BoundaryBlur from "@/components/BoundaryBlur";
import ComparePanel from "@/components/ComparePanel";
import MethodCard from "@/components/MethodCard";
import Footer from "@/components/Footer";
import { Example, Neighbors } from "@/lib/types";

async function getData() {
  const dataDir = path.join(process.cwd(), "public", "data");
  const [examplesRaw, neighborsRaw] = await Promise.all([
    fs.readFile(path.join(dataDir, "examples.json"), "utf8"),
    fs.readFile(path.join(dataDir, "neighbors.json"), "utf8"),
  ]);
  return {
    examples: JSON.parse(examplesRaw) as Example[],
    neighbors: JSON.parse(neighborsRaw) as Neighbors,
  };
}

export default async function Home() {
  const { examples, neighbors } = await getData();

  const nHigh = examples.filter((e) => e.overlap_score >= 0.6).length;
  const nDomains = new Set(examples.map((e) => e.domain)).size;

  return (
    <>
      <Nav />

      <main className="pt-16">
        {/* ── Hero ─────────────────────────────────────────────────── */}
        <Hero />

        <div className="w-full max-w-[68ch] mx-auto px-6">
          <div className="h-px bg-[#E2DDD6]" />
        </div>

        {/* ── 01 The Idea ──────────────────────────────────────────── */}
        <Section id="idea" num="01" title="The Idea">
          <div className="space-y-5 text-[1.0625rem] text-[#1C1917] leading-[1.8]">
            <p>
              When an AI safety system draws a line, it is drawing that line in a geometry
              it did not design. Sentence embeddings turn text into points in high-dimensional
              space, and those points cluster by statistical patterns in training data — not
              by intent, not by context, not by who is asking.
            </p>
            <p>
              The result is that concepts from very different categories often end up as
              neighbors in that space. A question about medication dosage lands near a question
              about overdose. A security research description shares vocabulary with an
              exploitation technique. A policy analysis of extremism occupies the same
              neighborhood as the thing it analyzes.
            </p>
            <p>
              This is not a flaw in any particular model. It is a consequence of how
              language works. Safety systems that use embedding similarity to make decisions
              inherit the geometry — and all the ambiguity that comes with it.
            </p>

            <CareNote>
              <strong>A map for thinking, not a judge.</strong> This project makes those
              neighborhoods visible. It does not argue for loosening safety standards. It
              argues for understanding what those standards are actually doing — and where
              they will struggle.
            </CareNote>

            <h3 className="text-[1.05rem] font-semibold text-[#1C1917] pt-2">
              Why should you care?
            </h3>
            <p>
              If you are building a content filter or reward model, this is a picture of
              where your rule will fire on benign content — and where it will miss harmful
              content that learned to sound clinical. If you are doing evals, this is a
              vocabulary for what &ldquo;near-miss&rdquo; means beyond a binary score. If
              you are new to alignment, this is an entry point that does not require reading
              papers first.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 py-4">
              {[
                {
                  num: `${examples.length}`,
                  label: "Concept descriptions",
                  sub: "across 10 domains",
                },
                {
                  num: `${nHigh}`,
                  label: "High-overlap examples",
                  sub: "sitting at band boundaries",
                },
                {
                  num: `${nDomains}`,
                  label: "Domains",
                  sub: "biology to law to AI",
                },
              ].map((stat) => (
                <div
                  key={stat.num}
                  className="bg-[#F2EFE9] border border-[#E2DDD6] rounded-xl p-4 text-center"
                >
                  <p className="text-[2rem] font-bold text-[#1C1917] leading-none mb-1">
                    {stat.num}
                  </p>
                  <p className="text-[13px] font-semibold text-[#1C1917]">{stat.label}</p>
                  <p className="text-[12px] text-[#78716C]">{stat.sub}</p>
                </div>
              ))}
            </div>
          </div>
        </Section>

        <div className="w-full max-w-[68ch] mx-auto px-6">
          <div className="h-px bg-[#E2DDD6]" />
        </div>

        {/* ── 02 The Geometry ──────────────────────────────────────── */}
        <Section id="geometry" num="02" title="The Geometry">
          <div className="space-y-5 text-[1.0625rem] text-[#1C1917] leading-[1.8]">
            <p>
              Every text snippet can be turned into a list of numbers — a vector — by a
              sentence embedding model. The model is trained to place similar texts near each
              other in this high-dimensional space. &ldquo;Similar&rdquo; here means
              statistically similar: same vocabulary, same sentence structure, same conceptual
              patterns in the training corpus.
            </p>
            <p>
              Cosine similarity measures the angle between two vectors. Two texts with
              similarity 1.0 point in exactly the same direction. Two texts with similarity
              0.0 are orthogonal — maximally unrelated in the model&apos;s learned space.
            </p>

            {/* Simple diagram */}
            <div className="bg-white border border-[#E2DDD6] rounded-xl p-6 my-6">
              <p className="text-[11px] font-semibold uppercase tracking-wider text-[#78716C] mb-5 text-center">
                Simplified 2D projection of embedding space
              </p>
              <svg viewBox="0 0 480 200" className="w-full h-auto" aria-label="Embedding space diagram">
                {/* Axes */}
                <line x1="40" y1="160" x2="440" y2="160" stroke="#E2DDD6" strokeWidth="1" />
                <line x1="40" y1="20" x2="40" y2="160" stroke="#E2DDD6" strokeWidth="1" />

                {/* Cluster A - benign */}
                {[
                  [120, 60], [145, 75], [130, 90], [155, 65], [110, 80],
                ].map(([cx, cy], i) => (
                  <circle key={i} cx={cx} cy={cy} r="6" fill="#1D4ED8" fillOpacity="0.7" />
                ))}
                <text x="130" y="115" textAnchor="middle" fontSize="11" fill="#57534E" fontWeight="600">
                  Benign cluster
                </text>

                {/* Cluster B - ambiguous - overlapping */}
                {[
                  [210, 80], [230, 65], [195, 70], [220, 95], [245, 75],
                ].map(([cx, cy], i) => (
                  <circle key={i} cx={cx} cy={cy} r="6" fill="#B45309" fillOpacity="0.7" />
                ))}
                <text x="220" y="115" textAnchor="middle" fontSize="11" fill="#57534E" fontWeight="600">
                  Ambiguous
                </text>

                {/* Overlap region label */}
                <rect x="175" y="55" width="70" height="55" rx="6" fill="#FEF3C7" stroke="#FDE68A" strokeWidth="1.5" fillOpacity="0.5" />
                <text x="210" y="78" textAnchor="middle" fontSize="10" fill="#92400E" fontWeight="600">
                  Overlap
                </text>
                <text x="210" y="91" textAnchor="middle" fontSize="10" fill="#92400E">
                  region
                </text>

                {/* Cluster C - policy */}
                {[
                  [340, 70], [360, 85], [325, 80], [350, 58], [375, 75],
                ].map(([cx, cy], i) => (
                  <circle key={i} cx={cx} cy={cy} r="6" fill="#B91C1C" fillOpacity="0.7" />
                ))}
                <text x="350" y="115" textAnchor="middle" fontSize="11" fill="#57534E" fontWeight="600">
                  Policy-relevant
                </text>

                {/* Similarity arrow */}
                <line x1="160" y1="72" x2="195" y2="72" stroke="#78716C" strokeWidth="1.5" strokeDasharray="4,2" markerEnd="url(#arr)" />
                <defs>
                  <marker id="arr" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto">
                    <path d="M 0 0 L 6 3 L 0 6 z" fill="#78716C" />
                  </marker>
                </defs>
                <text x="177" y="68" textAnchor="middle" fontSize="9" fill="#78716C">
                  high sim
                </text>
              </svg>
              <p className="text-[12px] text-[#78716C] text-center mt-3">
                When safety categories overlap in embedding space, no single threshold can
                cleanly separate them.
              </p>
            </div>

            <p>
              The 2D map in this lab is a UMAP projection from 384 dimensions down to 2. UMAP
              preserves local neighborhood structure — points that appear close really are
              semantically similar. But global distances are distorted. Two clusters that look
              far apart may share more similarity than the map suggests.
            </p>

            <CareNote variant="warning">
              <strong>The map is not the territory.</strong> The layout is a teaching aid.
              Do not draw conclusions solely from the visual distance between points.
            </CareNote>
          </div>
        </Section>

        <div className="w-full h-px bg-[#E2DDD6]" />

        {/* ── 03 The Map ───────────────────────────────────────────── */}
        <Section id="map" num="03" title="The Map" wide>
          <CareNote className="mb-8">
            This map is not a classifier, not a moderation system, and not a ground-truth
            measure of risk. All examples are sanitized — no entry provides actionable guidance
            for causing harm. The goal is to show where category boundaries become geometrically
            ambiguous.
          </CareNote>

          <OverlapMap examples={examples} neighbors={neighbors} />
        </Section>

        <div className="w-full h-px bg-[#E2DDD6]" />

        {/* ── 04 Boundary Blur ─────────────────────────────────────── */}
        <Section id="blur" num="04" title="Boundary Blur" wide>
          <CareNote variant="warning" className="mb-8">
            <strong>High blur does not mean unsafe.</strong> Blur is a geometric property — it
            means the concept sits near multiple band centroids simultaneously, not that it is
            harmful. Many high-blur concepts are straightforwardly benign.
          </CareNote>

          <BoundaryBlur examples={examples} />
        </Section>

        <div className="w-full h-px bg-[#E2DDD6]" />

        {/* ── 05 Compare ───────────────────────────────────────────── */}
        <Section id="compare" num="05" title="Compare" wide>
          <ComparePanel examples={examples} neighbors={neighbors} />
        </Section>

        <div className="w-full h-px bg-[#E2DDD6]" />

        {/* ── 06 Safety ────────────────────────────────────────────── */}
        <Section id="safety" num="06" title="Why This Matters for Safety">
          <div className="space-y-5 text-[1.0625rem] text-[#1C1917] leading-[1.8]">
            <p>
              Safety categories rarely fail in neat boxes. When a classifier draws a line in
              embedding space, the line is straight. The actual distribution of harmful and
              benign content is not.
            </p>
            <p>
              This creates two structural problems. First, false positives: legitimate content
              that lives near restricted content gets caught by the same rule. A clinical
              description of a medical risk, a security researcher&apos;s explanation, a
              policy analysis of extremism — each can land near the content it discusses.
              Second, false negatives: harmful content that successfully adopts clinical or
              educational language can slip through a threshold that would have caught its more
              blunt predecessors.
            </p>
            <p>
              Neither problem is fully fixable by improving the threshold. Both are
              consequences of how the underlying representation space is shaped.
            </p>

            <CareNote variant="ethics">
              <strong>What this project is not saying.</strong> This is not an argument
              against safety systems. It is an argument for understanding their geometry —
              because understanding failure modes is a precondition for improving them.
              The goal is not certainty. The goal is a better starting point for reflection.
            </CareNote>

            <h3 className="text-[1.05rem] font-semibold text-[#1C1917] pt-2">
              Intended uses
            </h3>
            <ul className="list-none space-y-2 pl-0">
              {[
                "Researchers and students studying embedding-based classification",
                "Safety practitioners building intuition for where thresholds will fail",
                "Policy analysts explaining the representation overlap problem",
                "Educators building curricula around AI safety and dual-use technology",
              ].map((u) => (
                <li key={u} className="flex gap-2">
                  <span className="text-[#1D4ED8] mt-1 shrink-0">&#8594;</span>
                  <span>{u}</span>
                </li>
              ))}
            </ul>

            <h3 className="text-[1.05rem] font-semibold text-[#1C1917] pt-2">
              Not intended for
            </h3>
            <ul className="list-none space-y-2 pl-0">
              {[
                "Making moderation decisions — this is not a classifier",
                "Building training datasets — do not use this to label data",
                "Justifying restrictions or permissions based on proximity",
                "Claiming any safety system is correct or incorrect",
              ].map((u) => (
                <li key={u} className="flex gap-2">
                  <span className="text-[#B91C1C] mt-1 shrink-0">&#8594;</span>
                  <span>{u}</span>
                </li>
              ))}
            </ul>
          </div>
        </Section>

        <div className="w-full max-w-[68ch] mx-auto px-6">
          <div className="h-px bg-[#E2DDD6]" />
        </div>

        {/* ── 07 Methods ───────────────────────────────────────────── */}
        <Section id="methods" num="07" title="Methods">
          <div className="space-y-2">
            <MethodCard step="1" title="Hand-curated dataset">
              113 concept descriptions across 10 domains and 5 safety bands, written and
              reviewed individually. No entry provides actionable guidance for causing harm.
              Abstract risk placeholders name types of restricted content without reproducing
              them. Source:{" "}
              <code className="text-[12px] bg-[#F2EFE9] px-1.5 py-0.5 rounded border border-[#E2DDD6]">
                data/safe_examples_seed.csv
              </code>
            </MethodCard>

            <MethodCard step="2" title="Sentence embeddings">
              Embeddings computed using{" "}
              <strong>all-MiniLM-L6-v2</strong> from sentence-transformers — a
              general-purpose semantic similarity model producing 384-dimensional vectors.
              The model was not trained for safety classification. Its neighborhoods reflect
              general language statistics.
            </MethodCard>

            <MethodCard step="3" title="Cosine similarity matrix">
              Pairwise cosine similarities computed for all 113 examples, producing a
              113&times;113 matrix. The overlap score for each example is the fraction of
              its 10 nearest neighbors that belong to a different safety band.
            </MethodCard>

            <MethodCard step="4" title="UMAP projection">
              384-dimensional embeddings projected to 2D using UMAP (n_neighbors=15,
              min_dist=0.1, cosine metric, random_state=42). The 2D layout preserves local
              neighborhood structure but distorts global distances. If UMAP is unavailable,
              PCA is used as a fallback.
            </MethodCard>

            <MethodCard step="5" title="Boundary blur score">
              Normalized Shannon entropy of each example&apos;s cosine similarities to three
              reference band centroids (benign, ambiguous, policy-relevant). High entropy
              means the example sits roughly equidistant from all three centroids. This is an
              exploration heuristic — not a safety signal.
            </MethodCard>

            <MethodCard step="6" title="Static export">
              All artifacts are precomputed offline using the Python pipeline in{" "}
              <code className="text-[12px] bg-[#F2EFE9] px-1.5 py-0.5 rounded border border-[#E2DDD6]">
                scripts/
              </code>{" "}
              and exported to{" "}
              <code className="text-[12px] bg-[#F2EFE9] px-1.5 py-0.5 rounded border border-[#E2DDD6]">
                public/data/
              </code>
              . The web app loads JSON at build time. No model inference happens at runtime.
            </MethodCard>
          </div>

          <div className="mt-10 space-y-3 text-[0.9rem] text-[#57534E] leading-relaxed border-t border-[#E2DDD6] pt-6">
            <p className="font-semibold text-[#1C1917]">Limitations</p>
            <p>
              <strong>Projection distortion.</strong> The 2D map loses information. Points that
              appear close may be further apart in 384-dimensional space.
            </p>
            <p>
              <strong>Model bias.</strong> all-MiniLM-L6-v2 encodes the statistical patterns of
              its training corpus, including biases about language, framing, and domain. The
              neighborhoods reflect those biases.
            </p>
            <p>
              <strong>Non-representative dataset.</strong> 113 examples designed to illustrate
              overlap — not a sample of any real query distribution. Do not use as a benchmark.
            </p>
            <p>
              <strong>Editorial categories.</strong> The five safety bands are editorial
              judgments, not ground truth validated against any benchmark.
            </p>
          </div>
        </Section>

        <div className="w-full max-w-[68ch] mx-auto px-6">
          <div className="h-px bg-[#E2DDD6]" />
        </div>

        {/* ── 08 Start Here ────────────────────────────────────────── */}
        <Section id="start" num="08" title="Start Here">
          <div className="space-y-5 text-[1.0625rem] text-[#1C1917] leading-[1.8]">
            <p className="text-[#57534E]">
              If you want to go deeper on representation, safety, or the ideas behind this
              lab, here are honest starting points.
            </p>

            <div className="space-y-4">
              {[
                {
                  title: "Representation Engineering (Zou et al., 2023)",
                  note: "Introduces a framework for understanding AI behavior through linear representations. Directly relevant to why embedding geometry matters for safety.",
                },
                {
                  title: "Towards Monosemanticity (Anthropic, 2023)",
                  note: "Shows that model internals are more entangled than clean feature boundaries suggest — the representational version of the overlap problem.",
                },
                {
                  title: "Sentence-BERT (Reimers & Gurevych, 2019)",
                  note: "The technical foundation for all-MiniLM-L6-v2. Understanding how the model was trained clarifies what its neighborhoods actually reflect.",
                },
                {
                  title: "UMAP: Uniform Manifold Approximation and Projection (McInnes et al., 2018)",
                  note: "The algorithm used for 2D projection. Knowing its assumptions — especially that it distorts global distances — is important for reading the map correctly.",
                },
                {
                  title: "On the Dangers of Stochastic Parrots (Bender et al., 2021)",
                  note: "Raises questions about what large language models encode and reproduce. Relevant to understanding what semantic embedding spaces actually contain.",
                },
              ].map((ref) => (
                <div
                  key={ref.title}
                  className="border-b border-[#E2DDD6] pb-4 last:border-0 last:pb-0"
                >
                  <p className="font-semibold text-[#1C1917] text-[15px] mb-0.5">{ref.title}</p>
                  <p className="text-[14px] text-[#57534E] leading-relaxed">{ref.note}</p>
                </div>
              ))}
            </div>

            <CareNote variant="info" className="mt-6">
              <strong>Feedback is welcome.</strong> If you find an example that crossed a line,
              a score that seems wrong, or a framing that could be more careful — open an issue
              on GitHub. The dataset is a plain CSV file and is easy to audit.
            </CareNote>
          </div>
        </Section>
      </main>

      <Footer />
    </>
  );
}
