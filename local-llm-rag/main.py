from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from vector import retriever

# Load your LLM
model = OllamaLLM(model="llama3.2")

# Improved and grammatically correct template
template = """
You are a helpful AI assistant. Use the following context to answer the user's question.
If you don't know the answer, clearly say: "Sorry, I can't understand."

Context:
{answer}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# Chain combines prompt and model
chain = prompt | model

# CLI loop
while True:
    print("\n\n----------------------------------------------")
    question = input("Ask your question (q for quit) \nQuestion: ")
    if question.lower() == "q":
        break

    # Get context from retriever
    context = retriever.invoke(question)
    result = chain.invoke({"question": question, "answer": context})
    print(result)
