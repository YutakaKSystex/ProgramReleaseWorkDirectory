from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.utils.auth import get_current_user
from app.schemas.schemas import (
    ApprovalFormCreate, ApprovalFormResponse, ApprovalFormUpdate,
    FormInitialize
)
from app.services.database import (
    create_approval_form, get_approval_form_by_id, get_all_approval_forms,
    update_approval_form, delete_approval_form
)
from app.models.models import User, UserRole

router = APIRouter(
    prefix="/approval-forms",
    tags=["approval forms"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=ApprovalFormResponse)
async def create_new_approval_form(
    form: ApprovalFormCreate, 
    current_user: User = Depends(get_current_user)
):
    new_form = create_approval_form(
        name=form.name,
        created_by=current_user.id,
        description=form.description,
        fields=form.fields,
        target_folder_id=form.target_folder_id
    )
    
    return new_form


@router.get("/", response_model=List[ApprovalFormResponse])
async def read_approval_forms(current_user: User = Depends(get_current_user)):
    forms = get_all_approval_forms()
    
    return forms


@router.get("/{form_id}", response_model=ApprovalFormResponse)
async def read_approval_form(form_id: str, current_user: User = Depends(get_current_user)):
    form = get_approval_form_by_id(form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    return form


@router.put("/{form_id}", response_model=ApprovalFormResponse)
async def update_approval_form_info(
    form_id: str, 
    form_data: ApprovalFormUpdate, 
    current_user: User = Depends(get_current_user)
):
    form = get_approval_form_by_id(form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    if form.created_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this form"
        )
    
    update_data = form_data.dict(exclude_unset=True)
    updated_form = update_approval_form(form_id, **update_data)
    
    return updated_form


@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approval_form_item(form_id: str, current_user: User = Depends(get_current_user)):
    form = get_approval_form_by_id(form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    if form.created_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this form"
        )
    
    delete_approval_form(form_id)
    
    return None


@router.post("/initialize", response_model=dict)
async def initialize_form(
    init_data: FormInitialize,
    current_user: User = Depends(get_current_user)
):
    form = get_approval_form_by_id(init_data.form_id)
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    return {"form_id": init_data.form_id, "initial_values": init_data.initial_values}
