from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Read the CSV file
df = pd.read_csv("./x.csv")
print(df.head(1))

# Initialize embeddings
embedding = OllamaEmbeddings(model="mxbai-embed-large")

# Define database location
db_loc = "./chroma_db"
add_doc = not os.path.exists(db_loc)

# List to store documents
if add_doc:
    documents = []
    for i, row in df.iterrows():
        # Ensure each document has valid page content and metadata
        doc = Document(
            page_content=row["Question"] + " " + row["Answer"],
            metadata={"rating": i}  # Metadata as a dictionary
        )
        documents.append(doc)  # Add document to the list

# Initialize Chroma vector store
vector_store = Chroma(
    collection_name="qna",
    persist_directory=db_loc,
    embedding_function=embedding
)

# Add documents to the vector store, if applicable
if add_doc:
    vector_store.add_documents(documents=documents)

# Initialize retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # Retrieve top 5 results
)
