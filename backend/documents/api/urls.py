from django.urls import path
from .views import DocumentUploadView, ChatAPIView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('chat/', ChatAPIView.as_view(), name='chat-api'),
]