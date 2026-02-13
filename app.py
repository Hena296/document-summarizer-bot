import streamlit as st
from PyPDF2 import PdfReader

st.title("📄 Document Summarizer Bot")

# Upload file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Function to extract text from PDF
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# Simple summarizer (basic version without AI API)
def simple_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:5])  # first 5 sentences as summary

# When file is uploaded
if uploaded_file is not None:
    text = extract_text(uploaded_file)

    st.subheader("Preview")
    st.write(text[:500])

    if st.button("Summarize"):
        summary = simple_summary(text)

        st.subheader("Summary")
        st.success(summary)
