

### 🧠 Clone the Repository
Start by cloning the project to your local machine:
```bash
git clone https://github.com/sidhyaashu/docktor-appoinment-multiagent.git
cd docktor-appoinment-multiagent
```

---

### 🐍 Set Up Python Environment (Using Conda)
Create a new isolated environment with Python 3.10:
```bash
conda create -p venv python=3.10 -y
```

Activate the environment:
```bash
conda activate ./venv
```

(If needed later, deactivate it with: `conda deactivate`)

---

### 📦 Install Dependencies
Install all required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 🚀 Run the Application

#### 🔹 To launch the **Streamlit Frontend**:
```bash
streamlit run streamlit.py
```

#### 🔹 To start the **FastAPI Backend**:
```bash
uvicorn main:app --reload --port 8003
```

Make sure both servers are running in separate terminals or use something like tmux or VS Code split terminal.

---
