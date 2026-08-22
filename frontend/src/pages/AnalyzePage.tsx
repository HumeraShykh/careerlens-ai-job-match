import { useEffect, useState, type FormEvent } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Plus, Sparkles } from "lucide-react";
import { ErrorBanner } from "../components/ErrorBanner";
import { JobEditor } from "../components/JobEditor";
import { ProcessingOverlay } from "../components/ProcessingOverlay";
import { ResumeUploader } from "../components/ResumeUploader";
import { AI_ENGINEER_SAMPLE_JOB, FRONTEND_SAMPLE_JOB, JAVA_SAMPLE_JOB } from "../data/sampleJob";
import { CareerLensApiError, analyzeResume, compareJobs, getSamples } from "../lib/api";
import { wordCount } from "../lib/format";
import { storeSession } from "../lib/storage";

const JOB_SLOTS = [
  {
    sample: AI_ENGINEER_SAMPLE_JOB,
    sampleLabel: "Use AI Engineer sample",
    title: "Job 1",
    hint: "Paste the posting, especially the requirements.",
  },
  {
    sample: FRONTEND_SAMPLE_JOB,
    sampleLabel: "Use Frontend sample",
    title: "Job 2",
    hint: "Optional. Add a second posting to see which job fits better.",
  },
  {
    sample: JAVA_SAMPLE_JOB,
    sampleLabel: "Use Java sample",
    title: "Job 3",
    hint: "Optional. Add a third posting if you are choosing among three roles.",
  },
] as const;

