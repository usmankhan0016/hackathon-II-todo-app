---
name: ui-components
description: Build reusable TaskList, TaskForm, and TaskItem React components with Tailwind CSS and ShadCN UI. Use when creating task management UI.
---

# UI Components Skill - Task Management Components

## Instructions

Build reusable, accessible React components for task management with Tailwind CSS styling, ShadCN UI patterns, and proper composition.

### 1. **TaskItem Component**
   - Display single task in list/card format
   - Show title, description, priority, status, due date
   - Color-coded status badges (pending, completed, overdue)
   - Priority indicators (high=red, medium=yellow, low=green)
   - Due date with relative time (e.g., "Due in 2 days")
   - Hover effects for interactivity
   - Click to expand or navigate to detail
   - Quick action buttons (edit, complete, delete)
   - Checkbox for marking complete

### 2. **TaskList Component**
   - Display paginated list of tasks
   - Support filtering by status and priority
   - Support sorting (by date, priority, title)
   - Empty state when no tasks
   - Loading skeleton while fetching
   - Infinite scroll or pagination controls
   - Search/filter UI controls
   - Responsive grid or list layout
   - Selected items counter
   - Bulk actions (delete, mark complete)

### 3. **TaskForm Component**
   - Modal or inline form for creating/editing task
   - Title input (required, 1-255 chars)
   - Description textarea (optional)
   - Priority dropdown selector
   - Due date picker (with date library)
   - Estimated hours input (optional)
   - Tags input (comma-separated or chips)
   - Submit button (Create/Update)
   - Cancel button to close
   - Form validation with error messages
   - Loading state during submission

### 4. **Component Features**
   - TypeScript types for props
   - Proper error boundaries
   - Loading states with spinners
   - Empty states with helpful messages
   - Keyboard navigation support
   - ARIA labels for accessibility
   - Responsive design (mobile-first)
   - Dark mode support via Tailwind classes
   - Proper composition (no deeply nested props)
   - Reusable and testable

### 5. **Styling & Layout**
   - Tailwind CSS utility classes
   - ShadCN UI components (Button, Input, Badge, etc.)
   - Consistent spacing and typography
   - Color scheme: Blue/Indigo primary, Green (completed), Red (overdue), Yellow (pending)
   - Smooth transitions and animations
   - Responsive breakpoints: mobile, tablet, desktop
   - Accessible contrast ratios

## Example Implementation

### TaskItem Component
```typescript
'use client';

import React, { useState } from 'react';
import { Task, TaskStatus, TaskPriority } from '@/lib/types';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import Checkbox from '@/components/ui/Checkbox';
import { formatDistanceToNow } from 'date-fns';
import { Trash2, Edit2, ChevronRight } from 'lucide-react';

interface TaskItemProps {
  task: Task;
  isSelected?: boolean;
  onSelect?: (taskId: string) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => void;
  onComplete?: (taskId: string, completed: boolean) => void;
  onClick?: () => void;
}

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  overdue: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
};

const priorityColors = {
  low: 'text-blue-500',
  medium: 'text-yellow-500',
  high: 'text-red-500',
};

export default function TaskItem({
  task,
  isSelected = false,
  onSelect,
  onEdit,
  onDelete,
  onComplete,
  onClick,
}: TaskItemProps) {
  const [isHovering, setIsHovering] = useState(false);

  const handleComplete = (e: React.MouseEvent) => {
    e.stopPropagation();
    onComplete?.(task.id, task.status !== TaskStatus.COMPLETED);
  };

  return (
    <div
      className={`
        p-4 border rounded-lg cursor-pointer transition-all
        hover:shadow-md hover:bg-slate-50 dark:hover:bg-slate-800
        ${isSelected ? 'bg-blue-50 dark:bg-blue-900 border-blue-500' : 'border-slate-200 dark:border-slate-700'}
      `}
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
      onClick={onClick}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <Checkbox
          checked={task.status === TaskStatus.COMPLETED}
          onChange={handleComplete}
          className="mt-1"
          aria-label={`Mark ${task.title} complete`}
        />

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold truncate ${
              task.status === TaskStatus.COMPLETED
                ? 'line-through text-slate-500'
                : 'text-slate-900 dark:text-white'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 mt-1">
              {task.description}
            </p>
          )}

          {/* Metadata */}
          <div className="flex flex-wrap gap-2 mt-3">
            {/* Status Badge */}
            <Badge className={statusColors[task.status]}>
              {task.status}
            </Badge>

            {/* Priority */}
            <span className={`text-sm font-medium ${priorityColors[task.priority]}`}>
              ⚫ {task.priority}
            </span>

            {/* Due Date */}
            {task.due_date && (
              <span className="text-sm text-slate-600 dark:text-slate-400">
                Due {formatDistanceToNow(new Date(task.due_date), { addSuffix: true })}
              </span>
            )}

            {/* Tags */}
            {task.tags && (
              <div className="flex gap-1">
                {task.tags.split(',').map((tag) => (
                  <span
                    key={tag.trim()}
                    className="text-xs bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded"
                  >
                    #{tag.trim()}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Action buttons (show on hover) */}
        {isHovering && (
          <div className="flex gap-2 shrink-0">
            <Button
              size="sm"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation();
                onEdit?.(task);
              }}
              aria-label={`Edit ${task.title}`}
            >
              <Edit2 className="w-4 h-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation();
                onDelete?.(task.id);
              }}
              aria-label={`Delete ${task.title}`}
            >
              <Trash2 className="w-4 h-4 text-red-500" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
```

