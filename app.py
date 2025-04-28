
### <---------- Imports ---------->
import streamlit as st
from dotenv import load_dotenv
import os
from util import summarizer  # Import only what you need

### <---------- Load Environment Variables ---------->
load_dotenv()

### <---------- Main App Function ---------->
def main():
    # Initialize response
    response = ""

    # Configure Streamlit page
    st.set_page_config(page_title="PDF QUICK SUM")

    # Page Title and Description
    st.title("📄 PDF QUICK SUM: PDF Summarizer App")
    st.write("Summarize your PDF file in just a few seconds!")
    st.divider()

    # File uploader for PDF
    pdf = st.file_uploader("Upload your PDF Document", type='pdf')

    # Button to trigger summarization
    submit = st.button("Generate Summary")

    # Access the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")  # Fixed the key name here
    if api_key is None:
        st.error("API Key is missing. Please check your .env file and ensure OPENAI_API_KEY is set.")
        return

    # If submit button is clicked
    if submit:
        with st.spinner('Generating summary... Please wait!'):
            response = summarizer(pdf, api_key)

        # Display the generated summary
        st.subheader('📝 Summary of the PDF File')
        st.write(response)

### <---------- Run the App ---------->
if __name__ == '__main__':
    main()
