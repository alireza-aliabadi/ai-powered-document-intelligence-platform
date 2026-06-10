from minio import Minio
from django.conf import settings

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.AI_STORAGE_ENDPOINT,
            access_key=settings.AI_STORAGE_ACCESS_KEY,
            secret_key=settings.AI_STORAGE_SECRET_KEY,
            secure=False
        )

    def upload_file(self, bucket_name, object_name, file_data):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.client.put_object(bucket_name, object_name, file_data, len(file_data))

    def download_file(self, bucket_name, object_name):
        response = self.client.get_object(bucket_name, object_name)
        return response.read()
    
storage_service = StorageService()