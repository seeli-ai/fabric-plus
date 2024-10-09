import streamlit as st
from dynamicpdf_api.pdf_text import PdfText
from dynamicpdf_api.pdf_resource import PdfResource
import tempfile
import os
import json
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow running asyncio in Jupyter-like environments
nest_asyncio.apply()

async def extract_text_from_pdf(api_key, file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        resource = PdfResource(tmp_file_path)
        pdf_text = PdfText(resource)
        pdf_text.api_key = api_key
        pdf_text.start_page = 1
        pdf_text.page_count = 10  # Adjust as needed
        response = await pdf_text.process_async()
        return response.json_content
    finally:
        os.unlink(tmp_file_path)  # Delete the temporary file


def decode_utf8(json_str):
    # Decode the JSON string
    decoded = json.loads(json_str)
    
    # Function to recursively decode UTF-8 in the JSON structure
    def decode_utf8_recursive(obj):
        if isinstance(obj, str):
            return obj.encode().decode('utf-8')
        elif isinstance(obj, list):
            return [decode_utf8_recursive(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: decode_utf8_recursive(value) for key, value in obj.items()}
        else:
            return obj
    
    return decode_utf8_recursive(decoded)


# Streamlit app
st.title("PDF Text Extractor")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# API key input (you might want to handle this more securely in a real application)

api_key = os.getenv("DYNAMIC_PDF_KEY")
if not api_key:
    st.error("API key not found. Please set the DYNAMIC_PDF_KEY environment variable.")
    st.stop()

if uploaded_file is not None:
    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            try:
                # Run the async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                extracted_text = loop.run_until_complete(extract_text_from_pdf(api_key, uploaded_file))
                
                decoded_text = decode_utf8(extracted_text)
                
                st.subheader("Raw JSON Response:")
                st.write(decoded_text)

                # Display the decoded text
                #st.subheader("Extracted Text:")
                #for page in decoded_text:
                 #   st.write(f"Page {page['pageNumber']}:")
                 #   st.text(page['text'])
                
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                loop.close()


