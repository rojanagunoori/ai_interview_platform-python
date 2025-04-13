import streamlit as st
import requests




import contextlib
import io
import traceback

import subprocess
import re


def run_code(code, language="python", user_input=""):
    output_buffer = io.StringIO()

    try:
        if language == "python":
            try:
                # Simulating the 'input' function by replacing it with user_input
                exec_globals = {'input': lambda: user_input}  # Override input function
                with contextlib.redirect_stdout(output_buffer):
                    exec(code, {})
                    #exec(code, exec_globals) 
                #return output_buffer.getvalue()
            except Exception as e:
                return str(e)
        elif language == "javascript":
            # Using Node.js to run JavaScript code
            result = subprocess.run(['node', '-e', code], capture_output=True, text=True)
            output_buffer.write(result.stdout if result.returncode == 0 else result.stderr)
        elif language == "java":
            # Save the code to a temporary file and compile it using `javac`
            try:
                # Find the public class name from the code
                match = re.search(r'public\s+class\s+(\w+)', code)
                class_name = match.group(1) if match else 'TempCode'
                filename = f"{class_name}.java"
                with open(filename, 'w') as f:
                    f.write(code)
                # Capture compilation errors
                compile_result = subprocess.run(["javac", filename], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    output_buffer.write("Java Compilation Error:\n")
                    output_buffer.write(compile_result.stderr)
                else:
                    result = subprocess.run(['java', class_name], capture_output=True, text=True)
                    output_buffer.write(result.stdout if result.returncode == 0 else result.stderr)
            except Exception as e:
                output_buffer.write(f"Java Execution Exception:\n{str(e)}")
        
        
        
        elif language == "c":
            match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = match.group(1) if match else 'TempCode'
            filename = f"{class_name}.c"
            if not filename:
                filename = "main.c"
            exe_name = filename.replace(".c", ".exe")
            with open(filename, 'w') as f:
                f.write(code)
            compile_result = subprocess.run(["gcc", filename, "-o", exe_name], capture_output=True, text=True)
            if compile_result.returncode != 0:
                output_buffer.write("C Compilation Error:\n" + compile_result.stderr)
            else:
                result = subprocess.run([exe_name], capture_output=True, text=True)
                output_buffer.write(result.stdout if result.returncode == 0 else result.stderr)
        elif language == "cpp":
            match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = match.group(1) if match else 'TempCode'
            filename = f"{class_name}.cpp"
            if not filename:
                filename = "main.cpp"
            exe_name = filename.replace(".cpp", ".exe")
            with open(filename, 'w') as f:
                f.write(code)
            compile_result = subprocess.run(["g++", filename, "-o", exe_name], capture_output=True, text=True)
            if compile_result.returncode != 0:
                output_buffer.write("C++ Compilation Error:\n" + compile_result.stderr)
            else:
                result = subprocess.run([exe_name], capture_output=True, text=True)
                output_buffer.write(result.stdout if result.returncode == 0 else result.stderr)
        
        
        
        else:
            output_buffer.write("Language not supported!")
        
        return output_buffer.getvalue()
    
    except Exception as e:
        return traceback.format_exc()


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