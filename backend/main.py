from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os

from app.api import auth, documents, projects, ai, workflows
from app.models.database import Base, engine

# Create FastAPI app
app = FastAPI(
    title="AI ServiceNow Document Repository",
    version="1.0.0",
    description="AI-powered document repository and RAG chatbot for ServiceNow consulting"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.servicenow-ai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for document storage
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Include routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(projects.router)
app.include_router(ai.router)
app.include_router(workflows.router)

@app.get("/")
async def root():
    return {"message": "AI ServiceNow Document Repository API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }