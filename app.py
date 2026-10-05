import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()
# API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")

st.title("AI Tender Assistant")

uploaded_file = st.file_uploader(
    "Upload Tender PDF",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.success("Tender Loaded")

    if st.button("Analyze Tender"):

        prompt = f"""
        Analyze this tender.

        Extract:

        1. Tender Summary
        2. Eligibility Criteria
        3. EMD
        4. Completion Period
        5. Important Dates
        6. Risk Factors

        Tender:
        {text[:50000]}
        """

        response = model.generate_content(prompt)

        st.write(response.text)