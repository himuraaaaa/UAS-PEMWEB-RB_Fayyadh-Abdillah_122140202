import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, useLocation, Outlet } from 'react-router-dom';

const RequireAuth = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to={`/login?redirect=${location.pathname}`} replace />;
  }

  return <Outlet />;
};

export default RequireAuth;
