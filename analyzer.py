# import spacy                        # Natural Language Processing library
# import re                            # Regular expressions for text processing

# nlp = spacy.load("en_core_web_sm")                                            # Load the English NLP model


# # Define a set of skills to look for in the resume text
# SKILL_SET = [
#     "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS",
#     "Machine Learning", "Data Analysis", "Project Management", "Communication",
#     "Problem Solving", "Teamwork", "Leadership", "Agile", "Scrum", "DevOps",
#     "Cloud Computing", "Cybersecurity", "Database Management", "Web Development",
#     "Mobile App Development", "Software Testing", "Version Control", "API Development"
# ]

# def extract_skills(text: str) -> list:
#     text_lower = text.lower()                            # Convert text to lowercase for case-insensitive matching
#     found_skills = []

#     for skill in SKILL_SET:                                  # Check each skill in the skill set
#         if skill.lower() in text_lower:                       # If the skill is found in the text
#             found_skills.append(skill)                        # Add it to the found skills list

#     return list(set(found_skills))                                 # Return unique skills found in the resume text

# def extract_experience(text: str) -> str:
#     experience_keywords = [                                               # Keywords to identify experience sections
#         "experience", "work history", "employment history", 
#         "professional experience", "career history", "employment"
#     ]

#     paragraphs = text.split("\n\n")                      # Split the text into paragraphs for better matching
#     for para in paragraphs:                                  # Check each paragraph for experience keywords
#         for keyword in experience_keywords:
#             if keyword in para.lower():
#                 return para.strip()

#     return "Not matched"

# def analyze_resume(text: str) -> str:
#     doc = nlp(text)                                                     # Process the text with spaCy NLP model
#     sentences = list(doc.sents)                                            # Extract sentences from the processed text
#     if len(sentences) > 3:                                                  # If there are more than 3 sentences, return the first 3
#         return " ".join([str(sentences[0]), str(sentences[1]), str(sentences[2])]) 
    
#     return text


# # def match_resume_to_job(resume_text:str,job_text:str)->dict:
# #     resume_doc =nlp(resume_text.lower())                                            # Process the resume text with spaCy NLP model
# #     job_doc = nlp(job_text.lower())                                                # Process the job description text with spaCy NLP model
# #     resume_words = set(token.text for token in resume_doc if token.is_alpha and not token.is_stop)        # Extract unique words from the resume text
# #     job_words = set(token.text for token in job_doc if token.is_alpha and not token.is_stop)  # Extract unique words from the job description text
# #     matched = resume_words.intersection(job_words)                # Find the intersection of words between the resume and job description
# #     total = len(job_words)                                                # Total number of unique words in the job description
# #     score =round(len((matched) / total)*100 , 2) if total > 0 else 0.0        # Calculate the match score as a percentage of matched words to total words
# #     return {
# #         "match_score": score,                                         # Return the match score
# #         "total_keywords": total,                                     # Return the total number of keywords in the job description
# #         "matched_keywords": list(matched)                            # Return the list of matched keywords
# #     }



# def match_resume_to_job(resume_text: str, job_text: str) -> dict:
#     resume_doc = nlp(resume_text.lower())
#     job_doc = nlp(job_text.lower())

#     resume_words = {token.text for token in resume_doc if token.is_alpha and not token.is_stop}
#     job_words = {token.text for token in job_doc if token.is_alpha and not token.is_stop}

#     matched = resume_words & job_words
#     total = len(job_words)

#     score = round((len(matched) / total) * 100, 2) if total > 0 else 0.0

#     return {
#         "match_score": score,
#         "total_keywords": total,
#         "matched_keywords": list(matched),
#     }




import re
from typing import Iterable, List, Optional, Dict
import spacy

# Load spaCy model

nlp = spacy.load("en_core_web_sm")


