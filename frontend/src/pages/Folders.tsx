import React, { useEffect, useState } from 'react';
import { getFolders, createFolder } from '../lib/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { FolderIcon, PlusIcon } from 'lucide-react';

interface Folder {
  id: string;
  name: string;
  created_by: string;
  created_at: string;
  parent_id: string | null;
}

export const Folders: React.FC = () => {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState(true);
  const [newFolderName, setNewFolderName] = useState('');
  const [currentParentId, setCurrentParentId] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    fetchFolders();
  }, [currentParentId]);

  const fetchFolders = async () => {
    try {
      setLoading(true);
      const data = await getFolders(currentParentId || undefined);
      setFolders(data as Folder[]);
    } catch (error) {
      console.error('Error fetching folders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFolder = async () => {
    if (!newFolderName.trim()) return;

    try {
      await createFolder({
        name: newFolderName,
        parent_id: currentParentId || undefined,
      });
      setNewFolderName('');
      setDialogOpen(false);
      fetchFolders();
    } catch (error) {
      console.error('Error creating folder:', error);
    }
  };

  const handleFolderClick = (folderId: string) => {
    setCurrentParentId(folderId);
  };

  const handleBackClick = () => {
    setCurrentParentId(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Folders</h1>
          <p className="text-gray-500 mt-1">Manage your document folders</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <PlusIcon className="mr-2 h-4 w-4" />
              New Folder
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Folder</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="name">Folder Name</label>
                <Input
                  id="name"
                  value={newFolderName}
                  onChange={(e) => setNewFolderName(e.target.value)}
                  placeholder="Enter folder name"
                />
              </div>
            </div>
            <Button onClick={handleCreateFolder}>Create Folder</Button>
          </DialogContent>
        </Dialog>
      </div>

      {currentParentId && (
        <Button variant="outline" onClick={handleBackClick}>
          Back to Parent Folder
        </Button>
      )}

      {loading ? (
        <div className="text-center py-10">Loading folders...</div>
      ) : folders.length === 0 ? (
        <div className="text-center py-10 text-gray-500">
          No folders found. Create a new folder to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {folders.map((folder) => (
            <Card
              key={folder.id}
              className="cursor-pointer hover:bg-gray-50 transition-colors"
              onClick={() => handleFolderClick(folder.id)}
            >
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center">
                  <FolderIcon className="mr-2 h-5 w-5 text-blue-500" />
                  {folder.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500">
                  Created: {new Date(folder.created_at).toLocaleDateString()}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
