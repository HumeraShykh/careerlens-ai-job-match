# CareerLens AI API

Interactive docs: `http://127.0.0.1:8000/docs`

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Process and database status |
| `GET` | `/api/samples` | Fictional resume and job description |
| `POST` | `/api/parse/resume` | Extract text from PDF, DOCX, or TXT |
| `POST` | `/api/analyze` | Parse (if needed) and score a match |
| `POST` | `/api/compare` | Score 2–3 jobs against one resume and rank them |
| `POST` | `/api/analyses` | Save result metadata |
| `GET` | `/api/analyses` | List saved results |
| `GET` | `/api/analyses/{id}` | Retrieve one saved result |
| `DELETE` | `/api/analyses/{id}` | Delete a saved result |

## Analyze

`multipart/form-data`

- `job_description` (required string)
- `resume_file` (optional file)
- `resume_text` (optional string)

Provide a file or pasted resume text. The job description must be at least 40 words.

## Compare

`multipart/form-data`

- `job_description_1` (required string)
- `job_description_2` (required string)
- `job_description_3` (optional string)
- `resume_file` (optional file)
- `resume_text` (optional string)

Each job is scored with the same engine as `/api/analyze`. The response ranks jobs by overall score and names a winner. If the top two scores are within 3 points, the summary says they are very close.

## Errors

Error bodies use `{ "detail": { "error": "...", "code": "..." } }` for handler-raised cases, or `{ "error", "code" }` for some global handlers.

Common codes:

- `unsupported_type`
- `file_too_large`
- `empty_file`
- `parse_failed`
- `resume_too_short`
- `job_too_short`
- `need_two_jobs`
- `too_many_jobs`
- `database_unavailable`
- `not_found`