export function AnalyzePage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [mode, setMode] = useState<"file" | "paste">("file");
  const [file, setFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [jobs, setJobs] = useState(["", "", ""]);
  const [visibleJobs, setVisibleJobs] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0);
  const [sampleReady, setSampleReady] = useState(false);

  const filledJobs = jobs.slice(0, visibleJobs).filter((job) => wordCount(job) >= 40);
  const comparing = filledJobs.length >= 2;

  useEffect(() => {
    if (!busy) return undefined;
    const timer = window.setInterval(() => {
      setStep((current) => (current < 2 ? current + 1 : current));
    }, 500);
    return () => window.clearInterval(timer);
  }, [busy]);

  function setJobAt(index: number, value: string) {
    setJobs((current) => current.map((job, jobIndex) => (jobIndex === index ? value : job)));
  }

  async function loadSampleResume() {
    try {
      const samples = await getSamples();
      setMode("paste");
      setResumeText(samples.resume.text);
      setFile(null);
      setError(null);
      return samples;
    } catch {
      setError("Could not load the sample. You can still paste your own resume.");
      return null;
    }
  }

  async function loadFullSample() {
    const samples = await loadSampleResume();
    setJobAt(0, samples?.job_description.text ?? AI_ENGINEER_SAMPLE_JOB);
    setVisibleJobs(1);
    setSampleReady(true);
  }

  async function loadCompareSamples() {
    await loadSampleResume();
    setJobs([AI_ENGINEER_SAMPLE_JOB, FRONTEND_SAMPLE_JOB, ""]);
    setVisibleJobs(2);
    setSampleReady(true);
  }

  useEffect(() => {
    if (searchParams.get("demo") === "1") {
      void loadFullSample();
    }
    if (searchParams.get("compare") === "1") {
      void loadCompareSamples();
    }
    // Run once when opened from the landing sample buttons.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (mode === "file" && !file) {
      setError("Please upload a resume, or tap Try a sample.");
      return;
    }
    if (mode === "paste" && resumeText.trim().length < 40) {
      setError("Please paste more resume text, or upload a file.");
      return;
    }

    const visible = jobs.slice(0, visibleJobs);
    if (wordCount(visible[0]) < 40) {
      setError("Please paste the full first job posting, including requirements. One short line is not enough.");
      return;
    }
    for (let index = 1; index < visible.length; index += 1) {
      const words = wordCount(visible[index]);
      if (words > 0 && words < 40) {
        setError(`Job ${index + 1} is too short. Paste the full posting, or remove that job.`);
        return;
      }
    }

    setBusy(true);
    setStep(0);
    setError(null);
    try {
      const resumeInput = {
        resumeFile: mode === "file" ? file : null,
        resumeText: mode === "paste" ? resumeText : undefined,
      };
      if (comparing) {
        const result = await compareJobs({ jobs: filledJobs, ...resumeInput });
        storeSession({ kind: "compare", result });
      } else {
        const result = await analyzeResume({ jobDescription: visible[0], ...resumeInput });
        storeSession({ kind: "single", result });
      }
      navigate("/results");
    } catch (err) {
      const message = err instanceof CareerLensApiError ? err.message : "Something went wrong. Is the backend running?";
      setError(message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 sm:py-10">
      {busy && <ProcessingOverlay step={step} comparing={comparing} />}
      <div className="text-center">
        <h1 className="text-3xl font-extrabold tracking-tight text-ink-950 dark:text-white sm:text-4xl">Check jobs in 2 steps</h1>
        <p className="mt-2 text-sm leading-6 text-ink-500">
          Upload your resume, then paste one job — or add a second job to see which posting fits better.
        </p>
        <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
          <button
            type="button"
            onClick={() => void loadFullSample()}
            className="focus-ring inline-flex items-center gap-2 rounded-full bg-white/80 px-5 py-2.5 text-sm font-semibold text-ink-900 shadow-sm dark:bg-white/10 dark:text-white"
          >
            <Sparkles className="h-4 w-4 text-brand-500" />
            {sampleReady ? "Sample loaded" : "Try a sample first"}
          </button>
          <button
            type="button"
            onClick={() => void loadCompareSamples()}
            className="focus-ring inline-flex items-center gap-2 rounded-full bg-brand-50 px-5 py-2.5 text-sm font-semibold text-brand-700 dark:bg-white/10 dark:text-brand-100"
          >
            Compare two sample jobs
          </button>
        </div>
      </div>

      <form onSubmit={onSubmit} className="mt-8 space-y-5">
        <div className="flex items-center gap-2 text-sm font-semibold text-ink-700 dark:text-slate-200">
          <span className="grid h-7 w-7 place-items-center rounded-full bg-brand-500 text-xs text-white">1</span>
          Add resume
        </div>
        <ResumeUploader
          file={file}
          resumeText={resumeText}
          mode={mode}
          onModeChange={setMode}
          onFileChange={setFile}
          onTextChange={setResumeText}
          onError={setError}
        />

        <div className="flex items-center gap-2 text-sm font-semibold text-ink-700 dark:text-slate-200">
          <span className="grid h-7 w-7 place-items-center rounded-full bg-brand-500 text-xs text-white">2</span>
          Paste job description{visibleJobs > 1 ? "s" : ""}
        </div>
        {JOB_SLOTS.slice(0, visibleJobs).map((slot, index) => (
          <JobEditor
            key={slot.title}
            id={`job-description-${index + 1}`}
            title={slot.title}
            hint={slot.hint}
            value={jobs[index]}
            sampleLabel={slot.sampleLabel}
            onChange={(value) => setJobAt(index, value)}
            onUseSample={() => setJobAt(index, slot.sample)}
            onRemove={index > 0 ? () => {
              setJobs((current) => {
                const next = [...current];
                next.splice(index, 1);
                next.push("");
                return next.slice(0, 3);
              });
              setVisibleJobs((count) => Math.max(1, count - 1));
            } : undefined}
          />
        ))}

        {visibleJobs < 3 && (
          <button
            type="button"
            onClick={() => setVisibleJobs((count) => Math.min(3, count + 1))}
            className="focus-ring flex w-full items-center justify-center gap-2 rounded-full bg-white/80 px-4 py-3 text-sm font-semibold text-ink-800 shadow-sm dark:bg-white/10 dark:text-white"
          >
            <Plus className="h-4 w-4" />
            {visibleJobs === 1 ? "Add another job to compare" : "Add a third job"}
          </button>
        )}

        {error && <ErrorBanner title="Almost there" message={error} />}

        <button type="submit" disabled={busy} className="focus-ring btn-glossy w-full rounded-full py-3.5 text-base font-semibold">
          {comparing ? "Compare these jobs" : "See my match"}
        </button>
        <p className="text-center text-xs leading-5 text-ink-500">
          Only add skills you really have. This is not an official ATS score.
        </p>
      </form>
    </div>
  );
}
