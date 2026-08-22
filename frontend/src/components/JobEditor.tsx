type JobEditorProps = {
  id: string;
  title: string;
  hint: string;
  value: string;
  sampleLabel?: string;
  onChange: (value: string) => void;
  onUseSample?: () => void;
  onRemove?: () => void;
};

export function JobEditor({
  id,
  title,
  hint,
  value,
  sampleLabel,
  onChange,
  onUseSample,
  onRemove,
}: JobEditorProps) {
  return (
    <section className="glass-card rounded-3xl p-5 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-ink-950 dark:text-white">{title}</h2>
          <p className="text-sm text-ink-500">{hint}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {onUseSample && sampleLabel && (
            <button
              type="button"
              onClick={onUseSample}
              className="focus-ring rounded-full bg-brand-50 px-3 py-1.5 text-sm font-semibold text-brand-700 dark:bg-white/10 dark:text-brand-100"
            >
              {sampleLabel}
            </button>
          )}
          {onRemove && (
            <button type="button" onClick={onRemove} className="focus-ring rounded-full px-3 py-1.5 text-sm font-medium text-ink-500">
              Remove
            </button>
          )}
          <button type="button" onClick={() => onChange("")} className="focus-ring rounded-full px-3 py-1.5 text-sm font-medium text-ink-500">
            Clear
          </button>
        </div>
      </div>
      <label htmlFor={id} className="sr-only">
        {title}
      </label>
      <textarea
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={8}
        className="field-input focus-ring mt-4"
        placeholder="Paste the job description here..."
      />
      <p className="mt-2 text-xs text-ink-500">{value.trim().length} characters</p>
    </section>
  );
}
