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

    # Create two columns
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

    # Recommended skills to learn
    st.subheader("Recommended Skills to Learn")

    if missing_skills:
        for skill in missing_skills:
            st.write("📚", skill)
    else:
        st.write("Your resume already matches the job requirements!")

    # Match Score
    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:
        score = int((len(matched_skills) / total_skills) * 100)

        st.subheader("Resume Match Score")

        total_skills = len(matched_skills) + len(missing_skills)

        if total_skills > 0:
            score = int((len(matched_skills) / total_skills) * 100)

            st.metric(label="Match Score", value=f"{score}%")

            st.progress(score / 100)