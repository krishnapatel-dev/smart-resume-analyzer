import streamlit as st

st.title("Smart Resume Analyzer")

st.write("Upload your resume and compare it with a job description.")

# Upload resume
resume = st.file_uploader("Upload your Resume", type=["txt"])

resume_text = ""

if resume:
    resume_text = resume.read().decode("utf-8")
    st.success("Resume uploaded successfully!")

    st.subheader("Resume Content")
    st.write(resume_text)


# Job description input
st.subheader("Paste Job Description")

job_description = st.text_area("Enter the Job Description")

if job_description:
    st.subheader("Job Description")
    st.write(job_description)