from __future__ import annotations

import os
from typing import Any

import aiofiles
from fastapi import FastAPI, UploadFile, File, HTTPException

# ---------------------------------------------------------------------------
# Local imports (adjust import paths to match your project structure)
# ---------------------------------------------------------------------------
try:
    from resume_perser import extract_text_from_pdf  # your existing PDF text extractor
except ImportError as exc:  # pragma: no cover - dev hint
    raise ImportError("Cannot import extract_text_from_pdf from resume_perser. Check module path/name.") from exc

from analyzer import (
    extract_skills,
    extract_experience_section,  # renamed from extract_experience
    analyze_resume,
    match_resume_to_job,
)

from model import (
    ResumeText,
    ResumeAnalysis,
    ResumeMatchRequest,
    ResumeMatchResponse,
)


# ---------------------------------------------------------------------------
# FastAPI app instance
# ---------------------------------------------------------------------------
app = FastAPI(title="Resume Analyzer API", version="1.0.0")


# ---------------------------------------------------------------------------
# Upload directory setup
# ---------------------------------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper: validate PDF filename
# ---------------------------------------------------------------------------
def _ensure_pdf(filename: str) -> None:
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")


# ---------------------------------------------------------------------------
# Endpoint: Upload resume PDF -> return extracted text
# ---------------------------------------------------------------------------
@app.post("/upload_resume", response_model=ResumeText, summary="Upload a PDF resume and extract text")
async def upload_resume(file: UploadFile = File(...)) -> ResumeText:
    _ensure_pdf(file.filename)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file asynchronously
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Extract text
    text = extract_text_from_pdf(file_path)
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text found in the PDF file.")

    return ResumeText(text=text)


# ---------------------------------------------------------------------------
# Endpoint: Analyze resume text -> summary, skills, experience section
# ---------------------------------------------------------------------------
@app.post("/analyze_resume", response_model=ResumeAnalysis, summary="Analyze resume text")
async def analyze_resume_endpoint(data: ResumeText) -> ResumeAnalysis:
    text = data.text

    skills = extract_skills(text)
    experience_section = extract_experience_section(text)
    summary_text = analyze_resume(text)

    return ResumeAnalysis(
        summary=summary_text,
        skills=skills,
        experience=experience_section,
    )


# ---------------------------------------------------------------------------
# Endpoint: Match resume to job description -> % scores
# ---------------------------------------------------------------------------
@app.post("/match-resume", response_model=ResumeMatchResponse)
async def match_resume(data: ResumeMatchRequest):
    result = match_resume_to_job(data.resume_text, data.job_description)
    if "experience_detail" not in result:
        # Backfill a generic message
        if result.get("experience_pct", 0.0) == 100.0:
            result["experience_detail"] = "No experience required or fully satisfied."
        else:
            result["experience_detail"] = "Experience comparison result."
    return result





