export const MAX_UPLOAD_BYTES = 5 * 1024 * 1024;
export const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"] as const;

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function fileExtension(name: string): string {
  const index = name.lastIndexOf(".");
  return index >= 0 ? name.slice(index).toLowerCase() : "";
}

export function validateResumeFile(file: File): string | null {
  const extension = fileExtension(file.name);
  if (!ALLOWED_EXTENSIONS.includes(extension as (typeof ALLOWED_EXTENSIONS)[number])) {
    return "Unsupported file type. Please upload a PDF, DOCX, or TXT resume.";
  }
  if (file.size <= 0) {
    return "The selected file is empty.";
  }
  if (file.size > MAX_UPLOAD_BYTES) {
    return "File is too large. The limit is 5 MB.";
  }
  return null;
}

export function scoreTone(score: number): "excellent" | "strong" | "moderate" | "needs" {
  if (score >= 80) return "excellent";
  if (score >= 65) return "strong";
  if (score >= 45) return "moderate";
  return "needs";
}

export function formatPercent(score: number): string {
  return `${Math.round(score)}%`;
}

export function wordCount(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

export function weightLabel(weight: number): string {
  return `${Math.round(weight * 100)}% of overall`;
}
