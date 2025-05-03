"""
In-memory database service for the document management system.
This is a simplified implementation for development purposes.
In a production environment, you would use a real database.
"""

from typing import Dict, List, Optional, Any
from uuid import uuid4
from datetime import datetime
from app.models.models import (
    User, Folder, Document, ApprovalForm, ApprovalRoute, 
    Application, UserRole, FolderPermission, FolderAccess,
    ApprovalStatus, ApprovalStep, FormField
)

users: Dict[str, User] = {}
folders: Dict[str, Folder] = {}
documents: Dict[str, Document] = {}
approval_forms: Dict[str, ApprovalForm] = {}
approval_routes: Dict[str, ApprovalRoute] = {}
applications: Dict[str, Application] = {}


def create_user(username: str, email: str, hashed_password: str, full_name: Optional[str] = None, 
                role: UserRole = UserRole.USER) -> User:
    user_id = str(uuid4())
    user = User(
        id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role
    )
    users[user_id] = user
    return user


def get_user_by_id(user_id: str) -> Optional[User]:
    return users.get(user_id)


def get_user_by_username(username: str) -> Optional[User]:
    for user in users.values():
        if user.username == username:
            return user
    return None


def get_user_by_email(email: str) -> Optional[User]:
    for user in users.values():
        if user.email == email:
            return user
    return None


def get_all_users() -> List[User]:
    return list(users.values())


