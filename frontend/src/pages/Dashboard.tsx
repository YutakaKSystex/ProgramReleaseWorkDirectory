import React, { useEffect, useState } from 'react';
import { useAuth } from '../lib/auth-context';
import { getApplicationsForApproval, getApplications } from '../lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { useNavigate } from 'react-router';
import { ClipboardCheckIcon, FileIcon, FolderIcon, InboxIcon } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [pendingApprovals, setPendingApprovals] = useState(0);
  const [myApplications, setMyApplications] = useState(0);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const approvals = await getApplicationsForApproval();
        setPendingApprovals(approvals.length);
        
        const applications = await getApplications();
        setMyApplications(applications.length);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };
    
    fetchData();
  }, []);
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Welcome, {user?.full_name || user?.username}</h1>
        <p className="text-gray-500 mt-1">Here's an overview of your document management system</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">My Applications</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold">{myApplications}</div>
              <div className="p-2 bg-blue-100 rounded-full">
                <ClipboardCheckIcon className="h-5 w-5 text-blue-600" />
              </div>
            </div>
            <Button 
              variant="ghost" 
              className="w-full mt-4 justify-start text-blue-600"
              onClick={() => navigate('/applications')}
            >
              View all applications
            </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Pending Approvals</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold">{pendingApprovals}</div>
              <div className="p-2 bg-amber-100 rounded-full">
                <InboxIcon className="h-5 w-5 text-amber-600" />
              </div>
            </div>
            <Button 
              variant="ghost" 
              className="w-full mt-4 justify-start text-amber-600"
              onClick={() => navigate('/applications/for-approval')}
            >
              Review pending approvals
            </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Documents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold">-</div>
              <div className="p-2 bg-green-100 rounded-full">
                <FileIcon className="h-5 w-5 text-green-600" />
              </div>
            </div>
            <Button 
              variant="ghost" 
              className="w-full mt-4 justify-start text-green-600"
              onClick={() => navigate('/documents')}
            >
              Manage documents
            </Button>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-500">Folders</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold">-</div>
              <div className="p-2 bg-purple-100 rounded-full">
                <FolderIcon className="h-5 w-5 text-purple-600" />
              </div>
            </div>
            <Button 
              variant="ghost" 
              className="w-full mt-4 justify-start text-purple-600"
              onClick={() => navigate('/folders')}
            >
              Manage folders
            </Button>
          </CardContent>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Applications</CardTitle>
            <CardDescription>Your recently submitted applications</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center py-6 text-gray-500">
              No recent applications
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Pending Approvals</CardTitle>
            <CardDescription>Applications waiting for your approval</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center py-6 text-gray-500">
              No pending approvals
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
