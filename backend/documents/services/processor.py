from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vector_store import vector_store_service


class DocumentProcessorService:
    def process(self, file_path):
        # Load the PDF document
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split the document into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        
        return chunks
        # Add the split documents to the vector store
        # vector_store_service.add_documents(split_documents)
        
processor_service = DocumentProcessorService()