import { ReactNode } from "react";
import clsx from "clsx";

type Variant = "default" | "warning" | "info" | "ethics";

const STYLES: Record<Variant, string> = {
  default: "border-[#B91C1C] bg-[#FEF2F2] text-[#7F1D1D]",
  warning: "border-[#B45309] bg-[#FFFBEB] text-[#78350F]",
  info: "border-[#1D4ED8] bg-[#EFF6FF] text-[#1E3A8A]",
  ethics: "border-[#6D28D9] bg-[#F5F3FF] text-[#4C1D95]",
};

export default function CareNote({
  children,
  variant = "default",
  className,
}: {
  children: ReactNode;
  variant?: Variant;
  className?: string;
}) {
  return (
    <div
      className={clsx(
        "border-l-[3px] px-4 py-3 rounded-r-md text-[0.9rem] leading-relaxed my-6",
        STYLES[variant],
        className
      )}
    >
      {children}
    </div>
  );
}
