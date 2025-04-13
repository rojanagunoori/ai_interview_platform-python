# ai_interview_platform/pages/landing.py
import streamlit as st
from PyPDF2 import PdfReader
import tempfile
#from PIL import Image
import time
from components import interview
import uuid


# 👇 Import the run_interview function from interview.py
from components.interview import run_interview

STYLE_CSS ="""
    <style>
        body {
            background-color: #fdf6f6; /* soft light maroon background */
        }

        .stApp {
            background-color: #fbecec;
            color: #4b1c1c;
        }

        /* Style titles and headers */
        h1, h2, h3 {
            color: #800000 !important;  /* dark maroon */
        }

        /* Style selectbox and file uploader */
        .stSelectbox label, .stFileUploader label {
            font-weight: bold;
            color: #800000;
        }
        
        * Selectbox input area (selected value) */
    div[data-baseweb="select"] {
        background-color: #fff8f8;
        border: 2px solid #a52a2a;
        border-radius: 8px;
        color: #4b1c1c;
    }

    /* Dropdown options */
    div[data-baseweb="popover"] {
        background-color: #fff8f8;
        border: 1px solid #800000;
        color: #4b1c1c;
    }

    /* Individual options hover effect */
    div[data-baseweb="popover"] div[role="option"]:hover {
        background-color: #fcdcdc;
        color: #800000;
    }

        /* Button styles */
        button[kind="primary"] {
            background-color: #800000;
            color: white;
            border: none;
            transition: all 0.3s ease;
            border-radius: 8px;
            padding: 0.6em 1.2em;
        }

        button[kind="primary"]:hover {
            background-color: #a52a2a;
            transform: scale(1.03);
            box-shadow: 0 0 10px #a52a2a88;
        }

        /* Style text area */
        textarea {
            border: 2px solid #a52a2a;
            border-radius: 5px;
            background-color: #fff8f8;
            color: #4b1c1c;
        }

        /* Animate section transitions */
        .stMarkdown, .stFileUploader, .stSelectbox, .stButton {
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
"""


def parse_resume(resume_file):
    reader = PdfReader(resume_file)
    full_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return full_text

def landing_page():
    st.title("\U0001F3AF AI Interview - Landing Page")
    st.markdown(STYLE_CSS, unsafe_allow_html=True)

    st.subheader("\U0001F454 Choose Role & Upload Resume (optional)")
    # Initialize `page_number` if it doesn't exist
    if "page_number" not in st.session_state:
        st.session_state.page_number = 0  # or any default value you prefer
    
    unique_key = f"job_role_{uuid.uuid4()}"
    job_role = st.selectbox("Role:", ["Frontend", "Backend", "Full Stack","React Developer","Nodejs Develoer", "ML Engineer", "Software Engineer"], key=f"job_role_{unique_key}"   )
    resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'], key=f"resume_uploader_{unique_key}")

    resume_text = ""
    if resume_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(resume_file.read())
            resume_text = parse_resume(temp_file.name)
            st.subheader("\U0001F4C4 Parsed Resume:")
            st.text_area("Resume Text", resume_text, height=300)
    #st.write(f"Button before clicked: Starting interview with role {job_role}") 

    
    # Only generate the key once per session
    if "start_button_key" not in st.session_state:
        st.session_state["start_button_key"] = f"start_btn_{str(uuid.uuid4())}"

     
    if st.button("\U0001F399️ Start Interview", key=st.session_state["start_button_key"]):
        # Clear all conflicting session state
        #for key in st.session_state.keys():
            #del st.session_state[key]
        #st.write(f"Button clicked: Starting interview with role {job_role}")  # Replacing print with st.write

        print(f"Button clicked: Starting interview with role {job_role}")
        
        interview.show_css_loader("Generating interview questions...")

        # Simulate delay
        time.sleep(2)

        
        
        st.session_state["role"] = job_role
        st.session_state["resume"] = resume_text
        st.session_state["interview_started"] = True
        st.session_state["page"] = "interview"
        
        print(f"Session State after button click: {st.session_state}")

        # Provide feedback and move to the interview page
        st.success("Interview started!")
        st.session_state.page = "interview"
        #st.session_state["page"] = "interview"  # Change the page state to "interview"
        print(f"Page set to: {st.session_state['page']}")

        # Add a debug message using Streamlit's st.write()
        #st.write("Session State:", st.session_state)
        #run_interview(job_role, resume_text)
        #st.experimental_rerun()
        time.sleep(1) 
        st.rerun()
        #st.stop() 
        


def interview_page():
    job_role = st.session_state["role"]
    resume_text = st.session_state["resume"]
    print(f"Rendering interview page for {job_role} with resume: {resume_text[:100]}...") 
    run_interview(job_role, resume_text)



def run():
    # Set default values
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "page" not in st.session_state:
        st.session_state.page = "landing"
        
    print(f"Checking session state: {st.session_state}")
    # Check if interview has started, and render the respective page
    if "interview_started" in st.session_state and st.session_state["interview_started"]:
    #if st.session_state.interview_started:
        if st.session_state.page == "interview":
            print("Rendering interview page...")
            interview_page()  # Render interview page
        else:
            print("Rendering landing page...")
            landing_page()  # Render landing page by default
    else:
        print("Interview hasn't started yet. Rendering landing page...")
        landing_page()  # Render landing page if interview hasn't started yet  