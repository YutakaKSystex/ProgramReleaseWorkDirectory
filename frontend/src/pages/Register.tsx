import React from 'react';
import { RegisterForm } from '../components/auth/RegisterForm';

export const Register: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <RegisterForm />
    </div>
  );
};