# Skill set
SKILL_SET = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS",
    "Machine Learning", "Data Analysis", "Project Management", "Communication",
    "Problem Solving", "Teamwork", "Leadership", "Agile", "Scrum", "DevOps",
    "Cloud Computing", "Cybersecurity", "Database Management", "Web Development",
    "Mobile App Development", "Software Testing", "Version Control", "API Development"
]

# Regex for years
_YEAR_PATTERN = re.compile(r"(?P<num>\\d+(?:\\.\\d+)?)\\s*(?:\\+)?\\s*(?:years?|yrs?|y/o)?", re.IGNORECASE)

def _extract_years(text: str) -> Optional[float]:
    vals = []
    for m in _YEAR_PATTERN.finditer(text):
        try:
            vals.append(float(m.group("num")))
        except ValueError:
            pass
    return max(vals) if vals else None

def extract_skills(text: str, skill_set: Iterable[str] = None) -> List[str]:
    if skill_set is None:
        skill_set = SKILL_SET
    text_lower = text.lower()
    return sorted({s for s in skill_set if s.lower() in text_lower}, key=lambda x: x.lower())

def extract_experience_section(text: str) -> str:
    keywords = ["experience", "work history", "employment history", "professional experience", "career history", "employment"]
    for para in text.split("\n\n"):
        if any(k in para.lower() for k in keywords):
            return para.strip()
    return "Not matched"

def analyze_resume(text: str) -> str:
    doc = nlp(text)
    sents = list(doc.sents)
    return " ".join(str(s) for s in sents[:3]) if len(sents) > 3 else text.strip()

# def match_resume_to_job(resume_text: str, job_text: str, skill_weight: float = 0.7, experience_weight: float = 0.3, skill_set: Optional[Iterable[str]] = None) -> Dict[str, float]:
#     if skill_set is None:
#         skill_set = SKILL_SET
#     total_weight = skill_weight + experience_weight or 1.0
#     sw, ew = skill_weight / total_weight, experience_weight / total_weight

#     # Skills
#     resume_skills = set(s.lower() for s in extract_skills(resume_text, skill_set))
#     job_skills = set(s.lower() for s in extract_skills(job_text, skill_set))
#     skill_pct = round(len(resume_skills & job_skills) / len(job_skills) * 100, 2) if job_skills else 100.0

#     # Experience
#     resume_years, job_years = _extract_years(resume_text.lower()), _extract_years(job_text.lower())
#     experience_pct = 100.0 if job_years is None else (0.0 if resume_years is None else round(min(resume_years / job_years, 1.0) * 100, 2))

#     return {
#         "experience_pct": experience_pct,
#         "skill_pct": skill_pct,
#         "overall_pct": round(sw * skill_pct + ew * experience_pct, 2)
#     }




def match_resume_to_job(resume_text: str, job_text: str, *, skill_weight=0.7, experience_weight=0.3) -> dict:
    # Normalize weights
    w_total = skill_weight + experience_weight or 1.0
    sw, ew = skill_weight / w_total, experience_weight / w_total

    # Extract skills
    resume_skills = set(s.lower() for s in extract_skills(resume_text))
    job_skills = set(s.lower() for s in extract_skills(job_text))
    skill_pct = round(len(resume_skills & job_skills) / len(job_skills) * 100, 2) if job_skills else 100.0

    # Extract years
    resume_years = _extract_years(resume_text.lower())
    job_years = _extract_years(job_text.lower())

    # Compute experience percentage and message
    if job_years is None:
        experience_pct = 100.0
        experience_msg = "No experience required"
    elif resume_years is None:
        experience_pct = 0.0
        experience_msg = "No experience found in resume"
    else:
        experience_pct = round(min(resume_years / job_years, 1.0) * 100, 2)
        experience_msg = f"Found {resume_years} yrs vs Required {job_years} yrs ({experience_pct}%)"

    overall_pct = round(sw * skill_pct + ew * experience_pct, 2)

    return {
        "experience_pct": experience_pct,
        "skill_pct": skill_pct,
        "overall_pct": overall_pct,
        "experience_detail": experience_msg  # <-- New descriptive field
    }
