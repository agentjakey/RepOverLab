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
    <section id={id} className={clsx("py-20 px-6 border-b border-[#E4E2DB]", className)}>
      <div className={clsx(wide ? "lab-col" : "prose-col")}>
        <div className="mb-12">
          <p className="section-num mb-3">{num}</p>
          <h2 className="section-title">{title}</h2>
        </div>
        {children}
      </div>
    </section>
  );
}
