#write a python function called explain_code(code: str,audience_level: Optional[str] = None) -> str
#this function should:
# 1. use the OpenRouter API to send the code for explanation
# 2. include audiance level in the request if provided E.g "beginner", "intermediate", "expert"
# 3. return only the explaination text (no extra formatting or metadata)
# 4. load the API key from an environment variable called API_KEY
# 5. handle http errors gracefully and return a user-friendly message
import os
import requests
from typing import Optional
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def explain_code(code: str, audience_level: Optional[str] = "Beginner") -> str:
    """
    Explain the given code using OpenRouter API
    
    Args:
        code: The code to explain
        audience_level: Target audience level (beginner, intermediate, expert)
    
    Returns:
        str: Explanation of the code
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Use the correct OpenRouter API endpoint for chat completions
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # Required by OpenRouter
        "X-Title": "Code Explainer"  # Optional but recommended
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert programmer explaining code for a {audience_level} audience. Provide clear, concise explanations without extra formatting."
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
        response.raise_for_status()
        data = response.json()
        
        # Debug: Print the response for troubleshooting
        print(f"OpenRouter API Response: {data}")
        
        # Extract the explanation from the response
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"].strip()
            return content if content else "The AI returned an empty response."
        elif "error" in data:
            return f"API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            return f"Unexpected response format: {data}"
            
    except requests.exceptions.HTTPError as http_err:
        try:
            error_detail = response.json()
            return f"HTTP {response.status_code}: {error_detail.get('error', {}).get('message', str(http_err))}"
        except:
            return f"HTTP error {response.status_code}: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error: {req_err}"
    except Exception as err:
        return f"Unexpected error: {err}"