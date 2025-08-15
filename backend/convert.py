#write a python function called convert_code(code: str, source_language: str, target_language: str) -> str
#this function should:
# 1. use the OpenRouter API to send the given code and request it to be converted from source_language to target_language
# 2. return only the converted code (no extra text)
# 3. load the API key from an environment variable called API_KEY
# 4 . handle http errors gracefully and return a user-friendly message
import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

def convert_code(code: str, source_language: str, target_language: str) -> str:
    """
    Convert code from one language to another using OpenRouter API
    
    Args:
        code: The code to convert
        source_language: Source programming language
        target_language: Target programming language
    
    Returns:
        str: Converted code
    """
    api_key = os.getenv("API_KEY")  # Using same API_KEY 
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  
        "X-Title": "Code Converter"  
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert programmer. Convert code from {source_language} to {target_language}. Return only the converted code without explanations or formatting."
            },
            {
                "role": "user",
                "content": f"Convert this {source_language} code to {target_language}:\n\n{code}"
            }
        ],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract the converted code from the response
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return "Code conversion failed."
            
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except Exception as err:
        return f"An unexpected error occurred: {err}"