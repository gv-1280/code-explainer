#create a streamlit app simple UI to interact with the server backend
# the app should have two sections:
# 1. Code Explanation: Takes code and audience level and returns an explanation of the code
# 2. Code Conversion: Takes code, source language, and target language and returns the converted code
# use streamlit for the UI
# ensure the app can handle errors gracefully and display user-friendly messages
# ensure the app is responsive and user-friendly
# ensure the app is well-structured and easy to navigate

import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000" # Updated to match the new backend URL
def check_backend_health():
    """Check if the backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/healthz", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def explain_code(code, audience_level):
    """Call the explain endpoint"""
    try:
        payload = {
            "code": code,
            "audience_level": audience_level
        }
        
        response = requests.post(
            f"{BACKEND_URL}/explain",
            json=payload,
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            explanation = result.get("explanation", "No explanation received")
            return explanation
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000."
    except requests.exceptions.Timeout:
        return "❌ Request timed out. The API is taking too long to respond."
    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {str(e)}"

def convert_code(code, source_lang, target_lang):
    """Call the convert endpoint"""
    try:
        payload = {
            "code": code,
            "source_language": source_lang,
            "target_language": target_lang
        }
        
        response = requests.post(
            f"{BACKEND_URL}/convert",
            json=payload,
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("converted_code", "No code received")
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000."
    except requests.exceptions.Timeout:
        return "❌ Request timed out. The API is taking too long to respond."
    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {str(e)}"

def main():
    st.set_page_config(
        page_title="AI Code Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title
    st.title("🤖 AI Code Assistant")
    st.markdown("*Explain and convert your code with the power of AI*")
    
    # Check backend health silently
    backend_status = check_backend_health()
    if not backend_status:
        st.error("⚠️ Backend server is not running. Please start it with: `uvicorn backend.server:app --reload`")
        st.stop()
    
    # Navigation in sidebar
    st.sidebar.title("🚀 Navigation")
    
    # Initialize session state for navigation
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = 'Code Explanation'
    
    # Radio button for navigation
    option = st.sidebar.radio(
        "Choose a feature:",
        ["Code Explanation", "Code Conversion"],
        index=0 if st.session_state.selected_option == 'Code Explanation' else 1
    )
    st.session_state.selected_option = option
    
    # Add separator
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tip:** Enter your code and select your preferred settings!")
    
    # Main content based on selection
    if st.session_state.selected_option == 'Code Explanation':
        st.header("📝 Code Explanation")
        st.markdown("Enter your code below and get a detailed explanation tailored to your experience level.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Code input
            code_input = st.text_area(
                "Your Code:",
                height=300,
                placeholder="def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Example: Recursive fibonacci function",
                help="Paste or type your code here"
            )
        
        with col2:
            st.markdown("#### Settings")
            # Audience level selection
            audience_level = st.selectbox(
                "Audience Level:",
                ["beginner", "intermediate", "expert"],
                index=0,
                help="Choose your programming experience level"
            )
            
            # Language hint (optional)
            language_hint = st.selectbox(
                "Language (Optional):",
                ["Auto-detect", "Python", "JavaScript", "Java", "C++", "C", "Go", "Rust"],
                index=0
            )
        
        # Explain button
        if st.button("🚀 Explain Code", type="primary", use_container_width=True):
            if code_input.strip():
                with st.spinner("🧠 Analyzing your code..."):
                    explanation = explain_code(code_input, audience_level)
                
                st.markdown("---")
                st.subheader("📖 Explanation")
                
                # Display explanation
                st.write(explanation)
                    
            else:
                st.warning("📝 Please enter some code to explain!")
    
    elif st.session_state.selected_option == 'Code Conversion':
        st.header("🔄 Code Conversion")
        st.markdown("Convert your code from one programming language to another.")
        
        # Code input
        code_input = st.text_area(
            "Code to Convert:",
            height=250,
            placeholder="function greet(name) {\n    console.log('Hello, ' + name + '!');\n}\n\n// Example: JavaScript function",
            help="Enter the code you want to convert"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "From Language:",
                ["python", "javascript", "java", "c++", "c", "go", "rust", "php", "ruby", "typescript"],
                index=1,
                help="Select the source programming language"
            )
        
        with col2:
            target_lang = st.selectbox(
                "To Language:",
                ["python", "javascript", "java", "c++", "c", "go", "rust", "php", "ruby", "typescript"],
                index=0,
                help="Select the target programming language"
            )
        
        # Convert button
        if st.button("🔄 Convert Code", type="primary", use_container_width=True):
            if code_input.strip():
                if source_lang == target_lang:
                    st.warning("⚠️ Source and target languages cannot be the same!")
                else:
                    with st.spinner(f"🔄 Converting from {source_lang.title()} to {target_lang.title()}..."):
                        converted_code = convert_code(code_input, source_lang, target_lang)
                    
                    st.markdown("---")
                    st.subheader("🎉 Converted Code")
                    
                    # Display converted code
                    st.code(converted_code, language=target_lang.lower())
                    
                    # Copy button hint
                    st.info("💡 Tip: You can copy the code by clicking on it and using Ctrl+A, Ctrl+C")
            else:
                st.warning("📝 Please enter some code to convert!")

if __name__ == "__main__":
    main()