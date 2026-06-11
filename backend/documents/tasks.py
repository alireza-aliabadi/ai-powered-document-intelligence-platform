from celery import shared_task
from .services.processor import processor_service
from .services.vector_store import vector_store_service

@shared_task
def process_document(file_path):
    chunks = processor_service.process(file_path)
    vector_store_service.add_documents(chunks)
    
