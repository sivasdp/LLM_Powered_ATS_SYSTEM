# Run command streamlit run app.py --server.enableXsrfProtection false

from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv('YOUR_API_KEY'))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_path(uploaded_file)

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="LLM Powered ATS Expert")
st.header("LLM Powered ATS Resume Screening System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

st.sidebar.header("Documentation:")
st.sidebar.write("---------------")
st.sidebar.write('''
Welcome to the documentation for the LLM (Large Language Model) Powered Applicant Tracking System (ATS) Expert! This documentation provides a brief overview of the system's features and usage instructions.

## Overview

The LLM Powered ATS Expert is a Streamlit application designed to assist in resume screening and evaluation processes. It leverages a powerful generative AI model to analyze resumes and provide insights based on job descriptions.

## Features

- **Resume Analysis**: Upload resumes in PDF format and receive detailed evaluations based on provided job descriptions.
- **Skill Improvement Suggestions**: Receive suggestions on how to improve skills based on submitted resumes and job descriptions.
- **Percentage Match Calculation**: Determine the percentage match between resumes and job descriptions, along with keywords missing and final thoughts.

## Getting Started

To get started with the LLM Powered ATS Expert, follow these simple steps:

1. **Access the Application**: Visit the website where the application is hosted.
2. **Upload a Resume**: Use the file uploader to upload a resume in PDF format.
3. **Enter Job Description**: Enter the job description or requirements in the provided text area.
4. **Choose Action**: Select one of the available actions, such as "Tell Me About the Resume" or "Percentage Match".
5. **View Results**: Once the analysis is complete, view the generated response within the application.

## Author Details

The LLM Powered ATS Expert is developed by [Developer Name]. For any inquiries or feedback, please contact [Developer Email].

## Support

For assistance or troubleshooting, please  reach out to our support team at sivadhandapanis25@gmail.com.

## FAQ

**Q: What file format does the application support for resume upload?**  
A: The application supports resumes in PDF format only.

**Q: Can I use the application without uploading a resume?**  
A: No, the application requires a resume to perform analysis.

**Q: Is there a limit to the size of the uploaded resume?**  
A: Currently, the ats system accepts only if the file is less than 200MB.

''')


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

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
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")