import streamlit as st

st.title("Smart Resume Analyzer")

st.write("Upload your resume and compare it with a job description.")

# Skills list
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

# Upload resume
resume = st.file_uploader("Upload your Resume", type=["txt"])

resume_text = ""

if resume:
    resume_text = resume.read().decode("utf-8").lower()
    st.success("Resume uploaded successfully!")

    st.subheader("Resume Content")
    st.write(resume_text)


# Job description
st.subheader("Paste Job Description")

job_description = st.text_area("Enter the Job Description")

if job_description:

    jd_text = job_description.lower()

    matched_skills = []

    for skill in skills:
        if skill in resume_text and skill in jd_text:
            matched_skills.append(skill)

    st.subheader("Matched Skills")

    if matched_skills:
        for skill in matched_skills:
            st.write("✅", skill)
    else:
        st.write("No matching skills found.")