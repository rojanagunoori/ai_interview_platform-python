
# ai_interview_platform/utils/gemini_utils.py
import os
import google.api_core.exceptions
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from google.generativeai import list_models
import json
import re
import time

load_dotenv()



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#genai.configure(api_key="AIzaSyC-tUEPXzdYoHGzxQvK_djNLvMu2b_-xUQ")
#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model = genai.GenerativeModel("gemini-pro")

MODEL_NAME ="models/gemini-1.5-pro"#"models/gemini-pro" #"models/gemini-1.5-pro-latest" 



#models = genai.list_models()
#for model in models:
    #st.write(model.name, model.supported_generation_methods)
    #print(model.name, model.supported_generation_methods)
    
    
def ask_gemini(prompt):
    #models = genai.list_models()
    #for model in models:
        #st.write(model.name, model.supported_generation_methods)
        #print(model.name, model.supported_generation_methods)
    
    model = genai.GenerativeModel(model_name="models/gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def get_coding_problems(role="Software Engineer"):
    prompt = f"Give 2 coding problems suitable for a {role} candidate in an interview. Include problem title and description."
    #model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text


def get_gemini_response(chat_history):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = chat_history + "\nWhat is the next interview question?"
    response = model.generate_content(prompt)
    return response.text.strip()

def get_questions(role: str, resumetext: str, num_questions: int = 5):
    behavioral_questions = [
        {"question": "Tell me about yourself.", "answer": "This is where you give a concise summary of your background, skills, and goals."},
        {"question": "What are your strengths and weaknesses?", "answer": "Explain one strength with an example and one weakness you're working on."},
        {"question": "Why do you want this job?", "answer": "Relate the job role to your goals, interests, and values."},
        {"question": "Describe a challenge you've faced and how you handled it.", "answer": "Explain the situation, actions you took, and outcome."},
        {"question": "Where do you see yourself in five years?", "answer": "Share career goals aligned with the company/role."}
    ]

    prompt = f"""Generate {num_questions} technical interview questions and answers for a {role} developer. 
Respond in JSON format like this:
[
  {{
    "question": "What is React?",
    "answer": "React is a JavaScript library for building user interfaces."
  }}
]
ONLY return valid JSON. Do not include markdown formatting like triple backticks or extra text.
"""

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt)

        raw_text = response.text.strip()
        cleaned_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()

        print("🔎 Gemini Raw Response:\n", cleaned_text)

        qa_pairs = json.loads(cleaned_text)
        if not isinstance(qa_pairs, list):
            raise ValueError("Not a list of Q&A")

        return qa_pairs

    except google.api_core.exceptions.ResourceExhausted:
        st.toast("⚠️ Gemini API quota exceeded. Showing default questions.", icon="🚫")
        return behavioral_questions

    except Exception as e:
        st.toast(f"❌ Error generating questions: {e}", icon="⚙️")
        print("👀 Cleaned text was:\n", cleaned_text)
        return behavioral_questions

def get_interview_feedback(questions, answers):
    qa_summary = [
        {"question": q["question"], "answer": answers[i] or "No response"} 
        for i, q in enumerate(questions)
    ]

    prompt = f"""
    You are an AI interview coach. Evaluate the following interview answers.
    Provide:
    1. A score out of 10 based on clarity, technical accuracy, and relevance.
    2. A short summary of overall performance.
    3. Specific improvement tips for weak areas.

    Here are the answers:
    {json.dumps(qa_summary, indent=2)}

    Format your response like this:
    {{
      "score": 8,
      "summary": "You answered most questions well with clear examples.",
      "improvement": "Try to give more specific examples when discussing challenges."
    }}
    Only return JSON.
    """

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    for attempt in range(3):  # Retry logic
        try:
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
            return json.loads(cleaned_text)

        except google.api_core.exceptions.ResourceExhausted:
            st.toast("⚠️ Gemini API quota exceeded. Retrying in 35 seconds...", icon="⏳")
            time.sleep(35)  # Wait before retry

        except Exception as e:
            st.toast(f"❌ Error while generating feedback: {e}", icon="🚫")
            break

    # If it fails after retries
    return {
        "score": "N/A",
        "summary": "Could not analyze feedback.",
        "improvement": "Please try again later after API quota resets."
    }

