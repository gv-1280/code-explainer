#create a FastAPI app with two endpoints:
# 1. /explain - Takes code,language, and audiance level and returns an explanation of the code
# 2. /convert - Takes code, source language, and target language and returns the converted code
# use Pydantic models for input validation
#load api keys from environment variables
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  
import os
from typing import Optional
from .explain import explain_code
from .convert import convert_code
from dotenv import load_dotenv

load_dotenv()

# Create a FastAPI app instance
app = FastAPI(title="Code Explainer and Converter", version="1.0.0")

class ExplainRequest(BaseModel):
    code: str
    audience_level: Optional[str] = "beginner"  # Default to beginner if not provided

class ConvertRequest(BaseModel):
    code: str
    source_language: str
    target_language: str

# Endpoint to explain code
@app.post("/explain")
async def explain(request: ExplainRequest):
    """Explain the provided code for the specified audience level"""
    try:
        explanation = explain_code(request.code, request.audience_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to convert code from one language to another
@app.post("/convert")
async def convert(request: ConvertRequest):
    """Convert code from source language to target language"""
    try:
        converted_code = convert_code(request.code, request.source_language, request.target_language)
        return {"converted_code": converted_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/healthz")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Ensure the environment variables are set for API keys
api_key = os.getenv("API_KEY")
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is not set")