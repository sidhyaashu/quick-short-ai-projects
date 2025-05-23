import streamlit as st
import requests
import json
import pandas as pd
import os
from io import BytesIO
import fitz  # PyMuPDF for PDF parsing
import docx  # python-docx for DOCX parsing

# Set page config
st.set_page_config(
    page_title="Assignment Grader",
    page_icon="📚",
    layout="wide"
)

# Constants
API_BASE_URL = "http://localhost:8000"

# Function to extract text from files
def extract_text_from_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        # Extract text from PDF
        bytes_data = uploaded_file.getvalue()
        with fitz.open(stream=bytes_data, filetype="pdf") as doc:
            text = "\n".join(page.get_text() for page in doc)
        return text
    elif file_extension in ['docx', 'doc']:
        # Extract text from DOCX
        bytes_data = BytesIO(uploaded_file.getvalue())
        doc = docx.Document(bytes_data)
        text = "\n".join(para.text for para in doc.paragraphs)
        return text
    elif file_extension in ['txt']:
        # Extract text from plain text
        return uploaded_file.getvalue().decode('utf-8')
    else:
        st.error(f"Unsupported file format: {file_extension}")
        return None

# Create sidebar for API keys
st.sidebar.title("API Settings")
gemini_api_key = st.sidebar.text_input("Gemini API Key", value="", type="password")
google_api_key = st.sidebar.text_input("Google API Key", value="", type="password")
search_engine_id = st.sidebar.text_input("Search Engine ID", value="")

# Main title
st.title("📚 Assignment Grader")
st.markdown("Grade assignments, check for plagiarism, and generate feedback using AI.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Grade Assignment", "Check Plagiarism", "Generate Feedback"])

# Tab 1: Grade Assignment
with tab1:
    st.header("Grade Assignment")
    
    # Input method selection
    input_method = st.radio("Select input method:", ["Upload File", "Text Input"])
    
    assignment_text = ""
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload assignment file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        if uploaded_file:
            assignment_text = extract_text_from_file(uploaded_file)
            if assignment_text:
                st.success(f"Successfully extracted text from {uploaded_file.name}")
                with st.expander("Preview Extracted Text"):
                    st.text_area("Assignment Text", assignment_text, height=200)
    else:
        assignment_text = st.text_area("Enter assignment text:", height=200)
    
    # Rubric input
    rubric = st.text_area("Enter grading rubric:", height=150, 
                         placeholder="Example: A: Excellent analysis and well-structured. B: Good analysis but some flaws. C: Basic understanding shown...")
    
    # Model selection
    model = st.selectbox(
        "Select AI model:",
        ["gemini-1.5-flash-8b", "gemini-2.0-flash"],
        index=0
    )
    
    # Grade button
    if st.button("Grade Assignment", key="grade_btn"):
        if not assignment_text or not rubric:
            st.error("Please provide both assignment text and rubric.")
        else:
            with st.spinner("Grading assignment..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/tools/grade_assignment",
                        json={
                            "text": assignment_text,
                            "rubric": rubric,
                            "model": model,
                            "gemini_api_key": gemini_api_key
                        },
                        timeout=60
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Assignment Grade: {result['grade']}")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")

