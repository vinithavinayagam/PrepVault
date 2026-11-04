# PrepVault

Examate - AI-Powered Course Notes Assistant

## Product Overview
A multi-tenant AI-powered course notes assistant for college students.

## Problem Statement
Students from different colleges need answers from their course materials. The system must handle high demand, protect college data, and manage shared LLM quotas.

## Key Challenges
- Quota management
- College and batch data isolation
- Handling high traffic
- Reliable answers grounded in course notes

## Technology Stack
- Python
- FastAPI
- Google Gemini API
- PostgreSQL
- pgvector
- SQLAlchemy
- Docker Compose

## Current Features
- Health check API
- Gemini-powered chat API
- Usage tracking
- PostgreSQL integration
- College, course, document, and document chunk models
- Docker Compose setup

## Run Locally
uvicorn app.main:app --reload

## Run with Docker
docker compose up --build -d

## API Documentation
http://localhost:8000/docs


