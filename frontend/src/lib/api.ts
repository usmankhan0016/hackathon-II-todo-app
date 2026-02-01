/**
 * API Client with JWT token management
 * Automatically attaches access token to all requests
 * Handles token refresh on 401 responses
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

interface UserData {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

interface AuthResponse {
  user: UserData;
  tokens: TokenResponse;
}

interface SignupRequest {
  email: string;
  password: string;
}

interface SigninRequest {
  email: string;
  password: string;
}

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

interface TaskCreateRequest {
  title: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
  tags?: string[];
}

interface TaskUpdateRequest {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
  tags?: string[];
}

interface PaginationParams {
  skip?: number;
  limit?: number;
  status?: string;
  priority?: string;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

class ApiClient {
  private baseURL: string;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL;
    this.loadTokens();
  }

  private loadTokens(): void {
    if (typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('access_token');
      this.refreshToken = localStorage.getItem('refresh_token');
    }
  }

  private storeTokens(
    accessToken: string,
    refreshToken: string,
    expiresIn: number
  ): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken);
      localStorage.setItem('token_expires_at', (Date.now() + expiresIn * 1000).toString());
    }
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
  }

  private clearTokens(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('token_expires_at');
    }
    this.accessToken = null;
    this.refreshToken = null;
  }

  private isTokenExpired(): boolean {
    if (typeof window === 'undefined') return false;
    const expiresAt = localStorage.getItem('token_expires_at');
    if (!expiresAt) return false;
    return Date.now() > parseInt(expiresAt);
  }

  private async refreshAccessToken(): Promise<boolean> {
    if (!this.refreshToken) return false;

    try {
      const response = await fetch(`${this.baseURL}/api/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.refreshToken}`,
        },
      });

      if (!response.ok) {
        this.clearTokens();
        return false;
      }

      const data: AuthResponse = await response.json();
      this.storeTokens(data.tokens.access_token, data.tokens.refresh_token, data.tokens.expires_in);
      return true;
    } catch (error) {
      this.clearTokens();
      return false;
    }
  }

  private async fetch(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    let response: Response;
    try {
      response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers,
      });
    } catch (networkError) {
      throw networkError;
    }

    if (response.status === 401 && this.refreshToken) {
      const refreshed = await this.refreshAccessToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${this.accessToken}`;
        response = await fetch(`${this.baseURL}${endpoint}`, {
          ...options,
          headers,
        });
      } else {
        this.clearTokens();
      }
    }

    return response;
  }

  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await this.fetch('/api/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || error.detail || 'Signup failed');
    }

    const authData: AuthResponse = await response.json();
    this.storeTokens(authData.tokens.access_token, authData.tokens.refresh_token, authData.tokens.expires_in);
    return authData;
  }

  async signin(data: SigninRequest): Promise<AuthResponse> {
    const response = await this.fetch('/api/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || error.detail || 'Signin failed');
    }

    const authData: AuthResponse = await response.json();
    this.storeTokens(authData.tokens.access_token, authData.tokens.refresh_token, authData.tokens.expires_in);
    return authData;
  }

  logout(): void {
    this.clearTokens();
  }

  async getTasks(params: PaginationParams = {}): Promise<{ items: Task[]; total: number }> {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params.status) queryParams.append('status', params.status);
    if (params.priority) queryParams.append('priority', params.priority);
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.order) queryParams.append('order', params.order);

    const query = queryParams.toString();
    const endpoint = query ? `/api/tasks/?${query}` : '/api/tasks/';

    const response = await this.fetch(endpoint);

    if (!response.ok) {
      throw new Error('Failed to fetch tasks');
    }

    return response.json();
  }

  async getTask(taskId: number): Promise<Task> {
    const response = await this.fetch(`/api/tasks/${taskId}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Task not found');
      }
      throw new Error('Failed to fetch task');
    }

    return response.json();
  }

  async createTask(data: TaskCreateRequest): Promise<Task> {
    const response = await this.fetch('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create task');
    }

    return response.json();
  }

  async updateTask(taskId: number, data: TaskUpdateRequest): Promise<Task> {
    const response = await this.fetch(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update task');
    }

    return response.json();
  }

  async patchTask(taskId: number, data: Partial<TaskUpdateRequest>): Promise<Task> {
    const response = await this.fetch(`/api/tasks/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update task');
    }

    return response.json();
  }

  async deleteTask(taskId: number): Promise<void> {
    const response = await this.fetch(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete task');
    }
  }

  async getHealth(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseURL}/health`);

    if (!response.ok) {
      throw new Error('Backend health check failed');
    }

    return response.json();
  }

  isAuthenticated(): boolean {
    return !!this.accessToken;
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }
}

export const apiClient = new ApiClient();

export type { AuthResponse, TokenResponse, UserData, SignupRequest, SigninRequest, Task, TaskCreateRequest, TaskUpdateRequest, PaginationParams };
