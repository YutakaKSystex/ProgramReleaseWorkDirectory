# Document Management System Implementation

## Overview
This pull request implements a complete document management system with electronic approval workflow and document storage capabilities.

## Features Implemented
- **Authentication System**
  - User login/registration with secure password handling
  - Role-based access control
  - JWT token authentication

- **Electronic Approval Workflow**
  - Approval route creation and management
  - Customizable application forms
  - Application submission and approval process
  - Automatic document storage in specified folders

- **Document Management**
  - User management (registration, modification, deletion)
  - Folder management with user permissions
  - Document storage with tree structure and search capabilities
  - Document upload, download, and deletion

- **API for Form Initialization**
  - Endpoint for setting initial values in application forms

## Technical Details
- **Frontend**: React with TypeScript, Tailwind CSS, shadcn/ui components
- **Backend**: FastAPI with JWT authentication
- **Database**: In-memory database for demonstration purposes

## Testing
All features have been manually tested and are working correctly:
- Authentication system works with admin/user accounts
- Electronic approval workflow functions properly
- Document management system allows organizing and accessing documents
- Form initialization API is implemented and functional

## Default Credentials
- Admin: username `admin`, password `password`
- User: username `user`, password `password`

## Link to Devin run
https://app.devin.ai/sessions/0eec708c856e485da9437c2cc09fbae3

## Requested by
yu-kobayashi@systex.co.jp
