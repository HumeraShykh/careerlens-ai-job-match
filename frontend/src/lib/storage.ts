import type { AnalysisResult, CompareResult } from "../types";

const SESSION_KEY = "careerlens.session.v4";
const THEME_KEY = "careerlens.theme";

export type StoredSession =
  | { kind: "single"; result: AnalysisResult }
  | { kind: "compare"; result: CompareResult };

export function storeSession(session: StoredSession): void {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function loadSession(): StoredSession | null {
  const raw = sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as StoredSession;
    if (parsed.kind === "single" || parsed.kind === "compare") return parsed;
    return null;
  } catch {
    return null;
  }
}

export function storeResult(result: AnalysisResult): void {
  storeSession({ kind: "single", result });
}

export function loadResult(): AnalysisResult | null {
  const session = loadSession();
  return session?.kind === "single" ? session.result : null;
}

export function clearResult(): void {
  sessionStorage.removeItem(SESSION_KEY);
}

export function loadTheme(): "light" | "dark" {
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function persistTheme(theme: "light" | "dark"): void {
  localStorage.setItem(THEME_KEY, theme);
}
