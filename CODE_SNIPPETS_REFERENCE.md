# Code Snippets Reference - Frontend Schema Update

## Quick Code Lookup

Use this document to quickly find and reference specific code changes.

---

## API Client Changes

### New Task Interface

**File**: `/frontend/src/lib/api.ts` (lines 40-51)

```typescript
interface Task {
  id: number;              // Changed from: string (UUID)
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;      // Changed from: status: 'pending' | ... (removed)
  priority: string;        // Changed from: 'low' | 'medium' | 'high' | 'urgent'
  due_date?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

### New Request Types

**File**: `/frontend/src/lib/api.ts` (lines 53-69)

```typescript
interface TaskCreateRequest {
  title: string;
  description?: string;
  completed?: boolean;     // NEW: was status
  priority?: string;
  due_date?: string;
  tags?: string[];
}

interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;     // NEW: was status
  priority?: string;
  due_date?: string;
  tags?: string[];
}
```

### Updated PaginationParams

**File**: `/frontend/src/lib/api.ts` (lines 71-78)

```typescript
interface PaginationParams {
  skip?: number;
  limit?: number;
  completed?: boolean;     // Changed from: status?: string
  priority?: string;
  sort_by?: string;
  order?: 'asc' | 'desc';
}
```

### Updated getTasks Method

**File**: `/frontend/src/lib/api.ts` (lines 224-243)

```typescript
async getTasks(params: PaginationParams = {}): Promise<{ items: Task[]; total: number }> {
  const queryParams = new URLSearchParams();
  if (params.skip !== undefined) queryParams.append('skip', params.skip.toString());
  if (params.limit !== undefined) queryParams.append('limit', params.limit.toString());
  if (params.completed !== undefined) queryParams.append('completed', params.completed.toString());
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
```

### Updated Method Signatures

**File**: `/frontend/src/lib/api.ts`

```typescript
// Changed from: async getTask(taskId: string): Promise<Task>
async getTask(taskId: number): Promise<Task> {
  // ...
}

// Changed from: async updateTask(taskId: string, ...): Promise<Task>
async updateTask(taskId: number, data: TaskUpdateRequest): Promise<Task> {
  // ...
}

// Changed from: async patchTask(taskId: string, ...): Promise<Task>
async patchTask(taskId: number, data: Partial<TaskUpdateRequest>): Promise<Task> {
  // ...
}

// Changed from: async deleteTask(taskId: string): Promise<void>
async deleteTask(taskId: number): Promise<void> {
  // ...
}
```

### New toggleTask Method

**File**: `/frontend/src/lib/api.ts` (lines 310-321)

```typescript
async toggleTask(taskId: number): Promise<Task> {
  const response = await this.fetch(`/api/tasks/${taskId}/toggle`, {
    method: 'PATCH',
  });

  if (!response.ok) {
    throw new Error('Failed to toggle task');
  }

  return response.json();
}
```

---

## Component Changes

### State Declarations

**File**: `/frontend/src/app/tasks/page.tsx` (lines 9-33)

```typescript
export default function TasksPage() {
  const router = useRouter();
  const { isAuthenticated, logout, checkAuth } = useAuthStore();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [newTaskCompleted, setNewTaskCompleted] = useState(false);  // NEW
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');  // Changed

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editCompleted, setEditCompleted] = useState(false);  // Changed from editStatus
  const [editPriority, setEditPriority] = useState('medium');  // Changed type
  const [isEditSubmitting, setIsEditSubmitting] = useState(false);

  // Delete confirmation state
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);
  // ...
}
```

### Load Tasks Logic

**File**: `/frontend/src/app/tasks/page.tsx` (lines 48-64)

```typescript
const loadTasks = async () => {
  setIsLoading(true);
  setError('');
  try {
    const params: any = {};
    if (filter === 'completed') {
      params.completed = true;
    } else if (filter === 'pending') {
      params.completed = false;
    }
    const response = await apiClient.getTasks(params);
    setTasks(response.items);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to load tasks';
    setError(message);
  } finally {
    setIsLoading(false);
  }
};
```

### Create Task Handler

**File**: `/frontend/src/app/tasks/page.tsx` (lines 66-87)

```typescript
const handleAddTask = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!newTaskTitle.trim()) return;

  setIsAddingTask(true);
  try {
    const newTask = await apiClient.createTask({
      title: newTaskTitle,
      description: newTaskDescription || undefined,
      completed: newTaskCompleted,  // NEW
      priority: 'medium',
    });
    setTasks([newTask, ...tasks]);
    setNewTaskTitle('');
    setNewTaskDescription('');
    setNewTaskCompleted(false);  // NEW
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to create task';
    setError(message);
  } finally {
    setIsAddingTask(false);
  }
};
```

### Toggle Task Handler

**File**: `/frontend/src/app/tasks/page.tsx` (lines 88-97)

```typescript
const handleToggleTask = async (task: Task) => {
  try {
    const updated = await apiClient.toggleTask(task.id);  // NEW: dedicated endpoint
    setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to toggle task';
    setError(message);
  }
};
```

### Edit Task Handler

**File**: `/frontend/src/app/tasks/page.tsx` (lines 117-123)

```typescript
const handleEditTask = (task: Task) => {
  setEditingTask(task);
  setEditTitle(task.title);
  setEditDescription(task.description || '');
  setEditCompleted(task.completed);  // Changed from: task.status as TaskStatus
  setEditPriority(task.priority);    // Changed from: task.priority as TaskPriority
};
```

### Save Edit Handler

**File**: `/frontend/src/app/tasks/page.tsx` (lines 125-145)

```typescript
const handleSaveEdit = async () => {
  if (!editingTask || !editTitle.trim()) return;

  setIsEditSubmitting(true);
  try {
    const updated = await apiClient.patchTask(editingTask.id, {
      title: editTitle,
      description: editDescription || undefined,
      completed: editCompleted,  // Changed from: status: editStatus
      priority: editPriority,
    });

    setTasks(tasks.map((t) => (t.id === editingTask.id ? updated : t)));
    setEditingTask(null);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to update task';
    setError(message);
  } finally {
    setIsEditSubmitting(false);
  }
};
```

### Filter Logic

**File**: `/frontend/src/app/tasks/page.tsx` (lines 155-168)

```typescript
const filteredTasks = tasks.filter((task) => {
  if (filter === 'all') return true;
  if (filter === 'completed') return task.completed;
  if (filter === 'pending') return !task.completed;
  return true;
});

