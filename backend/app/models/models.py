from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class FolderPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


class FolderAccess(BaseModel):
    user_id: str
    permission: FolderPermission


class Folder(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    access_list: List[FolderAccess] = []


class Document(BaseModel):
    id: str
    name: str
    folder_id: str
    file_path: str
    file_type: str
    file_size: int
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}


class FormFieldType(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    DATE = "date"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    FILE = "file"


class FormField(BaseModel):
    id: str
    name: str
    label: str
    type: FormFieldType
    required: bool = False
    options: Optional[List[str]] = None
    default_value: Optional[Any] = None
    order: int


class ApprovalForm(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    fields: List[FormField] = []
    created_by: str
    target_folder_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ApprovalStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELED = "canceled"


class ApprovalStep(BaseModel):
    id: str
    approver_id: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    comment: Optional[str] = None
    approved_at: Optional[datetime] = None
    order: int


class ApprovalRoute(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    steps: List[ApprovalStep] = []
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Application(BaseModel):
    id: str
    form_id: str
    route_id: str
    applicant_id: str
    current_step: int = 0
    status: ApprovalStatus = ApprovalStatus.DRAFT
    form_data: Dict[str, Any] = {}
    document_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
