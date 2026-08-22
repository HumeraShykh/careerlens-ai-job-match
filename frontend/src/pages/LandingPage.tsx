import { Link } from "react-router-dom";
import { ArrowRight, FileUp, Sparkles, WandSparkles } from "lucide-react";

const steps = [
  { n: "1", title: "Add your resume", body: "Upload a file or paste the text." },
  { n: "2", title: "Paste 1–3 jobs", body: "Check one posting, or compare two or three with the same resume." },
  { n: "3", title: "See the best fit", body: "Get a score, missing skills, and a ranked winner." },
];

export function LandingPage() {
  return (
    <div className="px-4 pb-16 sm:px-6">
      <section className="mx-auto max-w-3xl pt-12 text-center sm:pt-16">
        <p className="inline-flex items-center gap-2 rounded-full bg-white/70 px-3 py-1 text-sm font-medium text-brand-700 shadow-sm dark:bg-white/10 dark:text-brand-100">
          <Sparkles className="h-4 w-4" />
          Easy resume check
        </p>
        <h1 className="mt-5 text-4xl font-extrabold tracking-tight text-ink-950 dark:text-white sm:text-6xl">
          Does your resume fit this job?
        </h1>
        <p className="mx-auto mt-4 max-w-xl text-base leading-7 text-ink-700 dark:text-slate-300 sm:text-lg">
          Upload your resume, paste a job description, and get a clear match score in seconds. Choosing between roles? Compare 2–3 jobs with the same resume.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            to="/analyze"
            className="focus-ring btn-glossy inline-flex items-center gap-2 rounded-full px-6 py-3.5 text-base font-semibold"
          >
            Check my resume <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/analyze?demo=1"
            className="focus-ring inline-flex items-center gap-2 rounded-full bg-white/80 px-6 py-3.5 text-base font-semibold text-ink-900 shadow-sm dark:bg-white/10 dark:text-white"
          >
            <WandSparkles className="h-4 w-4 text-brand-500" />
            Try a sample
          </Link>
          <Link
            to="/analyze?compare=1"
            className="focus-ring inline-flex items-center gap-2 rounded-full bg-brand-50 px-6 py-3.5 text-base font-semibold text-brand-700 dark:bg-white/10 dark:text-brand-100"
          >
            Compare two jobs
          </Link>
        </div>
      </section>

      <section className="mx-auto mt-12 max-w-md">
        <div className="glass-card rounded-[2rem] p-6 text-left">
          <div className="flex items-center justify-between">
            <p className="text-sm text-ink-500">Sample match</p>
            <span className="rounded-full bg-teal-500/15 px-3 py-1 text-xs font-semibold text-teal-700">Looks good</span>
          </div>
          <p className="mt-4 text-6xl font-extrabold tracking-tight text-ink-950 dark:text-white">78%</p>
          <p className="mt-1 text-sm text-ink-500">Software Engineer role</p>
          <div className="mt-5 h-3 overflow-hidden rounded-full bg-brand-50 dark:bg-white/10">
            <div className="h-full rounded-full bg-gradient-to-r from-sky-400 to-violet-500" style={{ width: "78%" }} />
          </div>
          <div className="mt-5 flex flex-wrap gap-2">
            {["React", "TypeScript", "SQL"].map((skill) => (
              <span key={skill} className="rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700 dark:bg-white/10 dark:text-brand-100">
                {skill}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto mt-14 grid max-w-4xl gap-4 sm:grid-cols-3" id="how-it-works">
        {steps.map((step) => (
          <article key={step.n} className="glass-card rounded-3xl p-5 text-center sm:text-left">
            <p className="mx-auto grid h-9 w-9 place-items-center rounded-full bg-brand-500 text-sm font-bold text-white sm:mx-0">
              {step.n}
            </p>
            <h2 className="mt-3 text-lg font-semibold text-ink-950 dark:text-white">{step.title}</h2>
            <p className="mt-1 text-sm leading-6 text-ink-500">{step.body}</p>
          </article>
        ))}
      </section>

      <section className="mx-auto mt-10 max-w-3xl glass-card rounded-[2rem] p-6 text-center">
        <FileUp className="mx-auto h-6 w-6 text-brand-500" />
        <h2 className="mt-3 text-xl font-semibold text-ink-950 dark:text-white">Your file stays private</h2>
        <p className="mt-2 text-sm leading-6 text-ink-500">
          We read the resume to score it, then discard the file. This is a practice tool, not an official ATS score.
        </p>
      </section>
    </div>
  );
}