# Tab 2: Check Plagiarism
with tab2:
    st.header("Check Plagiarism")
    
    # Input method selection for plagiarism
    plag_input_method = st.radio("Select input method:", ["Upload File", "Text Input"], key="plag_input")
    
    plag_text = ""
    if plag_input_method == "Upload File":
        plag_uploaded_file = st.file_uploader("Upload file to check (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="plag_file")
        if plag_uploaded_file:
            plag_text = extract_text_from_file(plag_uploaded_file)
            if plag_text:
                st.success(f"Successfully extracted text from {plag_uploaded_file.name}")
                with st.expander("Preview Extracted Text"):
                    st.text_area("Text to Check", plag_text, height=200, key="plag_preview")
    else:
        plag_text = st.text_area("Enter text to check for plagiarism:", height=200, key="plag_text_input")
    
    # Similarity threshold
    similarity_threshold = st.slider("Similarity Threshold (%)", min_value=0, max_value=100, value=40)
    
    # Check button
    if st.button("Check Plagiarism", key="plag_btn"):
        if not plag_text:
            st.error("Please provide text to check for plagiarism.")
        else:
            with st.spinner("Checking for plagiarism..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/tools/check_plagiarism",
                        json={
                            "text": plag_text,
                            "similarity_threshold": similarity_threshold,
                            "google_api_key": google_api_key,
                            "search_engine_id": search_engine_id
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        result = response.json()
                        if result["results"]:
                            st.warning(f"Found {len(result['results'])} potential plagiarism matches.")
                            
                            # Convert to DataFrame for better display
                            df = pd.DataFrame(result["results"])
                            
                            # Color coding based on similarity
                            def color_similarity(val):
                                if val >= 80:
                                    return 'background-color: #ffcccc'  # Red for high similarity
                                elif val >= 60:
                                    return 'background-color: #ffffcc'  # Yellow for medium similarity
                                return ''
                            
                            # Apply styling
                            styled_df = df.style.applymap(color_similarity, subset=['similarity'])
                            
                            # Display as interactive table
                            st.dataframe(styled_df)
                        else:
                            st.success("No plagiarism detected above the set threshold.")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")

# Tab 3: Generate Feedback
with tab3:
    st.header("Generate Feedback")
    
    # Input method selection
    feedback_input_method = st.radio("Select input method:", ["Upload File", "Text Input"], key="feedback_input")
    
    feedback_text = ""
    if feedback_input_method == "Upload File":
        feedback_uploaded_file = st.file_uploader("Upload assignment file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="feedback_file")
        if feedback_uploaded_file:
            feedback_text = extract_text_from_file(feedback_uploaded_file)
            if feedback_text:
                st.success(f"Successfully extracted text from {feedback_uploaded_file.name}")
                with st.expander("Preview Extracted Text"):
                    st.text_area("Assignment Text", feedback_text, height=200, key="feedback_preview")
    else:
        feedback_text = st.text_area("Enter assignment text:", height=200, key="feedback_text_input")
    
    # Rubric input
    feedback_rubric = st.text_area("Enter grading rubric:", height=150, key="feedback_rubric",
                                  placeholder="Example: Clear thesis statement (20%), Evidence and analysis (30%), Structure (20%), Grammar (15%), Citations (15%)")
    
    # Model selection
    feedback_model = st.selectbox(
        "Select AI model:",
        ["gemini-1.5-flash-8b", "gemini-2.0-flash"],
        index=0,
        key="feedback_model"
    )
    
    # Generate feedback button
    if st.button("Generate Feedback", key="feedback_btn"):
        if not feedback_text or not feedback_rubric:
            st.error("Please provide both assignment text and rubric.")
        else:
            with st.spinner("Generating feedback..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/tools/generate_feedback",
                        json={
                            "text": feedback_text,
                            "rubric": feedback_rubric,
                            "model": feedback_model,
                            "gemini_api_key": gemini_api_key
                        },
                        timeout=60
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("Feedback")
                        st.markdown(result["feedback"])
                        
                        # Option to download feedback
                        feedback_text = result["feedback"]
                        st.download_button(
                            label="Download Feedback",
                            data=feedback_text,
                            file_name="assignment_feedback.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Assignment Grader Tool - Powered by AI")

# Check API connection
try:
    response = requests.get(f"{API_BASE_URL}/")
    if response.status_code == 200:
        st.sidebar.success("✅ API connected successfully")
    else:
        st.sidebar.error("❌ API connection error")
except:
    st.sidebar.error("❌ Could not connect to API server")
    st.sidebar.info("Make sure the FastAPI server is running at " + API_BASE_URL)
