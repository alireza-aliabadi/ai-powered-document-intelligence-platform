from io import BytesIO

from django.conf import settings
from minio import Minio


class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.AI_STORAGE_ENDPOINT,
            access_key=settings.AI_STORAGE_ACCESS_KEY,
            secret_key=settings.AI_STORAGE_SECRET_KEY,
            secure=False,
        )

    def upload_file(self, bucket_name, object_name, file_data):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

        size = getattr(file_data, "size", None)
        if size is not None and hasattr(file_data, "seek"):
            file_data.seek(0)
            self.client.put_object(bucket_name, object_name, file_data, size)
            return

        raw = file_data.read() if hasattr(file_data, "read") else bytes(file_data)
        self.client.put_object(bucket_name, object_name, BytesIO(raw), len(raw))

    def download_file(self, bucket_name, object_name) -> bytes:
        response = self.client.get_object(bucket_name, object_name)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()


storage_service = StorageService()
