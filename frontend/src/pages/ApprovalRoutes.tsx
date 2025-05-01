import React, { useEffect, useState } from 'react';
import { getApprovalRoutes, createApprovalRoute, deleteApprovalRoute } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { GitBranchIcon, PlusIcon, TrashIcon, PencilIcon } from 'lucide-react';
import { useNavigate } from 'react-router';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { getUsers } from '../lib/api';

interface ApprovalRoute {
  id: string;
  name: string;
  description: string;
  created_by: string;
  created_at: string;
  steps: Array<{
    step_number: number;
    approver_id: string;
    approver_name?: string;
  }>;
}

interface User {
  id: string;
  username: string;
  full_name?: string;
}

export const ApprovalRoutes: React.FC = () => {
  const [routes, setRoutes] = useState<ApprovalRoute[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [routeName, setRouteName] = useState('');
  const [routeDescription, setRouteDescription] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRoutes();
    fetchUsers();
  }, []);

  const fetchRoutes = async () => {
    try {
      setLoading(true);
      const data = await getApprovalRoutes();
      setRoutes(data);
    } catch (error) {
      console.error('Error fetching approval routes:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleCreateRoute = async () => {
    if (!routeName.trim()) return;

    try {
      await createApprovalRoute({
        name: routeName,
        description: routeDescription,
        steps: [],
      });
      setRouteName('');
      setRouteDescription('');
      setDialogOpen(false);
      fetchRoutes();
    } catch (error) {
      console.error('Error creating approval route:', error);
    }
  };

  const handleDeleteRoute = async (routeId: string) => {
    try {
      await deleteApprovalRoute(routeId);
      fetchRoutes();
    } catch (error) {
      console.error('Error deleting approval route:', error);
    }
  };

  const handleEditRoute = (routeId: string) => {
    navigate(`/approval-routes/${routeId}`);
  };

  const getUserName = (userId: string) => {
    const user = users.find(u => u.id === userId);
    return user ? (user.full_name || user.username) : 'Unknown User';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Approval Routes</h1>
          <p className="text-gray-500 mt-1">Manage your approval workflows</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <PlusIcon className="mr-2 h-4 w-4" />
              New Route
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Approval Route</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Route Name</Label>
                <Input
                  id="name"
                  value={routeName}
                  onChange={(e) => setRouteName(e.target.value)}
                  placeholder="Enter route name"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={routeDescription}
                  onChange={(e) => setRouteDescription(e.target.value)}
                  placeholder="Enter route description"
                />
              </div>
            </div>
            <Button onClick={handleCreateRoute} disabled={!routeName.trim()}>
              Create Route
            </Button>
          </DialogContent>
        </Dialog>
      </div>

      {loading ? (
        <div className="text-center py-10">Loading approval routes...</div>
      ) : routes.length === 0 ? (
        <div className="text-center py-10 text-gray-500">
          No approval routes found. Create a new route to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {routes.map((route) => (
            <Card key={route.id}>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <GitBranchIcon className="mr-2 h-5 w-5 text-blue-500" />
                  {route.name}
                </CardTitle>
                <CardDescription>{route.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-500">
                  <p>Steps: {route.steps.length}</p>
                  <p>Created: {new Date(route.created_at).toLocaleDateString()}</p>
                </div>
                {route.steps.length > 0 && (
                  <div className="mt-4">
                    <h4 className="text-sm font-medium mb-2">Approval Flow:</h4>
                    <div className="space-y-2">
                      {route.steps.map((step, index) => (
                        <div key={index} className="flex items-center">
                          <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-medium">
                            {step.step_number}
                          </div>
                          <div className="ml-2">{getUserName(step.approver_id)}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
              <CardFooter className="flex justify-end space-x-2">
                <Button variant="outline" size="sm" onClick={() => handleEditRoute(route.id)}>
                  <PencilIcon className="mr-1 h-4 w-4" />
                  Edit
                </Button>
                <Button variant="outline" size="sm" onClick={() => handleDeleteRoute(route.id)}>
                  <TrashIcon className="mr-1 h-4 w-4" />
                  Delete
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
