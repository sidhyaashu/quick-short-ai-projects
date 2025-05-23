import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class LLMModel:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
        
        self.model_name = model_name
        self.openai_model = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key  # ✅ Explicitly pass API key
        )
        
    def get_model(self):
        return self.openai_model

if __name__ == "__main__":
    llm_instance = LLMModel()
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("hi")

    print(response.content)  # ✅ .content gives clean output
