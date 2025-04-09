import streamlit as st
import speech_recognition as sr
from utils.voice_utils import speak, listen

QUESTIONS = [
    "Tell me about yourself.",
    "What are your strengths and weaknesses?",
    "Describe a recent project you've worked on."
]

def run():
    st.title("AI Voice Interview")
    run_interview()

def run_interview():
    st.subheader("🧠 Voice Q&A Interview")

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.transcripts = []

    if st.session_state.q_index < len(QUESTIONS):
        question = QUESTIONS[st.session_state.q_index]
        st.write(f"**Question {st.session_state.q_index + 1}:** {question}")

        if st.button("🔊 Ask Question (Voice)"):
            speak(question)

        if st.button("🎤 Record Answer"):
            try:
                st.info("🎙️ Listening... Please speak clearly.")
                text = listen(timeout=5, phrase_time_limit=10)
                st.success(f"🗣️ You said: {text}")
                st.session_state.transcripts.append((question, text))
                st.session_state.q_index += 1
            except sr.WaitTimeoutError:
                st.warning("⏰ No speech detected. Please try again.")
            except sr.UnknownValueError:
                st.error("❌ Could not understand what you said.")
            except sr.RequestError as e:
                st.error(f"🌐 Could not connect to the recognition service: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {str(e)}")
    else:
        st.success("🎉 Interview Complete! Check Evaluation tab.")
        if st.button("🔁 Restart"):
            st.session_state.q_index = 0
            st.session_state.transcripts = []
