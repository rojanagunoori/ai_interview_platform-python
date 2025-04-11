# ai_interview_platform/pages/landing.py
import streamlit as st
from PyPDF2 import PdfReader
import tempfile
from PIL import Image
from utils.gemini_utils import ask_gemini
from utils.voice_utils import speak, listen

# 👇 Import the run_interview function from interview.py
from pages.interview import run_interview


def parse_resume(resume_file):
    reader = PdfReader(resume_file)
    full_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return full_text

def run():
    st.title("\U0001F3AF AI Interview - Landing Page")

    st.subheader("\U0001F454 Choose Role & Upload Resume (optional)")
    job_role = st.selectbox("Role:", ["Frontend", "Backend", "Full Stack", "ML Engineer", "Software Engineer"])
    resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])

    resume_text = ""
    if resume_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(resume_file.read())
            resume_text = parse_resume(temp_file.name)
            st.subheader("\U0001F4C4 Parsed Resume:")
            st.text_area("Resume Text", resume_text, height=300)

    if st.button("\U0001F399️ Start Interview"):
        st.session_state["interview_started"] = True
        st.session_state["role"] = job_role
        st.session_state["resume"] = resume_text
        st.success("Interview started! Scroll down to answer questions.")

    if st.session_state.get("interview_started"):
        st.markdown("---")
        st.subheader("\U0001F916 AI Interview - Voice Interaction")

        image = Image.open("assets/interviewer.jpg")
        st.image(image, width=250, caption="AI Interviewer")

        
        run_interview(role=job_role,resumetext=resume_text)


        #if st.button("❌ End Interview"):
            #st.session_state["interview_started"] = False
            #st.session_state.q_index = 0
            #st.session_state.transcripts = []
            #st.success("✅ Interview Ended. Please go to Evaluation or Report Card from the sidebar.")
