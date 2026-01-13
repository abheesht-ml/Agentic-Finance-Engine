import os
from langchain_core.documents import Document
from langchain_text_splitters  import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.input_schemas import ProcessedDocument
Chroma_Path = "Chroma_db"
def get_vector_store():
    embedding_function = OpenAIEmbeddings(model= "text-embedding-3-small")
    vector_store = Chroma(
        persist_directory= Chroma_Path,
        embedding_function= embedding_function,
        collection_name= "10k_Filings"
    )
    return vector_store

def indexed_document(data: ProcessedDocument):
    header = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=header)
    markdown_header_splits = markdown_text_splitter.split_text(data.content)
    recursive_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 200
    )
    final_chunks = recursive_text_splitter.split_documents(markdown_header_splits)
    for chunk in final_chunks:
        chunk.metadata.update(data.metadata)
    
    db = get_vector_store()
    db.add_documents(final_chunks)
    print("Files have been succesfully vectorised and stored")

