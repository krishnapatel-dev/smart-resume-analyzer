import streamlit as st

st.title("Smart Resume Analyzer")

st.write("Upload your resume and compare it with a job description.")

resume = st.file_uploader("Upload your Resume", type=["pdf","txt"])

if resume:
    st.success("Resume uploaded successfully!")