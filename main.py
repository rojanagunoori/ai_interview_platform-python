import streamlit as st
from components import code_editor, landing, interview
from components import landing

st.set_page_config(page_title="AI Interview Platform", layout="wide", initial_sidebar_state="collapsed")

def main():
    
    
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
