from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
import json
import os
import shutil
from app.utils.auth import get_current_user
from app.schemas.schemas import DocumentCreate, DocumentResponse, DocumentUpdate
from app.services.database import (
    create_document, get_document_by_id, get_documents_by_folder,
    update_document, delete_document, get_folder_by_id
)
from app.models.models import User, UserRole, FolderPermission

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    folder_id: str = Form(...),
    metadata: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    folder = get_folder_by_id(folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    has_permission = False
    for access in folder.access_list:
        if access.user_id == current_user.id and access.permission in [FolderPermission.WRITE, FolderPermission.ADMIN]:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to upload to this folder"
        )
    
    os.makedirs("uploads", exist_ok=True)
    
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    metadata_dict = {}
    if metadata:
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid metadata format"
            )
    
    document = create_document(
        name=file.filename,
        folder_id=folder_id,
        file_path=file_path,
        file_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(file_path),
        created_by=current_user.id,
        metadata=metadata_dict
    )
    
    return document


@router.get("/", response_model=List[DocumentResponse])
async def read_documents(folder_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if folder_id:
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found"
            )
        
        has_access = False
        for access in folder.access_list:
            if access.user_id == current_user.id:
                has_access = True
                break
        
        if not has_access and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this folder"
            )
        
        documents = get_documents_by_folder(folder_id)
    else:
        documents = []
        
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(document_id: str, current_user: User = Depends(get_current_user)):
    document = get_document_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    folder = get_folder_by_id(document.folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    has_access = False
    for access in folder.access_list:
        if access.user_id == current_user.id:
            has_access = True
            break
    
    if not has_access and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this document"
        )
    
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document_info(
    document_id: str, 
    document_data: DocumentUpdate, 
    current_user: User = Depends(get_current_user)
):
    document = get_document_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    folder = get_folder_by_id(document.folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    has_permission = False
    for access in folder.access_list:
        if access.user_id == current_user.id and access.permission in [FolderPermission.WRITE, FolderPermission.ADMIN]:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this document"
        )
    
    if document_data.folder_id and document_data.folder_id != document.folder_id:
        target_folder = get_folder_by_id(document_data.folder_id)
        if not target_folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target folder not found"
            )
        
        has_target_permission = False
        for access in target_folder.access_list:
            if access.user_id == current_user.id and access.permission in [FolderPermission.WRITE, FolderPermission.ADMIN]:
                has_target_permission = True
                break
        
        if not has_target_permission and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to move document to target folder"
            )
    
    update_data = document_data.dict(exclude_unset=True)
    updated_document = update_document(document_id, **update_data)
    
    return updated_document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_item(document_id: str, current_user: User = Depends(get_current_user)):
    document = get_document_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    folder = get_folder_by_id(document.folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    has_permission = False
    for access in folder.access_list:
        if access.user_id == current_user.id and access.permission == FolderPermission.ADMIN:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this document"
        )
    
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    delete_document(document_id)
    
    return None
