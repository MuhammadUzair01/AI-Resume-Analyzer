from pydantic import BaseModel

class ResumeText(BaseModel):
    text: str

class ResumeAnalysis(BaseModel):
    summary: str
    skills: list[str]
    experience: list[str]
    