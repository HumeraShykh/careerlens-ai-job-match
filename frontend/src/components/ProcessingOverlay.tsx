const ANALYZE_STEPS = ["Reading your resume", "Comparing with the job", "Preparing simple tips"];
const COMPARE_STEPS = ["Reading your resume", "Scoring each job", "Ranking the best fit"];

type ProcessingOverlayProps = {
  step: number;
  comparing?: boolean;
};

export function ProcessingOverlay({ step, comparing = false }: ProcessingOverlayProps) {
  const steps = comparing ? COMPARE_STEPS : ANALYZE_STEPS;
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-[#152033]/40 px-4 backdrop-blur-md" role="status" aria-live="polite">
      <div className="glass-card w-full max-w-sm rounded-[2rem] p-6 text-center">
        <p className="text-sm font-semibold text-brand-600">Just a moment</p>
        <h2 className="mt-2 text-2xl font-bold text-ink-950 dark:text-white">
          {comparing ? "Comparing your jobs" : "Checking your match"}
        </h2>
        <ul className="mt-6 space-y-3 text-left">
          {steps.map((label, index) => {
            const active = index === step;
            const done = index < step;
            return (
              <li key={label} className="flex items-center gap-3 text-sm">
                <span
                  className={`grid h-6 w-6 place-items-center rounded-full text-[11px] font-semibold ${
                    done || active ? "bg-brand-500 text-white" : "bg-black/5 text-ink-500 dark:bg-white/10"
                  }`}
                >
                  {index + 1}
                </span>
                <span className={active ? "font-semibold text-ink-950 dark:text-white" : "text-ink-500"}>{label}</span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
