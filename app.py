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
# Define the API endpoints
API_EXPLAIN_URL = "http://localhost:8000/explain"
API_CONVERT_URL = "http://localhost:8000/convert"
# Function to explain code
def explain_code(code: str, audience_level: str):
    payload = {"code": code, "audience_level": audience_level}
    try:
        response = requests.post(API_EXPLAIN_URL, json=payload)
        response.raise_for_status()
        return response.json().get("explanation", "No explanation provided.")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
# Function to convert code
def convert_code(code: str, source_language: str, target_language: str):
    payload = {
        "code": code,
        "source_language": source_language,
        "target_language": target_language
    }
    try:
        response = requests.post(API_CONVERT_URL, json=payload)
        response.raise_for_status()
        return response.json().get("converted_code", "No converted code provided.")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
# Streamlit app layout for laptop and desktop 
# set the input and output fiels side by side E.g: code input on the left and output on the right 
st.set_page_config(layout="wide")
st.set_page_config(page_title="Code Explainer and Converter", layout="wide")
st.title("Code Explainer and Converter")
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Select an option", ["Code Explanation", "Code Conversion"])
if option == "Code Explanation":
    st.header("Code Explanation")
    code = st.text_area("Enter your code here:")
    audience_level = st.selectbox("Select Audience Level", ["beginner", "intermediate", "expert"])
    if st.button("Explain Code"):
        if code:
            explanation = explain_code(code, audience_level)
            st.success(explanation)
        else:
            st.error("Please enter some code to explain.")
elif option == "Code Conversion":
    st.header("Code Conversion")
    code = st.text_area("Enter your code here:")
    source_language = st.text_input("Source Language:")
    target_language = st.text_input("Target Language:")
    if st.button("Convert Code"):
        if code and source_language and target_language:
            converted_code = convert_code(code, source_language, target_language)
            st.success(converted_code)
        else:
            st.error("Please fill in all fields to convert the code.")
#change the icon color of UI elements to blue
# Run the Streamlit app using the command: streamlit run app.py
# Ensure the backend server is running before starting the Streamlit app
