# Building AI Chatbot in 10 Minutes Using LangChain and Gemini

Chatbots have become essential tools for businesses and developers. With AI advancements, creating a chatbot is now easy with basic programming knowledge. This guide will help you build your own AI chatbot using LangChain and Google's Gemini model.

## Types of Chatbots You Can Build

Before implementing, consider the type of chatbot you want to create:
- **Knowledge-Base Chatbot**: Answers questions based on specific documents
- **Customer Service Chatbot**: Handles customer inquiries and support
- **Personal Assistant Chatbot**: Helps with scheduling and reminders
- **E-commerce Chatbot**: Guides users through products and purchases
- **Content Creation Chatbot**: Assists with generating written content

This tutorial focuses on a **knowledge-base chatbot** that answers questions about specific documents, but you can adapt it for other chatbot types.

---

## Prerequisites
To follow along, you'll need:
- **Python 3.8+ installed**
- **Basic Python knowledge**
- **Google API key for Gemini** (Free tier available)
- **A text editor or IDE**
- **Your own documents (PDF, TXT, etc.)**

---

## Step 1: Set Up Your Environment

### 1. Create a Virtual Environment
```sh
python -m venv chatbot-env
source chatbot-env/bin/activate  # On Windows: chatbot-env\Scripts\activate
```

### 2. Install Required Packages
```sh
pip install langchain langchain-google-genai pypdf python-dotenv gradio
```

---

## Step 2: Obtain Your Google API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in or create an account
3. Navigate to **"API keys"** and create a new key
4. Copy your API key for later use

---

## Step 3: Create the Chatbot Script

### 1. Import Required Libraries
```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import gradio as gr
```

### 2. Load Environment Variables
```python
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

### 3. Initialize the Gemini Model
```python
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY)
```

### 4. Process Documents (PDF & TXT)
```python
def process_documents(file_paths):
    documents = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            continue
        documents.extend(loader.load())
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store
```

### 5. Load Documents
```python
document_paths = [os.path.join("documents", f) for f in os.listdir("documents")]
vector_store = process_documents(document_paths)
```

### 6. Set Up Conversation Memory
```python
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
```

### 7. Create the Conversation Chain
```python
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    memory=memory
)
```

### 8. Define the Response Function
```python
def generate_response(message, history):
    response = conversation_chain({"question": message})
    return response["answer"]
```

### 9. Build Gradio Chat Interface
```python
demo = gr.ChatInterface(
    fn=generate_response,
    title="Your AI Knowledge Assistant",
    description="Ask me anything about your documents!",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
```

---

## Step 4: Run Your Chatbot
```sh
python chatbot.py
```

---

## Step 5: Deploy Your Chatbot
You can deploy your chatbot using services like **Hugging Face Spaces**, **Streamlit**, or **Flask** for web hosting.

---

## Conclusion
By following these steps, you've successfully built a chatbot that can answer questions based on uploaded documents. You can customize and expand its capabilities for various use cases!

