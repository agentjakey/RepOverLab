import clsx from "clsx";
import { ReactNode } from "react";

interface SectionProps {
  id: string;
  num: string;
  title: string;
  wide?: boolean;
  children: ReactNode;
  className?: string;
}

export default function Section({
  id,
  num,
  title,
  wide = false,
  children,
  className,
}: SectionProps) {
  return (
    <section id={id} className={clsx("py-20 px-6", className)}>
      <div className={clsx(wide ? "lab-col" : "prose-col")}>
        <div className="mb-10">
          <p className="section-num mb-2">{num}</p>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#1C1917] tracking-tight leading-snug">
            {title}
          </h2>
        </div>
        {children}
      </div>
    </section>
  );
}
