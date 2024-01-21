from sentence_transformers import SentenceTransformer # using SentenceTransformers for embeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import os,langchain
from langchain.callbacks import get_openai_callback # Check number of token use per request
from langchain.llms import OpenAI     
from pypdf import PdfReader
import re
from langchain.docstore.document import Document
import streamlit as st
from langchain.vectorstores import FAISS


@st.cache_resource
def process(file):
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        output.append(text)
    document = [Document(page_content=text) for text in output]
    
    text_splitter =CharacterTextSplitter(chunk_size=1000,chunk_overlap=200,length_function=len)
    doc = text_splitter.split_documents(document)

    embedding_function = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2') 

    db = Chroma.from_documents(doc,embedding_function)
    #db = FAISS.from_documents(doc,embedding_function)
    return db

@st.cache_resource
def load_chain(OPENAI_API_KEY):

    qa_chain = load_qa_chain(llm=OpenAI(openai_api_key=OPENAI_API_KEY),chain_type="stuff")
    return qa_chain


def similarity(vectorstore,query):

    docs = vectorstore.similarity_search(query)

    return docs




























