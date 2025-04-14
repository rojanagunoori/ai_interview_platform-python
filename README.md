# 🎤 AI Voice Interview Platform

An AI-powered voice-based interview simulator that personalizes questions based on the user's uploaded resume and chosen job role. It features voice interaction using Text-to-Speech (TTS) and Speech Recognition (STT), simulating real-life interview experiences.

> 📌 **Live App**: [https://ai-interview-platform-python.onrender.com/](https://ai-interview-platform-python.onrender.com/)  
> 📁 **GitHub Repo**: [https://github.com/rojanagunoori/ai_interview_platform-python](https://github.com/rojanagunoori/ai_interview_platform-python)

---

## 🚀 Features

### 1. 📄 Resume Upload
- Upload a resume (PDF).
- Parsed using `PyPDF2`, and used to personalize interview questions.

### 2. 💼 Job Role Selection
- Choose a role: Frontend, Backend, Full Stack, etc.
- Questions are dynamically generated based on this.

### 3. 🧠 AI-Powered Interview Questions
- Questions are created using Gemini API logic (planned).
- Resume and role based question logic already implemented.

### 4. 🎙️ Voice Interview Interface
- **Text-to-Speech (TTS)**: Interview questions are spoken to the user.
- **Speech-to-Text (STT)**: Users can respond using their voice (planned).

### 5. 💻 Coding Simulation (Planned)
- Future support for coding exercises (like HackerRank/LeetCode).
- Currently simulated using code input section.

### 6. 🔁 Real-Time UX Enhancements
- Loading spinners while generating questions.
- Clean user interface with Streamlit components.

---

## 🛠️ Tech Stack & Tools, Libraries & Frameworks

| Category              | Technologies / Libraries / Tools             |
|-----------------------|----------------------------------------------|
| Programming           | Python                                       |
| Web Framework         | Streamlit                                    |
| Resume Parsing        | `PyPDF2`, `tempfile`                         |
| Data Handling          | NumPy, Pandas      |
| Text-to-Speech (TTS)  | `pyttsx3` or `gTTS`                          |
| Speech Recognition    | `speech_recognition`, Google Speech API      |
| AI/ML (Planned)       | Gemini API                                   |
| Unique IDs & Temp     | `uuid`, `tempfile`                           |
| UX Enhancements       | Streamlit HTML, Spinners                     |
| Version Control       | Git, GitHub                                  |
| IDE                   | Visual Studio Code, Git, GitHub  Code                           |
| Deployment            | Render.com                                   |
| Voice Skills          | Text-to-Speech (TTS), Speech-to-Text (STT)   |
| UX/UI                  | HTML tags, Streamlit spinners                          |
| Coding Platform       | (Planned) Code editor + test runner          |

---

## 💻 How to Run Locally

### 📦 Prerequisites

- Python 3.8+
- pip

### 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/rojanagunoori/ai_interview_platform-python.git
cd ai_interview_platform-python

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt
▶️ Run the App

streamlit run main.py
Then open your browser and go to: http://localhost:8501

🔗 Links
🌐 Live App: https://ai-interview-platform-python.onrender.com/

📁 GitHub Repository: https://github.com/rojanagunoori/ai_interview_platform-python


🧠 Challenges Faced
✨ Parsing resumes with inconsistent formatting using PyPDF2, pandas, numpy.

✨ Handling silent or noisy input from microphones in speech_recognition.

✨ Managing performance and rendering delays in deployed environments like Render.

✨ Designing dynamic voice flow for realistic AI interaction.

🧠 Future Enhancements
✨ Real-time answer evaluation using AI

🧪 Coding environment with auto-grading

📊 Analytics dashboard

🎯 Support for more roles and languages

 🧪 Gemini-powered contextual AI evaluation.

🧪 Fully functional live coding IDE in the browser.

🧪 Automated feedback based on user answers.

🧪 Candidate performance scoring and downloadable reports.

🙋‍♀️ Author
Nagunoori Roja
📧 nagunooriroja@gmail.com
🌐 GitHub: rojanagunoori

📜 License
This project is open-source and available under the MIT License.

yaml
Copy
Edit

---

Let me know if you'd like me to:
- Create a logo/banner for this
- Generate a video walkthrough script
- Prepare a Medium/Dev.to blog post format

Ready to help you shine online! 💫