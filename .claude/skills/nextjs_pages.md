---
name: nextjs-pages
description: Create Next.js App Router pages, layouts, and routing structure for todo application. Use when building page structure for Phase 2+ frontend.
---

# Next.js Pages Skill - App Router Pages & Layouts

## Instructions

Structure Next.js 16+ application with App Router, nested layouts, dynamic routes, and proper page organization for todo management.

### 1. **App Router Structure**
   - Use `app/` directory (not `pages/`)
   - Define routes via directory structure
   - Layout files: `layout.tsx` for shared UI
   - Page files: `page.tsx` for route endpoints
   - Middleware for authentication redirects
   - Route groups with parentheses: `(auth)`, `(dashboard)`

### 2. **Root Layout** (`app/layout.tsx`)
   - HTML, head, and body structure
   - Global providers (auth, theme, query client)
   - Global styles and fonts
   - Metadata configuration
   - Navigation structure
   - Dark/light mode toggle

### 3. **Authentication Routes** (`app/(auth)/`)
   - Login page: `app/(auth)/login/page.tsx`
   - Signup page: `app/(auth)/signup/page.tsx`
   - Redirect authenticated users to dashboard
   - Public routes (no auth required)
   - Form submission and token storage

### 4. **Dashboard Routes** (`app/(dashboard)/`)
   - Dashboard layout: `app/(dashboard)/layout.tsx`
   - Main tasks page: `app/(dashboard)/tasks/page.tsx`
   - Task detail page: `app/(dashboard)/tasks/[id]/page.tsx` (dynamic)
   - Settings page: `app/(dashboard)/settings/page.tsx`
   - Profile page: `app/(dashboard)/profile/page.tsx`
   - All require authentication

### 5. **Routing Features**
   - Dynamic segments: `[id]` for task details
   - Catch-all routes: `[...slug]` for 404 handling
   - Optional segments: `[[...slug]]` for SEO
   - Parallel routes for modals and sidebars
   - Route groups for layout organization
   - Navigation with `useRouter` client-side
   - Link components for server-side transitions

### 6. **Page Organization Best Practices**
   - Server components by default
   - Client components only for interactivity (`use client`)
   - Shared layouts for consistent UI
   - Error boundaries for error handling
   - Loading UI with Suspense
   - Streaming responses for large pages

## Example Implementation

### Root Layout (`app/layout.tsx`)
```typescript
import type { Metadata } from 'next';
import { Providers } from './providers';
import Navigation from '@/components/Navigation';
import './globals.css';

export const metadata: Metadata = {
  title: 'Todo App - Task Management',
  description: 'Organize and manage your tasks efficiently',
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          <Navigation />
          <main className="min-h-screen bg-background text-foreground">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
```

### Providers Component (`app/providers.tsx`)
```typescript
'use client';

import React from 'react';
import { ThemeProvider } from '@/components/theme-provider';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/query-client';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  );
}
```

### Auth Layout (`app/(auth)/layout.tsx`)
```typescript
import { redirect } from 'next/navigation';
import { getSession } from '@/lib/auth';

export default async function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Redirect authenticated users to dashboard
  const session = await getSession();
  if (session) {
    redirect('/dashboard');
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-900 dark:to-slate-800">
      <div className="w-full max-w-md">{children}</div>
    </div>
  );
}
```

### Login Page (`app/(auth)/login/page.tsx`)
```typescript
import { Metadata } from 'next';
import LoginForm from '@/components/auth/LoginForm';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Login - Todo App',
  description: 'Sign in to your account',
};

export default function LoginPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold tracking-tight">Welcome back</h1>
        <p className="text-muted-foreground">
          Sign in to your account to continue
        </p>
      </div>

      <LoginForm />

      <p className="text-center text-sm text-muted-foreground">
        Don't have an account?{' '}
        <Link
          href="/signup"
          className="font-medium text-primary hover:underline"
        >
          Sign up
        </Link>
      </p>
    </div>
  );
}
```

