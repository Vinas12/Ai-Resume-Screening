import streamlit as st
import fitz

st.title("AI Resume Screening System")

uploaded_file = st.file_uploader(
    "Upload your resume (pdf)",
    type=["pdf"]
    accept_multiple_files=True
    )

jd_file = st.file_uploader(
    "Upload job description",
    type =["txt"]
)

#read JD
jd_text = ""

if jd_file :
    jd_text = jd_file.read().decode("utf-8")

    st.write("job description")
    st.text(jd_text)


#read resume 
text = ""

if uploaded_file :

    pdf = fitz.open(
        stream = uploaded_file.read(),
        filetype = "pdf"
        )

    for page in pdf :
        text += page.get_text()

    st.success("STREAMLIT FILES UPLOADED SUCCESSFULLY ! ")

    st.write("resume preview")

    st.text(text[:1000])


# Analyze Button
analyze = st.button("analyze resume")

if analyze and uploaded_file and jd_file:

    skills = [
        line.strip().lower()
        for line in jd_text.splitlines()
        if line.strip()
        ]

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in text.lower():
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    st.subheader("results")

    st.metric(
        "Match Score",
        f"{round(score,2)}%"
    )

    st.write("### Matched Skills")

    for skill in matched_skills:
        st.success(skill)

    st.write("### Missing Skills")

    for skill in missing_skills:
        st.error(skill)


    #against an empty JD
    if len(skills)>0:
        score = (len(matched_skills)/len(skills))*100
    else:
        score=0

    import pandas as pd 

    result_df = pd.DataFrame({
        "matched_skills" : matched_skills
    })

    st.write("### Matched Skills Table")
    st.dataframe(result_df)