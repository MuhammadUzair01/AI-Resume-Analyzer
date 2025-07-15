import pdfplumber               # This library is used to extract text from PDF files.

def extract_text_from_pdf(file_path):
    text= ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text