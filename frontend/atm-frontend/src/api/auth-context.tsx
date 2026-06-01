/**
 * Auth context and provider for the frontend.
 *
 * Provides login/logout state and exposes the auth API client functions.
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { auth, isAuthenticated, logout as doLogout } from '@/api/auth-client';

interface AuthUser {
  id: string;
  username: string;
  email: string | null;
}

interface AuthContextValue {
  user: AuthUser | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // On mount, if we have stored tokens, try to fetch user info
  useEffect(() => {
    async function init() {
      if (!isAuthenticated()) {
        setIsLoading(false);
        return;
      }

      try {
        const me = await auth.getMe();
        setUser(me);
      } catch {
        // Token is invalid/expired — clear it
        doLogout();
      } finally {
        setIsLoading(false);
      }
    }

    init();
  }, []);

  // Listen for forced-logout events (e.g., from the token refresh interceptor)
  useEffect(() => {
    function handleLogout() {
      setUser(null);
    }
    window.addEventListener('bp:auth:logout', handleLogout);
    return () => window.removeEventListener('bp:auth:logout', handleLogout);
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    await auth.login(username, password);
    const me = await auth.getMe();
    setUser(me);
  }, []);

  const logout = useCallback(() => {
    doLogout();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoggedIn: !!user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}
