import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Document Summarizer Bot", page_icon="📄")

st.title("📄 Smart Document Summarizer Bot")
st.write("Upload a PDF, Word, or Text file and get a clean structured summary ✨")

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    if not text:
        return ""

    # Remove bad unicode (fixes UTF-8 error)
    text = text.encode("utf-8", "ignore").decode("utf-8")

    # Add spaces between joined words (CamelCase / merged text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Fix missing spaces after punctuation
    text = re.sub(r'([.,!?])([A-Za-z])', r'\1 \2', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ---------------- FILE TEXT EXTRACTION ----------------
def extract_text(file):
    file_type = file.name.split(".")[-1].lower()

    text = ""

    # -------- PDF --------
    if file_type == "pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    # -------- WORD --------
    elif file_type == "docx":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])

    # -------- TEXT --------
    elif file_type == "txt":
        text = file.read().decode("utf-8")

    else:
        st.error("❌ Unsupported file type")
        return ""

    return clean_text(text)


# ---------------- SIMPLE STRUCTURED SUMMARY ----------------
def generate_summary(text):
    if not text:
        return "No content to summarize."

    # Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    # Take important lines
    intro = sentences[:2]
    key_points = sentences[2:6]
    ending = sentences[-2:]

    summary = "### 📌 Summary\n\n"

    summary += "#### 🔹 Introduction\n"
    for line in intro:
        summary += f"- {line}\n"

    summary += "\n#### 🔹 Key Points\n"
    for line in key_points:
        summary += f"- {line}\n"

    summary += "\n#### 🔹 Conclusion\n"
    for line in ending:
        summary += f"- {line}\n"

    return summary


# ---------------- FILE UPLOADER ----------------
uploaded_file = st.file_uploader(
    "📤 Upload your file",
    type=["pdf", "docx", "txt"]
)

# ---------------- MAIN APP FLOW ----------------
if uploaded_file is not None:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    raw_text = extract_text(uploaded_file)

    # -------- PREVIEW --------
    st.subheader("📄 Preview")
    st.write(raw_text[:800] + "...")

    # -------- SUMMARY BUTTON --------
    if st.button("✨ Generate Summary"):
        with st.spinner("Generating smart summary..."):
            summary = generate_summary(raw_text)

        st.subheader("🧠 Smart Summary")
        st.markdown(summary)

else:
    st.info("⬆️ Upload a document to get started.")
