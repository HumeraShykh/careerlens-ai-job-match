# CareerLens AI Architecture

CareerLens AI is a local-first resume and job-description analyzer.

```text
Browser (React + TypeScript)
        │  multipart / JSON
        ▼
FastAPI (parse, analyze, optional history)
        │
        ├── Document parser (PDF / DOCX / TXT)
        ├── NLP pipeline (normalize, skills, TF-IDF, scoring)
        └── PostgreSQL (optional saved metadata)
```

## Why this shape

The product is a single user flow: upload or paste a resume, paste one to three jobs, read a report. That does not need microservices.

The backend is split so the analysis engine can later gain embeddings or an LLM without rewriting routes.

| Layer | Responsibility |
| --- | --- |
| `frontend/` | Landing, analyzer, results, print/export |
| `backend/app/api` | HTTP validation and status codes |
| `backend/app/services/parser.py` | Extract text only. Never execute files. |
| `backend/app/nlp` | Deterministic matching and scoring |
| `backend/app/db` | Optional history. Analysis works if Postgres is down. |

## Scoring

Weights live in `backend/app/core/scoring_weights.py` and are returned with every result:

- Skills match: 35%
- Keyword coverage: 25%
- Experience relevance: 15%
- Education coverage: 10%
- TF-IDF cosine similarity: 15%

This is CareerLens AI's relevance model, not an employer ATS score.

## Privacy

Uploaded bytes are read into memory, parsed, and discarded. Saved history stores scores, skills, keywords, and suggestions. It does not store the original file.
