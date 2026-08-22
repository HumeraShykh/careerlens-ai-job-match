type ErrorBannerProps = {
  title: string;
  message: string;
  onRetry?: () => void;
};

export function ErrorBanner({ title, message, onRetry }: ErrorBannerProps) {
  return (
    <div role="alert" className="rounded-3xl bg-rose-50 px-4 py-4 text-rose-900 dark:bg-rose-500/15 dark:text-rose-100">
      <p className="font-semibold">{title}</p>
      <p className="mt-1 text-sm leading-6">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="focus-ring mt-3 rounded-full bg-rose-700 px-4 py-2 text-sm font-semibold text-white"
        >
          Try again
        </button>
      )}
    </div>
  );
}
