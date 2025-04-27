import streamlit as st
from dotenv import load_dotenv
import os
from util import *

# Load environment variables from the .env file
load_dotenv()

def main():
    response = ""

    st.set_page_config(page_title="PDF Summarizer")

    # title for the page
    st.title("PDF Summarizing App")
    st.write("Summarize your pdf file in just a few seconds")
    st.divider()
    
    pdf = st.file_uploader("Upload your PDF Document", type='pdf')

    submit = st.button("Generate Summary")

    # Access the API key from environment variables
    api_key = os.getenv("OPEN_API_KEY")
    if api_key is None:
        st.error("API Key is missing. Please check your .env file.")
        return

    if submit :
        response = summarizer(pdf)
        st.subheader('Summary of PDF File')
        st.write(response)

if __name__ == '__main__':
    main()