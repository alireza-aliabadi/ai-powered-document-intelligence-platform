from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings

from .vector_store import vector_store_service

class RAGService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="glm-5.1",
            api_base=settings.OPENAI_API_BASE,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a document assistant. Answer only from this context."),
            ("human", "{context}"),
            ("human", "{question}")
        ])
        
    def ask(self, question):
        # Retrieve relevant documents from the vector store
        relevant_docs = vector_store_service.search(question)
        
        # Format the retrieved documents as context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate a response using the LLM
        response = self.llm.invoke(self.prompt_template.format(context=context, question=question))
        
        return response.content
    
rag_service = RAGService()