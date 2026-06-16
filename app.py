import os
import pdfplumber

# Read JD
with open("jd/job_description.txt", "r") as f:
    jd_txt = f.read()

skills = [
    line.strip().lower()
    for line in jd_txt.splitlines()
    if line.strip()
]

files = os.listdir("resumes")

results = []

for file in files:

    pdf_path = os.path.join("resumes", file)

    with pdfplumber.open(pdf_path) as pdf:

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    matched_skill = []

    for skill in skills:

        if skill in text.lower():

            matched_skill.append(skill)

    score = (len(matched_skill) / len(skills)) * 100

    results.append((file, score))

# Print Results
print("\n===== SCORES =====")

results.sort(
    key=lambda x : x[1],
    reverse=True
)

for resume,score in results :
    print(f"{resume} -> {round(score,2)}%")