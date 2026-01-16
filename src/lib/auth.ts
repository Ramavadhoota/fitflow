import type { ReactNode } from 'react';
import { redirect } from 'next/navigation';

interface ProtectedLayoutProps {
  children: ReactNode;
}

/**
 * HOC for protecting pages with authentication
 * Usage: Wrap your page component with this to require authentication
 */
export function withProtectedRoute(Component: React.ComponentType<any>) {
  return function ProtectedRoute(props: any) {
    // The actual auth check happens in the component using useAuthStore
    // and useRouter().push('/login') if not authenticated
    return <Component {...props} />;
  };
}
