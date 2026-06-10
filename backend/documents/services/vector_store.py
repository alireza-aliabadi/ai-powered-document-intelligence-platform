from langchain_chroma import Chroma
from langchain_core.embeddings import OpenAIEmbeddings
from django.conf import settings

class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            # api_base=settings.OPENAI_API_BASE,
            # api_key=settings.OPENAI_API_KEY
        )
        
        self.store = Chroma(
            collection_name="documents",
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        
    def add_documents(self, documets):
        self.store.add_documents(documets)
    
    def search(self, query, k=5):
        return self.store.similarity_search(query, k=k)
    
vector_store_service = VectorStoreService()
    