def update_user(user_id: str, **kwargs) -> Optional[User]:
    user = users.get(user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    user.updated_at = datetime.now()
    users[user_id] = user
    return user


def delete_user(user_id: str) -> bool:
    if user_id in users:
        del users[user_id]
        return True
    return False


def create_folder(name: str, created_by: str, parent_id: Optional[str] = None) -> Folder:
    folder_id = str(uuid4())
    folder = Folder(
        id=folder_id,
        name=name,
        parent_id=parent_id,
        created_by=created_by,
        access_list=[FolderAccess(user_id=created_by, permission=FolderPermission.ADMIN)]
    )
    folders[folder_id] = folder
    return folder


def get_folder_by_id(folder_id: str) -> Optional[Folder]:
    return folders.get(folder_id)


def get_folders_by_parent(parent_id: Optional[str]) -> List[Folder]:
    return [folder for folder in folders.values() if folder.parent_id == parent_id]


def get_user_accessible_folders(user_id: str) -> List[Folder]:
    return [
        folder for folder in folders.values() 
        if any(access.user_id == user_id for access in folder.access_list)
    ]


def update_folder(folder_id: str, **kwargs) -> Optional[Folder]:
    folder = folders.get(folder_id)
    if not folder:
        return None
    
    for key, value in kwargs.items():
        if hasattr(folder, key):
            setattr(folder, key, value)
    
    folder.updated_at = datetime.now()
    folders[folder_id] = folder
    return folder


def delete_folder(folder_id: str) -> bool:
    if folder_id in folders:
        del folders[folder_id]
        return True
    return False


def add_folder_access(folder_id: str, user_id: str, permission: FolderPermission) -> Optional[Folder]:
    folder = folders.get(folder_id)
    if not folder:
        return None
    
    folder.access_list = [access for access in folder.access_list if access.user_id != user_id]
    
    folder.access_list.append(FolderAccess(user_id=user_id, permission=permission))
    folder.updated_at = datetime.now()
    folders[folder_id] = folder
    return folder


def remove_folder_access(folder_id: str, user_id: str) -> Optional[Folder]:
    folder = folders.get(folder_id)
    if not folder:
        return None
    
    folder.access_list = [access for access in folder.access_list if access.user_id != user_id]
    folder.updated_at = datetime.now()
    folders[folder_id] = folder
    return folder


def create_document(name: str, folder_id: str, file_path: str, file_type: str, 
                   file_size: int, created_by: str, metadata: Dict[str, Any] = None) -> Document:
    document_id = str(uuid4())
    document = Document(
        id=document_id,
        name=name,
        folder_id=folder_id,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        created_by=created_by,
        metadata=metadata or {}
    )
    documents[document_id] = document
    return document


def get_document_by_id(document_id: str) -> Optional[Document]:
    return documents.get(document_id)


def get_documents_by_folder(folder_id: str) -> List[Document]:
    return [doc for doc in documents.values() if doc.folder_id == folder_id]


def get_documents_by_user(user_id: str) -> List[Document]:
    user_folders = get_user_accessible_folders(user_id)
    folder_ids = [folder.id for folder in user_folders]
    return [doc for doc in documents.values() if doc.folder_id in folder_ids]


def update_document(document_id: str, **kwargs) -> Optional[Document]:
    document = documents.get(document_id)
    if not document:
        return None
    
    for key, value in kwargs.items():
        if hasattr(document, key):
            setattr(document, key, value)
    
    document.updated_at = datetime.now()
    documents[document_id] = document
    return document


def delete_document(document_id: str) -> bool:
    if document_id in documents:
        del documents[document_id]
        return True
    return False


def create_approval_form(name: str, created_by: str, description: Optional[str] = None, 
                         fields: List[FormField] = None, target_folder_id: Optional[str] = None) -> ApprovalForm:
    form_id = str(uuid4())
    form = ApprovalForm(
        id=form_id,
        name=name,
        description=description,
        fields=fields or [],
        created_by=created_by,
        target_folder_id=target_folder_id
    )
    approval_forms[form_id] = form
    return form


def get_approval_form_by_id(form_id: str) -> Optional[ApprovalForm]:
    return approval_forms.get(form_id)


def get_all_approval_forms() -> List[ApprovalForm]:
    return list(approval_forms.values())


def update_approval_form(form_id: str, **kwargs) -> Optional[ApprovalForm]:
    form = approval_forms.get(form_id)
    if not form:
        return None
    
    for key, value in kwargs.items():
        if hasattr(form, key):
            setattr(form, key, value)
    
    form.updated_at = datetime.now()
    approval_forms[form_id] = form
    return form


def delete_approval_form(form_id: str) -> bool:
    if form_id in approval_forms:
        del approval_forms[form_id]
        return True
    return False


def create_approval_route(name: str, created_by: str, description: Optional[str] = None, 
                         steps: List[ApprovalStep] = None) -> ApprovalRoute:
    route_id = str(uuid4())
    route = ApprovalRoute(
        id=route_id,
        name=name,
        description=description,
        steps=steps or [],
        created_by=created_by
    )
    approval_routes[route_id] = route
    return route


def get_approval_route_by_id(route_id: str) -> Optional[ApprovalRoute]:
    return approval_routes.get(route_id)


def get_all_approval_routes() -> List[ApprovalRoute]:
    return list(approval_routes.values())


def update_approval_route(route_id: str, **kwargs) -> Optional[ApprovalRoute]:
    route = approval_routes.get(route_id)
    if not route:
        return None
    
    for key, value in kwargs.items():
        if hasattr(route, key):
            setattr(route, key, value)
    
    route.updated_at = datetime.now()
    approval_routes[route_id] = route
    return route


def delete_approval_route(route_id: str) -> bool:
    if route_id in approval_routes:
        del approval_routes[route_id]
        return True
    return False


def create_application(form_id: str, route_id: str, applicant_id: str, 
                      form_data: Dict[str, Any] = None) -> Application:
    application_id = str(uuid4())
    application = Application(
        id=application_id,
        form_id=form_id,
        route_id=route_id,
        applicant_id=applicant_id,
        form_data=form_data or {},
        status=ApprovalStatus.DRAFT
    )
    applications[application_id] = application
    return application


def get_application_by_id(application_id: str) -> Optional[Application]:
    return applications.get(application_id)


def get_applications_by_applicant(applicant_id: str) -> List[Application]:
    return [app for app in applications.values() if app.applicant_id == applicant_id]


def get_applications_for_approval(approver_id: str) -> List[Application]:
    result = []
    for app in applications.values():
        if app.status == ApprovalStatus.PENDING:
            route = approval_routes.get(app.route_id)
            if route and app.current_step < len(route.steps):
                step = route.steps[app.current_step]
                if step.approver_id == approver_id and step.status == ApprovalStatus.PENDING:
                    result.append(app)
    return result


def update_application(application_id: str, **kwargs) -> Optional[Application]:
    application = applications.get(application_id)
    if not application:
        return None
    
    for key, value in kwargs.items():
        if hasattr(application, key):
            setattr(application, key, value)
    
    application.updated_at = datetime.now()
    applications[application_id] = application
    return application


def delete_application(application_id: str) -> bool:
    if application_id in applications:
        del applications[application_id]
        return True
    return False


def submit_application(application_id: str) -> Optional[Application]:
    application = applications.get(application_id)
    if not application or application.status != ApprovalStatus.DRAFT:
        return None
    
    application.status = ApprovalStatus.PENDING
    application.updated_at = datetime.now()
    applications[application_id] = application
    return application


def approve_application_step(application_id: str, approver_id: str, comment: Optional[str] = None) -> Optional[Application]:
    application = applications.get(application_id)
    if not application or application.status != ApprovalStatus.PENDING:
        return None
    
    route = approval_routes.get(application.route_id)
    if not route or application.current_step >= len(route.steps):
        return None
    
    current_step = route.steps[application.current_step]
    if current_step.approver_id != approver_id:
        return None
    
    current_step.status = ApprovalStatus.APPROVED
    current_step.comment = comment
    current_step.approved_at = datetime.now()
    route.steps[application.current_step] = current_step
    
    application.current_step += 1
    if application.current_step >= len(route.steps):
        application.status = ApprovalStatus.APPROVED
        
        form = approval_forms.get(application.form_id)
        if form and form.target_folder_id:
            document = create_document(
                name=f"Application {application.id}",
                folder_id=form.target_folder_id,
                file_path=f"/applications/{application.id}.pdf",  # This would be a real file path in production
                file_type="application/pdf",
                file_size=0,  # This would be the real file size in production
                created_by=application.applicant_id,
                metadata={"application_id": application.id, "form_data": application.form_data}
            )
            application.document_id = document.id
    
    application.updated_at = datetime.now()
    applications[application_id] = application
    approval_routes[route.id] = route
    
    return application


def reject_application_step(application_id: str, approver_id: str, comment: Optional[str] = None) -> Optional[Application]:
    application = applications.get(application_id)
    if not application or application.status != ApprovalStatus.PENDING:
        return None
    
    route = approval_routes.get(application.route_id)
    if not route or application.current_step >= len(route.steps):
        return None
    
    current_step = route.steps[application.current_step]
    if current_step.approver_id != approver_id:
        return None
    
    current_step.status = ApprovalStatus.REJECTED
    current_step.comment = comment
    current_step.approved_at = datetime.now()
    route.steps[application.current_step] = current_step
    
    application.status = ApprovalStatus.REJECTED
    application.updated_at = datetime.now()
    
    applications[application_id] = application
    approval_routes[route.id] = route
    
    return application


def init_data():
    from app.utils.auth import get_password_hash
    
    admin = create_user(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Admin User",
        role=UserRole.ADMIN
    )
    
    user = create_user(
        username="user",
        email="user@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Regular User",
        role=UserRole.USER
    )
    
    root_folder = create_folder(
        name="Root",
        created_by=admin.id
    )
    
    add_folder_access(root_folder.id, user.id, FolderPermission.READ)
    
    documents_folder = create_folder(
        name="Documents",
        created_by=admin.id,
        parent_id=root_folder.id
    )
    
    applications_folder = create_folder(
        name="Applications",
        created_by=admin.id,
        parent_id=root_folder.id
    )
    
    create_document(
        name="Sample Document.pdf",
        folder_id=documents_folder.id,
        file_path="/documents/sample.pdf",
        file_type="application/pdf",
        file_size=1024,
        created_by=admin.id,
        metadata={"description": "Sample document for testing"}
    )
    
    form = create_approval_form(
        name="Expense Report",
        created_by=admin.id,
        description="Form for submitting expense reports",
        target_folder_id=applications_folder.id,
        fields=[
            FormField(
                id=str(uuid4()),
                name="amount",
                label="Amount",
                type="number",
                required=True,
                order=1
            ),
            FormField(
                id=str(uuid4()),
                name="description",
                label="Description",
                type="textarea",
                required=True,
                order=2
            ),
            FormField(
                id=str(uuid4()),
                name="receipt",
                label="Receipt",
                type="file",
                required=True,
                order=3
            )
        ]
    )
    
    route = create_approval_route(
        name="Manager Approval",
        created_by=admin.id,
        description="Route for manager approval",
        steps=[
            ApprovalStep(
                id=str(uuid4()),
                approver_id=admin.id,
                status=ApprovalStatus.PENDING,
                order=1
            )
        ]
    )
    
    create_application(
        form_id=form.id,
        route_id=route.id,
        applicant_id=user.id,
        form_data={
            "amount": 100.0,
            "description": "Office supplies",
            "receipt": "/uploads/receipt.jpg"
        }
    )


init_data()
