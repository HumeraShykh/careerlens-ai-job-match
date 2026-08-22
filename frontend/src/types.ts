export type Skill = {
  name: string;
  category: string;
  matched_on: string;
  frequency: number;
};

export type Keyword = {
  term: string;
  relevance: number;
  in_resume: boolean;
  frequency_in_job: number;
};

export type Suggestion = {
  title: string;
  detail: string;
  kind: string;
};

export type ScoreComponent = {
  key: string;
  label: string;
  score: number;
  weight: number;
  help: string;
};

export type Breakdown = {
  overall: number;
  interpretation: string;
  weights: Record<string, number>;
  components: ScoreComponent[];
};

export type PlainSummary = {
  match_title: string;
  match_blurb: string;
  job_too_short: boolean;
  experience: string;
  improve: string[];
  matched_names: string[];
  missing_names: string[];
};

export type AnalysisResult = {
  disclaimer: string;
  job_title_guess: string | null;
  source_filename: string | null;
  resume_word_count: number;
  job_word_count: number;
  breakdown: Breakdown;
  plain_summary?: PlainSummary | null;
  matched_skills: Skill[];
  missing_skills: Skill[];
  resume_skills: Skill[];
  job_skills: Skill[];
  keywords: Keyword[];
  suggestions: Suggestion[];
  strengths: string[];
  gaps: string[];
};

export type HealthResponse = {
  status: string;
  version: string;
  database: {
    enabled: boolean;
    available: boolean;
    error: string | null;
  };
};

export type ComparedJob = {
  label: string;
  rank: number;
  is_best: boolean;
  job_title_guess: string | null;
  score: number;
  match_title: string;
  experience: string;
  matched_skills: Skill[];
  missing_skills: Skill[];
  improve: string[];
};

export type CompareResult = {
  winner_label: string;
  winner_title: string | null;
  summary: string;
  jobs: ComparedJob[];
};

export type ApiError = {
  error: string;
  code: string;
  detail?: unknown;
};
