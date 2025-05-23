from fastapi import FastAPI, HTTPException, Depends, Request
import uvicorn
import openai
import os
import sys
from pydantic import BaseModel
from typing import List, Optional
import requests
from functools import lru_cache
import logging
from google import genai

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Config class
class Settings:
    def __init__(self):
        self.gemini_api_key = ""
        self.google_api_key = ""
        self.search_engine_id = ""

# Log config
settings = Settings()
logger.info(f"OpenAI API Key set: {'Yes' if settings.gemini_api_key else 'No'}")
logger.info(f"Google Search Engine ID set: {'Yes' if settings.search_engine_id else 'No'}")
logger.info(f"Google API Key set: {'Yes' if settings.google_api_key else 'No'}")
logger.info(f"Python version: {sys.version}")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

# Pydantic Models
class BaseRequest(BaseModel):
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    search_engine_id: Optional[str] = None

class ParseFileRequest(BaseRequest):
    file_path: str

class PlagiarismRequest(BaseRequest):
    text: str
    similarity_threshold: Optional[int] = 40

class GradeRequest(BaseRequest):
    text: str
    rubric: str
    model: Optional[str] = "gemini-1.5-flash-8b"

class GradeResponse(BaseModel):
    grade: str

class PlagirismResult(BaseModel):
    url: str
    similarity: int

class PlagiarismResponse(BaseModel):
    results: List[PlagirismResult]

# FastAPI init
app = FastAPI(
    title="Assignment Grader API",
    description="Grade and check assignments using AI",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Assignment Grader API", "status": "running", "version": "1.0.0"}

# API key extraction
def get_api_keys(request, settings):
    return {
        "gemini_api_key": getattr(request, "gemini_api_key", None) or settings.gemini_api_key,
        "google_api_key": getattr(request, "google_api_key", None) or settings.google_api_key,
        "search_id": getattr(request, "search_engine_id", None) or settings.search_engine_id
    }

async def parse_pdf(file_path: str) -> str:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)
    except ImportError:
        raise HTTPException(status_code=500, detail="Missing dependency: install PyMuPDF (`pip install pymupdf`)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing error: {str(e)}")

async def parse_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except ImportError:
        raise HTTPException(status_code=500, detail="Missing dependency: install python-docx (`pip install python-docx`)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX parsing error: {str(e)}")

@app.post("/tools/check_plagiarism", response_model=PlagiarismResponse)
async def check_plagiarism(request: PlagiarismRequest, settings: Settings = Depends(get_settings)):
    try:
        from fuzzywuzzy import fuzz
        keys = get_api_keys(request, settings)
        if not keys["google_api_key"] or not keys["search_id"]:
            raise HTTPException(status_code=400, detail="Google API key and Search Engine ID are required.")
        text = request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty.")
        query = text[:300]
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {"key": keys["google_api_key"], "cx": keys["search_id"], "q": query}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Google API error: {response.text}")
        data = response.json()
        results = data.get("items", [])
        plagiarism_results = [
            PlagirismResult(url=item["link"], similarity=fuzz.token_set_ratio(text, item.get("snippet", "")))
            for item in results
        ]
        plagiarism_results.sort(key=lambda x: x.similarity, reverse=True)
        threshold = request.similarity_threshold or 0
        return PlagiarismResponse(results=[r for r in plagiarism_results if r.similarity >= threshold])
    except ImportError:
        raise HTTPException(status_code=500, detail="Install fuzzywuzzy with `pip install fuzzywuzzy`")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Gemini completion
async def call_gemini_api(prompt: str, model: str, api_key: str) -> str:

    try:

        if not prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
        
        if not model:
            raise HTTPException(status_code=400, detail="Model cannot be empty.")
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
    
        return response.text.strip()
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

@app.post("/tools/grade_assignment", response_model=GradeResponse)
async def grade_assignment(request: GradeRequest, settings: Settings = Depends(get_settings)):
    if not request.text.strip() or not request.rubric.strip():
        raise HTTPException(status_code=400, detail="Text and rubric cannot be empty.")
    
    keys = get_api_keys(request, settings)
    if not keys["gemini_api_key"]:
        raise HTTPException(status_code=400, detail="Gemini API key not configured.")
    
    prompt = f"""You are an expert educator. Grade the following assignment based on the provided rubric. Return only the grade (e.g., A, B+, C-).

Rubric:
{request.rubric}

Assignment:
{request.text}

Grade:"""
    
    grade = await call_gemini_api(prompt, request.model, keys["gemini_api_key"])
    return GradeResponse(grade=grade)

@app.post("/tools/generate_feedback")
async def generate_feedback(request: GradeRequest, settings: Settings = Depends(get_settings)):
    if not request.text.strip() or not request.rubric.strip():
        raise HTTPException(status_code=400, detail="Text and rubric cannot be empty.")
    keys = get_api_keys(request, settings)
    if not keys["gemini_api_key"]:
        raise HTTPException(status_code=400, detail="Gemini API key not configured.")
    prompt = f"""Provide constructive feedback for the assignment below based on the rubric:

Assignment:
{request.text}

Rubric:
{request.rubric}

Feedback:"""
    feedback = await call_gemini_api(prompt, request.model, keys["gemini_api_key"])
    return {"feedback": feedback}

if __name__ == "__main__":
    logger.info("Assignment Grader API running at http://localhost:8088")
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
