import os
import tempfile

from celery import shared_task

from .repositories.document_repo import repo
from .services.processor import processor_service
from .services.sotrage import storage_service
from .services.vector_store import vector_store_service


@shared_task(bind=True)
def process_document(self, object_name: str, document_id: str | None = None) -> dict:
    """Download a PDF from object storage, chunk it, and index embeddings."""
    if document_id:
        repo.update_document(document_id, {"status": "processing", "task_id": self.request.id})

    raw = storage_service.download_file("documents", object_name)
    fd, path = tempfile.mkstemp(suffix=".pdf")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
        chunks = processor_service.process(path)
        if not chunks:
            if document_id:
                repo.update_document(document_id, {"status": "done", "chunks": 0})
            return {"chunks": 0, "status": "done"}

        batch_size = 16
        for i in range(0, len(chunks), batch_size):
            vector_store_service.add_documents(chunks[i : i + batch_size])

        if document_id:
            repo.update_document(document_id, {"status": "done", "chunks": len(chunks)})
        return {"chunks": len(chunks), "status": "done"}
    except Exception as exc:
        if document_id:
            repo.update_document(document_id, {"status": "failed", "error": str(exc)})
        raise
    finally:
        if os.path.exists(path):
            os.unlink(path)
