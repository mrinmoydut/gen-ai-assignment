import streamlit as st
import tempfile
import fitz  # PyMuPDF
import os
import openai
from io import BytesIO

OPENAI_API_KEY = 'sk-proj-COOaWbFJMfj2cgnWtZS7T3BlbkFJum6DEUSH0n5l9jrVg3A5'

def text_extract(file):
    doc_text = ""
    if file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "uploaded_file.pdf")
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file.read())
            try:
                with fitz.open(temp_file_path) as doc:
                    for page_num in range(doc.page_count):
                        page = doc.load_page(page_num)
                        doc_text += page.get_text("text")
            except Exception as e:
                st.error(f"Error extracting text: {e}")
    return doc_text


def main():
    st.title("PDF Text Extractor")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        doc_contents = text_extract(uploaded_file)
        if doc_contents:
            st.header("PDF Contents:")
            st.text(doc_contents)

            if OPENAI_API_KEY:
                if st.button("Process with OpenAI"):
                    try:
                        openai.api_key = OPENAI_API_KEY
                        response = openai.Completion.create(
                            model="gpt-3.5-turbo",
                            prompt=f"Extracted Text: {doc_contents}\n\nProvide a summary:",
                            max_tokens=150
                        )
                        st.header("OpenAI Response:")
                        st.text(response.choices[0].text.strip())
                    except Exception as e:
                        st.error(f"Error using OpenAI API: {e}")
                else:
                    st.error("OpenAI API key is not set")
        else:
            st.error("No text found in the uploaded PDF.")

if __name__ =="__main__":
    main()
# streamlit run pdf_text_extractor.py
