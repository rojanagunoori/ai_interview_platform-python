import streamlit as st
from components import code_editor, landing, interview
from components import landing

st.set_page_config(page_title="AI Interview Platform", layout="wide", initial_sidebar_state="collapsed")


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


def main():
    st.markdown(STYLE_CSS, unsafe_allow_html=True)
    
    
    # 👇 Hide Streamlit's default elements
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Initialize session state variables
    if "role" not in st.session_state:
        st.session_state["role"] = None  # or a default value like "candidate" or "interviewer"

    if "resume" not in st.session_state:
        st.session_state["resume"] = None  

    # Initialize the session state if not set
    if "page" not in st.session_state:
        st.session_state["page"] = "landing"  # Default page

    if "role" not in st.session_state:
        st.session_state["role"] = ""  # Default role

    if "resume" not in st.session_state:
        st.session_state["resume"] = ""  # Default resume

    #if "interview_started" not in st.session_state:
        #st.session_state["interview_started"] = False  # Interview started flag
    if "interview_started" in st.session_state and st.session_state["interview_started"]:
        if st.session_state.get("page") == "interview":
            landing.interview_page()
        else:
            landing.landing_page()

    
    # Show the appropriate page based on the session state
    if st.session_state["page"] == "landing":
        pass
        landing.run()
    elif st.session_state["page"] == "interview":
        # Ensure that role and resume are set in session state before passing to interview
        if "role" in st.session_state and "resume" in st.session_state:
            pass
            #role = st.session_state["role"]
            #resume = st.session_state["resume"]

            # Debugging print statements
            #st.write(f"Role: {role}")  # Check if role is set
            #st.write(f"Resume: {resume}")  # Check if resume is set

            # Pass the role and resume to interview
            #interview.run_interview(role=role, resumetext=resume)
        else:
            pass
            #st.error("Role or resume not found in session state!")
        
        # Show feedback after interview
        if st.session_state.get("interview_completed"):
            st.session_state["page"] = "feedback"
            pass
            #st.experimental_rerun()
    elif st.session_state["page"] == "feedback":
        pass
        interview.display_feedback()
        
    #landing.run()

if __name__ == "__main__":
    main()
