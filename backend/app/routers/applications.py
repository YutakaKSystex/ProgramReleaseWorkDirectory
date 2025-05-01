from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.utils.auth import get_current_user
from app.schemas.schemas import (
    ApplicationCreate, ApplicationResponse, ApplicationUpdate,
    ApplicationSubmit, ApplicationApprove, ApplicationReject
)
from app.services.database import (
    create_application, get_application_by_id, get_applications_by_applicant,
    get_applications_for_approval, update_application, delete_application,
    submit_application, approve_application_step, reject_application_step
)
from app.models.models import User, UserRole, ApprovalStatus

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=ApplicationResponse)
async def create_new_application(
    application: ApplicationCreate, 
    current_user: User = Depends(get_current_user)
):
    new_application = create_application(
        form_id=application.form_id,
        route_id=application.route_id,
        applicant_id=current_user.id,
        form_data=application.form_data
    )
    
    return new_application


@router.get("/", response_model=List[ApplicationResponse])
async def read_applications(current_user: User = Depends(get_current_user)):
    applications = get_applications_by_applicant(current_user.id)
    
    return applications


@router.get("/for-approval", response_model=List[ApplicationResponse])
async def read_applications_for_approval(current_user: User = Depends(get_current_user)):
    applications = get_applications_for_approval(current_user.id)
    
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
async def read_application(application_id: str, current_user: User = Depends(get_current_user)):
    application = get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if (application.applicant_id != current_user.id and 
        current_user.role != UserRole.ADMIN):
        is_approver = False
        
        if not is_approver:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view this application"
            )
    
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application_info(
    application_id: str, 
    application_data: ApplicationUpdate, 
    current_user: User = Depends(get_current_user)
):
    application = get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if (application.applicant_id != current_user.id or 
        application.status != ApprovalStatus.DRAFT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this application or application is not in draft status"
        )
    
    update_data = application_data.dict(exclude_unset=True)
    updated_application = update_application(application_id, **update_data)
    
    return updated_application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application_item(application_id: str, current_user: User = Depends(get_current_user)):
    application = get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if (application.applicant_id != current_user.id or 
        application.status != ApprovalStatus.DRAFT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this application or application is not in draft status"
        )
    
    delete_application(application_id)
    
    return None


@router.post("/submit", response_model=ApplicationResponse)
async def submit_application_for_approval(
    submit_data: ApplicationSubmit,
    current_user: User = Depends(get_current_user)
):
    application = get_application_by_id(submit_data.application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if (application.applicant_id != current_user.id or 
        application.status != ApprovalStatus.DRAFT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to submit this application or application is not in draft status"
        )
    
    submitted_application = submit_application(submit_data.application_id)
    if not submitted_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to submit application"
        )
    
    return submitted_application


@router.post("/approve", response_model=ApplicationResponse)
async def approve_application(
    approve_data: ApplicationApprove,
    current_user: User = Depends(get_current_user)
):
    application = get_application_by_id(approve_data.application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    approved_application = approve_application_step(
        approve_data.application_id,
        current_user.id,
        approve_data.comment
    )
    
    if not approved_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to approve application or you are not the current approver"
        )
    
    return approved_application


@router.post("/reject", response_model=ApplicationResponse)
async def reject_application(
    reject_data: ApplicationReject,
    current_user: User = Depends(get_current_user)
):
    application = get_application_by_id(reject_data.application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    rejected_application = reject_application_step(
        reject_data.application_id,
        current_user.id,
        reject_data.comment
    )
    
    if not rejected_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reject application or you are not the current approver"
        )
    
    return rejected_application