### TaskList Component
```typescript
'use client';

import React, { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import { fetchTasks, updateTask, deleteTask } from '@/lib/api/tasks';
import { Task } from '@/lib/types';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import Skeleton from '@/components/ui/Skeleton';
import { Plus } from 'lucide-react';

interface TaskListProps {
  page?: number;
  status?: string;
  priority?: string;
}

export default function TaskList({
  page = 1,
  status,
  priority,
}: TaskListProps) {
  const [selectedTasks, setSelectedTasks] = useState<Set<string>>(new Set());
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch tasks
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['tasks', page, status, priority, searchQuery],
    queryFn: () =>
      fetchTasks({
        page,
        limit: 20,
        status,
        priority,
        search: searchQuery,
      }),
  });

  const handleSelect = useCallback((taskId: string) => {
    setSelectedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(taskId)) {
        next.delete(taskId);
      } else {
        next.add(taskId);
      }
      return next;
    });
  }, []);

  const handleComplete = useCallback(
    async (taskId: string, completed: boolean) => {
      await updateTask(taskId, {
        status: completed ? 'completed' : 'pending',
      });
      refetch();
    },
    [refetch]
  );

  const handleDelete = useCallback(
    async (taskId: string) => {
      if (confirm('Are you sure?')) {
        await deleteTask(taskId);
        refetch();
      }
    },
    [refetch]
  );

  const handleBulkDelete = useCallback(async () => {
    if (confirm(`Delete ${selectedTasks.size} tasks?`)) {
      await Promise.all(
        Array.from(selectedTasks).map((id) => deleteTask(id))
      );
      setSelectedTasks(new Set());
      refetch();
    }
  }, [selectedTasks, refetch]);

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">Failed to load tasks</p>
        <Button onClick={() => refetch()} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  const isEmpty = !isLoading && (!data?.items || data.items.length === 0);

  return (
    <div className="space-y-4">
      {/* Search and filter bar */}
      <div className="flex gap-2 flex-wrap items-center">
        <Input
          placeholder="Search tasks..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 min-w-64"
        />
        <Select
          value={status || ''}
          onChange={(e) => {
            // Handle filter change (router.push with query params)
          }}
          options={[
            { value: '', label: 'All Status' },
            { value: 'pending', label: 'Pending' },
            { value: 'completed', label: 'Completed' },
            { value: 'overdue', label: 'Overdue' },
          ]}
        />
        <Button
          onClick={() => {
            setEditingTask(null);
            setIsFormOpen(true);
          }}
        >
          <Plus className="w-4 h-4 mr-2" />
          New Task
        </Button>
      </div>

      {/* Bulk actions */}
      {selectedTasks.size > 0 && (
        <div className="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg flex justify-between items-center">
          <span className="font-medium">
            {selectedTasks.size} task{selectedTasks.size !== 1 ? 's' : ''} selected
          </span>
          <Button
            variant="destructive"
            onClick={handleBulkDelete}
          >
            Delete Selected
          </Button>
        </div>
      )}

      {/* Task list */}
      <div className="space-y-2">
        {isLoading ? (
          <>
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-24" />
            ))}
          </>
        ) : isEmpty ? (
          <div className="text-center py-12">
            <p className="text-slate-500 text-lg">No tasks yet</p>
            <p className="text-slate-400">Create your first task to get started</p>
          </div>
        ) : (
          data!.items.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              isSelected={selectedTasks.has(task.id)}
              onSelect={handleSelect}
              onEdit={(t) => {
                setEditingTask(t);
                setIsFormOpen(true);
              }}
              onDelete={handleDelete}
              onComplete={handleComplete}
            />
          ))
        )}
      </div>

      {/* Pagination */}
      {data && data.total > 20 && (
        <div className="flex justify-center gap-2 mt-6">
          <Button disabled={page === 1}>Previous</Button>
          <span className="px-4 py-2">
            Page {page} of {Math.ceil(data.total / 20)}
          </span>
          <Button
            disabled={page >= Math.ceil(data.total / 20)}
          >
            Next
          </Button>
        </div>
      )}

      {/* Task form modal */}
      {isFormOpen && (
        <TaskForm
          task={editingTask}
          onClose={() => {
            setIsFormOpen(false);
            setEditingTask(null);
          }}
          onSuccess={() => {
            setIsFormOpen(false);
            setEditingTask(null);
            refetch();
          }}
        />
      )}
    </div>
  );
}
```