const getCompletionBadge = (completed: boolean) => {
  if (completed) {
    return 'bg-green-100 text-green-800';
  }
  return 'bg-yellow-100 text-yellow-800';
};
```

---

## UI Components

### Filter Buttons

**File**: `/frontend/src/app/tasks/page.tsx` (lines 262-281)

```typescript
<div className="flex gap-2 mb-6 flex-wrap">
  <button
    onClick={() => setFilter('all')}
    className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'all' ? 'btn-primary' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
  >
    All
  </button>
  <button
    onClick={() => setFilter('pending')}
    className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'pending' ? 'btn-primary' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
  >
    Todo
  </button>
  <button
    onClick={() => setFilter('completed')}
    className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'completed' ? 'btn-primary' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
  >
    Done
  </button>
</div>
```

### Create Form with Completed Checkbox

**File**: `/frontend/src/app/tasks/page.tsx` (lines 239-255)

```typescript
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
  <label className="flex items-center gap-2 cursor-pointer">
    <input
      type="checkbox"
      checked={newTaskCompleted}
      onChange={(e) => setNewTaskCompleted(e.target.checked)}
      disabled={isAddingTask}
      className="w-4 h-4"
    />
    <span className="text-sm text-gray-700">Mark as completed</span>
  </label>
  <button
    type="submit"
    disabled={isAddingTask || !newTaskTitle.trim()}
    className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
  >
    {isAddingTask ? 'Adding...' : 'Add Task'}
  </button>
</form>
```

### Task Card Display

**File**: `/frontend/src/app/tasks/page.tsx` (lines 300-334)

```typescript
<div className="space-y-3">
  {filteredTasks.map((task) => (
    <div key={task.id} className="card flex items-start gap-4 group hover:shadow-lg transition-shadow">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => handleToggleTask(task)}
        className="mt-1 w-5 h-5 cursor-pointer"
      />
      <div className="flex-1 min-w-0">
        <h3
          className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-600 mt-1 line-clamp-2">
            {task.description}
          </p>
        )}
        <div className="flex gap-2 mt-2 flex-wrap">
          <span className={`text-xs px-2 py-1 rounded-full ${getCompletionBadge(task.completed)}`}>
            {task.completed ? '✓ Done' : '○ Todo'}
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
```

### Edit Modal - Completed Checkbox

**File**: `/frontend/src/app/tasks/page.tsx` (lines 422-435)

```typescript
{/* Completed Checkbox */}
<div>
  <label className="flex items-center gap-2 cursor-pointer">
    <input
      type="checkbox"
      checked={editCompleted}
      onChange={(e) => setEditCompleted(e.target.checked)}
      disabled={isEditSubmitting}
      className="w-4 h-4"
    />
    <span className="text-sm font-medium text-gray-700">Completed</span>
  </label>
</div>

{/* Priority Dropdown */}
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Priority
  </label>
  <select
    value={editPriority}
    onChange={(e) => setEditPriority(e.target.value)}
    className="input-base"
    disabled={isEditSubmitting}
  >
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
    <option value="urgent">Urgent</option>
  </select>
