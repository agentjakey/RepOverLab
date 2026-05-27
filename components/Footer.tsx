export default function Footer() {
  return (
    <footer className="border-t border-[#E2DDD6] bg-[#F2EFE9] mt-24 py-12 px-6">
      <div className="max-w-[68ch] mx-auto">
        <p className="text-[12px] font-semibold uppercase tracking-widest text-[#57534E] mb-3">
          Latent Space Lab
        </p>
        <p className="text-[14px] text-[#57534E] leading-relaxed mb-4">
          Representation Overlap Lab is an educational visualization. It is not a safety
          classifier, not a moderation system, and not a ground-truth measure of risk.
          The map is a teaching aid. The goal is better intuition, not certainty.
        </p>
        <p className="text-[13px] text-[#78716C]">
          Built with open data, sanitized examples, and publicly available tools.
          Dataset:{" "}
          <code className="text-[12px] bg-white px-1.5 py-0.5 rounded border border-[#E2DDD6]">
            data/safe_examples_seed.csv
          </code>{" "}
          &mdash; 113 hand-reviewed concept descriptions.
        </p>
        <p className="text-[12px] text-[#78716C] mt-4">
          &copy; {new Date().getFullYear()} &middot; MIT License &middot;{" "}
          <a
            href="https://github.com/agentjakey/representation-overlap-lab"
            className="underline hover:text-[#1C1917] transition-colors"
          >
            GitHub
          </a>
        </p>
      </div>
    </footer>
  );
}
