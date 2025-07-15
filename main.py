from fastapi import FastAPI, UploadFile, File, HTTPException
from resume_perser import extract_text_from_pdf
from analyzer import extract_skills, extract_experience, analyze_resume
from model import ResumeText, ResumeAnalysis
import aiofiles                                             # This library is used for asynchronous file operations
import os                                                   # This library is used to handle file paths and directories


app = FastAPI()

UPLOAD_DIR = "uploads"                                              # Directory where uploaded resumes will be stored
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_resume", response_model=ResumeText)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):                                    # Check if the uploaded file is a PDF
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)                               # Create a path for the uploaded file

    async with aiofiles.open(file_path, 'wb') as out_file:                 # Open the file asynchronously for writing
        content = await file.read()                                        # Read the content of the uploaded file
        await out_file.write(content)                                      # Write the content to the file

    text = extract_text_from_pdf(file_path)                                 # Extract text from the uploaded PDF file

    if not text:
        raise HTTPException(status_code=400, detail="No text found in the PDF file")

    return {"text": text}                                                        # Return the extracted text as a response 


@app.post("/analyze_resume", response_model=ResumeAnalysis)
async def analyze_resume_endpoint(data: ResumeText):
    text = data.text                                                   # Get the resume text from the request data
    skills=extract_skills(text)                                             # Extract skills from the resume text
    experience = extract_experience(text)                                     # Extract experience from the resume text
    summary = analyze_resume(text)                                             # Analyze the resume to get a summary
    
    return {
        "summary": summary,
        "skills": skills,
        "experience": experience
    }
