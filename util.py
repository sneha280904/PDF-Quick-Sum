## <---------- Imports ---------->
### Import required libraries
import openai
from openai import OpenAIError, RateLimitError

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from pypdf import PdfReader


## <---------- Function: Process Text ---------->
### Splits input text into chunks, generates embeddings, and creates FAISS knowledge base
def process_text(text):
    """
    Splits the input text into manageable chunks, generates embeddings,
    and creates a FAISS knowledge base.
    """
    # Initialize a text splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    # Split text into chunks
    chunks = text_splitter.split_text(text)

    # Load Hugging Face embeddings model
    embeddings_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a FAISS index from the text chunks
    knowledge_base = FAISS.from_texts(chunks, embeddings_model)

    return knowledge_base


## <---------- Function: Summarizer ---------->
### Summarizes content from uploaded PDF file using OpenAI's GPT model
def summarizer(pdf, api_key):
    """
    Summarizes the content of an uploaded PDF file into 3-5 sentences
    using OpenAI's GPT model.
    """
    if pdf is not None:
        # Read the PDF file
        reader = PdfReader(pdf)
        text = ""

        # Extract text from each page
        for page in reader.pages:
            text += page.extract_text() or ""

        # Process the extracted text to create a knowledge base
        knowledge_base = process_text(text)

        # Define the query for summarization
        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."

        if query:
            # Perform a similarity search based on the query
            docs = knowledge_base.similarity_search(query)

            # Specify the OpenAI model for generating the summary
            openai_model_name = "gpt-3.5-turbo-16k"
            llm = ChatOpenAI(model=openai_model_name, temperature=0.8, openai_api_key=api_key)

            # Load a question-answering chain with the specified model
            chain = load_qa_chain(llm, chain_type='stuff')

            ## <---------- Exception Handling ---------->
            ### Handle different exceptions like quota exceeded or unexpected errors
            try:
                response = chain.run(input_documents=docs, question=query)
                return response

            except RateLimitError:
                print("You have exceeded your OpenAI quota. Please check your billing details.")
                return "Quota Exceeded: Please update your API key or billing."

            # except OpenAIError as e:
                print(f"An OpenAI error occurred: {e}")
                return "An error occurred with OpenAI."

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return "An unexpected error occurred during summarization."
