---
name: api-client
description: Build type-safe API client with automatic JWT token attachment and error handling. Use when creating frontend data fetching layer.
---

# API Client Skill - JWT-Authenticated API Wrapper

## Instructions

Create a centralized, type-safe API client for frontend that automatically manages JWT tokens, handles errors, and provides typed endpoints for task management.

### 1. **Client Configuration**
   - Base URL from environment: `NEXT_PUBLIC_API_URL`
   - Default headers (Content-Type: application/json)
   - Axios or Fetch-based HTTP client
   - Request interceptors for token injection
   - Response interceptors for error handling
   - Request timeout (30 seconds)
   - Automatic token refresh on 401

### 2. **Token Management**
   - Retrieve JWT token from localStorage or cookies
   - Attach token to Authorization header: `Bearer <token>`
   - Store token in secure location (httpOnly cookies preferred)
   - Refresh token on expiry (retry failed requests)
   - Handle token not available gracefully
   - Redirect to login on 401 Unauthorized

### 3. **Error Handling**
   - Parse error response from API
   - Extract error message from response body
   - Handle network errors (no connection)
   - Handle timeout errors (server slow)
   - Display user-friendly error messages
   - Log errors for debugging
   - Retry on transient failures (5xx)

### 4. **Typed Endpoints**
   - Tasks: GET, POST, PATCH, DELETE
   - Auth: LOGIN, SIGNUP, REFRESH, LOGOUT
   - User: GET profile, UPDATE profile
   - TypeScript interfaces for requests/responses
   - Request parameter validation
   - Response data transformation

### 5. **Query Integration**
   - Integration with @tanstack/react-query
   - Query key factories for consistency
   - Mutation hooks for create/update/delete
   - Cache invalidation strategies
   - Automatic retry on failure
   - Loading and error states

## Example Implementation

### API Client Core (`lib/api/client.ts`)
```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';
import { getToken, setToken } from '@/lib/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle errors and token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    // Handle 401 Unauthorized (token expired or invalid)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Attempt token refresh
        const { access_token } = await refreshToken();
        setToken(access_token);

        // Retry original request with new token
        apiClient.defaults.headers.common[
          'Authorization'
        ] = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Handle other errors
    return Promise.reject(error);
  }
);

export default apiClient;

// Refresh token function
async function refreshToken(): Promise<{ access_token: string }> {
  const response = await axios.post(`${API_URL}/auth/refresh`, {
    refresh_token: localStorage.getItem('refresh_token'),
  });
  return response.data;
}
```

### Task API Endpoints (`lib/api/tasks.ts`)
```typescript
import apiClient from './client';
import { Task, TaskCreateRequest, TaskUpdateRequest } from '@/lib/types';

interface FetchTasksParams {
  page?: number;
  limit?: number;
  status?: string;
  priority?: string;
  search?: string;
}

interface TasksResponse {
  total: number;
  page: number;
  limit: number;
  items: Task[];
}

/**
 * Fetch paginated list of tasks with optional filters
 */
export async function fetchTasks(
  params?: FetchTasksParams
): Promise<TasksResponse> {
  const response = await apiClient.get<TasksResponse>('/tasks', {
    params: {
      page: params?.page || 1,
      limit: params?.limit || 20,
      ...(params?.status && { status: params.status }),
      ...(params?.priority && { priority: params.priority }),
      ...(params?.search && { search: params.search }),
    },
  });
  return response.data;
}

/**
 * Fetch single task by ID
 */
export async function fetchTask(id: string): Promise<Task> {
  const response = await apiClient.get<Task>(`/tasks/${id}`);
  return response.data;
}

/**
 * Create new task
 */
export async function createTask(
  data: TaskCreateRequest
): Promise<Task> {
  const response = await apiClient.post<Task>('/tasks', data);
  return response.data;
}

/**
 * Update task (full replacement)
 */
export async function updateTask(
  id: string,
  data: TaskCreateRequest
): Promise<Task> {
  const response = await apiClient.put<Task>(`/tasks/${id}`, data);
  return response.data;
}

/**
 * Partially update task
 */
export async function partialUpdateTask(
  id: string,
  data: Partial<TaskUpdateRequest>
): Promise<Task> {
  const response = await apiClient.patch<Task>(`/tasks/${id}`, data);
  return response.data;
}

/**
 * Delete task
 */
export async function deleteTask(id: string): Promise<void> {
  await apiClient.delete(`/tasks/${id}`);
}

/**
 * Search tasks
 */
export async function searchTasks(query: string): Promise<Task[]> {
  const response = await apiClient.get<Task[]>('/tasks/search', {
    params: { q: query },
  });
  return response.data;
}
```

### Auth API Endpoints (`lib/api/auth.ts`)
```typescript
import apiClient from './client';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user_id: string;
  email: string;
}

/**
 * Sign up new user
 */
export async function signup(data: SignupRequest): Promise<AuthResponse> {
  const response = await apiClient.post<AuthResponse>('/auth/signup', data);
  return response.data;
}

/**
 * Sign in user
 */
export async function signin(data: LoginRequest): Promise<AuthResponse> {
  const response = await apiClient.post<AuthResponse>('/auth/signin', data);
  return response.data;
}

/**
 * Refresh access token
 */
export async function refreshAccessToken(): Promise<{ access_token: string }> {
  const refreshToken = localStorage.getItem('refresh_token');
  const response = await apiClient.post<{ access_token: string }>(
    '/auth/refresh',
    { refresh_token }
  );
  return response.data;
}

/**
 * Sign out user
 */
export async function signout(): Promise<void> {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
```

