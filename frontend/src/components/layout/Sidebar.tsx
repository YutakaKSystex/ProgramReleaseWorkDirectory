import React from 'react';
import { useNavigate } from 'react-router';
import { useLocation } from 'react-router';
import { useAuth } from '../../lib/auth-context';
import { Button } from '../ui/button';
import { 
  FolderIcon, 
  FileTextIcon, 
  UsersIcon, 
  ClipboardListIcon, 
  GitBranchIcon,
  InboxIcon,
  LogOutIcon
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname.startsWith(path);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="h-screen w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold">Document Management</h1>
      </div>
      
      <div className="p-4 border-b border-gray-800">
        <div className="text-sm text-gray-400">Logged in as:</div>
        <div className="font-medium">{user?.full_name || user?.username}</div>
        <div className="text-xs text-gray-400">{user?.role}</div>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        <Button
          variant={isActive('/dashboard') ? "secondary" : "ghost"}
          className="w-full justify-start"
          onClick={() => navigate('/dashboard')}
        >
          <InboxIcon className="mr-2 h-4 w-4" />
          Dashboard
        </Button>
        
        <Button
          variant={isActive('/documents') ? "secondary" : "ghost"}
          className="w-full justify-start"
          onClick={() => navigate('/documents')}
        >
          <FileTextIcon className="mr-2 h-4 w-4" />
          Documents
        </Button>
        
        <Button
          variant={isActive('/folders') ? "secondary" : "ghost"}
          className="w-full justify-start"
          onClick={() => navigate('/folders')}
        >
          <FolderIcon className="mr-2 h-4 w-4" />
          Folders
        </Button>
        
        <Button
          variant={isActive('/applications') ? "secondary" : "ghost"}
          className="w-full justify-start"
          onClick={() => navigate('/applications')}
        >
          <ClipboardListIcon className="mr-2 h-4 w-4" />
          Applications
        </Button>
        
        <Button
          variant={isActive('/approval-routes') ? "secondary" : "ghost"}
          className="w-full justify-start"
          onClick={() => navigate('/approval-routes')}
        >
          <GitBranchIcon className="mr-2 h-4 w-4" />
          Approval Routes
        </Button>
        
        {user?.role === 'ADMIN' && (
          <Button
            variant={isActive('/users') ? "secondary" : "ghost"}
            className="w-full justify-start"
            onClick={() => navigate('/users')}
          >
            <UsersIcon className="mr-2 h-4 w-4" />
            Users
          </Button>
        )}
      </nav>
      
      <div className="p-4 border-t border-gray-800">
        <Button
          variant="ghost"
          className="w-full justify-start text-red-400 hover:text-red-300 hover:bg-red-900/20"
          onClick={handleLogout}
        >
          <LogOutIcon className="mr-2 h-4 w-4" />
          Logout
        </Button>
      </div>
    </div>
  );
};
