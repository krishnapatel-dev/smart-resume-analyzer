import streamlit as st
import pdfplumber
import docx
import spacy
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_skills(text):
    doc = nlp(text)
    skills = []

    skill_keywords = ["python","sql","docker","aws","machine learning","react"]

    for token in doc:
        if token.text.lower() in skill_keywords:
            skills.append(token.text.lower())

    return list(set(skills))


def extract_text(file):

    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    elif file.type == "text/plain":
        return file.read().decode("utf-8")


st.title("Smart Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

resume = st.file_uploader("Upload your Resume", type=["txt", "pdf", "docx"])
resume_text = ""

if resume:
    resume_text = extract_text(resume).lower()
    resume_skills = extract_skills(resume_text)
    st.success("Resume uploaded successfully!")

st.subheader("Paste Job Description")
job_description = st.text_area("Enter the Job Description")

if resume_text and job_description:

    jd_text = job_description.lower()

    # Sentence Transformer similarity
    resume_embedding = model.encode(resume_text)
    jd_embedding = model.encode(job_description)

    similarity = util.cos_sim(resume_embedding, jd_embedding)

    semantic_score = float(similarity[0][0]) * 100

    st.subheader("Semantic Similarity Score")

    st.metric(label="Resume-JD Similarity", value=f"{semantic_score:.2f}%")

    st.progress(semantic_score / 100)
