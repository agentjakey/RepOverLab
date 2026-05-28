const SIBLING_PROJECTS = [
  {
    label: "Representation Overlap Lab",
    href: "https://representation-overlap-lab.vercel.app/",
  },
  {
    label: "Failure Mode Atlas",
    href: "https://failuremodeatlas.vercel.app/",
  },
  {
    label: "CoT Faithfulness",
    href: "https://cot-faithfulness.vercel.app/",
  },
  {
    label: "Neural Polysemanticity",
    href: "https://neural-polysemanticity.vercel.app/",
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-[#E4E2DB] bg-[#F0EDE8] mt-0">
      <div className="max-w-[720px] mx-auto px-6 pt-12 pb-10">

        {/* Top two-column grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-10 mb-10">

          {/* About */}
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-widest text-[#79746E] mb-3">
              About
            </p>
            <p className="text-[13px] text-[#5C5A54] leading-relaxed">
              Built by{" "}
            <a
              href="https://www.linkedin.com/in/jacob-ortiz-ab6421348/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline underline-offset-2 hover:text-[#1A1915] transition-colors"
            >
              Jacob Ortiz
            </a>{" "}
            as a learning tool and public-interest resource.
              Representation Overlap Lab explores how embedding geometry can blur
              boundaries between benign, ambiguous, policy-relevant, and harmful-seeming
              concepts. It is an educational visualization, not a safety classifier,
              moderation system, or benchmark.
            </p>
          </div>

          {/* Sibling projects */}
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-widest text-[#79746E] mb-3">
              Sibling Projects
            </p>
            <ul className="space-y-2">
              {SIBLING_PROJECTS.map((p) => (
                <li key={p.href}>
                  <a
                    href={p.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[13px] text-[#5C5A54] underline underline-offset-2 hover:text-[#1A1915] transition-colors"
                  >
                    {p.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-[#E4E2DB] mb-8" />

        {/* About this project */}
        <div className="mb-8">
          <p className="text-[10px] font-semibold uppercase tracking-widest text-[#79746E] mb-3">
            About This Project
          </p>
          <p className="text-[13px] text-[#5C5A54] leading-relaxed">
            Built as part of a broader effort to learn AI safety in public, make
            difficult concepts more accessible, and invite careful feedback. The map is
            not the territory, but it can help you ask better questions.
          </p>
        </div>

        {/* Bottom meta */}
        <p className="text-[12px] text-[#79746E] mb-3">
          Last updated: May 2026 &middot; MIT License &middot;{" "}
          <a
            href="https://github.com/agentjakey/RepOverLab"
            target="_blank"
            rel="noopener noreferrer"
            className="underline underline-offset-2 hover:text-[#1A1915] transition-colors"
          >
            GitHub
          </a>
        </p>
        <p className="text-[12px] text-[#79746E]">
          If this was useful, you can{" "}
          <a
            href="https://ko-fi.com/agentjakey"
            target="_blank"
            rel="noopener noreferrer"
            className="underline underline-offset-2 hover:text-[#1A1915] transition-colors"
          >
            support my work on Ko-fi
          </a>
          .
        </p>

      </div>
    </footer>
  );
}
