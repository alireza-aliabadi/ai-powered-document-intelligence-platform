from django.urls import path

from .views import ChatAPIView, DocumentUploadView, JobStatusView

urlpatterns = [
    path("upload/", DocumentUploadView.as_view(), name="document-upload"),
    path("jobs/<str:task_id>/", JobStatusView.as_view(), name="job-status"),
    path("chat/", ChatAPIView.as_view(), name="chat-api"),
]
