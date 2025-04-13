import streamlit as st
import speech_recognition as sr
from components import code_editor, landing, interview

import time
from components.code_editor import run_code
#import threading
from utils.gemini_utils import get_questions, get_coding_problems,get_gemini_response,get_interview_feedback
from utils.voice_utils import speak, listen, stop_speaking
import uuid
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



    
if 'last_audio_index' not in st.session_state:
    st.session_state.last_audio_index = -1


def reset_interview(role, resumetext):
    st.session_state.questions = get_questions(role, resumetext, num_questions=5)
    st.session_state.current_question_index = 0
    st.session_state.responses = []
    st.session_state.chat_history = []
    st.session_state.audio_file = None
    
    st.session_state.coding_questions = get_coding_problems(role, resumetext)
    st.session_state.current_code_index = 0
    st.session_state.code_responses = []
    st.session_state.code_outputs = []


def run_interview(role, resumetext):
    st.title("🎤 AI Interviewer")
    

    if 'questions' not in st.session_state or not st.session_state.questions:
        reset_interview(role, resumetext)

    index = st.session_state.current_question_index
    questions = st.session_state.questions

    if index < len(questions):#==
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
                    "answer": transcript,
                    'recorded_audio':audio['bytes']  # Store the recorded audio with the chat
                })
                st.session_state.current_question_index += 1
                st.session_state.audio_file = None
                st.session_state.recorded_audio = None#audio['bytes']  # Save the recorded audio
                st.rerun()
                
           
        
            if st.button("❌ End Interview"):
                st.session_state.current_question_index = len(questions)
                # Ensure coding questions start from index 0 if not already started
                st.session_state.current_code_index = len(st.session_state.coding_questions)
                #if 'current_code_index' not in st.session_state:
                    #st.session_state.current_code_index = 0
                st.rerun()

        with col2:
            st.markdown("### 💬 Interview Chat")
            for i, chat in enumerate(st.session_state.chat_history):
                with st.chat_message("🤖 AI"):
                    st.markdown(f"**Q{i+1}:** {chat['question']}")
                with st.chat_message("👤 You"):
                    st.markdown(f"**A{i+1}:** {chat['answer']}")
                     # Display the recorded audio once the recording is finished
                    if 'recorded_audio' in chat:#st.session_state and st.session_state.recorded_audio:
                        st.markdown("### 🎶 Your Recorded Audio:")
                        audio_bytes = chat['recorded_audio']#st.session_state.recorded_audio
                        st.audio(audio_bytes, format="audio/wav")  # Display and play the recorded audio
            

    else:
        # All interview questions are done ✅
        #if 'current_code_index' not in st.session_state:
            #st.session_state.current_code_index = 0
        # Init session state vars if not present
        if 'code_outputs' not in st.session_state:
            st.session_state.code_outputs = []

        if 'code_responses' not in st.session_state:
            st.session_state.code_responses = []

        if 'show_output' not in st.session_state:
            st.session_state.show_output = False
            

        code_index = st.session_state.current_code_index
        coding_questions = st.session_state.coding_questions

        if code_index < len(coding_questions):
            st.header("🧪 Coding Challenges")
            current_code_q = coding_questions[code_index]
            st.subheader(f"💻 Coding Problem {code_index + 1}")
            st.markdown(f"**{current_code_q['question']}**")
            
            #language = st.selectbox("Select Language", ["python", "javascript", "java", "c", "cpp"], index=0)
            # Dynamically create a unique key for each selectbox based on the question index
            language = st.selectbox(
                "Select Language", 
                ["python", "javascript", "java", "c", "cpp"], 
                index=0,
                key=f"language_{st.session_state.current_code_index}"  # Unique key
            )



            code_input = st.text_area(
                "✍️ Write your code here:",
                 key=f"code_input_{st.session_state.current_code_index}",  # Unique key for each code area

                #key=f"code_input_{code_index}",
                height=250,
                placeholder="Write your Python code..."
            )
            
            # Simulating input for Python's `input()`
            if language != "":
                user_input ="" #st.text_input("Simulate input() here:", "Enter your name")  # Default value to guide the user
            else:
                user_input = ""  # For now, input simulation is limited to Python.


            run_btn = st.button("▶️ Run Code")
            if run_btn:
                output = run_code(code_input, language, user_input)
    
                if len(st.session_state.code_responses) <= code_index:
                    st.session_state.code_responses.append(code_input)
                    st.session_state.code_outputs.append(output)
                else:
                    st.session_state.code_responses[code_index] = code_input
                    st.session_state.code_outputs[code_index] = output

                st.session_state.show_output = True
                #st.rerun()
                
                # Show output if available
            if st.session_state.show_output and code_index < len(st.session_state.code_outputs):
                st.subheader("🧾 Output:")
                st.code(st.session_state.code_outputs[code_index])

                # Show next button only after output is displayed
                next_btn = st.button("➡️ Next Question")
                if next_btn:
                    st.session_state.current_code_index += 1
                    st.session_state.show_output = False
                    st.rerun()

                #st.session_state.current_code_index += 1
                #st.rerun()
        
        else:
            st.session_state["interview_completed"] = True  # Mark interview as completed
            st.session_state["page"] = "feedback"  # Change page state to feedback
            display_feedback()
            st.rerun()  


