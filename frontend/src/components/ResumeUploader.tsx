import { useRef, useState } from "react";
import { FileText, Upload, X } from "lucide-react";
import { formatBytes, validateResumeFile } from "../lib/format";

type ResumeUploaderProps = {
  file: File | null;
  resumeText: string;
  mode: "file" | "paste";
  onModeChange: (mode: "file" | "paste") => void;
  onFileChange: (file: File | null) => void;
  onTextChange: (text: string) => void;
  onError: (message: string | null) => void;
};

export function ResumeUploader({
  file,
  resumeText,
  mode,
  onModeChange,
  onFileChange,
  onTextChange,
  onError,
}: ResumeUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  function applyFile(next: File | null) {
    if (!next) {
      onFileChange(null);
      onError(null);
      return;
    }
    const problem = validateResumeFile(next);
    if (problem) {
      onFileChange(null);
      onError(problem);
      return;
    }
    onError(null);
    onFileChange(next);
  }

  return (
    <section className="glass-card rounded-3xl p-5 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-ink-950 dark:text-white">Your resume</h2>
          <p className="text-sm text-ink-500">PDF, Word, or text. Max 5 MB.</p>
        </div>
        <div className="inline-flex rounded-full bg-black/5 p-1 dark:bg-white/10" role="tablist" aria-label="Resume input mode">
          <button
            type="button"
            role="tab"
            aria-selected={mode === "file"}
            className={`rounded-full px-3 py-1.5 text-sm font-medium ${mode === "file" ? "bg-white text-ink-950 shadow-sm dark:bg-ink-900 dark:text-white" : "text-ink-500"}`}
            onClick={() => onModeChange("file")}
          >
            Upload
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={mode === "paste"}
            className={`rounded-full px-3 py-1.5 text-sm font-medium ${mode === "paste" ? "bg-white text-ink-950 shadow-sm dark:bg-ink-900 dark:text-white" : "text-ink-500"}`}
            onClick={() => onModeChange("paste")}
          >
            Paste text
          </button>
        </div>
      </div>

      {mode === "file" ? (
        <div className="mt-5">
          <label
            htmlFor="resume-file"
            className={`grid min-h-40 cursor-pointer place-items-center rounded-2xl border-2 border-dashed px-4 py-8 text-center transition ${
              dragOver ? "border-brand-500 bg-brand-50 dark:bg-brand-500/10" : "border-brand-200 bg-white/70 dark:border-white/15 dark:bg-white/5"
            }`}
            onDragOver={(event) => {
              event.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(event) => {
              event.preventDefault();
              setDragOver(false);
              applyFile(event.dataTransfer.files[0] ?? null);
            }}
          >
            <Upload className="mb-3 h-6 w-6 text-brand-500" />
            <span className="font-semibold text-ink-950 dark:text-white">Drop file here</span>
            <span className="mt-1 text-sm text-ink-500">or tap to choose</span>
          </label>
          <input
            ref={inputRef}
            id="resume-file"
            type="file"
            accept=".pdf,.docx,.txt,application/pdf,text/plain,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            className="sr-only"
            onChange={(event) => applyFile(event.target.files?.[0] ?? null)}
          />
          {file && (
            <div className="mt-4 flex items-center justify-between gap-3 rounded-2xl bg-black/5 px-4 py-3 dark:bg-white/5">
              <div className="flex min-w-0 items-center gap-3">
                <FileText className="h-5 w-5 shrink-0 text-brand-500" />
                <div className="min-w-0">
                  <p className="truncate font-medium text-ink-950 dark:text-white">{file.name}</p>
                  <p className="text-xs text-ink-500">
                    {file.name.split(".").pop()?.toUpperCase()} · {formatBytes(file.size)}
                  </p>
                </div>
              </div>
              <button
                type="button"
                className="focus-ring rounded-full p-2 text-ink-500 hover:bg-black/5 dark:hover:bg-white/10"
                aria-label="Remove file"
                onClick={() => {
                  applyFile(null);
                  if (inputRef.current) inputRef.current.value = "";
                }}
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="mt-5">
          <label htmlFor="resume-text" className="text-sm font-medium text-ink-700 dark:text-slate-300">
            Paste resume text
          </label>
          <textarea
            id="resume-text"
            value={resumeText}
            onChange={(event) => onTextChange(event.target.value)}
            rows={8}
            className="field-input focus-ring mt-2"
            placeholder="Paste the full resume..."
          />
          <p className="mt-2 text-xs text-ink-500">{resumeText.trim().length} characters</p>
        </div>
      )}
    </section>
  );
}
