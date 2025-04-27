import streamlit as st
import os
from util import *


def main():
    st.set_page_config(page_title="PDF Summarizer")

    # title for the page
    st.title("PDF Summarizing App")
    st.write("Summarize your pdf file in just a few seconds")
    st.divider()
    
    pdf = st.file_uploader("Upload your PDF Document", type='pdf')

    submit = st.button("Generate Summary")

    os.environ["OP"]

if __name__ == '__main__':
    main()