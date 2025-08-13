#write a python function called convert_code(code: str, source_language: str, target_language: str) -> str
#this function should:
# 1. use the OpenRouter API to send the given code and request it to be converted from source_language to target_language
# 2. return only the converted code (no extra text)
# 3. load the API key from an environment variable called API_KEY
# 4 . handle http errors gracefully and return a user-friendly message
from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel
import os
from typing import Optional
import requests
def convert_code(code: str, source_language: str, target_language: str) -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    url = "https://api.openrouter.ai/v1/convert"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "model": "deepseek/deepseek-r1:free",  
        "source_language": source_language,
        "target_language": target_language
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("converted_code", "")
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")
        return response.json().get("converted_code", "")
# Ensure the required packages are installed
# Create a FastAPI app instance
app = FastAPI()
class ConvertRequest(BaseModel):
    code: str
    source_language: str
    target_language: str
    audience_level: Optional[str] = None
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
if not os.getenv("CONVERT_API_KEY"):
    raise ValueError("API_KEY environment variable is not set")
# Run the FastAPI app using uvicorn
# Use the command: uvicorn FastAPI:app --reload