### TaskForm Component
```typescript
'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Task, TaskPriority } from '@/lib/types';
import { createTask, updateTask } from '@/lib/api/tasks';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import Select from '@/components/ui/Select';
import DatePicker from '@/components/ui/DatePicker';
import Modal from '@/components/ui/Modal';
import { X } from 'lucide-react';

const taskSchema = z.object({
  title: z.string().min(1, 'Title required').max(255),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']),
  due_date: z.date().optional(),
  estimated_hours: z.number().int().positive().optional(),
  tags: z.string().optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormProps {
  task?: Task | null;
  onClose: () => void;
  onSuccess: () => void;
}

export default function TaskForm({
  task,
  onClose,
  onSuccess,
}: TaskFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      priority: task?.priority || 'medium',
      due_date: task?.due_date ? new Date(task.due_date) : undefined,
      estimated_hours: task?.estimated_hours || undefined,
      tags: task?.tags || '',
    },
  });

  const onSubmit = async (data: TaskFormData) => {
    try {
      setIsSubmitting(true);
      setError(null);

      if (task?.id) {
        await updateTask(task.id, data);
      } else {
        await createTask(data);
      }

      onSuccess();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to save task'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen onClose={onClose}>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">
            {task ? 'Edit Task' : 'New Task'}
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="bg-red-50 dark:bg-red-900 p-3 rounded text-red-700 dark:text-red-200">
              {error}
            </div>
          )}

          {/* Title */}
          <div>
            <label className="block text-sm font-medium mb-2">Title</label>
            <Input
              {...register('title')}
              placeholder="Task title"
              error={errors.title?.message}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <Textarea
              {...register('description')}
              placeholder="Task description (optional)"
              rows={3}
            />
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium mb-2">Priority</label>
            <Select
              {...register('priority')}
              options={[
                { value: 'low', label: 'Low' },
                { value: 'medium', label: 'Medium' },
                { value: 'high', label: 'High' },
              ]}
            />
          </div>

          {/* Due Date */}
          <div>
            <label className="block text-sm font-medium mb-2">Due Date</label>
            <DatePicker
              value={watch('due_date')}
              onChange={(date) => {
                // Handle date change
              }}
            />
          </div>

          {/* Estimated Hours */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Estimated Hours
            </label>
            <Input
              {...register('estimated_hours', { valueAsNumber: true })}
              type="number"
              placeholder="Hours (optional)"
              min="0"
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium mb-2">Tags</label>
            <Input
              {...register('tags')}
              placeholder="Comma-separated tags"
            />
          </div>

          {/* Actions */}
          <div className="flex gap-2 justify-end pt-4">
            <Button
              variant="outline"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting
                ? 'Saving...'
                : task
                  ? 'Update Task'
                  : 'Create Task'}
            </Button>
          </div>
        </form>
      </div>
    </Modal>
  );
}
```

## Acceptance Criteria
- [ ] TaskItem displays task with title, description, priority, status
- [ ] TaskItem shows color-coded badges for status and priority
- [ ] TaskItem has hover effects with action buttons
- [ ] TaskItem checkbox toggles completion status
- [ ] TaskList displays paginated list of tasks
- [ ] TaskList supports filtering by status and priority
- [ ] TaskList has search functionality
- [ ] TaskList shows empty state when no tasks
- [ ] TaskList loading skeleton displays while fetching
- [ ] TaskList bulk delete working
- [ ] TaskForm creates new tasks
- [ ] TaskForm edits existing tasks
- [ ] TaskForm validates all fields
- [ ] All components responsive (mobile-first)
- [ ] Dark mode support working

## Dependencies
- **React**: 19+ (with hooks)
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **ShadCN UI**: UI components
- **react-hook-form**: Form management
- **zod**: Schema validation
- **@tanstack/react-query**: Data fetching
- **date-fns**: Date formatting
- **lucide-react**: Icons

## Related Skills
- `nextjs_pages` – Pages using these components
- `api_client` – Fetch data for components
