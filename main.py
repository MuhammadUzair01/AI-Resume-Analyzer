from fastapi import FastAPI, UploadFile, File,HTTPException
from resume_perser import extract_text_from_pdf
from model import ResumeText                                    
import aiofiles                                                 # This library is used for asynchronous file operations
import os                                                       # This library is used to handle file paths and directories

app= FastAPI()

UPLOAD_DIR = "uploads"                              # Directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok= True)             # Ensure the upload directory exists

@app.post("/upload_resume",response_model=ResumeText)      
async def upload_resume(file: UploadFile = File(...)):     
    if file.filename.endswith('.pdf'):                                         # Check if the uploaded file is a PDF
        raise 
    HTTPException(status_code=400, detail= "Only PDF files are allowed")          
    file_path =os.path.join(UPLOAD_DIR, file.filename)                          # Save the uploaded file
    async with aiofiles.open(file_path, 'wb') as out_file:                     # Open the file in write-binary mode
        content = await file.read()                                             # Read the content of the uploaded file
        await out_file.write(content)                                           # Write the content to the file
    text = extract_text_from_pdf(file_path)
    if not text:
        raise HTTPException(status_code=400, detail="No text found in the PDF file")
    return { "resume_text": text }                                                # Return the extracted text as a ResumeText model