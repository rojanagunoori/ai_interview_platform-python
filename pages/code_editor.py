import streamlit as st
import requests




import contextlib
import io
import traceback

def run_code(code):
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})
        return output_buffer.getvalue()
    except Exception:
        return traceback.format_exc()

def main():
    st.set_page_config(page_title="Local Python Compiler", layout="centered")
    st.title("🧠 Local Python Code Compiler")
    st.write("Type your Python code below and hit **Run** to see the output.")

    code = st.text_area("📝 Enter Python Code:", height=250, placeholder="print('Hello, world!')")

    if st.button("▶️ Run Code"):
        if code.strip() == "":
            st.warning("Please enter some code.")
        else:
            output = run_code(code)
            if output.strip():
                st.code(output, language='python')
            else:
                st.success("✅ Code ran successfully. No output returned.")








LANGUAGES = {"Python": 71, "C++": 54, "Java": 62}
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"

HEADERS = {
    "X-RapidAPI-Key": "your_judge0_api_key",
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "Content-Type": "application/json"
}

def run1():
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