
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
import numpy as np
import pandas as pd

#import pandas as pd
#import numpy as np

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
    cleaned_text=""


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

def get_coding_problems(role: str, resumetext: str, num_problems: int = 2):
    prompt1 = f"""Generate {num_problems} Python coding interview questions for a {role} based on this resume:
{resumetext}

Respond ONLY in JSON format like:
[
  {{
    "question": "Write a function to reverse a string.",
    "difficulty": "Easy"
  }}
]
"""
    prompt = f"""You are an expert interviewer generating technical coding questions.

Generate {num_problems} coding interview questions for the role of "{role}", 
ONLY in one of the following programming languages: Python, Java, or JavaScript.

Base the questions on this resume:
{resumetext}

Make sure the questions test programming knowledge (e.g., algorithms, data structures, problem-solving) 
and not general frontend or backend concepts. Avoid non-coding questions.

Respond ONLY in JSON format like:
[
  {{
    "question": "Write a Python function to reverse a string.",
    "difficulty": "Easy",
    "language": "Python"
  }},
  {{
    "question": "Write a JavaScript function to check if a string is a palindrome.",
    "difficulty": "Medium",
    "language": "JavaScript"
  }}
]
"""

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        cleaned_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()

        print("🧠 Gemini Coding Problems:\n", cleaned_text)

        return json.loads(cleaned_text)

    except Exception as e:
        st.toast(f"Error generating coding problems: {e}")
        return [
            {"question": "Write a function to check if a number is prime.", "difficulty": "Easy"},
            {"question": "Write a function to find the factorial of a number using recursion.", "difficulty": "Medium"}
        ]





def get_interview_feedback(questions, answers, coding_questions, code_responses, code_outputs):
    # Interview QA DataFrame
    min_len_qa = min(len(questions), len(answers))

    qa_data = pd.DataFrame({
    "question": [q["question"] for q in questions[:min_len_qa]],
    "answer": answers[:min_len_qa]
    })

    qa_data["answer"] = qa_data["answer"].replace("", "No response")
    qa_data["word_count"] = qa_data["answer"].apply(lambda x: len(str(x).split()))
    
    # Drop questions with empty answers if needed (optional)
    qa_data = qa_data[qa_data["answer"] != "No response"]

    # Limit to top 5 longest answers to reduce size
    qa_data = qa_data.sort_values(by="word_count", ascending=False).head(5)

    qa_summary = qa_data[["question", "answer"]].to_dict(orient="records")

    min_len = min(len(coding_questions), len(code_responses), len(code_outputs))

    code_data = pd.DataFrame({
    "problem": [q["question"] for q in coding_questions[:min_len]],
    "code": code_responses[:min_len],
    "output": code_outputs[:min_len]
    })

    code_data["code"] = code_data["code"].replace("", "No code submitted")
    code_data["output"] = code_data["output"].replace("", "No output")
    code_data["code_length"] = code_data["code"].apply(len)

    # Limit to top 3 longest code solutions
    code_data = code_data.sort_values(by="code_length", ascending=False).head(3)

    code_summary = code_data[["problem", "code", "output"]].to_dict(orient="records")

    # Build prompt for Gemini
    prompt = f"""
    You are an AI interview coach. Evaluate the following interview AND coding challenge answers.

    Provide:
    1. A score out of 10 for interview answers based on clarity, technical accuracy, and relevance.
    2. A score out of 10 for coding challenge quality (correctness, clarity, efficiency).
    3. A short summary of overall performance.
    4. Specific improvement tips for weak areas.

    Interview Answers:
    {json.dumps(qa_summary, indent=2)}

    Coding Challenges:
    {json.dumps(code_summary, indent=2)}

    Format your response like this:
    {{
      "interview_score": 8,
      "coding_score": 7,
      "summary": "Great understanding overall with clean coding style.",
      "improvement": "Improve code efficiency and give more structured interview answers."
    }}
    Only return JSON.
    """

    # Gemini API Call (same as before)
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
            return json.loads(cleaned_text)

        except google.api_core.exceptions.ResourceExhausted:
            st.toast("⚠️ Gemini API quota exceeded. Retrying in 35 seconds...", icon="⏳")
            time.sleep(35)

        except Exception as e:
            st.toast(f"❌ Error while generating feedback: {e}", icon="🚫")
            break

            
    st.warning("⚠️ Gemini failed. Using local analysis with NumPy & Pandas.")
    try:
        # Interview answer word analysis
        word_data = []
        for qa in qa_summary:
            words = qa["answer"].split()
            word_lengths = [len(w) for w in words]
            word_data.append({
                "question": qa["question"],
                "word_count": len(words),
                "avg_word_length": round(np.mean(word_lengths), 2) if word_lengths else 0
            })

        qa_df = pd.DataFrame(word_data)

        avg_word_count = qa_df["word_count"].mean()
        avg_word_len = qa_df["avg_word_length"].mean()

        # Skills frequency from code
        skills = ["python", "javascript", "sql", "api", "react", "node", "class", "function", "loop", "recursion"]
        all_code = " ".join(code_responses).lower()
        skill_freq = {s: all_code.count(s) for s in skills if s in all_code}

        feedback_json = {
            "interview_score": 7 if avg_word_count > 10 else 4,
            "coding_score": 6 if len(code_responses) > 0 else 2,
            "summary": f"Interview responses are {'well-explained' if avg_word_count > 10 else 'too short'}, and code uses these skills: {', '.join(skill_freq.keys()) or 'None'}.",
            "improvement": "Try giving more detailed answers and include more relevant code patterns and logic."
        }
        return feedback_json

    except Exception as e:
        return {
            "interview_score": "N/A",
            "coding_score": "N/A",
            "summary": "Could not analyze feedback.",
            "improvement": f"Fallback analysis failed: {str(e)}"
        }




