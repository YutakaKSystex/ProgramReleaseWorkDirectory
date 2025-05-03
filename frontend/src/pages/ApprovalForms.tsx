import React, { useEffect, useState } from 'react';
import { getApprovalForms, createApprovalForm, deleteApprovalForm } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { ClipboardIcon, PlusIcon, TrashIcon, PencilIcon } from 'lucide-react';
import { useNavigate } from 'react-router';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { getFolders } from '../lib/api';

interface ApprovalForm {
  id: string;
  name: string;
  description: string;
  created_by: string;
  created_at: string;
  fields: Array<{
    id: string;
    name: string;
    type: string;
    required: boolean;
    options?: string[];
  }>;
  target_folder_id: string | null;
}

interface Folder {
  id: string;
  name: string;
}

export const ApprovalForms: React.FC = () => {
  const [forms, setForms] = useState<ApprovalForm[]>([]);
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState(true);
  const [formName, setFormName] = useState('');
  const [formDescription, setFormDescription] = useState('');
  const [targetFolderId, setTargetFolderId] = useState<string>('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchForms();
    fetchFolders();
  }, []);

  const fetchForms = async () => {
    try {
      setLoading(true);
      const data = await getApprovalForms();
      setForms(data as ApprovalForm[]);
    } catch (error) {
      console.error('Error fetching approval forms:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFolders = async () => {
    try {
      const data = await getFolders();
      const folderData = data as Folder[];
      setFolders(folderData);
      if (folderData.length > 0 && !targetFolderId) {
        setTargetFolderId(folderData[0].id);
      }
    } catch (error) {
      console.error('Error fetching folders:', error);
    }
  };

  const handleCreateForm = async () => {
    if (!formName.trim()) return;

    try {
      await createApprovalForm({
        name: formName,
        description: formDescription,
        fields: [],
        target_folder_id: targetFolderId || null,
      });
      setFormName('');
      setFormDescription('');
      setDialogOpen(false);
      fetchForms();
    } catch (error) {
      console.error('Error creating approval form:', error);
    }
  };

  const handleDeleteForm = async (formId: string) => {
    try {
      await deleteApprovalForm(formId);
      fetchForms();
    } catch (error) {
      console.error('Error deleting approval form:', error);
    }
  };

  const handleEditForm = (formId: string) => {
    navigate(`/approval-forms/${formId}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Approval Forms</h1>
          <p className="text-gray-500 mt-1">Manage your approval forms</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <PlusIcon className="mr-2 h-4 w-4" />
              New Form
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Approval Form</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Form Name</Label>
                <Input
                  id="name"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  placeholder="Enter form name"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formDescription}
                  onChange={(e) => setFormDescription(e.target.value)}
                  placeholder="Enter form description"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="folder">Target Folder (for approved documents)</Label>
                <Select value={targetFolderId} onValueChange={setTargetFolderId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a folder" />
                  </SelectTrigger>
                  <SelectContent>
                    {folders.map((folder) => (
                      <SelectItem key={folder.id} value={folder.id}>
                        {folder.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <Button onClick={handleCreateForm} disabled={!formName.trim()}>
              Create Form
            </Button>
          </DialogContent>
        </Dialog>
      </div>

      {loading ? (
        <div className="text-center py-10">Loading approval forms...</div>
      ) : forms.length === 0 ? (
        <div className="text-center py-10 text-gray-500">
          No approval forms found. Create a new form to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {forms.map((form) => (
            <Card key={form.id}>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ClipboardIcon className="mr-2 h-5 w-5 text-blue-500" />
                  {form.name}
                </CardTitle>
                <CardDescription>{form.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-500">
                  <p>Fields: {form.fields.length}</p>
                  <p>Created: {new Date(form.created_at).toLocaleDateString()}</p>
                </div>
              </CardContent>
              <CardFooter className="flex justify-end space-x-2">
                <Button variant="outline" size="sm" onClick={() => handleEditForm(form.id)}>
                  <PencilIcon className="mr-1 h-4 w-4" />
                  Edit
                </Button>
                <Button variant="outline" size="sm" onClick={() => handleDeleteForm(form.id)}>
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
