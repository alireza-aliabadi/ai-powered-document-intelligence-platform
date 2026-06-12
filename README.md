# ai-powered-document-intelligence-platform
Upload documents → extract knowledge → query with natural language

## Overview
This project ingests documents, extracts structured knowledge (OCR + NLP), builds vector embeddings, and exposes a queryable API backed by retrieval-augmented generation (RAG). It provides a Django backend, document processing services, and a simple vector store integration.

## Features
- Document ingestion (PDF, DOCX, images)
- OCR and text extraction
- NLP processing and knowledge extraction
- Vector embeddings and RAG-based question answering
- REST API and admin interface

## Quickstart
Prerequisites:
- Python 3.10+
- Docker (for database/storage services)

Recommended local setup:

```bash
# start database and storage services
docker compose -f db-storage-compose.yml up -d

# create virtualenv and install dependencies (or use poetry)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# migrate and run server
python backend/manage.py migrate
python backend/manage.py createsuperuser   # optional
python backend/manage.py runserver
```

Environment:
- Set `DJANGO_SETTINGS_MODULE` to `config.settings` if needed.

## Project layout
- [backend/manage.py](backend/manage.py) — Django management entrypoint
- [config/](config) — Django project settings and WSGI/ASGI
- [documents/](documents) — app for ingestion, processing, and APIs
	- [documents/services/processor.py](documents/services/processor.py) — processing pipeline
	- [documents/services/vector_store.py](documents/services/vector_store.py) — vector store integration
	- [documents/api/](documents/api) — serializers and API views

## Development
- Run tests: `pytest` or `python -m pytest`
- Formatting: `black .` / `isort .`
