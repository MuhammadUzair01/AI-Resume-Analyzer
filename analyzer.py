import spacy                        # Natural Language Processing library
import re                            # Regular expressions for text processing

nlp = spacy.load("en_core_web_sm")                                            # Load the English NLP model


# Define a set of skills to look for in the resume text
SKILL_SET = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS",
    "Machine Learning", "Data Analysis", "Project Management", "Communication",
    "Problem Solving", "Teamwork", "Leadership", "Agile", "Scrum", "DevOps",
    "Cloud Computing", "Cybersecurity", "Database Management", "Web Development",
    "Mobile App Development", "Software Testing", "Version Control", "API Development"
]

def extract_skills(text: str) -> list:
    text_lower = text.lower()                            # Convert text to lowercase for case-insensitive matching
    found_skills = []

    for skill in SKILL_SET:                                  # Check each skill in the skill set
        if skill.lower() in text_lower:                       # If the skill is found in the text
            found_skills.append(skill)                        # Add it to the found skills list

    return list(set(found_skills))                                 # Return unique skills found in the resume text

def extract_experience(text: str) -> str:
    experience_keywords = [                                               # Keywords to identify experience sections
        "experience", "work history", "employment history", 
        "professional experience", "career history", "employment"
    ]

    paragraphs = text.split("\n\n")                      # Split the text into paragraphs for better matching
    for para in paragraphs:                                  # Check each paragraph for experience keywords
        for keyword in experience_keywords:
            if keyword in para.lower():
                return para.strip()

    return "Not matched"

def analyze_resume(text: str) -> str:
    doc = nlp(text)                                                     # Process the text with spaCy NLP model
    sentences = list(doc.sents)                                            # Extract sentences from the processed text
    if len(sentences) > 3:                                                  # If there are more than 3 sentences, return the first 3
        return " ".join([str(sentences[0]), str(sentences[1]), str(sentences[2])]) 
    
    return text
