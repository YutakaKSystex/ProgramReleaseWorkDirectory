import React from 'react';
import { useAuth } from '../../lib/auth-context';
import { Button } from '../ui/button';
import { BellIcon, SearchIcon } from 'lucide-react';
import { Input } from '../ui/input';

export const Header: React.FC = () => {
  const { user } = useAuth();

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <div className="flex items-center">
        <h1 className="text-xl font-semibold text-gray-800">Document Management System</h1>
      </div>
      
      <div className="flex items-center space-x-4">
        <div className="relative">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input 
            className="pl-10 w-64" 
            placeholder="Search documents..." 
          />
        </div>
        
        <Button variant="ghost" size="icon">
          <BellIcon className="h-5 w-5" />
        </Button>
        
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700 font-semibold">
            {user?.username?.charAt(0).toUpperCase()}
          </div>
          <span className="text-sm font-medium">{user?.full_name || user?.username}</span>
        </div>
      </div>
    </header>
  );
};