### Dashboard Layout (`app/(dashboard)/layout.tsx`)
```typescript
import { redirect } from 'next/navigation';
import { getSession } from '@/lib/auth';
import Sidebar from '@/components/dashboard/Sidebar';
import Header from '@/components/dashboard/Header';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Protect dashboard routes
  const session = await getSession();
  if (!session) {
    redirect('/login');
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar user={session.user} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header user={session.user} />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
```

### Tasks Page (`app/(dashboard)/tasks/page.tsx`)
```typescript
import { Metadata } from 'next';
import { Suspense } from 'react';
import TaskList from '@/components/tasks/TaskList';
import TaskListSkeleton from '@/components/tasks/TaskListSkeleton';
import TaskActions from '@/components/tasks/TaskActions';

export const metadata: Metadata = {
  title: 'Tasks - Todo App',
  description: 'Manage your tasks',
};

export default function TasksPage({
  searchParams,
}: {
  searchParams: { page?: string; status?: string; priority?: string };
}) {
  const page = parseInt(searchParams.page || '1');
  const status = searchParams.status;
  const priority = searchParams.priority;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Tasks</h1>
        <TaskActions />
      </div>

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList
          page={page}
          status={status}
          priority={priority}
        />
      </Suspense>
    </div>
  );
}
```

### Task Detail Page (`app/(dashboard)/tasks/[id]/page.tsx`)
```typescript
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import TaskDetail from '@/components/tasks/TaskDetail';
import { fetchTask } from '@/lib/api/tasks';

interface TaskDetailPageProps {
  params: { id: string };
}

export async function generateMetadata(
  { params }: TaskDetailPageProps
): Promise<Metadata> {
  try {
    const task = await fetchTask(params.id);
    return {
      title: `${task.title} - Todo App`,
      description: task.description || 'Task details',
    };
  } catch {
    return {
      title: 'Task - Todo App',
    };
  }
}

export default async function TaskDetailPage({
  params,
}: TaskDetailPageProps) {
  try {
    const task = await fetchTask(params.id);

    return (
      <div className="max-w-2xl">
        <TaskDetail task={task} />
      </div>
    );
  } catch (error) {
    notFound();
  }
}
```

### Not Found Page (`app/not-found.tsx`)
```typescript
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className="text-4xl font-bold">404</h1>
      <p className="text-muted-foreground">Page not found</p>
      <Link
        href="/dashboard"
        className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
      >
        Go back to dashboard
      </Link>
    </div>
  );
}
```

### Error Boundary (`app/error.tsx`)
```typescript
'use client';

import { useEffect } from 'react';
import Button from '@/components/ui/Button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Error boundary caught:', error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h2 className="text-2xl font-bold">Something went wrong</h2>
      <p className="text-muted-foreground">{error.message}</p>
      <Button onClick={() => reset()}>Try again</Button>
    </div>
  );
}
```

### Middleware for Protected Routes (`middleware.ts`)
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });

  // Redirect to login if accessing protected routes without token
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // Redirect to dashboard if authenticated user tries to access auth pages
  if (request.nextUrl.pathname.startsWith('/(auth)')) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/(auth)/:path*'],
};
```

## Acceptance Criteria
- [ ] App Router structure using `app/` directory
- [ ] Root layout with providers and global styles
- [ ] Auth routes in route group `(auth)`
- [ ] Dashboard routes in route group `(dashboard)`
- [ ] Login and signup pages in auth routes
- [ ] Protected dashboard routes redirect unauthenticated users
- [ ] Dynamic route for task details `[id]`
- [ ] Metadata configured for SEO
- [ ] Server components by default
- [ ] Client components marked with `use client`
- [ ] Error boundary for error handling
- [ ] Suspense with loading UI
- [ ] Middleware redirects working correctly
- [ ] Navigation between pages working

## Dependencies
- **Next.js**: 16+ with App Router
- **React**: 19+ with server components
- **next-auth**: Authentication (if using)
- **@tanstack/react-query**: Data fetching
- **tailwindcss**: Styling

## Related Skills
- `ui_components` – Implement components in pages
- `api_client` – Fetch data in pages
- `nextjs_pages` – Page/layout organization
