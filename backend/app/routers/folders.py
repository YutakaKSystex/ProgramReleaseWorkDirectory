from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.utils.auth import get_current_user
from app.schemas.schemas import FolderCreate, FolderResponse, FolderUpdate, FolderAccessBase
from app.services.database import (
    create_folder, get_folder_by_id, get_folders_by_parent,
    get_user_accessible_folders, update_folder, delete_folder,
    add_folder_access, remove_folder_access
)
from app.models.models import User, UserRole, FolderPermission

router = APIRouter(
    prefix="/folders",
    tags=["folders"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=FolderResponse)
async def create_new_folder(folder: FolderCreate, current_user: User = Depends(get_current_user)):
    if folder.parent_id:
        parent_folder = get_folder_by_id(folder.parent_id)
        if not parent_folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent folder not found"
            )
        
        has_permission = False
        for access in parent_folder.access_list:
            if access.user_id == current_user.id and access.permission in [FolderPermission.WRITE, FolderPermission.ADMIN]:
                has_permission = True
                break
        
        if not has_permission and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to create folder in this location"
            )
    
    new_folder = create_folder(
        name=folder.name,
        created_by=current_user.id,
        parent_id=folder.parent_id
    )
    
    return new_folder


@router.get("/", response_model=List[FolderResponse])
async def read_folders(parent_id: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if parent_id:
        folders = get_folders_by_parent(parent_id)
        
        if current_user.role != UserRole.ADMIN:
            folders = [
                folder for folder in folders 
                if any(access.user_id == current_user.id for access in folder.access_list)
            ]
    else:
        folders = get_user_accessible_folders(current_user.id)
    
    return folders


@router.get("/{folder_id}", response_model=FolderResponse)
async def read_folder(folder_id: str, current_user: User = Depends(get_current_user)):
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
    
    return folder


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder_info(
    folder_id: str, 
    folder_data: FolderUpdate, 
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
        if access.user_id == current_user.id and access.permission == FolderPermission.ADMIN:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this folder"
        )
    
    update_data = folder_data.dict(exclude_unset=True)
    updated_folder = update_folder(folder_id, **update_data)
    
    return updated_folder


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder_item(folder_id: str, current_user: User = Depends(get_current_user)):
    folder = get_folder_by_id(folder_id)
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
            detail="Not enough permissions to delete this folder"
        )
    
    delete_folder(folder_id)
    return None


@router.post("/{folder_id}/access", response_model=FolderResponse)
async def add_user_access(
    folder_id: str, 
    access: FolderAccessBase, 
    current_user: User = Depends(get_current_user)
):
    folder = get_folder_by_id(folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    has_permission = False
    for folder_access in folder.access_list:
        if folder_access.user_id == current_user.id and folder_access.permission == FolderPermission.ADMIN:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to manage access for this folder"
        )
    
    updated_folder = add_folder_access(folder_id, access.user_id, access.permission)
    return updated_folder


@router.delete("/{folder_id}/access/{user_id}", response_model=FolderResponse)
async def remove_user_access(
    folder_id: str, 
    user_id: str, 
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
        if access.user_id == current_user.id and access.permission == FolderPermission.ADMIN:
            has_permission = True
            break
    
    if not has_permission and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to manage access for this folder"
        )
    
    updated_folder = remove_folder_access(folder_id, user_id)
    return updated_folder
