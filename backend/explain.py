#write a python function called explain_code(code: str,audience_level: Optional[str] = None) -> str
#this function should:
# 1. use the OpenRouter API to send the code for explanation
# 2. include audiance level in the request if provided E.g "beginner", "intermediate", "expert"
# 3. return only the explaination text (no extra formatting or metadata)
# 4. load the API key from an environment variable called API_KEY
# 5. handle http errors gracefully and return a user-friendly message
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Optional
from explain import explain_code
import requests
# Ensure the required packages are installed
# Create a FastAPI app instance
app = FastAPI()
class ExplainRequest(BaseModel):
    code: str
    # Optional audience level for the explanation
    audiance_level: Optional[str] = None
# Endpoint to explain code
@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        explanation = explain_code(request.code, request.audiance_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# select a custom model and prompt for the explanation
# Health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
# Ensure the environment variables are set for API keys
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is not set")
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is not set")
# Run the FastAPI app using uvicorn
# Use the command: uvicorn FastAPI:app --reload
def explain_code(code: str, audiance_level : str = "Beginner") -> str:
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
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert programmer explaining code for a {audiance_level} audience."
            },
            {
                "role": "user",
                "content": f"Explain the following code:\n\n{code}"
            }
        ],
        "max_tokens": 500
        
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        response.raise_for_status()

    # Decide which key to return from
        if "choices" in data:
           return data["choices"][0]["message"]["content"]
        else:
           return data.get("explanation", "No explanation provided.")

    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")
        
# Ensure the required packages are installed
# Create a FastAPI app instance
