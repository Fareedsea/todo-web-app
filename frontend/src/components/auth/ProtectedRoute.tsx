'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';

interface ProtectedRouteProps {
  children: ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isLoggedIn) {
      // Redirect to login if not authenticated
      router.push('/auth');
    }
  }, [isLoggedIn, isLoading, router]);

  // Show nothing while checking authentication status
  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  // Render children only if user is authenticated
  if (isLoggedIn) {
    return <>{children}</>;
  }

  // Return null if not authenticated (redirect effect will handle navigation)
  return null;
};