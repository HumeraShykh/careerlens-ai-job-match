# CareerLens AI

**Upload a resume. Paste a job. See the fit.**

CareerLens AI scores a resume against 1–3 job postings and ranks the best-fit role. You get a match %, matching skills, gaps, and honest next steps — never invented achievements.

Explainable NLP (TF-IDF + skill lexicon). FastAPI + React. No paid LLM. **Not an ATS. Not a hiring promise.**

[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=white)](frontend)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?logo=fastapi&logoColor=white)](backend)
[![License: MIT](https://img.shields.io/badge/License-MIT-0F8F86.svg)](LICENSE)

---

## Run it

Need **Python 3.12+** and **Node 20+**. No database required.

**Terminal 1 — API**

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — app**

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5175** → **Try a sample** or **Compare two jobs**.

Health check: http://127.0.0.1:8000/api/health · API docs: http://127.0.0.1:8000/docs  
`degraded` means Postgres is off. Scoring still works.

First time: `cp .env.example .env && cp backend/.env.example backend/.env && cp frontend/.env.example frontend/.env`  
Keep `VITE_API_URL` empty in `frontend/.env`.

---

## Score (transparent)

| Skills 35% | Keywords 25% | Experience 15% | Education 10% | Text similarity 15% |
| --- | --- | --- | --- | --- |

80+ excellent · 65–79 strong · 45–64 okay · below 45 weak

---

## Stack

React + TypeScript · FastAPI · scikit-learn TF-IDF · PDF/DOCX parse · pytest + Vitest

Details: [architecture](docs/architecture.md) · [API](docs/api.md) · samples in `samples/`

```bash
cd backend && source .venv/bin/activate && pytest
cd ../frontend && npm test
```

MIT · [`LICENSE`](LICENSE)
