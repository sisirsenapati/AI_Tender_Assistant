import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Model
model = genai.GenerativeModel("gemini-2.5-flash-lite")
# UI
st.set_page_config(
    page_title="AI Tender Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Tender Assistant")
st.write("Upload a Tender PDF and get instant AI analysis.")

uploaded_file = st.file_uploader(
    "Upload Tender PDF",
    type=["pdf"]
)

if uploaded_file:

    try:
        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        st.success("Tender PDF Loaded Successfully")

        if st.button("Analyze Tender"):

            with st.spinner("Analyzing Tender..."):

                prompt = f"""
                Analyze the following tender document.

                Provide:

                1. Tender Summary
                2. Eligibility Criteria
                3. EMD Details
                4. Completion Period
                5. Important Dates
                6. Risk Factors
                7. Key Recommendations

                Tender Document:

                {text[:50000]}
                """

                response = model.generate_content(prompt)

                st.subheader("Tender Analysis")

                st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")