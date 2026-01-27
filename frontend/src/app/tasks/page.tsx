'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/stores/authStore';
import { apiClient, type Task } from '@/lib/api';

type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';
type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';

export default function TasksPage() {
  const router = useRouter();
  const { isAuthenticated, logout, checkAuth } = useAuthStore();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [filter, setFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all');

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editStatus, setEditStatus] = useState<TaskStatus>('pending');
  const [editPriority, setEditPriority] = useState<TaskPriority>('medium');
  const [isEditSubmitting, setIsEditSubmitting] = useState(false);

  // Delete confirmation state
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (!isAuthenticated && typeof window !== 'undefined') {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated) {
      loadTasks();
    }
  }, [filter, isAuthenticated]);

  const loadTasks = async () => {
    setIsLoading(true);
    setError('');
    try {
      const params: any = {};
      if (filter !== 'all') {
        params.status = filter;
      }
      const response = await apiClient.getTasks(params);
      setTasks(response.items);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load tasks';
      setError(message);
      // Auto-dismiss error after 5 seconds
      setTimeout(() => setError(''), 5000);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    setIsAddingTask(true);
    setError('');
    try {
      const newTask = await apiClient.createTask({
        title: newTaskTitle,
        description: newTaskDescription || undefined,
        status: 'pending',
        priority: 'medium',
      });
      setTasks([newTask, ...tasks]);
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create task';
      setError(message);
      // Auto-dismiss error after 5 seconds
      setTimeout(() => setError(''), 5000);
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleTask = async (task: Task) => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    setError('');
    try {
      const updated = await apiClient.patchTask(task.id, { status: newStatus });
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update task';
      setError(message);
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleDeleteTask = async (task: Task) => {
    setTaskToDelete(task);
  };

  const confirmDeleteTask = async () => {
    if (!taskToDelete) return;

    setError('');
    try {
      await apiClient.deleteTask(taskToDelete.id);
      setTasks(tasks.filter((t) => t.id !== taskToDelete.id));
      setTaskToDelete(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete task';
      setError(message);
      // Auto-dismiss error after 5 seconds
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setEditStatus(task.status as TaskStatus);
    setEditPriority(task.priority as TaskPriority);
  };

  const handleSaveEdit = async () => {
    if (!editingTask || !editTitle.trim()) return;

    setIsEditSubmitting(true);
    setError('');
    try {
      const updated = await apiClient.patchTask(editingTask.id, {
        title: editTitle,
        description: editDescription || undefined,
        status: editStatus,
        priority: editPriority,
      });

      setTasks(tasks.map((t) => (t.id === editingTask.id ? updated : t)));
      setEditingTask(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update task';
      setError(message);
      setTimeout(() => setError(''), 5000);
    } finally {
      setIsEditSubmitting(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'text-red-600';
      case 'high':
        return 'text-orange-600';
      case 'medium':
        return 'text-blue-600';
      case 'low':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  if (!isAuthenticated && typeof window !== 'undefined') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="container">
          <div className="text-center">
            <p className="text-xl text-gray-600 mb-4">Redirecting...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-md">
        <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            <Link href="/tasks">My Tasks</Link>
          </h1>
          <button
            onClick={handleLogout}
            className="btn-secondary"
          >
            Sign Out
          </button>
        </div>
      </nav>

      <main className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="error-text">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Task</h2>
              <form onSubmit={handleAddTask} className="space-y-3">
                <div>
                  <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="What do you need to do?"
                    className="input-base"
                    disabled={isAddingTask}
                    required
                  />
                </div>
                <div>
                  <textarea
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    placeholder="Add task details (optional)"
                    className="input-base resize-none"
                    rows={3}
                    disabled={isAddingTask}
                    maxLength={5000}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {newTaskDescription.length} / 5000 characters
                  </p>
                </div>
                <button
                  type="submit"
                  disabled={isAddingTask || !newTaskTitle.trim()}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isAddingTask ? 'Adding...' : 'Add Task'}
                </button>
              </form>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="flex gap-2 mb-6 flex-wrap">
              {(['all', 'pending', 'in_progress', 'completed'] as const).map((status) => (
                <button
                  key={status}
                  onClick={() => setFilter(status)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === status ? 'btn-primary' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
                </button>
              ))}
            </div>

            {isLoading ? (
              <div className="card">
                <p className="text-gray-600 text-center py-8">Loading tasks...</p>
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="card">
                <p className="text-gray-600 text-center py-8">
                  {filter === 'all'
                    ? 'No tasks yet. Create one to get started!'
                    : `No ${filter.replace('_', ' ')} tasks.`}
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredTasks.map((task) => (
                  <div key={task.id} className="card flex items-start gap-4 group hover:shadow-lg transition-shadow">
                    <input
                      type="checkbox"
                      checked={task.status === 'completed'}
                      onChange={() => handleToggleTask(task)}
                      className="mt-1 w-5 h-5 cursor-pointer"
                    />
                    <div className="flex-1 min-w-0">
                      <h3
                        className={`font-medium ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'}`}
                      >
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                          {task.description}
                        </p>
                      )}
                      <div className="flex gap-2 mt-2 flex-wrap">
                        <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(task.status)}`}>
                          {task.status.replace('_', ' ')}
                        </span>
                        <span className={`text-xs font-medium ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                        {task.due_date && (
                          <span className="text-xs text-gray-500">
                            Due: {new Date(task.due_date).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-all">
                      <button
                        onClick={() => handleEditTask(task)}
                        className="p-2 text-gray-400 hover:text-blue-600"
                        title="Edit task"
                      >
                        ✏️
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task)}
                        className="p-2 text-gray-400 hover:text-red-600"
                        title="Delete task"
                      >
                        X
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {taskToDelete && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-sm w-full">
              <div className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-2">Delete Task?</h2>
                <p className="text-gray-600 mb-6">
                  Are you sure you want to delete <span className="font-semibold">"{taskToDelete.title}"</span>? This cannot be undone.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => setTaskToDelete(null)}
                    className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmDeleteTask}
                    className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Edit Task Modal */}
        {editingTask && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
              <div className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Edit Task</h2>

                <div className="space-y-4">
                  {/* Title Field */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Title
                    </label>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="input-base"
                      placeholder="Task title"
                      disabled={isEditSubmitting}
                    />
                  </div>

                  {/* Description Field */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description
                    </label>
                    <textarea
                      value={editDescription}
                      onChange={(e) => setEditDescription(e.target.value)}
                      className="input-base resize-none"
                      placeholder="Add task details"
                      rows={3}
                      disabled={isEditSubmitting}
                      maxLength={5000}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      {editDescription.length} / 5000 characters
                    </p>
                  </div>

                  {/* Status Dropdown */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Status
                    </label>
                    <select
                      value={editStatus}
                      onChange={(e) => setEditStatus(e.target.value as TaskStatus)}
                      className="input-base"
                      disabled={isEditSubmitting}
                    >
                      <option value="pending">Pending</option>
                      <option value="in_progress">In Progress</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </div>

                  {/* Priority Dropdown */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Priority
                    </label>
                    <select
                      value={editPriority}
                      onChange={(e) => setEditPriority(e.target.value as TaskPriority)}
                      className="input-base"
                      disabled={isEditSubmitting}
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                  </div>
                </div>

                {/* Buttons */}
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleCancelEdit}
                    disabled={isEditSubmitting}
                    className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors disabled:opacity-50"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveEdit}
                    disabled={isEditSubmitting || !editTitle.trim()}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isEditSubmitting ? 'Saving...' : 'Save'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
