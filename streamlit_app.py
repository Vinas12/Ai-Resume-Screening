import streamlit as st
import fitz
import pandas as pd

from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

st.title("AI Resume Screening System")

st.markdown("""

This AI Resume Screening System ranks candidates based on:

- Skill Match Score
- AI Semantic Similarity Score
- Final ATS Score

Upload multiple resumes and a Job Description to find the best candidate automatically.
""")

uploaded_files = st.file_uploader(
    "Upload your resume (pdf)",
    type=["pdf"],
    accept_multiple_files=True 
    )

if not uploaded_files:
    st.warning("Please upload at least one resume.")

jd_file = st.file_uploader(
    "Upload job description",
    type =["txt"]
)

if not jd_file:
    st.warning("Please upload a Job Description file.")

#read JD
jd_text = ""
results = []
score = 0

if jd_file :
    jd_text = jd_file.read().decode("utf-8")

    st.write("job description")
    st.text(jd_text)


#read resume 
text = ""

if uploaded_files and jd_text:

    
    skills = [
    line.strip().lower()
    for line in jd_text.splitlines()
    if line.strip()
    ]

    results = []


    for uploaded_file in uploaded_files:

        
        pdf = fitz.open(
            stream = uploaded_file.read(),
            filetype = "pdf"
            )

        text = "" 

        for page in pdf :
            text += page.get_text()

        email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
        )

        if email_match:
            email = email_match.group()
        else:
            email = "Not Found"

        phone_match = re.search(
        r'(\+91[\s-]?)?[6-9]\d{9}',
        text
        )

        if phone_match:
            phone = phone_match.group()
        else:
            phone = "Not Found"

        jd_embedding = model.encode(jd_text)

        resume_embedding = model.encode(text)

        ai_score = util.cos_sim(
            jd_embedding,
            resume_embedding
        ).item()


        matched_skills = []
        missing_skills = []

        ai_score = round(ai_score * 100, 2)
        
        for skill in skills:

            if skill in text.lower():
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        score = (len(matched_skills) / len(skills)) * 100

        final_score = (score * 0.4) + (ai_score * 0.6)

        results.append(
        (
        uploaded_file.name,
        score,
        email,
        phone,
        ai_score,
        final_score,
        matched_skills,
        missing_skills
        )
        )

results.sort(
    key=lambda x: x[4],
    reverse=True
)

#BEST CANDIDATE 
if len(results) > 0:

    top_candidate = results[0]

    st.write("## 🥇 Best Candidate")

    st.success(
        f"{top_candidate[0]} | Score: {round(top_candidate[4],2)}%"
    )
    
table_data = []

for resume, score, email,phone,ai_score, final_score, matched_skills, missing_skills in results:

    table_data.append({
        "resume" : resume,
        "email": email,
        "Phone": phone,
        "final_score %" : f"{round(final_score,2)}"
    })

df = pd.DataFrame(table_data)

st.write("📊 Candidate Summary")
st.dataframe(df)

#RANKING 
st.write("## 🏆 Candidate Ranking")

for resume, score, email,phone,ai_score, final_score, matched_skills, missing_skills in results:

    st.write(f"### {resume}")

    st.write(f"Score: {score}%")

    st.write(f"Final Score: {round(final_score,2)}%")

    st.progress(int(final_score))

    if final_score >= 80:
        st.success("Excellent Candidate ⭐")
    elif final_score >= 60:
        st.warning("Good Candidate")
    else:
        st.error("Needs Improvement")

    st.info(
    f"Matched {len(matched_skills)} out of {len(skills)} skills"
    )

    st.write("Matched Skills:")

    for skill in matched_skills:
        st.success(skill)

    st.write("missing skills:")

    for skill in  missing_skills:
        st.error(skill)

    st.divider()
