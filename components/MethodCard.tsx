import { ReactNode } from "react";

interface Props {
  step: string;
  title: string;
  children: ReactNode;
}

export default function MethodCard({ step, title, children }: Props) {
  return (
    <div className="flex gap-4 py-5 border-b border-[#E2DDD6] last:border-0">
      <div className="shrink-0">
        <div className="w-9 h-9 rounded-full bg-[#F2EFE9] border border-[#E2DDD6] flex items-center justify-center">
          <span className="text-[12px] font-bold text-[#57534E]">{step}</span>
        </div>
      </div>
      <div>
        <h4 className="font-semibold text-[#1C1917] text-[15px] mb-1">{title}</h4>
        <div className="text-[14px] text-[#57534E] leading-relaxed">{children}</div>
      </div>
    </div>
  );
}
