from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from pypdf import PdfReader

def process_text(text):
    # process the given text splitting it into chunks and converting
    # these chunks into embeddings to form a knowledge BaseException
    # Initialize a text splitter to divide the text into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    # split the text into chunks
    chunks = text_splitter.split_text(text)

    #load a model for generating embeddings from Hugging Face
    embeddings_model  = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all=MiniLM-L6-v2')

    # Create a FAISS indec from the text chunks from the text chunks using the embeddings
    knowledgeBase = FAISS.from_texts(chunks, embeddings_model )

    return knowledgeBase


def summarizer(pdf):
    # Function to summarize the content of a PDF File.

    if pdf is not None:
        # If a PDF File is provided

        # Read the PDF File
        reader = PdfReader(pdf)
        text = "" 

        # Extract text from each page of the PDF
        for page in reader.pages:
            text += page.extract_text() or ""

        # Process the extracted text to create a knowledge base
        knowledgeBase = process_text(text)

        # Define the query fir summarization 
        query = "Summarize the content of the uploaded PDF file in appropriately 3-5 sentences."

        if query:
            # Perform a similarity search in the knowledge base using the query
            docs = knowledgeBase.similarity_search(query)

            # Specify the model to use for generating the summary
            OpenAIModel = "gpt-3.5-turbo-16k"
            llm = ChatOpenAI(model = OpenAIModel, temperature = 0.8)

            # load a question-answering chain with the specifies model
            chain = load_qa_chain(llm, chain_type = 'stuff')

            # with get_openai_callback() as cost:
            #     # Run the chain to get a response and track the code
            #     response = chain.run(input_documents = docs, question = query)
            #     # Print the cost of the operation
            #     print(cost)
            #     # Return the generated summary
            #     return response

            # Run the chain to get a response and track the code
            response = chain.run(input_documents = docs, question = query)
            # Return the generated summary
            return response 
