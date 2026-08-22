import { Link } from "react-router-dom";

type LogoProps = {
  compact?: boolean;
};

export function Logo({ compact = false }: LogoProps) {
  return (
    <Link to="/" className="focus-ring inline-flex items-center gap-2.5 rounded-full">
      <span
        aria-hidden="true"
        className="grid h-9 w-9 place-items-center rounded-2xl bg-gradient-to-br from-sky-400 to-violet-500 text-white shadow-glow"
      >
        <svg viewBox="0 0 32 32" className="h-5 w-5" fill="none">
          <circle cx="16" cy="16" r="10" stroke="currentColor" strokeWidth="2" />
          <circle cx="16" cy="16" r="4.5" stroke="currentColor" strokeWidth="2" />
          <path d="M23 23l5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </span>
      <span className="font-bold tracking-tight text-ink-950 dark:text-white">
        CareerLens <span className="text-brand-500">AI</span>
        {!compact && <span className="ml-2 hidden text-sm font-medium text-ink-500 sm:inline">Resume check</span>}
      </span>
    </Link>
  );
}
