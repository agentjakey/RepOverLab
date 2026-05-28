"use client";

import { useState } from "react";

const NAV_ITEMS = [
  { href: "#idea", label: "The Idea" },
  { href: "#geometry", label: "Geometry" },
  { href: "#map", label: "The Map" },
  { href: "#blur", label: "Boundary Blur" },
  { href: "#compare", label: "Compare" },
  { href: "#safety", label: "Safety" },
  { href: "#methods", label: "Methods" },
  { href: "#start", label: "Start Here" },
];

export default function Nav() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#F7F5F0]/95 backdrop-blur border-b border-[#EAE7E0]">
      <div className="max-w-[1100px] mx-auto px-6 h-14 flex items-center justify-between">
        <a href="#top" className="group flex items-center">
          <span className="text-[11px] font-semibold tracking-widest uppercase text-[#79746E] group-hover:text-[#1A1917] transition-colors">
            Latent Space Lab
          </span>
          <span className="mx-2 text-[#C4C0BB] text-[10px]">/</span>
          <span className="text-[11px] font-semibold tracking-wider uppercase text-[#1A1917]">
            Representation Overlap
          </span>
        </a>

        <nav className="hidden md:flex items-center gap-6">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-[12px] font-medium text-[#5C5751] hover:text-[#1A1917] transition-colors"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <button
          onClick={() => setOpen(!open)}
          className="md:hidden p-2 text-[#5C5751] hover:text-[#1A1917] transition-colors"
          aria-label="Toggle menu"
        >
          <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
            {open ? (
              <>
                <line x1="4" y1="4" x2="14" y2="14" />
                <line x1="14" y1="4" x2="4" y2="14" />
              </>
            ) : (
              <>
                <line x1="3" y1="5" x2="15" y2="5" />
                <line x1="3" y1="9" x2="15" y2="9" />
                <line x1="3" y1="13" x2="15" y2="13" />
              </>
            )}
          </svg>
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-[#EAE7E0] bg-[#F7F5F0]">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={() => setOpen(false)}
              className="block px-6 py-3 text-[13px] text-[#5C5751] hover:text-[#1A1917] transition-colors"
            >
              {item.label}
            </a>
          ))}
        </div>
      )}
    </header>
  );
}
