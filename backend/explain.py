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
# Ensure the required packages are installed
# Create a FastAPI app instance
app = FastAPI()
class ExplainRequest(BaseModel):
    code: str
    # Optional audience level for the explanation
    audience_level: Optional[str] = None
# Endpoint to explain code
@app.post("/explain")
async def explain_code(request: ExplainRequest):
    try:
        explanation = explain_code(request.code, request.audience_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
# Ensure the environment variables are set for API keys
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is not set")
if not os.getenv("EXPLAIN_API_KEY"):
    raise ValueError("EXPLAIN_API_KEY environment variable is not set")
# Run the FastAPI app using uvicorn
# Use the command: uvicorn FastAPI:app --reload