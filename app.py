import streamlit as st

st.title("Smart Resume Analyzer")

st.write("Upload your resume and compare it with a job description.")

skills = [
    "python",
    "java",
    "sql",
    "machine learning",
    "data analysis",
    "react",
    "javascript",
    "docker",
]

resume = st.file_uploader("Upload your Resume", type=["txt"])

resume_text = ""

if resume:
    resume_text = resume.read().decode("utf-8").lower()
    st.success("Resume uploaded successfully!")

st.subheader("Paste Job Description")
job_description = st.text_area("Enter the Job Description")

if resume_text and job_description:

    jd_text = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in skills:
        if skill in jd_text:
            if skill in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    st.subheader("Matched Skills")

    for skill in matched_skills:
        st.write("✅", skill)

    st.subheader("Missing Skills")

    for skill in missing_skills:
        st.write("❌", skill)

    # Match Score
    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:
        score = int((len(matched_skills) / total_skills) * 100)

        st.subheader("Resume Match Score")

        st.write(f"### {score}% Match")

        st.progress(score / 100)