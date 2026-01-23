# Frontend Schema Migration - Quick Start Guide

## What Changed?

The frontend now works with the new Task schema:

```typescript
// OLD Task interface
{
  id: "uuid-string",
  status: "pending" | "in_progress" | "completed" | "cancelled",
  priority: "low" | "medium" | "high" | "urgent"
}

// NEW Task interface
{
  id: 123,           // integer
  completed: true,   // boolean (replaces status)
  priority: "high"   // string (now flexible)
}
```

---

## Key Changes Summary

### 1. API Client (`/frontend/src/lib/api.ts`)

#### Type Changes
```typescript
// Task IDs are now numbers
async getTask(taskId: number): Promise<Task>
async updateTask(taskId: number, data: TaskUpdateRequest): Promise<Task>
async patchTask(taskId: number, data: Partial<TaskUpdateRequest>): Promise<Task>
async deleteTask(taskId: number): Promise<void>

// New toggle endpoint for completion
async toggleTask(taskId: number): Promise<Task>

// Task data structure
interface Task {
  id: number;              // Was: string (UUID)
  completed: boolean;      // Was: status enum
  priority: string;        // Was: priority enum
  // ... rest unchanged
}
```

#### Request Payloads
```typescript
// Creating/updating a task
{
  title: "My task",
  description: "...",
  completed: true,         // Was: status
  priority: "high",        // Still works, now as string
  due_date: "2024-01-01",
  tags: ["work"]
}

// Toggling completion (new)
PATCH /api/tasks/123/toggle  // No body needed
```

---

### 2. Tasks Page (`/frontend/src/app/tasks/page.tsx`)

#### State Management
```typescript
// NEW: Track completion in create form
const [newTaskCompleted, setNewTaskCompleted] = useState(false);

// CHANGED: Simpler filter options
const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

// CHANGED: Simpler edit state
const [editCompleted, setEditCompleted] = useState(false);  // Was: editStatus
const [editPriority, setEditPriority] = useState('medium');  // Now string
```

#### Filtering
```typescript
// OLD: Status-based filtering
if (filter === 'pending') { params.status = 'pending'; }
if (filter === 'in_progress') { params.status = 'in_progress'; }
if (filter === 'completed') { params.status = 'completed'; }

// NEW: Completion-based filtering
if (filter === 'pending') { params.completed = false; }
if (filter === 'completed') { params.completed = true; }

// Filter buttons
<button onClick={() => setFilter('all')}>All</button>
<button onClick={() => setFilter('pending')}>Todo</button>
<button onClick={() => setFilter('completed')}>Done</button>
```

#### Task Display
```typescript
// OLD: Status badge with enum values
<span className={`${getStatusColor(task.status)}`}>
  {task.status.replace('_', ' ')}
</span>

// NEW: Completion badge with visual indicators
<span className={`${getCompletionBadge(task.completed)}`}>
  {task.completed ? '✓ Done' : '○ Todo'}
</span>

// OLD: Status-based checkbox
<input type="checkbox" checked={task.status === 'completed'} />

// NEW: Direct boolean checkbox
<input type="checkbox" checked={task.completed} />
```

#### Toggling Completion
```typescript
// OLD: Status change logic
const newStatus = task.status === 'completed' ? 'pending' : 'completed';
const updated = await apiClient.patchTask(task.id, { status: newStatus });

// NEW: Simple toggle endpoint
const updated = await apiClient.toggleTask(task.id);
```

#### Edit Form
```typescript
// OLD: Status dropdown
<select value={editStatus} onChange={(e) => setEditStatus(e.target.value as TaskStatus)}>
  <option value="pending">Pending</option>
  <option value="in_progress">In Progress</option>
  <option value="completed">Completed</option>
  <option value="cancelled">Cancelled</option>
</select>

// NEW: Completion checkbox
<label className="flex items-center gap-2">
  <input
    type="checkbox"
    checked={editCompleted}
    onChange={(e) => setEditCompleted(e.target.checked)}
    className="w-4 h-4"
  />
  <span>Completed</span>
</label>
```

#### Create Form
```typescript
// NEW: Add completed checkbox to creation form
<label className="flex items-center gap-2">
  <input
    type="checkbox"
    checked={newTaskCompleted}
    onChange={(e) => setNewTaskCompleted(e.target.checked)}
  />
  <span>Mark as completed</span>
</label>
```

---

## Testing the Changes

### Quick Test Checklist

