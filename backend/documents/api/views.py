from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from documents.services.sotrage import storage_service
from documents.tasks import process_document
from documents.repositories.document_repo import repo
from ducuments.services.rag import rag_service

class DocumentUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save file to storage
        storage_service.upload_file("documents", file.name, file)
        
        # Create document record in database
        document_data = {
            'filename': file.name,
            'size': file.size,
            'content_type': file.content_type
        }
        document_id = repo.insert_document(document_data)
        
        # Trigger background processing task
        process_document.delay(file.name)
        
        return Response({'message': 'File uploaded successfully', 'file_id': str(document_id)}, status=status.HTTP_201_CREATED)
    
class ChatAPIView(APIView):
    def post(self, request):
        answer = rag_service.ask(request.data.get('question', ''))
        return Response({'answer': answer}, status=status.HTTP_200_OK)