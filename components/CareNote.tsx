import { ReactNode } from "react";
import clsx from "clsx";

type Variant = "default" | "warning" | "info" | "ethics";

const BORDER_STYLES: Record<Variant, string> = {
  default: "border-[#C2411C]",
  warning: "border-[#B45309]",
  info: "border-[#1D4ED8]",
  ethics: "border-[#6D28D9]",
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
    <aside
      className={clsx(
        "border-l-[3px] pl-5 py-1 my-8",
        BORDER_STYLES[variant],
        className
      )}
    >
      <div
        className="text-[1.0625rem] leading-[1.8] text-[#5C5A54]"
        style={{
          fontFamily:
            "var(--font-lora), Georgia, Cambria, 'Times New Roman', Times, serif",
        }}
      >
        {children}
      </div>
    </aside>
  );
}