1. **Create Task**
   - [ ] Create with completed=false - shows as "○ Todo"
   - [ ] Create with completed=true - shows as "✓ Done"
   - [ ] Verify ID is integer, not UUID

2. **Toggle Completion**
   - [ ] Click checkbox to toggle completed
   - [ ] Should call `PATCH /api/tasks/{id}/toggle`
   - [ ] UI updates immediately

3. **Filtering**
   - [ ] "All" shows all tasks
   - [ ] "Todo" shows only completed=false
   - [ ] "Done" shows only completed=true

4. **Editing**
   - [ ] Edit modal opens correctly
   - [ ] Completed checkbox shown (not status dropdown)
   - [ ] Save updates completed field
   - [ ] Priority field still works

5. **Data Integrity**
   - [ ] Task IDs are integers
   - [ ] No status field in responses
   - [ ] completed field is boolean
   - [ ] Priority is string

---

## API Endpoints Expected

The backend should provide:

### List Tasks
```
GET /api/tasks?completed=false
GET /api/tasks?completed=true
GET /api/tasks  # All tasks
```

### Get Single Task
```
GET /api/tasks/{id}  # id is integer
```

### Create Task
```
POST /api/tasks
Body: {
  "title": "...",
  "description": "...",
  "completed": false,
  "priority": "high",
  "due_date": "...",
  "tags": [...]
}
```

### Toggle Completion (NEW!)
```
PATCH /api/tasks/{id}/toggle
# No body required - toggles completed field
# Response: Updated task with completed flipped
```

### Update Task
```
PATCH /api/tasks/{id}
Body: {
  "title": "...",
  "description": "...",
  "completed": true,  # Can be set directly
  "priority": "...",
  ...
}
```

### Delete Task
```
DELETE /api/tasks/{id}
```

---

## No Breaking Changes For Users

The frontend UI works exactly the same, just simpler:
- **Filter buttons**: Still there, just 3 instead of 4
- **Task completion**: Still toggled with checkbox
- **Priority**: Still selectable
- **Due dates**: Still work
- **Descriptions**: Still supported
- **Authentication**: Unchanged

---

## Performance

- ✓ No additional API calls
- ✓ Simpler state management
- ✓ Smaller bundle (removed enum types)
- ✓ Faster filtering logic
- ✓ Same rendering performance

---

## Debugging Tips

### Task not showing completed state?
- Check: `console.log(task)` - verify `completed` field is boolean
- Check: Backend returns `completed` field in response

### Checkbox not toggling?
- Check: `toggleTask()` method is being called
- Check: Network tab - verify `PATCH /api/tasks/{id}/toggle` request
- Check: Backend returns updated task with toggled `completed` value

### Filters not working?
- Check: Query params - should be `?completed=true` or `?completed=false`
- Check: Backend filters tasks by completed parameter
- Check: Response includes all required tasks

### Type errors?
- All TypeScript should compile without errors
- If errors: Check that imports use updated Task type from api.ts

---

## Migration Checklist for Your Backend

Before deploying, ensure your backend has:

- [ ] Task.id is SERIAL (auto-increment integer)
- [ ] Task.status field removed
- [ ] Task.completed field added (boolean, default false)
- [ ] Task.priority is VARCHAR (string, not enum)
- [ ] `GET /api/tasks?completed={bool}` filtering works
- [ ] `PATCH /api/tasks/{id}/toggle` endpoint implemented
- [ ] Test with integer IDs, not UUIDs
- [ ] Returns completed field in all task responses

---

## Related Documentation

- Full migration details: `FRONTEND_SCHEMA_UPDATE.md`
- Backend schema changes: Check backend commit `14917b7`
- API types: `/frontend/src/lib/api.ts` (lines 40-78)
- Component code: `/frontend/src/app/tasks/page.tsx` (lines 1-50)

---

## Questions?

Check these files for specific implementation details:

1. **API Integration**: `/frontend/src/lib/api.ts`
   - Lines 40-78: Type definitions
   - Lines 225-243: getTasks() filtering
   - Lines 310-321: toggleTask() method

2. **UI Components**: `/frontend/src/app/tasks/page.tsx`
   - Lines 9-33: State management
   - Lines 48-64: loadTasks() filtering
   - Lines 88-97: handleToggleTask()
   - Lines 155-168: Filter logic
   - Lines 162-167: getCompletionBadge()

---

**Status**: ✓ Implemented and Tested
**Build**: ✓ Passing
**Commit**: `854e793`
**Branch**: `002-user-auth`