def clear_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
            

def display_feedback():
    st.success("✅ Interview & Coding Completed!")
    st.markdown("## 📝 Interview Summary")

    # Display interview responses
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        st.markdown(f"**Answer:** {st.session_state.responses[i] if i < len(st.session_state.responses) else 'No response'}")

    # Display coding responses and outputs
    st.markdown("## 💻 Coding Summary")
    for i, cq in enumerate(st.session_state.coding_questions):
        st.markdown(f"**Problem {i+1}: {cq['question']}**")
        st.markdown("**Your Code:**")
        if i < len(st.session_state.code_responses):
            st.code(st.session_state.code_responses[i])
            st.markdown("**Output:**")
            st.code(st.session_state.code_outputs[i])
        else:
            st.markdown("**No Output Generated**")

    # Get feedback on both sections
    answers = st.session_state.responses + ["No response"] * (len(st.session_state.questions) - len(st.session_state.responses))
    feedback = get_interview_feedback(
        st.session_state.questions,
        answers,
        st.session_state.coding_questions,
        st.session_state.code_responses,
        st.session_state.code_outputs
    )

    # Display the feedback
    st.markdown("### 💡 Final Feedback")
    st.markdown(f"**🧠 Interview Score:** {feedback.get('interview_score', '0')} / 10")
    st.markdown(f"**💻 Coding Score:** {feedback.get('coding_score', '0')} / 10")
    st.markdown(f"**📋 Summary:** {feedback.get('summary', 'No summary available.')}")
    st.markdown(f"**🔧 Improvement Tips:** {feedback.get('improvement', 'No tips available.')}")
    
    if "restart_start_button_key" not in st.session_state:
        st.session_state["restart_start_button_key"] = f"restart_start_button_key_{str(uuid.uuid4())}"

     
    
    if st.button("🔁 Start Again", key=st.session_state["restart_start_button_key"]):
        clear_session()
        show_css_loader("Restarting... Please wait")
        #time.sleep(1)
        
         # Clear session state
        
        role = st.session_state.get("role", None)
        resume = st.session_state.get("resume", None)

        reset_interview(role, resume)
        #st.session_state["interview_started"] = False
        #reset_interview(st.session_state["role"], st.session_state["resume"])
        st.session_state.current_code_index = 0
        #st.session_state["page"] = "landing"  # Change page back to landing
        landing.run()
        st.rerun()  # Refresh to show the landing page


      
def give_feedback():
    all_answers = "\n".join(st.session_state.answers)
    prompt = f"""Based on the following interview answers, give professional feedback with strengths and suggestions for improvement:

{all_answers}
"""
    feedback = get_gemini_response(prompt)
    st.subheader("📝 AI Feedback:")
    st.write(feedback)
        

def show_css_loader(text="Loading..."):
    st.markdown(
        f"""
        <style>
        .loader-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 200px;
        }}
        .loader {{
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
        <div class="loader-container">
            <div class="loader"></div>
            <p style="margin-top: 15px; font-weight: bold;">{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )












