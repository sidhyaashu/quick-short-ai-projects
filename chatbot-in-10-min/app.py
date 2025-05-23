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

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=GOOGLE_API_KEY)

# Function to process documents
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
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return vector_store

# Process your documents
document_paths = [os.path.join("documents", f) for f in os.listdir("documents")]
vector_store = process_documents(document_paths)

# Set up conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the conversation chain
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    memory=memory
)

# Function to generate response
def generate_response(message, history):
    response = conversation_chain({"question": message})
    return response["answer"]

# Create Gradio interface
demo = gr.ChatInterface(
    fn=generate_response,
    title="Your AI Knowledge Assistant",
    description="Ask me anything about your documents!",
    theme="soft"
)

# Launch the app
if __name__ == "__main__":
    demo.launch()