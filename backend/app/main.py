from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api.routes import analyses, analyze, health, parse, samples
from app.core.config import get_settings
from app.db.session import init_database


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_database()
    yield


settings = get_settings()

app = FastAPI(
    title="CareerLens AI API",
    description=(
        "Transparent resume and job-description match analysis. "
        "Scores are CareerLens AI relevance metrics, not employer ATS results."
    ),
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(parse.router)
app.include_router(analyze.router)
app.include_router(analyses.router)
app.include_router(samples.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "The request was invalid.", "code": "validation_error", "detail": exc.errors()},
    )


@app.exception_handler(RuntimeError)
async def runtime_exception_handler(_request: Request, exc: RuntimeError) -> JSONResponse:
    message = str(exc)
    if "Database" in message or "database" in message:
        return JSONResponse(
            status_code=503,
            content={"error": message, "code": "database_unavailable"},
        )
    return JSONResponse(status_code=500, content={"error": message, "code": "server_error"})
