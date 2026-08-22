import { Trophy } from "lucide-react";
import { ScoreRing } from "./ScoreRing";
import { SkillChips } from "./SkillChips";
import { formatPercent, scoreTone } from "../lib/format";
import type { CompareResult } from "../types";

const TONE_COPY = {
  excellent: "text-teal-700 dark:text-teal-200",
  strong: "text-brand-700 dark:text-brand-100",
  moderate: "text-amber-700 dark:text-amber-200",
  needs: "text-rose-700 dark:text-rose-200",
};

type CompareResultsProps = {
  result: CompareResult;
};

export function CompareResults({ result }: CompareResultsProps) {
  const best = result.jobs[0];
  const tone = scoreTone(best.score);

  return (
    <>
      <div className="text-center">
        <h1 className="text-3xl font-extrabold text-ink-950 dark:text-white">Which job fits better?</h1>
        <p className="mt-2 text-sm leading-6 text-ink-500">{result.summary}</p>
      </div>

      <section className="glass-card mt-6 rounded-[2rem] px-6 py-8 text-center">
        <p className="inline-flex items-center gap-2 rounded-full bg-teal-500/15 px-3 py-1 text-xs font-semibold text-teal-800 dark:text-teal-100">
          <Trophy className="h-3.5 w-3.5" />
          Best fit
        </p>
        <p className="mt-3 text-lg font-semibold text-ink-950 dark:text-white">
          {best.job_title_guess ?? best.label}
        </p>
        <div className="mt-4">
          <ScoreRing score={best.score} label="Match" />
        </div>
        <p className={`mt-2 text-lg font-semibold ${TONE_COPY[tone]}`}>{best.match_title}</p>
      </section>

      <section className="mt-6 space-y-4">
        {result.jobs.map((job) => (
          <article
            key={job.label}
            className={`glass-card rounded-3xl p-5 ${job.is_best ? "ring-2 ring-teal-400/70" : ""}`}
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
                  #{job.rank} · {job.label}
                </p>
                <h2 className="mt-1 text-lg font-semibold text-ink-950 dark:text-white">
                  {job.job_title_guess ?? job.label}
                </h2>
                <p className="mt-1 text-sm text-ink-500">{job.match_title}</p>
              </div>
              <p className="text-2xl font-extrabold text-ink-950 dark:text-white">{formatPercent(job.score)}</p>
            </div>

            <p className="mt-3 text-sm leading-6 text-ink-700 dark:text-slate-300">{job.experience}</p>

            <div className="mt-4">
              <p className="text-sm font-semibold text-ink-950 dark:text-white">Matching skills</p>
              <div className="mt-2">
                <SkillChips skills={job.matched_skills} empty="No matching skills were found in this job text." />
              </div>
            </div>

            <div className="mt-4">
              <p className="text-sm font-semibold text-ink-950 dark:text-white">Skills to improve</p>
              <div className="mt-2">
                <SkillChips
                  skills={job.missing_skills}
                  tone="missing"
                  empty="No extra job skills look missing."
                />
              </div>
            </div>

            {job.improve.length > 0 && (
              <ul className="mt-4 space-y-2 text-sm leading-6 text-ink-700 dark:text-slate-300">
                {job.improve.slice(0, 2).map((tip) => (
                  <li key={tip}>{tip}</li>
                ))}
              </ul>
            )}
          </article>
        ))}
      </section>
    </>
  );
}
