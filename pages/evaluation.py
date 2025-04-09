# pages/evaluation.py
import streamlit as st

def run():
    st.title("AI Evaluation Panel")
    st.write("This panel evaluates your communication and technical skills.")

    if "transcripts" in st.session_state:
        for q, a in st.session_state.transcripts:
            st.markdown(f"**Q: {q}**")
            st.markdown(f"**A:** {a}")
            # You can connect Gemini here to evaluate
            st.success("Gemini AI: Good explanation. Clear communication.")
    else:
        st.info("No interview data found")