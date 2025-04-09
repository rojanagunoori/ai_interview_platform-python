
# ai_interview_platform/utils/gemini_utils.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from google.generativeai import list_models
import json
import re


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

def get_questions(role: str, num_questions: int = 5):
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
        return []

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
