import streamlit as st
import pdfplumber
import docx
import spacy
from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def load_models():
    nlp = spacy.load("en_core_web_sm")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return nlp, model

nlp, model = load_models()

SKILLS = [
    "python","java","javascript","react","node","express",
    "machine learning","deep learning","tensorflow","pytorch",
    "sql","mongodb","mysql","docker","kubernetes","aws",
    "azure","gcp","linux","data structures","algorithms",
    "cybersecurity","networking"
    ]


def extract_skills(text):

    found_skills = []

    doc = nlp(text)

    for token in doc:
        if token.text.lower() in SKILLS:
            found_skills.append(token.text.lower())

    return list(set(found_skills))


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
    resume_text = extract_text(resume).lower().replace("\n"," ")
    resume_skills = extract_skills(resume_text)
    st.success("Resume uploaded successfully!")

st.subheader("Paste Job Description")
job_description = st.text_area("Enter the Job Description")

if resume_text and job_description:

    jd_text = job_description.lower()

    skills = SKILLS


    matched_skills = []
    missing_skills = []

    for skill in skills:
        if skill in jd_text:
            if skill in resume_text:

                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    st.subheader("Skills Found in Resume")
    if resume_skills:
        st.write(", ".join(resume_skills))
    else:
        st.write("No predefined skills detected in resume")

    # Sentence Transformer similarity
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, jd_embedding)

    semantic_score = float(similarity[0][0]) * 100

    st.subheader("Semantic Similarity Score")

    st.metric(label="Resume-JD Similarity", value=f"{semantic_score:.2f}%")

    st.progress(semantic_score / 100)

    st.subheader("Skill Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write("✅", skill)
        else:
            st.write("No matched skills")

    with col2:
        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write("❌", skill)
        else:
            st.write("No missing skills")


    skill_score = (len(matched_skills) / len(skills)) * 100 if skills else 0
    final_score = (semantic_score * 0.6) + (skill_score * 0.4)


    st.subheader("Recommended Skills to Learn")
    

    if missing_skills:
        for skill in missing_skills:
            st.write("📚", skill)
    else:
        st.write("Your resume already matches the job requirements!")

    st.subheader("Final ATS Score")

    st.metric(label="ATS Resume Score", value=f"{final_score:.2f}%")

    st.progress(final_score/100)

