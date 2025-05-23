# 📚 AI Assignment Grader

An AI-powered application that automates assignment grading, detects plagiarism, and provides structured feedback to students. It combines the strengths of Google Gemini AI, Google Custom Search, and a user-friendly Streamlit interface for educators and evaluators.

---

## ✨ Features

- **📄 Document Processing**  
  Upload and process PDF or DOCX assignment files.

- **🔍 Plagiarism Detection**  
  Leverages Google Custom Search API to find content similarities on the web.

- **🧠 AI Grading System**  
  Utilizes Google Gemini AI (or optionally OpenAI) to evaluate assignments based on customizable rubrics.

- **📝 Constructive Feedback**  
  Generates detailed, section-specific feedback to aid student improvement.

- **🌐 User Interface**  
  Streamlit-based interface that’s intuitive and accessible via the browser.

- **⚙️ Modular System**  
  Clean separation between frontend (Streamlit) and backend (FastAPI) services for better scalability and maintenance.

---

## 🧱 Architecture Overview

```
+----------------------+     +----------------------+
|     Frontend UI      | <-> |      Backend API     |
|  (Streamlit - app.py)|     |  (FastAPI - server.py)|
+----------------------+     +----------------------+
            |                         |
            |                         |
        File Upload          AI Evaluation + Plagiarism Check
            |                         |
            +---------+   +----------+
                      |   |
        +-------------v---v-------------+
        |   Google APIs (Gemini, Search)|
        +-------------------------------+
```

---

## 🛠️ Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- `uv` package manager (lightweight, fast Python environment tool)
- API Keys:
  - Google API Key
  - Google Custom Search Engine ID
  - Google Gemini API Key
  - (Optional) OpenAI API Key

---

### 📦 Installation

#### 1. Clone the repository:

```bash
git clone https://github.com/sidhyaashu/ai-assignment-grader.git
cd ai-assignment-grader
```

#### 2. Set up environment with `uv`:

```bash
uv init assignment-grader
cd assignment-grader
uv venv
.venv\Scripts\activate      # On Windows
# OR
source .venv/bin/activate  # On macOS/Linux

uv add -r requirements.txt
```

#### 3. Configure environment variables:

Create a `.env` file in the project root with the following content:

```env
# API Server Configuration
API_SERVER_URL=http://localhost:8000

# Google Search API for plagiarism checking
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CX=your_google_custom_search_id_here

# Gemini API for grading and feedback
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI API as a fallback (optional)
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ▶️ Running the Application

### 1. Start the backend server

```bash
python server.py
```

### 2. Start the frontend (Streamlit client)

```bash
streamlit run app.py
```

### 3. Access the App

Open your browser and navigate to:  
👉 `http://localhost:8501`

---

## 🧭 Usage Guide

1. **Upload File Tab**  
   Upload your assignment file (PDF or DOCX) and process it.

2. **Grade Assignments Tab**  
   Define your grading rubric, enable optional plagiarism check, and submit for grading.

3. **Results Tab**  
   View AI-generated grade, feedback, and a plagiarism similarity score/report.

---

## 🛠️ Customization Options

- **Rubric Adjustments**  
  Modify the grading criteria directly through the interface before submitting assignments.

- **API Configuration**  
  Change API keys and model preferences in the sidebar settings or update the `.env` file.

- **Model Switching**  
  Default: Google Gemini 1.5 Pro  
  Optional: OpenAI GPT (fallback if Gemini fails or not preferred)

---

## ❗ Troubleshooting

| Issue                       | Solution                                                                 |
|----------------------------|--------------------------------------------------------------------------|
| File not uploading         | Ensure it's a valid PDF or DOCX and not password-protected               |
| API errors                 | Check API keys and network connectivity                                  |
| Backend not responding     | Ensure `server.py` is running on `http://localhost:8000`                 |
| Gemini/OpenAI issues       | Ensure respective API keys are correct and your quota is not exhausted   |

---

## 📂 Folder Structure

```
assignment-grader/
├── .env                    # API credentials
├── .gitignore              # Git ignored files
├── .python-version         # Python version for environment
├── app.py                  # Streamlit frontend application
├── server.py               # FastAPI backend server
├── requirements.txt        # Project dependencies
├── pyproject.toml          # Python project config
├── uv.lock                 # uv dependency lock file
└── README.md               # Project documentation
```

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

---

## 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.
