import { Logo } from "./Logo";

export function Footer() {
  return (
    <footer className="no-print px-4 py-8 text-center">
      <Logo compact />
      <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-ink-500">
        CareerLens AI is a practice tool. It does not promise that an employer will shortlist you.
      </p>
      <p className="mt-4 text-xs text-ink-500">© {new Date().getFullYear()} CareerLens AI</p>
    </footer>
  );
}
