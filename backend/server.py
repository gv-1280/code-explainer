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
# Ensure the required packages are installed
# Create a FastAPI app instance
app = FastAPI()
class ExplainRequest(BaseModel):
    code: str
    
# Optional audience level for the explanation
class ConvertRequest(BaseModel):
    code: str
    source_language: str
    target_language: str
    audience_level: Optional[str] = None

# Endpoint to explain code
@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        explanation = explain_code(request.code, request.audience_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Endpoint to convert code from one language to another
@app.post("/convert")
async def convert(request: ConvertRequest):
    try:
        converted_code = convert_code(request.code, request.source_language, request.target_language)
        return {"converted_code": converted_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
# Ensure the environment variables are set for API keys
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is not set")
if not os.getenv("CONVERT_API_KEY"):
    raise ValueError("CONVERT_API_KEY environment variable is not set")
# Run the FastAPI app using uvicorn
# Use the command: uvicorn FastAPI:app --reload