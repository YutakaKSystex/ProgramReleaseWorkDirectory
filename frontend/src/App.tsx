import React from 'react';
import { RouterProvider, createBrowserRouter, Navigate, RouteObject } from 'react-router-dom';
import { AuthProvider, useAuth } from './lib/auth-context';
import { Layout } from './components/layout/Layout';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Folders } from './pages/Folders';
import { Documents } from './pages/Documents';
import { ApprovalForms } from './pages/ApprovalForms';
import { ApprovalRoutes } from './pages/ApprovalRoutes';
import { Applications } from './pages/Applications';
import './App.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }
  
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  const routes: RouteObject[] = [
    {
      path: '/',
      element: <Navigate to="/login" replace />,
    },
    {
      path: '/login',
      element: (
        <PublicRoute>
          <Login />
        </PublicRoute>
      ),
    },
    {
      path: '/register',
      element: (
        <PublicRoute>
          <Register />
        </PublicRoute>
      ),
    },
    {
      path: '/',
      element: (
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      ),
      children: [
        {
          path: 'dashboard',
          element: <Dashboard />,
        },
        {
          path: 'folders',
          element: <Folders />,
        },
        {
          path: 'documents',
          element: <Documents />,
        },
        {
          path: 'approval-forms',
          element: <ApprovalForms />,
        },
        {
          path: 'approval-routes',
          element: <ApprovalRoutes />,
        },
        {
          path: 'applications',
          element: <Applications />,
        },
      ],
    },
  ];

  const router = createBrowserRouter(routes);

  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
