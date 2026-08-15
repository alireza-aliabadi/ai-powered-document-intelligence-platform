from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.repositories.document_repo import repo
from documents.services.rag import rag_service
from documents.services.sotrage import storage_service
from documents.tasks import process_document


class DocumentUploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        storage_service.upload_file("documents", file.name, file)

        document_data = {
            "filename": file.name,
            "size": file.size,
            "content_type": file.content_type,
            "status": "queued",
        }
        document_id = repo.insert_document(document_data)

        async_result = process_document.delay(file.name, str(document_id))
        repo.update_document(document_id, {"task_id": async_result.id})

        return Response(
            {
                "message": "File uploaded successfully",
                "file_id": str(document_id),
                "task_id": async_result.id,
            },
            status=status.HTTP_201_CREATED,
        )


class JobStatusView(APIView):
    def get(self, request, task_id: str):
        result = AsyncResult(task_id)
        payload = {
            "task_id": task_id,
            "status": result.status,  # PENDING | STARTED | SUCCESS | FAILURE
        }
        if result.successful():
            payload["result"] = result.result
            payload["done"] = True
        elif result.failed():
            payload["done"] = True
            payload["error"] = str(result.result)
        else:
            payload["done"] = False
        return Response(payload, status=status.HTTP_200_OK)


class ChatAPIView(APIView):
    def post(self, request):
        question = request.data.get("question", "")
        try:
            answer = rag_service.ask(question)
        except Exception as exc:  # noqa: BLE001 - keep UI usable with readable errors
            answer = f"Chat failed: {exc}"
        return Response({"answer": answer}, status=status.HTTP_200_OK)
