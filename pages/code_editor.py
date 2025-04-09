import streamlit as st
import requests

LANGUAGES = {"Python": 71, "C++": 54, "Java": 62}
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"

HEADERS = {
    "X-RapidAPI-Key": "your_judge0_api_key",
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "Content-Type": "application/json"
}

def run():
    st.title("Code Editor")
    st.write("AI Challenge: Write a function to reverse a string")

    lang = st.selectbox("Choose Language", list(LANGUAGES.keys()))
    code = st.text_area("Your Code:", height=300)

    if st.button("Run Code"):
        payload = {
            "language_id": LANGUAGES[lang],
            "source_code": code,
            "stdin": ""
        }
        response = requests.post(JUDGE0_URL + "?base64_encoded=false&wait=true", json=payload, headers=HEADERS)
        result = response.json()
        st.code(result.get("stdout", "No output"))
        st.error(result.get("stderr", ""))