import React, { useEffect, useState } from 'react';
import { getDocuments, uploadDocument, deleteDocument } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { FileIcon, PlusIcon, TrashIcon, DownloadIcon } from 'lucide-react';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { getFolders } from '../lib/api';

interface Document {
  id: string;
  name: string;
  folder_id: string;
  file_path: string;
  file_type: string;
  file_size: number;
  created_by: string;
  created_at: string;
  metadata: Record<string, any>;
}

interface Folder {
  id: string;
  name: string;
}

export const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedFolderId, setSelectedFolderId] = useState<string>('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [currentFolderId, setCurrentFolderId] = useState<string | null>(null);

  useEffect(() => {
    fetchDocuments();
    fetchFolders();
  }, [currentFolderId]);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const data = await getDocuments(currentFolderId || undefined);
      setDocuments(data as Document[]);
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFolders = async () => {
    try {
      const data = await getFolders();
      const folderData = data as Folder[];
      setFolders(folderData);
      if (folderData.length > 0 && !selectedFolderId) {
        setSelectedFolderId(folderData[0].id);
      }
    } catch (error) {
      console.error('Error fetching folders:', error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !selectedFolderId) return;

    try {
      await uploadDocument(selectedFile, selectedFolderId);
      setSelectedFile(null);
      setDialogOpen(false);
      fetchDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
    }
  };

  const handleDelete = async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      fetchDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Documents</h1>
          <p className="text-gray-500 mt-1">Manage your documents</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <PlusIcon className="mr-2 h-4 w-4" />
              Upload Document
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Upload New Document</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="folder">Select Folder</Label>
                <Select value={selectedFolderId} onValueChange={setSelectedFolderId}>
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
              <div className="grid gap-2">
                <Label htmlFor="file">Document File</Label>
                <Input id="file" type="file" onChange={handleFileChange} />
              </div>
            </div>
            <Button onClick={handleUpload} disabled={!selectedFile || !selectedFolderId}>
              Upload Document
            </Button>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-4">
        <Label>Filter by Folder</Label>
        <Select value={currentFolderId || 'all'} onValueChange={(value) => setCurrentFolderId(value === 'all' ? null : value)}>
          <SelectTrigger>
            <SelectValue placeholder="All Folders" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Folders</SelectItem>
            {folders.map((folder) => (
              <SelectItem key={folder.id} value={folder.id}>
                {folder.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {loading ? (
        <div className="text-center py-10">Loading documents...</div>
      ) : documents.length === 0 ? (
        <div className="text-center py-10 text-gray-500">
          No documents found. Upload a document to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {documents.map((document) => (
            <Card key={document.id} className="overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center text-base">
                  <FileIcon className="mr-2 h-5 w-5 text-blue-500" />
                  {document.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-500 space-y-1">
                  <p>Size: {formatFileSize(document.file_size)}</p>
                  <p>Type: {document.file_type}</p>
                  <p>Created: {new Date(document.created_at).toLocaleDateString()}</p>
                </div>
                <div className="flex space-x-2 mt-4">
                  <Button variant="outline" size="sm" asChild>
                    <a href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${document.file_path.replace('uploads', '/uploads')}`} target="_blank" rel="noopener noreferrer">
                      <DownloadIcon className="mr-1 h-4 w-4" />
                      Download
                    </a>
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => handleDelete(document.id)}>
                    <TrashIcon className="mr-1 h-4 w-4" />
                    Delete
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
