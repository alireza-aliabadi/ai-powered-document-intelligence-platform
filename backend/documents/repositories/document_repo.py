from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient


def _as_id(document_id):
    if isinstance(document_id, ObjectId):
        return document_id
    return ObjectId(str(document_id))


class DocumentRepository:
    """Lazy Mongo client so Celery prefork workers stay fork-safe."""

    def __init__(self):
        self._client = None
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            self._client = MongoClient(settings.MONGO_URI, connect=False)
            self._collection = self._client[settings.MONGO_DATABASE]["documents"]
        return self._collection

    def insert_document(self, document):
        return self._get_collection().insert_one(document).inserted_id

    def get_document(self, document_id):
        return self._get_collection().find_one({"_id": _as_id(document_id)})

    def update_document(self, document_id, update_data):
        return self._get_collection().update_one(
            {"_id": _as_id(document_id)}, {"$set": update_data}
        )

    def delete_document(self, document_id):
        return self._get_collection().delete_one({"_id": _as_id(document_id)})


repo = DocumentRepository()
