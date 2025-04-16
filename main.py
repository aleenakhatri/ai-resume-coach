import streamlit as st
import os
import docx
import fitz  # PyMuPDF
import random

# ========= Resume File Handling =========
def read_uploaded_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_type == "pdf":
        pdf_bytes = uploaded_file.read()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    else:
        return "Unsupported file type"

# ========= UI =========
st.title("AI Resume Coach (Mock Mode 🧠)")
st.write("This AI-style tool gives tailored resume feedback — without using paid APIs!")

input_method = st.radio("Choose how you want to enter your resume and job description:", ["Upload files", "Paste text"])
job_type = st.selectbox("Select the job category you're applying for:", [
    "Software Engineer", "Frontend Developer", "Data Analyst", "Cybersecurity", "UX/UI Designer",
    "Product Manager", "Tech Support", "Machine Learning", "Digital Marketing", "Other"
])

resume = ""
job_desc = ""

if input_method == "Upload files":
    resume_file = st.file_uploader("Upload your resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    job_file = st.file_uploader("Upload the job description (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

    if resume_file is not None:
        resume = read_uploaded_file(resume_file)

    if job_file is not None:
        job_desc = read_uploaded_file(job_file)

elif input_method == "Paste text":
    resume = st.text_area("Paste your resume here", height=200)
    job_desc = st.text_area("Paste the job description here", height=200)

st.text_area("Resume Preview", resume, height=200)
st.text_area("Job Description Preview", job_desc, height=200)

# ========= Analyze Button =========
if st.button("Analyze"):
    if resume and job_desc:
        with st.spinner("Analyzing with mock AI..."):

            resume_lower = resume.lower()
            job_lower = job_desc.lower()

            # ---------- Job + Resume Logic ----------
            if "cybersecurity" in resume_lower and "backend" in job_lower:
                score = "Low"
                feedback = """
Missing Keywords:
backend development, APIs, database systems

Suggestions:
- Emphasize transferable skills like scripting or system design
- Add backend-related projects to show relevance
"""

            elif "python" in resume_lower and "git" not in resume_lower:
                score = "Medium"
                feedback = """
Missing Keywords:
version control, collaboration tools

Suggestions:
- Consider mentioning Git or GitHub
- Employers expect version control with Python skills
"""

            elif "collaborate" not in resume_lower and job_type in ["Product Manager", "Tech Support", "UX/UI Designer"]:
                score = "Low"
                feedback = """
Missing Keywords:
collaboration, teamwork, cross-functional

Suggestions:
- Emphasize group work or communication skills
- Include projects where you worked with others
"""

            elif "cloud" in job_lower and "aws" not in resume_lower and "azure" not in resume_lower:
                score = "Low"
                feedback = """
Missing Keywords:
AWS, Azure, cloud infrastructure

Suggestions:
- Add cloud platform experience or certifications
- Show familiarity with deployment environments
"""

            elif "data" in job_type.lower() and "sql" not in resume_lower:
                score = "Medium"
                feedback = """
Missing Keywords:
SQL, data queries, relational databases

Suggestions:
- Mention any experience querying data or using dashboards
- Add courses or tools like PostgreSQL, MySQL
"""

            else:
                score = random.choice(["High", "Medium", "Low"])
                mock_feedback = {
                    "High": """
Missing Keywords:
collaboration, GitHub

Suggestions:
- Strengthen teamwork stories
- Add more detail about tools used in your projects
""",
                    "Medium": """
Missing Keywords:
cloud services, APIs

Suggestions:
- Mention technical environments you've worked in
- Describe how your work fits into larger systems
""",
                    "Low": """
Missing Keywords:
testing, performance optimization

Suggestions:
- Add metrics to your achievements
- Show how you debug or optimize code
"""
                }
                feedback = mock_feedback[score]

            # ---------- Tone of Voice ----------
            tones = [
                "You're on the right track — just a few tweaks away from a great match!",
                "Nice foundation — time to level up a few areas!",
                "You've got potential here. Let’s bridge the gap with a few additions.",
                "Solid effort! Let’s align your resume more with this role."
            ]
            tone_msg = random.choice(tones)

            # ---------- Visual Score ----------
            st.subheader("Match Score")
            if score == "High":
                st.markdown("🌟🌟🌟🌟🌟 Excellent fit")
            elif score == "Medium":
                st.markdown("🌟🌟🌟 Some alignment — needs improvement")
            else:
                st.markdown("🌟 Possibly a stretch — update your resume")

            # ---------- Display Output ----------
            st.subheader("Feedback Summary")
            st.markdown(feedback)

            st.subheader("AI Coach Says...")
            st.info(tone_msg)

    else:
        st.warning("Please enter both a resume and a job description.")
