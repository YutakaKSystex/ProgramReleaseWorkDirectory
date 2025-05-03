import React, { useEffect, useState } from 'react';
import { getApplications, getApplicationsForApproval, submitApplication, approveApplication, rejectApplication, deleteApplication } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { ClipboardCheckIcon, TrashIcon, CheckIcon, XIcon } from 'lucide-react';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '../components/ui/dialog';
import { Textarea } from '../components/ui/textarea';

interface Application {
  id: string;
  form_id: string;
  form_name: string;
  route_id: string;
  route_name: string;
  applicant_id: string;
  applicant_name: string;
  status: string;
  current_step: number;
  created_at: string;
  updated_at: string;
  form_data: Record<string, any>;
  approval_history: Array<{
    step: number;
    approver_id: string;
    approver_name: string;
    status: string;
    comment: string;
    timestamp: string;
  }>;
}

export const Applications: React.FC = () => {
  const [myApplications, setMyApplications] = useState<Application[]>([]);
  const [pendingApprovals, setPendingApprovals] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('my-applications');
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [comment, setComment] = useState('');
  const [actionType, setActionType] = useState<'approve' | 'reject' | null>(null);

  useEffect(() => {
    if (activeTab === 'my-applications') {
      fetchMyApplications();
    } else {
      fetchPendingApprovals();
    }
  }, [activeTab]);

  const fetchMyApplications = async () => {
    try {
      setLoading(true);
      const data = await getApplications();
      setMyApplications(data as Application[]);
    } catch (error) {
      console.error('Error fetching my applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPendingApprovals = async () => {
    try {
      setLoading(true);
      const data = await getApplicationsForApproval();
      setPendingApprovals(data as Application[]);
    } catch (error) {
      console.error('Error fetching pending approvals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitApplication = async (applicationId: string) => {
    try {
      await submitApplication(applicationId);
      fetchMyApplications();
    } catch (error) {
      console.error('Error submitting application:', error);
    }
  };

  const handleDeleteApplication = async (applicationId: string) => {
    try {
      await deleteApplication(applicationId);
      fetchMyApplications();
    } catch (error) {
      console.error('Error deleting application:', error);
    }
  };

  const openApprovalDialog = (application: Application, type: 'approve' | 'reject') => {
    setSelectedApplication(application);
    setActionType(type);
    setComment('');
    setDialogOpen(true);
  };

  const handleApprovalAction = async () => {
    if (!selectedApplication || !actionType) return;

    try {
      if (actionType === 'approve') {
        await approveApplication(selectedApplication.id, comment);
      } else {
        await rejectApplication(selectedApplication.id, comment);
      }
      setDialogOpen(false);
      fetchPendingApprovals();
    } catch (error) {
      console.error(`Error ${actionType}ing application:`, error);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'DRAFT':
        return <Badge variant="outline">Draft</Badge>;
      case 'PENDING':
        return <Badge variant="secondary">Pending</Badge>;
      case 'APPROVED':
        return <Badge className="bg-green-100 text-green-800">Approved</Badge>;
      case 'REJECTED':
        return <Badge variant="destructive">Rejected</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  const renderApplications = (applications: Application[], isPendingApprovals = false) => {
    if (loading) {
      return <div className="text-center py-10">Loading applications...</div>;
    }

    if (applications.length === 0) {
      return (
        <div className="text-center py-10 text-gray-500">
          {isPendingApprovals
            ? 'No applications pending your approval.'
            : 'No applications found. Start a new application from the approval forms page.'}
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 gap-4">
        {applications.map((application) => (
          <Card key={application.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="flex items-center">
                    <ClipboardCheckIcon className="mr-2 h-5 w-5 text-blue-500" />
                    {application.form_name}
                  </CardTitle>
                  <CardDescription>
                    Route: {application.route_name} | Submitted: {new Date(application.created_at).toLocaleDateString()}
                  </CardDescription>
                </div>
                <div>{getStatusBadge(application.status)}</div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-gray-500">
                {isPendingApprovals ? (
                  <p>Applicant: {application.applicant_name}</p>
                ) : (
                  <p>Status: Step {application.current_step} of {application.approval_history.length}</p>
                )}
              </div>
            </CardContent>
            <CardFooter className="flex justify-end space-x-2">
              {isPendingApprovals ? (
                <>
                  <Button variant="outline" size="sm" onClick={() => openApprovalDialog(application, 'reject')}>
                    <XIcon className="mr-1 h-4 w-4" />
                    Reject
                  </Button>
                  <Button variant="default" size="sm" onClick={() => openApprovalDialog(application, 'approve')}>
                    <CheckIcon className="mr-1 h-4 w-4" />
                    Approve
                  </Button>
                </>
              ) : (
                <>
                  {application.status === 'DRAFT' && (
                    <>
                      <Button variant="outline" size="sm" onClick={() => handleDeleteApplication(application.id)}>
                        <TrashIcon className="mr-1 h-4 w-4" />
                        Delete
                      </Button>
                      <Button variant="default" size="sm" onClick={() => handleSubmitApplication(application.id)}>
                        Submit
                      </Button>
                    </>
                  )}
                </>
              )}
            </CardFooter>
          </Card>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Applications</h1>
        <p className="text-gray-500 mt-1">Manage your approval applications</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="my-applications">My Applications</TabsTrigger>
          <TabsTrigger value="pending-approvals">Pending Approvals</TabsTrigger>
        </TabsList>
        <TabsContent value="my-applications" className="mt-6">
          {renderApplications(myApplications)}
        </TabsContent>
        <TabsContent value="pending-approvals" className="mt-6">
          {renderApplications(pendingApprovals, true)}
        </TabsContent>
      </Tabs>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {actionType === 'approve' ? 'Approve Application' : 'Reject Application'}
            </DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <label htmlFor="comment" className="text-sm font-medium">
              Comment (Optional)
            </label>
            <Textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add a comment..."
              className="mt-2"
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant={actionType === 'approve' ? 'default' : 'destructive'}
              onClick={handleApprovalAction}
            >
              {actionType === 'approve' ? 'Approve' : 'Reject'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};
