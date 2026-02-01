'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/stores/authStore';
import { apiClient, type Task } from '@/lib/api';
import {
  ClipboardList,
  Hourglass,
  Rocket,
  CheckCircle2,
  Search,
  X,
  Edit2,
  Trash2,
  Calendar,
  Clock,
  Flame,
  Zap,
  MapPin,
  Sprout,
  LogOut,
  AlertTriangle,
  Loader2,
  Save,
  Inbox,
  Plus
} from 'lucide-react';

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
  const [searchQuery, setSearchQuery] = useState('');

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
  }, [isAuthenticated]);

  const loadTasks = async () => {
    setIsLoading(true);
    setError('');
    try {
      const response = await apiClient.getTasks();
      setTasks(response.items);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load tasks';
      setError(message);
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
    // Apply status filter
    const statusMatch = filter === 'all' || task.status === filter;

    // Apply search filter (case-insensitive, search in title and description)
    const searchMatch = !searchQuery.trim() ||
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (task.description?.toLowerCase().includes(searchQuery.toLowerCase()) || false);

    return statusMatch && searchMatch;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676]';
      case 'in_progress':
        return 'bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676]';
      case 'pending':
        return 'bg-[#0B0F0E] border border-[#1F2A28] text-[#9FB3AD]';
      case 'cancelled':
        return 'bg-[#0B0F0E] border border-[#1F2A28] text-[#6B7F7A]';
      default:
        return 'bg-[#0B0F0E] border border-[#1F2A28] text-[#6B7F7A]';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'text-[#E5484D]';
      case 'high':
        return 'text-[#E5484D]';
      case 'medium':
        return 'text-[#9FB3AD]';
      case 'low':
        return 'text-[#6B7F7A]';
      default:
        return 'text-[#6B7F7A]';
    }
  };

  if (!isAuthenticated && typeof window !== 'undefined') {
    return (
      <div className="min-h-screen bg-[#0B0F0E] flex items-center justify-center">
        <div className="container">
          <div className="text-center">
            <p className="text-[#9FB3AD]">Redirecting...</p>
          </div>
        </div>
      </div>
    );
  }

  const completedCount = tasks.filter((t) => t.status === 'completed').length;
  const pendingCount = tasks.filter((t) => t.status === 'pending').length;
  const inProgressCount = tasks.filter((t) => t.status === 'in_progress').length;

  return (
    <div className="min-h-screen bg-[#0B0F0E]">
      {/* Navigation Header */}
      <nav className="bg-[#111716] border-b border-[#1F2A28] sticky top-0 z-40">
        <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <img
                src="/logo.svg"
                alt="TaskFlow Logo"
                className="w-10 h-10"
              />
              <div>
                <h1 className="text-xl font-semibold text-[#E6F2EF]">
                  TaskFlow
                </h1>
                <p className="text-xs text-[#6B7F7A]">Organize your day</p>
              </div>
            </div>

            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 bg-transparent border-2 border-[#00E676] text-[#00E676] font-medium rounded-lg hover:bg-[rgba(0,230,118,0.1)] hover:text-[#00C965] transition-colors duration-200 text-sm"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      <main className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Toast */}
        {error && (
          <div className="mb-6 p-4 bg-[#0B0F0E] border border-[#E5484D] rounded-lg">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-[#E5484D]" />
              <p className="text-[#E5484D] text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Task Statistics Dashboard */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[#6B7F7A] uppercase tracking-wide mb-2">Total Tasks</p>
                <p className="text-2xl font-semibold text-[#E6F2EF]">{tasks.length}</p>
              </div>
              <div className="w-10 h-10 bg-[#0B0F0E] border border-[#1F2A28] rounded-lg flex items-center justify-center">
                <ClipboardList className="w-5 h-5 text-[#9FB3AD]" />
              </div>
            </div>
          </div>

          <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[#6B7F7A] uppercase tracking-wide mb-2">Pending</p>
                <p className="text-2xl font-semibold text-[#9FB3AD]">{pendingCount}</p>
              </div>
              <div className="w-10 h-10 bg-[#0B0F0E] border border-[#1F2A28] rounded-lg flex items-center justify-center">
                <Hourglass className="w-5 h-5 text-[#9FB3AD]" />
              </div>
            </div>
          </div>

          <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[#6B7F7A] uppercase tracking-wide mb-2">In Progress</p>
                <p className="text-2xl font-semibold text-[#00E676]">{inProgressCount}</p>
              </div>
              <div className="w-10 h-10 bg-[rgba(0,230,118,0.15)] border border-[#00E676] rounded-lg flex items-center justify-center">
                <Rocket className="w-5 h-5 text-[#00E676]" />
              </div>
            </div>
          </div>

          <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[#6B7F7A] uppercase tracking-wide mb-2">Completed</p>
                <p className="text-2xl font-semibold text-[#00E676]">{completedCount}</p>
              </div>
              <div className="w-10 h-10 bg-[rgba(0,230,118,0.15)] border border-[#00E676] rounded-lg flex items-center justify-center">
                <CheckCircle2 className="w-5 h-5 text-[#00E676]" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Add Task Card - Left Column */}
          <div className="lg:col-span-1">
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-6 sticky top-24">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 bg-[#00E676] rounded-lg flex items-center justify-center">
                  <Plus className="w-5 h-5 text-[#0B0F0E]" />
                </div>
                <h2 className="text-lg font-semibold text-[#E6F2EF]">Create Task</h2>
              </div>

              <form onSubmit={handleAddTask} className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                    Task Title
                  </label>
                  <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="What do you need to do?"
                    className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none placeholder-[#6B7F7A] text-sm"
                    disabled={isAddingTask}
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                    Description (Optional)
                  </label>
                  <textarea
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    placeholder="Add task details..."
                    className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none placeholder-[#6B7F7A] resize-none text-sm"
                    rows={4}
                    disabled={isAddingTask}
                    maxLength={5000}
                  />
                  <p className="text-xs text-[#6B7F7A] mt-2">
                    {newTaskDescription.length} / 5000
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={isAddingTask || !newTaskTitle.trim()}
                  className="w-full px-4 py-2.5 bg-[#00E676] text-[#0B0F0E] font-medium rounded-lg hover:bg-[#00C965] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
                >
                  {isAddingTask ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Adding...
                    </>
                  ) : (
                    <>
                      <Plus className="w-4 h-4" />
                      Add Task
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Task List - Right Column */}
          <div className="lg:col-span-2">
            {/* Search Bar and Filters */}
            <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5 mb-6 space-y-4">
              {/* Search Input */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Search className="w-4 h-4 text-[#6B7F7A]" />
                </div>
                <input
                  type="text"
                  placeholder="Search tasks by title or description..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-11 pr-10 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none placeholder-[#6B7F7A] text-sm"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#6B7F7A] hover:text-[#9FB3AD] transition-colors"
                    title="Clear search"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Filter Buttons */}
              <div className="flex gap-2 flex-wrap">
                {(['all', 'pending', 'in_progress', 'completed'] as const).map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilter(status)}
                    className={`px-3 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center gap-2 text-sm ${
                      filter === status
                        ? 'bg-[#00E676] text-[#0B0F0E]'
                        : 'bg-[#0B0F0E] border border-[#1F2A28] text-[#9FB3AD] hover:bg-[#111716] hover:text-[#E6F2EF]'
                    }`}
                  >
                    {status === 'all' && <ClipboardList className="w-4 h-4" />}
                    {status === 'pending' && <Hourglass className="w-4 h-4" />}
                    {status === 'in_progress' && <Rocket className="w-4 h-4" />}
                    {status === 'completed' && <CheckCircle2 className="w-4 h-4" />}
                    <span>
                      {status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
                    </span>
                  </button>
                ))}
              </div>

              {/* Active Filters Display */}
              {(searchQuery || filter !== 'all') && (
                <div className="flex items-center gap-2 pt-3 border-t border-[#1F2A28]">
                  <span className="text-xs text-[#6B7F7A] font-medium uppercase tracking-wide">Active filters:</span>
                  {searchQuery && (
                    <span className="px-2.5 py-1 bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676] text-xs font-medium rounded flex items-center gap-1.5">
                      Search: "{searchQuery.substring(0, 20)}{searchQuery.length > 20 ? '...' : ''}"
                      <button
                        onClick={() => setSearchQuery('')}
                        className="text-[#00E676] hover:text-[#00C965]"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  )}
                  {filter !== 'all' && (
                    <span className="px-2.5 py-1 bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676] text-xs font-medium rounded flex items-center gap-1.5">
                      Status: {filter.replace('_', ' ')}
                      <button
                        onClick={() => setFilter('all')}
                        className="text-[#00E676] hover:text-[#00C965]"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  )}
                  <button
                    onClick={() => {
                      setSearchQuery('');
                      setFilter('all');
                    }}
                    className="ml-auto text-xs text-[#6B7F7A] hover:text-[#9FB3AD] font-medium"
                  >
                    Clear all
                  </button>
                </div>
              )}
            </div>

            {/* Results Count */}
            {!isLoading && filteredTasks.length > 0 && (searchQuery || filter !== 'all') && (
              <div className="bg-[rgba(0,230,118,0.15)] border border-[#00E676] rounded-lg p-3 mb-4">
                <p className="text-sm text-[#E6F2EF]">
                  <span className="text-[#00E676] font-semibold">{filteredTasks.length}</span>
                  {' '}
                  {filteredTasks.length === 1 ? 'task' : 'tasks'} found
                  {searchQuery && ` matching "${searchQuery}"`}
                  {filter !== 'all' && ` with status "${filter.replace('_', ' ')}"`}
                </p>
              </div>
            )}

            {/* Task List Content */}
            {isLoading ? (
              <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-12">
                <div className="flex flex-col items-center justify-center gap-3">
                  <Loader2 className="w-8 h-8 text-[#00E676] animate-spin" />
                  <p className="text-[#9FB3AD] text-sm">Loading your tasks...</p>
                </div>
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="bg-[#111716] border border-[#1F2A28] rounded-lg p-12">
                <div className="flex flex-col items-center justify-center gap-4">
                  <div className="w-16 h-16 bg-[#0B0F0E] border border-[#1F2A28] rounded-full flex items-center justify-center">
                    {searchQuery ? (
                      <Search className="w-8 h-8 text-[#6B7F7A]" />
                    ) : tasks.length === 0 ? (
                      <Inbox className="w-8 h-8 text-[#6B7F7A]" />
                    ) : (
                      <ClipboardList className="w-8 h-8 text-[#6B7F7A]" />
                    )}
                  </div>
                  <p className="text-[#9FB3AD] font-medium text-center">
                    {searchQuery && tasks.length > 0
                      ? 'No tasks match your search'
                      : filter === 'all' && tasks.length === 0
                      ? 'No tasks yet. Create your first task!'
                      : filter !== 'all' && tasks.length === 0
                      ? 'No tasks yet. Create one to get started!'
                      : `No ${filter.replace('_', ' ')} tasks found.`}
                  </p>
                  <p className="text-[#6B7F7A] text-sm text-center max-w-md">
                    {searchQuery && tasks.length > 0
                      ? 'Try adjusting your search terms or clear the search filter.'
                      : filter === 'all' && tasks.length === 0
                      ? 'Add your first task using the form on the left to start organizing your work.'
                      : filter !== 'all' && tasks.length === 0
                      ? 'Once you create tasks, you can filter them by status here.'
                      : 'Try changing the status filter to see more tasks.'}
                  </p>
                  {(filter !== 'all' || searchQuery) && (
                    <div className="flex gap-2 mt-2">
                      {searchQuery && (
                        <button
                          onClick={() => setSearchQuery('')}
                          className="px-3 py-2 bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676] hover:bg-[rgba(0,230,118,0.25)] rounded-lg text-sm transition-colors"
                        >
                          Clear search
                        </button>
                      )}
                      {filter !== 'all' && (
                        <button
                          onClick={() => setFilter('all')}
                          className="px-3 py-2 bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676] hover:bg-[rgba(0,230,118,0.25)] rounded-lg text-sm transition-colors"
                        >
                          View all tasks
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredTasks.map((task) => (
                  <div
                    key={task.id}
                    className="bg-[#111716] border border-[#1F2A28] rounded-lg p-5 group hover:border-[#00E676] transition-colors duration-200"
                  >
                    <div className="flex items-start gap-4">
                      {/* Checkbox */}
                      <div className="flex-shrink-0 mt-1">
                        <input
                          type="checkbox"
                          checked={task.status === 'completed'}
                          onChange={() => handleToggleTask(task)}
                          className="w-5 h-5 cursor-pointer rounded border-2 border-[#1F2A28] bg-[#0B0F0E] text-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors"
                        />
                      </div>

                      {/* Task Content */}
                      <div className="flex-1 min-w-0">
                        {/* Title */}
                        <h3
                          className={`text-base font-semibold mb-2 leading-snug ${
                            task.status === 'completed'
                              ? 'line-through text-[#6B7F7A]'
                              : 'text-[#E6F2EF]'
                          }`}
                        >
                          {task.title}
                        </h3>

                        {/* Description */}
                        {task.description && (
                          <p className="text-sm text-[#9FB3AD] leading-relaxed mb-3 line-clamp-2">
                            {task.description}
                          </p>
                        )}

                        {/* Status, Priority, and Metadata Badges */}
                        <div className="flex gap-2 flex-wrap items-center">
                          {/* Status Badge */}
                          <span
                            className={`text-xs px-2.5 py-1 rounded font-medium uppercase tracking-wide flex items-center gap-1.5 ${getStatusColor(task.status)}`}
                          >
                            {task.status === 'pending' && <Hourglass className="w-3 h-3" />}
                            {task.status === 'in_progress' && <Rocket className="w-3 h-3" />}
                            {task.status === 'completed' && <CheckCircle2 className="w-3 h-3" />}
                            {task.status === 'cancelled' && <X className="w-3 h-3" />}
                            {task.status.replace('_', ' ')}
                          </span>

                          {/* Priority Badge */}
                          <span
                            className={`text-xs px-2.5 py-1 rounded font-medium uppercase tracking-wide flex items-center gap-1.5 ${
                              task.priority === 'urgent' || task.priority === 'high'
                                ? 'bg-[#0B0F0E] border border-[#E5484D] text-[#E5484D]'
                                : 'bg-[#0B0F0E] border border-[#1F2A28] text-[#9FB3AD]'
                            }`}
                          >
                            {task.priority === 'urgent' && <Flame className="w-3 h-3" />}
                            {task.priority === 'high' && <Zap className="w-3 h-3" />}
                            {task.priority === 'medium' && <MapPin className="w-3 h-3" />}
                            {task.priority === 'low' && <Sprout className="w-3 h-3" />}
                            {task.priority}
                          </span>

                          {/* Due Date Badge */}
                          {task.due_date && (
                            <span className="text-xs px-2.5 py-1 rounded bg-[#0B0F0E] border border-[#1F2A28] text-[#9FB3AD] font-medium flex items-center gap-1.5">
                              <Calendar className="w-3 h-3" />
                              Due: {new Date(task.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                            </span>
                          )}

                          {/* Created Date Badge */}
                          {task.created_at && (
                            <span className="text-xs px-2.5 py-1 rounded bg-[#0B0F0E] border border-[#1F2A28] text-[#6B7F7A] font-medium flex items-center gap-1.5">
                              <Clock className="w-3 h-3" />
                              Created {new Date(task.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Action Buttons - Always visible on mobile, hover on desktop */}
                      <div className="flex-shrink-0 flex gap-2 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity duration-200">
                        <button
                          onClick={() => handleEditTask(task)}
                          className="p-2 bg-[rgba(0,230,118,0.15)] border border-[#00E676] text-[#00E676] hover:bg-[rgba(0,230,118,0.25)] rounded-lg transition-colors duration-200"
                          title="Edit task"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task)}
                          className="p-2 bg-transparent border border-[#E5484D] text-[#E5484D] hover:bg-[rgba(229,72,77,0.1)] rounded-lg transition-colors duration-200"
                          title="Delete task"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {taskToDelete && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
            <div className="bg-[#151C1B] border border-[#1F2A28] rounded-lg max-w-md w-full">
              <div className="p-6">
                <div className="flex items-center justify-center w-14 h-14 bg-transparent border border-[#E5484D] rounded-full mx-auto mb-4">
                  <AlertTriangle className="w-7 h-7 text-[#E5484D]" />
                </div>

                <h2 className="text-xl font-semibold text-[#E6F2EF] mb-3 text-center">Delete Task?</h2>

                <p className="text-[#9FB3AD] text-sm mb-2 text-center">
                  Are you sure you want to delete
                </p>
                <p className="text-[#E6F2EF] font-medium mb-6 text-center px-4 py-2 bg-[#111716] border border-[#1F2A28] rounded-lg text-sm">
                  "{taskToDelete.title}"
                </p>
                <p className="text-sm text-[#E5484D] mb-6 text-center">
                  This action cannot be undone.
                </p>

                <div className="flex gap-3">
                  <button
                    onClick={() => setTaskToDelete(null)}
                    className="flex-1 px-4 py-2.5 bg-transparent border-2 border-[#00E676] text-[#00E676] rounded-lg font-medium hover:bg-[rgba(0,230,118,0.1)] transition-colors duration-200 text-sm"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmDeleteTask}
                    className="flex-1 px-4 py-2.5 bg-transparent border border-[#E5484D] text-[#E5484D] rounded-lg font-medium hover:bg-[rgba(229,72,77,0.1)] transition-colors duration-200 text-sm"
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
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
            <div className="bg-[#151C1B] border border-[#1F2A28] rounded-lg max-w-lg w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-[#00E676] rounded-lg flex items-center justify-center">
                    <Edit2 className="w-5 h-5 text-[#0B0F0E]" />
                  </div>
                  <h2 className="text-lg font-semibold text-[#E6F2EF]">Edit Task</h2>
                </div>

                <div className="space-y-5">
                  {/* Title Field */}
                  <div>
                    <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                      Task Title
                    </label>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none placeholder-[#6B7F7A] text-sm"
                      placeholder="Task title"
                      disabled={isEditSubmitting}
                    />
                  </div>

                  {/* Description Field */}
                  <div>
                    <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                      Description
                    </label>
                    <textarea
                      value={editDescription}
                      onChange={(e) => setEditDescription(e.target.value)}
                      className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none placeholder-[#6B7F7A] resize-none text-sm"
                      placeholder="Add task details"
                      rows={4}
                      disabled={isEditSubmitting}
                      maxLength={5000}
                    />
                    <p className="text-xs text-[#6B7F7A] mt-2">
                      {editDescription.length} / 5000
                    </p>
                  </div>

                  {/* Status and Priority in Grid */}
                  <div className="grid grid-cols-2 gap-4">
                    {/* Status Dropdown */}
                    <div>
                      <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                        Status
                      </label>
                      <select
                        value={editStatus}
                        onChange={(e) => setEditStatus(e.target.value as TaskStatus)}
                        className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none text-sm"
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
                      <label className="block text-sm font-medium text-[#E6F2EF] mb-2">
                        Priority
                      </label>
                      <select
                        value={editPriority}
                        onChange={(e) => setEditPriority(e.target.value as TaskPriority)}
                        className="w-full px-4 py-2.5 bg-[#0B0F0E] border border-[#1F2A28] text-[#E6F2EF] rounded-lg focus:border-[#00E676] focus:ring-2 focus:ring-[rgba(0,230,118,0.15)] transition-colors duration-200 outline-none text-sm"
                        disabled={isEditSubmitting}
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                        <option value="urgent">Urgent</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleCancelEdit}
                    disabled={isEditSubmitting}
                    className="flex-1 px-4 py-2.5 bg-transparent border-2 border-[#00E676] text-[#00E676] rounded-lg font-medium hover:bg-[rgba(0,230,118,0.1)] transition-colors duration-200 disabled:opacity-50 text-sm"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveEdit}
                    disabled={isEditSubmitting || !editTitle.trim()}
                    className="flex-1 px-4 py-2.5 bg-[#00E676] text-[#0B0F0E] rounded-lg font-medium hover:bg-[#00C965] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
                  >
                    {isEditSubmitting ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4" />
                        Save Changes
                      </>
                    )}
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
