from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    try:
        # Try gemini-2.0-flash first
        model = genai.GenerativeModel('gemini-2.0-flash')
        resume_text = pdf_content[0]["data"] if isinstance(pdf_content[0], dict) else pdf_content[0]
        response = model.generate_content(f"{input}\n\nResume:\n{resume_text}\n\nInstructions: {prompt}")
        return response.text
    except Exception as e:
        st.error(f"Model error: {str(e)}")
        st.info("Trying alternative model...")
        try:
            # Try gemini-pro as fallback
            model = genai.GenerativeModel('gemini-pro')
            resume_text = pdf_content[0]["data"] if isinstance(pdf_content[0], dict) else pdf_content[0]
            response = model.generate_content(f"{input}\n\nResume:\n{resume_text}\n\nInstructions: {prompt}")
            return response.text
        except Exception as e2:
            return f"Error: {str(e2)}"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Extract text from PDF
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return [text]
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            st.stop()
            return None
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
