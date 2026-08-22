import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { RefreshCw } from "lucide-react";
import { CompareResults } from "../components/CompareResults";
import { ErrorBanner } from "../components/ErrorBanner";
import { ScoreRing } from "../components/ScoreRing";
import { SkillChips } from "../components/SkillChips";
import { scoreTone } from "../lib/format";
import { loadSession, type StoredSession } from "../lib/storage";
import type { AnalysisResult } from "../types";

const TONE_COPY = {
  excellent: "text-teal-700 dark:text-teal-200",
  strong: "text-brand-700 dark:text-brand-100",
  moderate: "text-amber-700 dark:text-amber-200",
  needs: "text-rose-700 dark:text-rose-200",
};

function easyTitle(result: AnalysisResult): string {
  return result.plain_summary?.match_title ?? simpleTitle(result.breakdown.overall);
}

function easyBlurb(result: AnalysisResult): string {
  return result.plain_summary?.match_blurb ?? "Here is a simple reading of your resume against this job.";
}

function simpleTitle(score: number): string {
  if (score >= 80) return "Strong match";
  if (score >= 65) return "Good match";
  if (score >= 45) return "Okay match";
  return "Weak match";
}

function SingleResult({ result }: { result: AnalysisResult }) {
  const tone = scoreTone(result.breakdown.overall);
  const jobTooShort = result.plain_summary?.job_too_short ?? result.job_word_count < 80;
  const experience =
    result.plain_summary?.experience ?? "This job did not clearly say how many years of experience it wants.";
  const improve = result.plain_summary?.improve?.length
    ? result.plain_summary.improve
    : result.missing_skills.length
      ? [`If you really have these skills, add them clearly: ${result.missing_skills.map((skill) => skill.name).slice(0, 5).join(", ")}.`]
      : ["Keep the resume honest. Only add skills you can talk about in an interview."];

  return (
    <>
      <div className="text-center">
        <h1 className="text-3xl font-extrabold text-ink-950 dark:text-white">Your simple result</h1>
        <p className="mt-2 text-sm leading-6 text-ink-500">{easyBlurb(result)}</p>
        <p className="mt-1 text-lg font-semibold text-brand-600">{easyTitle(result)}</p>
      </div>

      <section className="glass-card mt-6 rounded-[2rem] px-6 py-8 text-center">
        <ScoreRing score={result.breakdown.overall} label="Match" />
        <p className={`mt-2 text-lg font-semibold ${TONE_COPY[tone]}`}>{easyTitle(result)}</p>
      </section>

      {jobTooShort && (
        <div className="mt-4 rounded-3xl bg-amber-50 px-4 py-4 text-sm leading-6 text-amber-900 dark:bg-amber-500/15 dark:text-amber-100">
          This job text is too short, so the result is weak. Paste the <strong>full job posting</strong> (duties + requirements) and check again.
        </div>
      )}

      <section className="glass-card mt-4 rounded-3xl p-5">
        <h2 className="text-lg font-semibold text-ink-950 dark:text-white">Your matching skills</h2>
        <p className="mt-1 text-sm text-ink-500">These job skills are already in your resume.</p>
        <div className="mt-4">
          <SkillChips skills={result.matched_skills} empty="No matching skills were found in this job text." />
        </div>
      </section>

      <section className="glass-card mt-4 rounded-3xl p-5">
        <h2 className="text-lg font-semibold text-ink-950 dark:text-white">Skills to improve</h2>
        <p className="mt-1 text-sm text-ink-500">Add these only if you really have them. Do not fake skills.</p>
        <div className="mt-4">
          <SkillChips
            skills={result.missing_skills}
            tone="missing"
            empty="No extra job skills look missing."
          />
        </div>
      </section>

      <section className="glass-card mt-4 rounded-3xl p-5">
        <h2 className="text-lg font-semibold text-ink-950 dark:text-white">Experience needed</h2>
        <p className="mt-2 text-sm leading-6 text-ink-700 dark:text-slate-300">{experience}</p>
      </section>

      <section className="mt-4 space-y-3">
        <h2 className="text-lg font-semibold text-ink-950 dark:text-white">What to do next</h2>
        {improve.map((tip) => (
          <article key={tip} className="glass-card rounded-3xl p-5 text-sm leading-6 text-ink-700 dark:text-slate-300">
            {tip}
          </article>
        ))}
      </section>
    </>
  );
}

export function ResultsPage() {
  const navigate = useNavigate();
  const [session, setSession] = useState<StoredSession | null>(null);

  useEffect(() => {
    setSession(loadSession());
  }, []);

  if (!session) {
    return (
      <div className="mx-auto max-w-lg px-4 py-16 text-center">
        <ErrorBanner title="No result yet" message="Check a resume first." />
        <Link to="/analyze" className="mt-6 inline-flex font-semibold text-brand-600">
          Go back
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-xl px-4 py-8 sm:px-6">
      {session.kind === "compare" ? <CompareResults result={session.result} /> : <SingleResult result={session.result} />}

      <button
        type="button"
        onClick={() => navigate("/analyze")}
        className="focus-ring btn-glossy mt-8 flex w-full items-center justify-center gap-2 rounded-full py-3.5 text-base font-semibold"
      >
        <RefreshCw className="h-4 w-4" />
        {session.kind === "compare" ? "Compare other jobs" : "Check again with the full job"}
      </button>
    </div>
  );
}
