from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["documents"])

@router.get("/documents")
async def list_documents(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents (placeholder)"""
    return {"message": "Documents endpoint not yet implemented"}