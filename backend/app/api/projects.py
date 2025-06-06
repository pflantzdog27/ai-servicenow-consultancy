from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..models.database import Project, Client, get_db
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["projects"])

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    created_at: str
    document_count: int

@router.get("/projects")
async def list_projects(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List client's projects (placeholder)"""
    return {"message": "Projects endpoint not yet implemented"}