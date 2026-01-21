/**
 * Zustand store for authentication state management
 * Manages user info, tokens, and authentication actions
 */

import { create } from 'zustand';
import { apiClient } from '@/lib/api';

interface AuthStore {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  signup: (email: string, password: string) => Promise<void>;
  signin: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  isAuthenticated: false,
  isLoading: false,
  error: null,

  signup: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.signup({ email, password });
      set({ isAuthenticated: true, isLoading: false });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Signup failed';
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  signin: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.signin({ email, password });
      set({ isAuthenticated: true, isLoading: false });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Signin failed';
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  logout: () => {
    apiClient.logout();
    set({ isAuthenticated: false, error: null });
  },

  clearError: () => {
    set({ error: null });
  },

  checkAuth: () => {
    const isAuth = apiClient.isAuthenticated();
    set({ isAuthenticated: isAuth });
  },
}));
