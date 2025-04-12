import streamlit as st
import speech_recognition as sr

#import threading
from utils.gemini_utils import get_questions, get_coding_problems,get_gemini_response,get_interview_feedback
from utils.voice_utils import speak, listen, stop_speaking

#import tkinter as tk
#import time

#import wave
#import pyaudio

from gtts import gTTS
#import pygame
import os
import tempfile
from streamlit_mic_recorder import mic_recorder



# Audio transcription
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name
    with sr.AudioFile(temp_audio_path) as source:
        audio = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "⚠️ Could not understand audio."
    except sr.RequestError as e:
        transcript = f"⚠️ API error: {e}"
    os.remove(temp_audio_path)
    return transcript

# Text to audio file
def generate_audio(text):
    tts = gTTS(text)
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    tts.save(path)
    return path

# Reset interview state
def reset_interview(role, resumetext):
    st.session_state.current_question_index = 0
    st.session_state.responses = []
    #st.session_state.questions = []
    st.session_state.audio_file = None
    st.session_state.chat_history = []
    
    # Get fresh Gemini questions
    #st.session_state.questions = get_questions(role, resumetext)
    #if isinstance(st.session_state.questions, str):  # In case it's a raw JSON string
        #import json
        #st.session_state.questions = json.loads(st.session_state.questions)

    #st.success("🔄 Interview reset! Fresh questions loaded.")
    
if 'last_audio_index' not in st.session_state:
    st.session_state.last_audio_index = -1


def reset_interview(role, resumetext):
    st.session_state.questions = get_questions(role, resumetext, num_questions=5)
    st.session_state.current_question_index = 0
    st.session_state.responses = []
    st.session_state.chat_history = []
    st.session_state.audio_file = None

def run_interview(role, resumetext):
    st.title("🎤 AI Interviewer")

    if 'questions' not in st.session_state or not st.session_state.questions:
        reset_interview(role, resumetext)

    index = st.session_state.current_question_index
    questions = st.session_state.questions

    if index < len(questions):
        current_question = questions[index]['question']
        
        # ✅ Automatically generate audio when question index changes
        if st.session_state.get("last_audio_index") != index:
            st.session_state.audio_file = generate_audio(current_question)
            st.session_state.last_audio_index = index

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ❓ Question")
            st.markdown(f"**{current_question}**")

            if st.session_state.audio_file is None:
                st.session_state.audio_file = generate_audio(current_question)
                st.session_state.audio_autoplay = True

            if st.session_state.audio_file:
                audio_bytes = open(st.session_state.audio_file, 'rb').read()
                st.audio(audio_bytes, format='audio/mp3')

            st.markdown("### 🎤 Your Response")
            audio = mic_recorder(
                start_prompt="Start Recording",
                stop_prompt="Stop Recording",
                just_once=True,
                format="wav"
            )

            if audio and audio['bytes']:
                transcript = transcribe_audio(audio['bytes'])
                st.session_state.responses.append(transcript)
                st.session_state.chat_history.append({
                    "question": current_question,
                    "answer": transcript
                })
                st.session_state.current_question_index += 1
                st.session_state.audio_file = None
                st.rerun()
        
            if st.button("❌ End Interview"):
                st.session_state.current_question_index = len(questions)
                st.rerun()

        with col2:
            st.markdown("### 💬 Interview Chat")
            for i, chat in enumerate(st.session_state.chat_history):
                with st.chat_message("🤖 AI"):
                    st.markdown(f"**Q{i+1}:** {chat['question']}")
                with st.chat_message("👤 You"):
                    st.markdown(f"**A{i+1}:** {chat['answer']}")

    else:
        st.success("✅ Interview Completed!")
        st.markdown("## 📝 Interview Summary")

        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            st.markdown(f"**Answer:** {st.session_state.responses[i] if i < len(st.session_state.responses) else 'No response'}")

        
        #feedback = get_interview_feedback(st.session_state.questions, st.session_state.responses)
        # Pad missing responses with "No response"
        answers = st.session_state.responses + ["No response"] * (len(st.session_state.questions) - len(st.session_state.responses))
        feedback = get_interview_feedback(st.session_state.questions, answers)


        st.markdown("### 💡 Feedback")
        st.markdown(f"**🧠 Score:** {feedback['score']} / 10")
        st.markdown(f"**📝 Summary:** {feedback['summary']}")
        st.markdown(f"**🔧 Areas to Improve:** {feedback['improvement']}")

        if st.button("🔁 Start Again"):
            reset_interview(role, resumetext)
            st.rerun()





















def run_interview1(role,resumetext):
    st.title("🎤 AI Interviewer")

    

       
def give_feedback():
    all_answers = "\n".join(st.session_state.answers)
    prompt = f"""Based on the following interview answers, give professional feedback with strengths and suggestions for improvement:

{all_answers}
"""
    feedback = get_gemini_response(prompt)
    st.subheader("📝 AI Feedback:")
    st.write(feedback)
        















# Custom shimmer animation for timeout
def loading_animation():
    st.markdown("""
        <style>
        .loader {
          height: 20px;
          background: linear-gradient(to right, #06f 0%, #09f 50%, #06f 100%);
          background-size: 200% auto;
          animation: shimmer 2s linear infinite;
        }
        @keyframes shimmer {
          0% { background-position: 200% center; }
          100% { background-position: -200% center; }
        }
        </style>
        <div class='loader'></div>
    """, unsafe_allow_html=True)

def run():
    st.title("🎯AI Voice Interview")
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.transcripts = []
        # Simulate AI questions
        QUESTIONS = [
         "Tell me about yourself",
    "What are your strengths and weaknesses?",
    "Describe a recent project you've worked on",
        ]

    if st.session_state.q_index < len(QUESTIONS):
        question = QUESTIONS[st.session_state.q_index]
        st.write(f"**Question {st.session_state.q_index + 1}:** {question}")

        if st.button("Ask Question (Voice)"):
            speak(question)

        if st.button("Record Answer (Requires mic access)"):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                st.success(f"You said: {text}")
                st.session_state.transcripts.append((question, text))
                st.session_state.q_index += 1
            except Exception as e:
                st.error("Could not recognize speech. Try again.")
    else:
        st.success("Interview Done! View Evaluation & Report Card")
        st.session_state.q_index = 0
   