### React Query Integration (`lib/api/queries.ts`)
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as tasksApi from './tasks';
import { Task, TaskCreateRequest } from '@/lib/types';

// Query key factory
const tasksQueryKeys = {
  all: ['tasks'],
  lists: () => [...tasksQueryKeys.all, 'list'],
  list: (filters: any) => [...tasksQueryKeys.lists(), filters],
  details: () => [...tasksQueryKeys.all, 'detail'],
  detail: (id: string) => [...tasksQueryKeys.details(), id],
};

/**
 * Hook: Fetch paginated tasks
 */
export function useTasks(page: number = 1, filters?: any) {
  return useQuery({
    queryKey: tasksQueryKeys.list({ page, ...filters }),
    queryFn: () => tasksApi.fetchTasks({ page, ...filters }),
    staleTime: 1000 * 60, // 1 minute
    gcTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook: Fetch single task
 */
export function useTask(id: string) {
  return useQuery({
    queryKey: tasksQueryKeys.detail(id),
    queryFn: () => tasksApi.fetchTask(id),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook: Create task mutation
 */
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: TaskCreateRequest) => tasksApi.createTask(data),
    onSuccess: () => {
      // Invalidate task lists to refetch
      queryClient.invalidateQueries({
        queryKey: tasksQueryKeys.lists(),
      });
    },
  });
}

/**
 * Hook: Update task mutation
 */
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Task> }) =>
      tasksApi.partialUpdateTask(id, data),
    onSuccess: (task) => {
      // Update detail cache
      queryClient.setQueryData(tasksQueryKeys.detail(task.id), task);
      // Invalidate lists
      queryClient.invalidateQueries({
        queryKey: tasksQueryKeys.lists(),
      });
    },
  });
}

/**
 * Hook: Delete task mutation
 */
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => tasksApi.deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: tasksQueryKeys.lists(),
      });
    },
  });
}
```

### Token Management (`lib/auth.ts`)
```typescript
const TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

/**
 * Get current access token
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Set access token
 */
export function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

/**
 * Get refresh token
 */
export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

/**
 * Set refresh token
 */
export function setRefreshToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(REFRESH_TOKEN_KEY, token);
  }
}

/**
 * Clear all tokens
 */
export function clearTokens(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  }
}

/**
 * Decode JWT to get user ID
 */
export function getUserIdFromToken(): string | null {
  const token = getToken();
  if (!token) return null;

  try {
    const [, payloadBase64] = token.split('.');
    const payload = JSON.parse(atob(payloadBase64));
    return payload.sub || null;
  } catch {
    return null;
  }
}

/**
 * Check if token is expired
 */
export function isTokenExpired(): boolean {
  const token = getToken();
  if (!token) return true;

  try {
    const [, payloadBase64] = token.split('.');
    const { exp } = JSON.parse(atob(payloadBase64));
    return Date.now() >= exp * 1000;
  } catch {
    return true;
  }
}
```

### Error Handling Utilities (`lib/api/errors.ts`)
```typescript
import { AxiosError } from 'axios';

export interface ApiErrorResponse {
  error: string;
  message: string;
  status_code: number;
  detail?: string;
}

/**
 * Extract error message from API error
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response?.data) {
      const apiError = error.response.data as ApiErrorResponse;
      return apiError.message || apiError.error || 'An error occurred';
    }
    if (error.message === 'Network Error') {
      return 'Network error. Please check your connection.';
    }
    if (error.code === 'ECONNABORTED') {
      return 'Request timeout. Please try again.';
    }
    return error.message || 'An error occurred';
  }
  return error instanceof Error ? error.message : 'An unknown error occurred';
}

/**
 * Check if error is retryable
 */
export function isRetryableError(error: unknown): boolean {
  if (error instanceof AxiosError) {
    // Retry on network errors and 5xx responses
    return (
      !error.response ||
      (error.response.status >= 500 && error.response.status < 600)
    );
  }
  return false;
}
```

## Acceptance Criteria
- [ ] API client configured with base URL from environment
- [ ] JWT token automatically attached to all requests
- [ ] Token stored in localStorage or secure cookies
- [ ] 401 errors trigger token refresh attempt
- [ ] Failed refresh redirects to login
- [ ] All task endpoints implemented (CRUD)
- [ ] All auth endpoints implemented (signin, signup, refresh)
- [ ] Error messages extracted and displayed
- [ ] Network errors handled gracefully
- [ ] Timeout handling working
- [ ] React Query hooks implemented
- [ ] Query key factory for consistency
- [ ] Mutations with cache invalidation
- [ ] Token helper functions working
- [ ] Error utilities working

## Dependencies
- **axios**: HTTP client
- **@tanstack/react-query**: Data fetching and caching
- **TypeScript**: Type safety
- **zod** (optional): Request validation
- **next/router**: Navigation/redirects

## Related Skills
- `ui_components` – Use hooks in components
- `nextjs_pages` – Call API from pages
- `error_handling` – Handle API errors
