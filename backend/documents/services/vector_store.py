import hashlib

from django.conf import settings
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


def _api_key_configured() -> bool:
    key = (settings.OPENAI_API_KEY or "").strip()
    return bool(key) and "placeholder" not in key.lower()


class HashingEmbeddings(Embeddings):
    """Fast offline embeddings (no model download) for local/dev RAG."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in text.lower().split():
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            idx = int(digest, 16) % self.dim
            vec[idx] += 1.0
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class VectorStoreService:
    """Uses a collection name tied to embedding dim to avoid 384 vs 1536 clashes."""

    def __init__(self):
        if _api_key_configured():
            # text-embedding-3-small default dim is 1536
            self.embeddings: Embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE or None,
            )
            self.collection_name = "documents_openai_1536"
        else:
            self.embeddings = HashingEmbeddings(dim=384)
            self.collection_name = "documents_hash_384"

        self.store = Chroma(
            collection_name=self.collection_name,
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents):
        self.store.add_documents(documents)

    def search(self, query, k=5):
        return self.store.similarity_search(query, k=k)


vector_store_service = VectorStoreService()
