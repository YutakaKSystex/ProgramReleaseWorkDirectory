import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => Promise.reject(error)
);

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post('/token', formData);
  return response.data;
};

export const register = async (userData: {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}) => {
  const response = await api.post('/register', userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/me');
  return response.data;
};

export const getUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};

export const getUser = async (userId: string) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export const updateUser = async (userId: string, userData: any) => {
  const response = await api.put(`/users/${userId}`, userData);
  return response.data;
};

export const deleteUser = async (userId: string) => {
  const response = await api.delete(`/users/${userId}`);
  return response.data;
};

export const getFolders = async (parentId?: string) => {
  const url = parentId ? `/folders?parent_id=${parentId}` : '/folders';
  const response = await api.get(url);
  return response.data;
};

export const getFolder = async (folderId: string) => {
  const response = await api.get(`/folders/${folderId}`);
  return response.data;
};

export const createFolder = async (folderData: { name: string; parent_id?: string }) => {
  const response = await api.post('/folders', folderData);
  return response.data;
};

export const updateFolder = async (folderId: string, folderData: any) => {
  const response = await api.put(`/folders/${folderId}`, folderData);
  return response.data;
};

export const deleteFolder = async (folderId: string) => {
  const response = await api.delete(`/folders/${folderId}`);
  return response.data;
};

export const addFolderAccess = async (folderId: string, accessData: { user_id: string; permission: string }) => {
  const response = await api.post(`/folders/${folderId}/access`, accessData);
  return response.data;
};

export const removeFolderAccess = async (folderId: string, userId: string) => {
  const response = await api.delete(`/folders/${folderId}/access/${userId}`);
  return response.data;
};

export const getDocuments = async (folderId?: string) => {
  const url = folderId ? `/documents?folder_id=${folderId}` : '/documents';
  const response = await api.get(url);
  return response.data;
};

export const getDocument = async (documentId: string) => {
  const response = await api.get(`/documents/${documentId}`);
  return response.data;
};

export const uploadDocument = async (file: File, folderId: string, metadata?: any) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder_id', folderId);
  
  if (metadata) {
    formData.append('metadata', JSON.stringify(metadata));
  }
  
  const response = await api.post('/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const updateDocument = async (documentId: string, documentData: any) => {
  const response = await api.put(`/documents/${documentId}`, documentData);
  return response.data;
};

export const deleteDocument = async (documentId: string) => {
  const response = await api.delete(`/documents/${documentId}`);
  return response.data;
};

export const getApprovalForms = async () => {
  const response = await api.get('/approval-forms');
  return response.data;
};

export const getApprovalForm = async (formId: string) => {
  const response = await api.get(`/approval-forms/${formId}`);
  return response.data;
};

export const createApprovalForm = async (formData: any) => {
  const response = await api.post('/approval-forms', formData);
  return response.data;
};

export const updateApprovalForm = async (formId: string, formData: any) => {
  const response = await api.put(`/approval-forms/${formId}`, formData);
  return response.data;
};

export const deleteApprovalForm = async (formId: string) => {
  const response = await api.delete(`/approval-forms/${formId}`);
  return response.data;
};

export const initializeForm = async (formId: string, initialValues: any) => {
  const response = await api.post('/approval-forms/initialize', {
    form_id: formId,
    initial_values: initialValues,
  });
  return response.data;
};

export const getApprovalRoutes = async () => {
  const response = await api.get('/approval-routes');
  return response.data;
};

export const getApprovalRoute = async (routeId: string) => {
  const response = await api.get(`/approval-routes/${routeId}`);
  return response.data;
};

export const createApprovalRoute = async (routeData: any) => {
  const response = await api.post('/approval-routes', routeData);
  return response.data;
};

export const updateApprovalRoute = async (routeId: string, routeData: any) => {
  const response = await api.put(`/approval-routes/${routeId}`, routeData);
  return response.data;
};

export const deleteApprovalRoute = async (routeId: string) => {
  const response = await api.delete(`/approval-routes/${routeId}`);
  return response.data;
};

export const getApplications = async () => {
  const response = await api.get('/applications');
  return response.data;
};

export const getApplicationsForApproval = async () => {
  const response = await api.get('/applications/for-approval');
  return response.data;
};

export const getApplication = async (applicationId: string) => {
  const response = await api.get(`/applications/${applicationId}`);
  return response.data;
};

export const createApplication = async (applicationData: any) => {
  const response = await api.post('/applications', applicationData);
  return response.data;
};

export const updateApplication = async (applicationId: string, applicationData: any) => {
  const response = await api.put(`/applications/${applicationId}`, applicationData);
  return response.data;
};

export const deleteApplication = async (applicationId: string) => {
  const response = await api.delete(`/applications/${applicationId}`);
  return response.data;
};

export const submitApplication = async (applicationId: string) => {
  const response = await api.post('/applications/submit', { application_id: applicationId });
  return response.data;
};

export const approveApplication = async (applicationId: string, comment?: string) => {
  const response = await api.post('/applications/approve', { 
    application_id: applicationId,
    comment
  });
  return response.data;
};

export const rejectApplication = async (applicationId: string, comment?: string) => {
  const response = await api.post('/applications/reject', { 
    application_id: applicationId,
    comment
  });
  return response.data;
};
