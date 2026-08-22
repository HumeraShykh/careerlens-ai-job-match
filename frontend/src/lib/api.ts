import type { AnalysisResult, ApiError, CompareResult, HealthResponse } from "../types";

const rawApiUrl = (import.meta.env.VITE_API_URL as string | undefined)?.trim();
const API_URL = rawApiUrl ? rawApiUrl.replace(/\/$/, "") : "";

export class CareerLensApiError extends Error {
  status: number;
  code: string;

  constructor(message: string, status: number, code: string) {
    super(message);
    this.name = "CareerLensApiError";
    this.status = status;
    this.code = code;
  }
}

async function readError(response: Response): Promise<CareerLensApiError> {
  try {
    const body = (await response.json()) as { detail?: ApiError | string; error?: string; code?: string };
    if (typeof body.detail === "object" && body.detail) {
      return new CareerLensApiError(body.detail.error, response.status, body.detail.code);
    }
    if (typeof body.detail === "string") {
      return new CareerLensApiError(body.detail, response.status, body.code ?? "request_failed");
    }
    if (body.error) {
      return new CareerLensApiError(body.error, response.status, body.code ?? "request_failed");
    }
  } catch {
    // Fall through to a generic network message.
  }
  if (response.status === 0 || response.status >= 500) {
    return new CareerLensApiError(
      "The CareerLens AI server is unavailable. Confirm the backend is running.",
      response.status,
      "server_unavailable",
    );
  }
  return new CareerLensApiError("The request failed.", response.status, "request_failed");
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/api/health`);
  if (!response.ok) throw await readError(response);
  return response.json() as Promise<HealthResponse>;
}

export async function getSamples(): Promise<{ resume: { text: string }; job_description: { text: string } }> {
  const response = await fetch(`${API_URL}/api/samples`);
  if (!response.ok) throw await readError(response);
  return response.json() as Promise<{ resume: { text: string }; job_description: { text: string } }>;
}

export async function analyzeResume(input: {
  jobDescription: string;
  resumeText?: string;
  resumeFile?: File | null;
}): Promise<AnalysisResult> {
  const form = new FormData();
  form.append("job_description", input.jobDescription);
  if (input.resumeFile) {
    form.append("resume_file", input.resumeFile);
  }
  if (input.resumeText?.trim()) {
    form.append("resume_text", input.resumeText.trim());
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}/api/analyze`, {
      method: "POST",
      body: form,
    });
  } catch {
    throw new CareerLensApiError(
      "Could not reach the CareerLens AI API. Start the backend on port 8000 and try again.",
      0,
      "network_error",
    );
  }

  if (!response.ok) throw await readError(response);
  return response.json() as Promise<AnalysisResult>;
}

export async function compareJobs(input: {
  jobs: string[];
  resumeText?: string;
  resumeFile?: File | null;
}): Promise<CompareResult> {
  const filled = input.jobs.map((job) => job.trim()).filter(Boolean);
  if (filled.length < 2) {
    throw new CareerLensApiError("Paste at least two full job postings to compare.", 400, "need_two_jobs");
  }

  const form = new FormData();
  form.append("job_description_1", filled[0]);
  form.append("job_description_2", filled[1]);
  if (filled[2]) {
    form.append("job_description_3", filled[2]);
  }
  if (input.resumeFile) {
    form.append("resume_file", input.resumeFile);
  }
  if (input.resumeText?.trim()) {
    form.append("resume_text", input.resumeText.trim());
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}/api/compare`, {
      method: "POST",
      body: form,
    });
  } catch {
    throw new CareerLensApiError(
      "Could not reach the CareerLens AI API. Start the backend on port 8000 and try again.",
      0,
      "network_error",
    );
  }

  if (!response.ok) throw await readError(response);
  return response.json() as Promise<CompareResult>;
}

export async function saveAnalysis(result: AnalysisResult, label?: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/analyses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      label,
      job_preview: result.job_title_guess,
      result,
    }),
  });
  if (!response.ok) throw await readError(response);
}
