# AI-Powered Document Intelligence Platform

> Upload documents → Extract knowledge → Search semantically → Chat with
> your data

A production-style AI document intelligence platform built with Django,
React, TypeScript, Celery, Redis, MongoDB, and S3-compatible object
storage.

## Key Features

-   Document ingestion pipeline
-   Text extraction and preprocessing
-   Document chunking
-   Embedding generation
-   Semantic search
-   Retrieval Augmented Generation (RAG)
-   Natural language document Q&A
-   Async processing with Celery
-   Docker-based deployment

## Architecture

    User
     |
     v
    React + TypeScript
     |
     v
    Django REST API
     |
     +----------------+
     |                |
     v                v
    Celery        PostgreSQL
    Workers
     |
     +----------------+
     |        |       |
     v        v       v
    Redis  MongoDB  S3 Storage

## AI Processing Pipeline

    Upload Document
          |
          v
    Object Storage
          |
          v
    Celery Worker
          |
          v
    Text Extraction
          |
          v
    Chunking
          |
          v
    Embedding Generation
          |
          v
    Semantic Retrieval
          |
          v
    LLM Response

## Technology Stack

### Backend

-   Django
-   Django REST Framework
-   Celery
-   Redis
-   PostgreSQL
-   MongoDB

### AI

-   LLM integration
-   Embeddings
-   RAG pipeline
-   Semantic search

### Frontend

-   React
-   TypeScript
-   Vite
-   Axios

### Infrastructure

-   Docker
-   Docker Compose
-   AIStor / S3-compatible storage

## Quick Start

``` bash
cp .env.example .env
chmod +x docker-setup.sh
./docker-setup.sh
```

Start services:

``` bash
make up
```

View logs:

``` bash
make logs
```

## Services

  Service           URL
  ----------------- -----------------------------
  Frontend          http://localhost:3000
  API               http://localhost:8000
  Django Admin      http://localhost:8000/admin
  Storage Console   http://localhost:9001

## Engineering Highlights

This project demonstrates:

-   AI application architecture
-   RAG system design
-   Distributed processing
-   Scalable backend engineering
-   Modern frontend development