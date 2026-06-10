from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

class DocumentRepository:
    def __init__(self):
        self.collection = db['documents']

    def insert_document(self, document):
        return self.collection.insert_one(document).inserted_id

    def get_document(self, document_id):
        return self.collection.find_one({'_id': document_id})

    def update_document(self, document_id, update_data):
        return self.collection.update_one({'_id': document_id}, {'$set': update_data})

    def delete_document(self, document_id):
        return self.collection.delete_one({'_id': document_id})

repo = DocumentRepository()