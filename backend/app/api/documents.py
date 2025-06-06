from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
import os
import shutil

from ..models.database import get_db, DocumentFile, Project
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["documents"])


class DocumentResponse(BaseModel):
    id: str
    project_id: str
    filename: str
    file_type: str
    file_size: int
    processed: bool
    created_at: str

@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for the authenticated client."""
    docs = (
        db.query(DocumentFile)
        .filter(DocumentFile.client_id == current_user.id)
        .order_by(DocumentFile.created_at.desc())
        .all()
    )
    return [
        DocumentResponse(
            id=d.id,
            project_id=d.project_id,
            filename=d.filename,
            file_type=d.file_type,
            file_size=d.file_size,
            processed=d.processed,
            created_at=d.created_at.isoformat(),
        )
        for d in docs
    ]


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a document for a project."""
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.client_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    doc_id = str(uuid.uuid4())
    storage_dir = os.path.join("storage", "documents")
    os.makedirs(storage_dir, exist_ok=True)
    stored_filename = f"{doc_id}_{file.filename}"
    path = os.path.join(storage_dir, stored_filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_size = os.path.getsize(path)

    doc = DocumentFile(
        id=doc_id,
        client_id=current_user.id,
        project_id=project_id,
        filename=file.filename,
        stored_filename=stored_filename,
        file_type=file.content_type or "application/octet-stream",
        file_size=file_size,
        file_path=path,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        project_id=doc.project_id,
        filename=doc.filename,
        file_type=doc.file_type,
        file_size=doc.file_size,
        processed=doc.processed,
        created_at=doc.created_at.isoformat(),
    )