</div>
```

---

## Type Definitions Removed

**File**: `/frontend/src/app/tasks/page.tsx` (lines 1-10)

```typescript
// REMOVED - No longer needed
// type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';
// type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';

// REPLACED with:
export default function TasksPage() {
  // ... component code uses direct types (number, boolean, string)
}
```

---

## API Usage Examples

### Create a Task

```typescript
// OLD
const task = await apiClient.createTask({
  title: 'Buy groceries',
  status: 'pending',      // Enum
  priority: 'medium',
});

// NEW
const task = await apiClient.createTask({
  title: 'Buy groceries',
  completed: false,       // Boolean (optional, defaults to false)
  priority: 'medium',
});
```

### Update a Task

```typescript
// OLD
const updated = await apiClient.patchTask(taskId: string, {
  status: 'completed',    // Must send status
  priority: 'high',
});

// NEW
const updated = await apiClient.patchTask(taskId: number, {
  completed: true,        // Boolean
  priority: 'high',
});
```

### Toggle Task Completion

```typescript
// OLD (not available - had to patch with status)
const newStatus = task.status === 'completed' ? 'pending' : 'completed';
const updated = await apiClient.patchTask(task.id, { status: newStatus });

// NEW (dedicated endpoint)
const updated = await apiClient.toggleTask(task.id);
// Returns: task with completed flipped (true → false, false → true)
```

### List Tasks with Filtering

```typescript
// OLD
const response = await apiClient.getTasks({
  status: 'pending',  // String enum value
});

// NEW
const response = await apiClient.getTasks({
  completed: false,   // Boolean
});
```

---

## Common Patterns

### State Management Pattern

```typescript
// Before: Complex enum state
const [status, setStatus] = useState<TaskStatus>('pending');
const newStatus = status === 'completed' ? 'pending' : 'completed';

// After: Simple boolean state
const [completed, setCompleted] = useState(false);
const newCompleted = !completed;
```

### Rendering Pattern

```typescript
// Before: Enum-based switch
const statusColor = (() => {
  switch (task.status) {
    case 'completed': return 'green';
    case 'pending': return 'yellow';
    // ... more cases
  }
})();

// After: Boolean-based ternary
const statusColor = task.completed ? 'green' : 'yellow';
```

### Filtering Pattern

```typescript
// Before: Filter by enum string
const filtered = tasks.filter(t => t.status === filterStatus);

// After: Filter by boolean
const filtered = filter === 'completed'
  ? tasks.filter(t => t.completed)
  : tasks.filter(t => !t.completed);
```

---

## Compilation & Build Commands

### Build Frontend

```bash
cd /home/usmankhan/projects/hackathon\ II/todo-app/frontend
npm run build
```

**Expected Output**:
```
✓ Compiled successfully
✓ Running TypeScript
✓ Generating static pages
Route (app)
├ ○ /
├ ○ /login
├ ○ /signup
└ ○ /tasks
```

### Development Server

```bash
cd /home/usmankhan/projects/hackathon\ II/todo-app/frontend
npm run dev
```

Then visit: `http://localhost:3000`

---

## Troubleshooting Code

### If TypeScript Errors

Check these common issues:

```typescript
// ERROR: Property 'status' does not exist on type 'Task'
// FIX: Use 'completed' instead
task.completed  // ✓ Correct

// ERROR: Cannot assign type 'string' to type 'number'
// FIX: Task ID is now number, not string
const id: number = task.id;  // ✓ Correct

// ERROR: Type 'string' is not assignable to type 'boolean'
// FIX: completed is boolean, not string
const completed: boolean = task.completed;  // ✓ Correct
```

### If API Errors

```typescript
// ERROR: 404 on PATCH /api/tasks/{id}/toggle
// FIX: Backend must implement toggle endpoint
// See: BACKEND_INTEGRATION_CHECKLIST.md

// ERROR: Response has 'status' field but UI expects 'completed'
// FIX: Backend must remove status field, add completed field
// See: BACKEND_INTEGRATION_CHECKLIST.md

// ERROR: Task ID is string, expected number
// FIX: Backend must return integer IDs (SERIAL)
// See: BACKEND_INTEGRATION_CHECKLIST.md
```

---

## File Locations

### API Client
- **Location**: `/home/usmankhan/projects/hackathon II/todo-app/frontend/src/lib/api.ts`
- **Lines**: 40-331
- **Key Sections**:
  - Task interface: 40-51
  - Request types: 53-78
  - getTasks: 224-243
  - toggleTask: 310-321

### Tasks Page
- **Location**: `/home/usmankhan/projects/hackathon II/todo-app/frontend/src/app/tasks/page.tsx`
- **Lines**: 1-473
- **Key Sections**:
  - State: 9-33
  - Handlers: 48-150
  - Filter logic: 155-168
  - UI components: 220-470

---

**Last Updated**: 2024-01-23
**Commit**: `854e793`
**Branch**: `002-user-auth`
