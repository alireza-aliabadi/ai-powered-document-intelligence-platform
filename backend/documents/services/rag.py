from django.conf import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .vector_store import _api_key_configured, vector_store_service


class RAGService:
    def __init__(self):
        self.llm = None
        if _api_key_configured():
            self.llm = ChatOpenAI(
                model=getattr(settings, "LLM_MODEL", None) or "gpt-4o-mini",
                base_url=settings.OPENAI_API_BASE or None,
                api_key=settings.OPENAI_API_KEY,
                temperature=0,
            )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a document assistant. Answer only from this context."),
                ("human", "Context:\n{context}\n\nQuestion: {question}"),
            ]
        )

    def ask(self, question: str) -> str:
        relevant_docs = vector_store_service.search(question or "document topics overview", k=8)
        if not relevant_docs:
            return (
                "No indexed document content found yet. "
                "Upload a PDF and wait for processing to finish, then try again."
            )

        context = "\n\n".join(doc.page_content for doc in relevant_docs)

        if self.llm is not None:
            response = self.llm.invoke(
                self.prompt_template.format(context=context, question=question)
            )
            return response.content

        # Offline extractive fallback when OPENAI_API_KEY is missing/placeholder
        topics = []
        for doc in relevant_docs:
            line = " ".join(doc.page_content.split())
            if len(line) < 24:
                continue
            topics.append(line[:220] + ("…" if len(line) > 220 else ""))
            if len(topics) >= 8:
                break

        numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(topics, 1))
        return (
            "Indexed document excerpts (local mode — set a real OPENAI_API_KEY for LLM answers):\n\n"
            f"{numbered}"
        )


rag_service = RAGService()
