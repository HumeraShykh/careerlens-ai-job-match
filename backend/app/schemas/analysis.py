from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SkillOut(BaseModel):
    name: str
    category: str
    matched_on: str
    frequency: int


class KeywordOut(BaseModel):
    term: str
    relevance: float
    in_resume: bool
    frequency_in_job: int


class SuggestionOut(BaseModel):
    title: str
    detail: str
    kind: str


class ScoreComponentOut(BaseModel):
    key: str
    label: str
    score: float
    weight: float
    help: str


class BreakdownOut(BaseModel):
    overall: float
    interpretation: str
    weights: dict[str, float]
    components: list[ScoreComponentOut]


class ParseResponse(BaseModel):
    filename: str
    file_type: str
    file_size: int
    word_count: int
    text: str = Field(description="Extracted resume text. Not logged by the API.")


class PlainSummaryOut(BaseModel):
    match_title: str
    match_blurb: str
    job_too_short: bool
    experience: str
    improve: list[str]
    matched_names: list[str]
    missing_names: list[str]


class AnalysisResult(BaseModel):
    disclaimer: str
    job_title_guess: str | None = None
    source_filename: str | None = None
    resume_word_count: int
    job_word_count: int
    breakdown: BreakdownOut
    plain_summary: PlainSummaryOut | None = None
    matched_skills: list[SkillOut]
    missing_skills: list[SkillOut]
    resume_skills: list[SkillOut]
    job_skills: list[SkillOut]
    keywords: list[KeywordOut]
    suggestions: list[SuggestionOut]
    strengths: list[str]
    gaps: list[str]


class ComparedJobOut(BaseModel):
    label: str
    rank: int
    is_best: bool
    job_title_guess: str | None = None
    score: float
    match_title: str
    experience: str
    matched_skills: list[SkillOut]
    missing_skills: list[SkillOut]
    improve: list[str]


class CompareResult(BaseModel):
    winner_label: str
    winner_title: str | None = None
    summary: str
    jobs: list[ComparedJobOut]


class SavedAnalysisOut(BaseModel):
    id: UUID
    created_at: datetime
    label: str | None
    job_title_guess: str | None
    source_filename: str | None
    overall_score: float
    interpretation: str
    resume_word_count: int
    job_preview: str | None
    result: dict[str, Any]


class SaveAnalysisRequest(BaseModel):
    label: str | None = Field(default=None, max_length=160)
    job_preview: str | None = Field(default=None, max_length=240)
    result: AnalysisResult
