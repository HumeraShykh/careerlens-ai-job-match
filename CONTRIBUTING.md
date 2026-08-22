# Contributing to CareerLens AI

This repository is a portfolio product, but the same rules apply if you fork it.

## Ground rules

- Do not invent ATS accuracy claims.
- Do not add fake scores, fake users, or hard-coded analysis results.
- Keep resume text out of logs.
- Prefer a small, testable change over a large rewrite.

## Local setup

Follow the root `README.md`. Use Python 3.12+ and Node 20+.

## Checks before opening a pull request

```bash
cd backend
source .venv/bin/activate
pytest

cd ../frontend
npm test
npm run build
```

## Suggestions that fit the product

- Richer skill aliases
- Better PDF extraction for messy layouts
- Optional embeddings behind a clear feature flag
- Multi-job comparison, marked as such

Please include tests for scoring or parsing changes.
