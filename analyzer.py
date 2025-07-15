import spacy                    # This library is used for natural language processing tasks.
import re                       # This library is used for regular expressions


nlp=spacy.load("en_core_web_sm")            # Load the English NLP model

 # List of skills to be extracted from the resume
SKILL_SET =[                                                                   
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS",
    "Machine Learning", "Data Analysis", "Project Management", "Communication",
    "Problem Solving", "Teamwork", "Leadership", "Agile", "Scrum", "DevOps",
    "Cloud Computing", "Cybersecurity", "Database Management", "Web Development",
    "Mobile App Development", "Software Testing", "Version Control", "API Development"
]
def extract_skills(text :str) -> list:                           # Extract skills from the resume text
    doc = nlp(text.lower())                                     # Process the text with the NLP model
    skills_found =[]                                            # Initialize an empty list to store found skills
    
    for token in doc:                                           # Iterate through each token in the processed text
        if token.text in SKILL_SET:                            # Check if the token is in the skill set
            skills_found.append(token.text)                    # Append the skill to the list if found
    return list(set(skills_found))                             # Return unique skills found in the resume text


def extract_experience(text: str) -> str:
    pattern = r"(?i)(experience|work history|employment history|professional experience|career history):?\s*(.*?)(?=\n\n|\Z)"   # Regular expression to match experience sections
    match= re.search(pattern, text.lower())  # Search for the pattern in the text
    return match.group(0) if match else "Not matched"       # Return the matched experience section or "Not matched" if no match is found


def analyze_resume(text: str) -> str:
    doc =nlp(text)                                    # Process the resume text with the NLP model
    sentances =list(doc.sents)                            # Split the text into sentences
    if len(sentances)> 3:
        return " ".join ([str(sentances[0]), str(sentances[1]), str(sentances[2])]) # Return the first three sentences as a summary
    return text
    
    