def get_interview_feedback1(questions, answers, coding_questions, code_responses, code_outputs):
    #qa_summary = [
       # {"question": q["question"], "answer": answers[i] or "No response"} 
       # for i, q in enumerate(questions)
    #]
    qa_summary = []
    for i, q in enumerate(questions):
        answer = answers[i] if i < len(answers) else "No response"
        qa_summary.append({
            "question": q["question"],
            "answer": answer
        })


    prompt1 = f"""
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


    #code_summary = [
        #{
           # "problem": coding_questions[i]["question"],
            #"code": code_responses[i],
            #"output": code_outputs[i]
        #}
        #for i in range(len(coding_questions))
    #]
    code_summary = []
    for i in range(len(coding_questions)):
        code = code_responses[i] if i < len(code_responses) else "No code submitted"
        output = code_outputs[i] if i < len(code_outputs) else "No output"
        code_summary.append({
            "problem": coding_questions[i]["question"],
            "code": code,
            "output": output
        })


    prompt = f"""
    You are an AI interview coach. Evaluate the following interview AND coding challenge answers.

    Provide:
    1. A score out of 10 for **interview answers** based on clarity, technical accuracy, and relevance.
    2. A score out of 10 for **coding challenge** quality (correctness, clarity, efficiency).
    3. A short summary of overall performance.
    4. Specific improvement tips for weak areas.

    Interview Answers:
    {json.dumps(qa_summary, indent=2)}

    Coding Challenges:
    {json.dumps(code_summary, indent=2)}

    Format your response like this:
    {{
      "interview_score": 8,
      "coding_score": 7,
      "summary": "Great understanding overall with clean coding style.",
      "improvement": "Improve code efficiency and give more structured interview answers."
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
    #return {
        #"score": "N/A",
        #"coding_score": "N/A",
        #"summary": "Could not analyze feedback.",
       # "improvement": "Please try again later after API quota resets."
    #}

    # 👇 Use NumPy and Pandas fallback if Gemini fails
    st.warning("⚠️ Gemini failed. Using local analysis with NumPy & Pandas.")
    try:
        # Interview answer word analysis
        word_data = []
        for qa in qa_summary:
            words = qa["answer"].split()
            word_lengths = [len(w) for w in words]
            word_data.append({
                "question": qa["question"],
                "word_count": len(words),
                "avg_word_length": round(np.mean(word_lengths), 2) if word_lengths else 0
            })

        qa_df = pd.DataFrame(word_data)

        avg_word_count = qa_df["word_count"].mean()
        avg_word_len = qa_df["avg_word_length"].mean()

        # Skills frequency from code
        skills = ["python", "javascript", "sql", "api", "react", "node", "class", "function", "loop", "recursion"]
        all_code = " ".join(code_responses).lower()
        skill_freq = {s: all_code.count(s) for s in skills if s in all_code}

        feedback_json = {
            "interview_score": 7 if avg_word_count > 10 else 4,
            "coding_score": 6 if len(code_responses) > 0 else 2,
            "summary": f"Interview responses are {'well-explained' if avg_word_count > 10 else 'too short'}, and code uses these skills: {', '.join(skill_freq.keys()) or 'None'}.",
            "improvement": "Try giving more detailed answers and include more relevant code patterns and logic."
        }
        return feedback_json

    except Exception as e:
        return {
            "interview_score": "N/A",
            "coding_score": "N/A",
            "summary": "Could not analyze feedback.",
            "improvement": f"Fallback analysis failed: {str(e)}"
        }
