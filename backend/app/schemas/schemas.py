from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field
from app.models.models import UserRole, FolderPermission, ApprovalStatus, FormFieldType


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class FolderAccessBase(BaseModel):
    user_id: str
    permission: FolderPermission


class FolderBase(BaseModel):
    name: str
    parent_id: Optional[str] = None


class FolderCreate(FolderBase):
    pass


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None


class FolderResponse(FolderBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    access_list: List[FolderAccessBase]


class DocumentBase(BaseModel):
    name: str
    folder_id: str
    file_type: str
    metadata: Dict[str, Any] = {}


class DocumentCreate(DocumentBase):
    file_content: bytes


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    folder_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(DocumentBase):
    id: str
    file_path: str
    file_size: int
    created_by: str
    created_at: datetime
    updated_at: datetime


class FormFieldBase(BaseModel):
    name: str
    label: str
    type: FormFieldType
    required: bool = False
    options: Optional[List[str]] = None
    default_value: Optional[Any] = None
    order: int


class FormFieldCreate(FormFieldBase):
    pass


class FormFieldUpdate(BaseModel):
    label: Optional[str] = None
    type: Optional[FormFieldType] = None
    required: Optional[bool] = None
    options: Optional[List[str]] = None
    default_value: Optional[Any] = None
    order: Optional[int] = None


class FormFieldResponse(FormFieldBase):
    id: str


class ApprovalFormBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_folder_id: Optional[str] = None


class ApprovalFormCreate(ApprovalFormBase):
    fields: List[FormFieldCreate] = []


class ApprovalFormUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_folder_id: Optional[str] = None
    fields: Optional[List[FormFieldCreate]] = None


class ApprovalFormResponse(ApprovalFormBase):
    id: str
    fields: List[FormFieldResponse]
    created_by: str
    created_at: datetime
    updated_at: datetime


class ApprovalStepBase(BaseModel):
    approver_id: str
    order: int


class ApprovalStepCreate(ApprovalStepBase):
    pass


class ApprovalStepUpdate(BaseModel):
    approver_id: Optional[str] = None
    status: Optional[ApprovalStatus] = None
    comment: Optional[str] = None
    order: Optional[int] = None


class ApprovalStepResponse(ApprovalStepBase):
    id: str
    status: ApprovalStatus
    comment: Optional[str] = None
    approved_at: Optional[datetime] = None


class ApprovalRouteBase(BaseModel):
    name: str
    description: Optional[str] = None


class ApprovalRouteCreate(ApprovalRouteBase):
    steps: List[ApprovalStepCreate] = []


class ApprovalRouteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[ApprovalStepCreate]] = None


class ApprovalRouteResponse(ApprovalRouteBase):
    id: str
    steps: List[ApprovalStepResponse]
    created_by: str
    created_at: datetime
    updated_at: datetime


class ApplicationBase(BaseModel):
    form_id: str
    route_id: str
    form_data: Dict[str, Any] = {}


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    form_data: Optional[Dict[str, Any]] = None


class ApplicationResponse(ApplicationBase):
    id: str
    applicant_id: str
    current_step: int
    status: ApprovalStatus
    document_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ApplicationSubmit(BaseModel):
    application_id: str


class ApplicationApprove(BaseModel):
    application_id: str
    comment: Optional[str] = None


class ApplicationReject(BaseModel):
    application_id: str
    comment: Optional[str] = None


class FormInitialize(BaseModel):
    form_id: str
    initial_values: Dict[str, Any]