###main but chnaged beacuse of toast this working fine
def get_interview_feedback1(questions, answers):
    qa_summary = [
        {"question": q["question"], "answer": answers[i] or "No response"} 
        for i, q in enumerate(questions)
    ]
    
    prompt = f"""
    You are an AI interview coach. Evaluate the following interview answers.
    Provide:
    1. A score out of 10 based on clarity, technical accuracy, and relevance.
    2. A short summary of overall performance.
    3. Specific improvement tips for weak areas.

    Here are the answers:
    {json.dumps(qa_summary, indent=2)}
    
    Format your response like this:
    {{
      "score": 8,
      "summary": "You answered most questions well with clear examples.",
      "improvement": "Try to give more specific examples when discussing challenges."
    }}
    Only return JSON.
    """

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    cleaned_text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
    
    try:
        return json.loads(cleaned_text)
    except Exception as e:
        print("Feedback JSON parsing error:", e)
        return {
            "score": "N/A",
            "summary": "Could not analyze feedback.",
            "improvement": "Please try again or check your answers."
        }

    # 🔄 Replace static feedback with Gemini-powered feedback

def get_questions1(role: str,resumetext:str, num_questions: int = 5):
    behavioral_questions = [
        {"question": "Tell me about yourself.", "answer": "This is where you give a concise summary of your background, skills, and goals."},
        {"question": "What are your strengths and weaknesses?", "answer": "Explain one strength with an example and one weakness you're working on."},
        {"question": "Why do you want this job?", "answer": "Relate the job role to your goals, interests, and values."},
        {"question": "Describe a challenge you've faced and how you handled it.", "answer": "Explain the situation, actions you took, and outcome."},
        {"question": "Where do you see yourself in five years?", "answer": "Share career goals aligned with the company/role."}
    ]
    prompt = f"""Generate {num_questions} technical interview questions and answers for a {role} developer. 
Respond in JSON format like this:
[
  {{
    "question": "What is React?",
    "answer": "React is a JavaScript library for building user interfaces."
  }}
]
ONLY return valid JSON. Do not include markdown formatting like triple backticks or extra text.
"""
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    
    # Clean up markdown ```json or ``` wrappers if present
    raw_text = response.text.strip()
    cleaned_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()
   
    print("🔎 Gemini Raw Response:\n",cleaned_text)

    try:
        qa_pairs = json.loads(cleaned_text)
        if not isinstance(qa_pairs, list):
            raise ValueError("Not a list of Q&A")
        return qa_pairs
    except Exception as e:
        print("Error parsing questions:", e)
        print("👀 Cleaned text was:\n", cleaned_text)
        #return []
        return behavioral_questions+qa_pairs
  

#############end

def get_questions2(role: str, num_questions: int = 5):
    for model in list_models():
        st.write(model.name)
        print(model.name)
    prompt = f"Generate 12 technical and behavioral interview questions for the role of {role}."
    #prompt = f"Generate {num_questions} interview questions and answers for a {role} developer. Format them as JSON like this: " + """
#[
  #{"question": "What is React?", "answer": "React is a JavaScript library for building user interfaces."},
  #...
#]
#"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    try:
        qa_pairs = eval(response.text)  # 🛑 Only for trusted responses! Consider `json.loads()` for safety.
        return qa_pairs
    except Exception as e:
        print("Error parsing questions:", e)
        return []
    
    
    
def get_questions1(role="Software Engineer"):
    prompt = f"Generate 12 technical and behavioral interview questions for the role of {role}."
    #model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    questions = response.text.split("\n")
    return [q for q in questions if q.strip() != ""][:12]
