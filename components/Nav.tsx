"use client";

import { useState } from "react";
import clsx from "clsx";

const NAV_ITEMS = [
  { href: "#idea", label: "The Idea" },
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
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#F8F6F1]/95 backdrop-blur border-b border-[#E2DDD6]">
      <div className="max-w-[1100px] mx-auto px-6 h-16 flex items-center justify-between">
        {/* Wordmark */}
        <a href="#top" className="flex items-center gap-2 group">
          <span className="text-[11px] font-semibold tracking-widest uppercase text-[#57534E] group-hover:text-[#1C1917] transition-colors">
            Latent Space Lab
          </span>
          <span className="w-px h-4 bg-[#E2DDD6]" />
          <span className="text-[13px] font-semibold text-[#1C1917]">
            Representation Overlap
          </span>
        </a>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="px-3 py-1.5 rounded-md text-[13px] font-medium text-[#57534E] hover:text-[#1C1917] hover:bg-[#F2EFE9] transition-colors"
            >
              {item.label}
            </a>
          ))}
        </nav>

        {/* Mobile hamburger */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden p-2 rounded-md text-[#57534E] hover:text-[#1C1917] hover:bg-[#F2EFE9]"
          aria-label="Toggle menu"
        >
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            {open ? (
              <>
                <line x1="4" y1="4" x2="16" y2="16" />
                <line x1="16" y1="4" x2="4" y2="16" />
              </>
            ) : (
              <>
                <line x1="3" y1="6" x2="17" y2="6" />
                <line x1="3" y1="12" x2="17" y2="12" />
                <line x1="3" y1="18" x2="17" y2="18" />
              </>
            )}
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden border-t border-[#E2DDD6] bg-[#F8F6F1]">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={() => setOpen(false)}
              className="block px-6 py-3 text-[14px] font-medium text-[#57534E] hover:text-[#1C1917] hover:bg-[#F2EFE9] transition-colors"
            >
              {item.label}
            </a>
          ))}
        </div>
      )}
    </header>
  );
}
