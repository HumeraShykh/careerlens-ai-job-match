import { formatPercent, scoreTone } from "../lib/format";

const COLORS = {
  excellent: "#14B8A6",
  strong: "#4F7CFF",
  moderate: "#F59E0B",
  needs: "#F43F5E",
};

type ScoreRingProps = {
  score: number;
  label?: string;
};

export function ScoreRing({ score, label = "Match" }: ScoreRingProps) {
  const tone = scoreTone(score);
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.max(0, Math.min(score, 100)) / 100) * circumference;

  return (
    <div className="relative grid place-items-center">
      <svg viewBox="0 0 160 160" className="h-44 w-44 -rotate-90 sm:h-52 sm:w-52" role="img" aria-label={`${formatPercent(score)} ${label}`}>
        <circle cx="80" cy="80" r={radius} fill="none" stroke="currentColor" strokeWidth="12" className="text-black/5 dark:text-white/10" />
        <circle
          cx="80"
          cy="80"
          r={radius}
          fill="none"
          stroke={COLORS[tone]}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="absolute text-center">
        <p className="text-5xl font-extrabold tracking-tight text-ink-950 dark:text-white sm:text-6xl">{formatPercent(score)}</p>
        <p className="mt-1 text-sm text-ink-500">{label}</p>
      </div>
    </div>
  );
}
