from pydantic import BaseModel
from typing import List

class ResumeText(BaseModel):
    text: str

class ResumeAnalysis(BaseModel):
    summary: str
    skills: List[str]
    experience: str  # paragraph or "Not matched"

class ResumeMatchRequest(BaseModel):
    resume_text: str
    job_description: str

class ResumeMatchResponse(BaseModel):
    experience_pct: float
    skill_pct: float
    overall_pct: float
    experience_detail: str   # <-- new descriptive message
