import streamlit as st
from pages import landing, interview, code_editor, evaluation, report_card

def main():
    st.set_page_config(page_title="AI Interview Platform", layout="wide")
    
    pages = {
        "Landing Page": landing.run,
        "Interview (Voice/Text)": interview.run,
        "Code Editor": code_editor.run,
        "Evaluation": evaluation.run,
        "Report Card": report_card.run
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()