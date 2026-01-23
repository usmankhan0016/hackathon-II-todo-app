# Backend Integration Checklist - Task Schema Update

## Overview

The frontend has been updated to work with the new Task schema. This document provides a checklist for integrating these changes with the backend API.

**Frontend Commit**: `854e793` - refactor: Update frontend for new Task schema with boolean completed field
**Backend Status**: Ready for implementation

---

## Expected API Response Format

### New Task Response Format

The frontend expects responses in this format:

```json
{
  "id": 123,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "priority": "high",
  "due_date": "2024-01-31",
  "tags": ["tag1", "tag2"],
  "created_at": "2024-01-23T10:00:00Z",
  "updated_at": "2024-01-23T10:00:00Z"
}
```

### Key Requirements

- `id`: **Integer** (SERIAL), not UUID string
- `completed`: **Boolean** (true/false), not status enum
- `priority`: **String** (flexible), was enum
- `status` field: **MUST NOT** be present
- All timestamps: ISO 8601 format

---

## API Endpoints to Implement

### 1. List Tasks (GET)

#### Request
```http
GET /api/tasks
GET /api/tasks?completed=false
GET /api/tasks?completed=true
GET /api/tasks?priority=high
GET /api/tasks?skip=0&limit=10
```

#### Query Parameters
- `completed`: **Optional boolean** - Filter by completion state
- `priority`: **Optional string** - Filter by priority
- `skip`: **Optional integer** - Pagination offset (default: 0)
- `limit`: **Optional integer** - Page size (default: 10)
- `sort_by`: **Optional string** - Sort field
- `order`: **Optional string** - 'asc' or 'desc'

#### Response
```json
{
  "items": [
    {
      "id": 1,
      "completed": false,
      ...
    }
  ],
  "total": 42
}
```

#### Status Code
- `200 OK` - Success
- `401 Unauthorized` - Invalid token
- `400 Bad Request` - Invalid parameters

#### Notes
- Must filter by user_id from JWT token
- `completed` parameter should be boolean, not string
- Response must include `total` count

---

### 2. Get Single Task (GET)

#### Request
```http
GET /api/tasks/{id}
```

#### Path Parameters
- `id`: **Integer** - Task ID (SERIAL)

#### Response
```json
{
  "id": 123,
  "user_id": "...",
  "title": "Task title",
  "description": "...",
  "completed": false,
  "priority": "high",
  "due_date": "2024-01-31",
  "tags": [],
  "created_at": "...",
  "updated_at": "..."
}
```

#### Status Codes
- `200 OK` - Task found
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - Task belongs to different user
- `404 Not Found` - Task doesn't exist

#### Notes
- Verify task belongs to authenticated user
- Return 403 (not 404) if user doesn't own task

---

### 3. Create Task (POST)

#### Request
```http
POST /api/tasks
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "due_date": "2024-01-31",
  "tags": ["shopping"]
}
```

#### Request Body
```typescript
{
  "title": string,                  // Required, 1-500 chars
  "description": string,            // Optional, max 5000 chars
  "completed": boolean,             // Optional, default false
  "priority": string,               // Optional, e.g. "high"
  "due_date": string,              // Optional, ISO 8601
  "tags": string[]                 // Optional array
}
```

#### Response
```json
{
  "id": 123,
  "user_id": "uuid...",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "due_date": "2024-01-31T00:00:00Z",
  "tags": ["shopping"],
  "created_at": "2024-01-23T10:00:00Z",
  "updated_at": "2024-01-23T10:00:00Z"
}
```

#### Status Codes
- `201 Created` - Task created successfully
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid token

#### Notes
- User ID from JWT token, not request
- ID auto-generated (SERIAL)
- Default `completed` to false if not provided
- Validate title is not empty

---

### 4. Update Task (PUT)

#### Request
```http
PUT /api/tasks/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "due_date": "2024-02-01",
  "tags": ["updated"]
}
```

#### Path Parameters
- `id`: **Integer** - Task ID

#### Request Body
- Same as Create (all fields optional)

#### Response
- Same as Get Single Task

#### Status Codes
- `200 OK` - Updated successfully
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - Task belongs to different user
- `404 Not Found` - Task doesn't exist

#### Notes
- Full replacement (not partial)
- Verify task ownership
- Must return completed as boolean

---

### 5. Partial Update (PATCH)

#### Request
```http
PATCH /api/tasks/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "completed": true,
  "priority": "high"
}
```

#### Path Parameters
- `id`: **Integer** - Task ID

#### Request Body
- Any subset of task fields (all optional)

#### Response
- Same as Get Single Task (full task object)

#### Status Codes
- `200 OK` - Updated successfully
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - Task belongs to different user
- `404 Not Found` - Task doesn't exist

#### Notes
- Partial update (only sent fields updated)
- Still return full task object
- Must return completed as boolean

---

### 6. Toggle Task Completion (PATCH) **[NEW]**

#### Request
```http
PATCH /api/tasks/{id}/toggle
Authorization: Bearer {token}
```

#### Path Parameters
- `id`: **Integer** - Task ID

#### Request Body
- **None** (empty body)

#### Response
```json
{
  "id": 123,
  "user_id": "...",
  "title": "Task title",
  "completed": true,  // Flipped from false
  "priority": "...",
  ...
}
```

#### Status Codes
- `200 OK` - Toggled successfully
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - Task belongs to different user
- `404 Not Found` - Task doesn't exist

#### Notes
- **NEW ENDPOINT** - Frontend expects this
- Flips `completed` boolean (true → false, false → true)
- Most common operation - optimized for speed
- No body required
- Returns updated task with flipped completion

---

### 7. Delete Task (DELETE)

#### Request
```http
DELETE /api/tasks/{id}
Authorization: Bearer {token}
```

#### Path Parameters
- `id`: **Integer** - Task ID

#### Response
- Empty body

#### Status Codes
- `204 No Content` - Deleted successfully
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - Task belongs to different user
- `404 Not Found` - Task doesn't exist

#### Notes
- Verify task ownership before deletion
- Return 204 (No Content) on success
- No response body needed

---

## TypeScript Request/Response Models

### Expected Pydantic/FastAPI Models

```python
# Response model - what frontend expects
class TaskResponse(BaseModel):
    id: int  # SERIAL integer
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool  # Boolean, not enum!
    priority: str  # String, not enum
    due_date: Optional[str] = None
    tags: List[str] = []
    created_at: str
    updated_at: str

# Create/Update request model
class TaskRequest(BaseModel):
    title: str  # Required for POST
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[List[str]] = []

# List response
class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
```

---

## Database Schema Requirements

### Task Table Structure

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,  -- Auto-increment integer
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  description TEXT,  -- Max 5000 chars
  completed BOOLEAN DEFAULT false,  -- Boolean, not status enum!
  priority VARCHAR(50),  -- String, flexible
  due_date TIMESTAMP,
  tags TEXT[],  -- Array
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- Constraints
  CONSTRAINT title_not_empty CHECK (LENGTH(title) > 0),
  CONSTRAINT title_max_length CHECK (LENGTH(title) <= 500),
  CONSTRAINT description_max_length CHECK (description IS NULL OR LENGTH(description) <= 5000)
);

-- Indexes for common queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
CREATE INDEX idx_tasks_user_due_date ON tasks(user_id, due_date);
```

### Migration from Old Schema

If migrating from status enum:

```sql
-- Add completed column
ALTER TABLE tasks ADD COLUMN completed BOOLEAN DEFAULT false;

-- Migrate data (adjust logic as needed)
UPDATE tasks
SET completed = (status IN ('completed', 'in_progress'))
WHERE completed = false;

-- Remove old status column
ALTER TABLE tasks DROP COLUMN status;

-- Add constraints
ALTER TABLE tasks ADD CONSTRAINT completed_not_null NOT NULL DEFAULT false;
```

---

## Frontend Testing Requirements

Before declaring complete, test these scenarios:

### 1. Task Listing
- [ ] GET /api/tasks returns tasks with `id` as integer
- [ ] GET /api/tasks?completed=false returns incomplete tasks
- [ ] GET /api/tasks?completed=true returns completed tasks
- [ ] Response includes `total` count
- [ ] Tasks do not have `status` field

### 2. Task Creation
- [ ] POST /api/tasks creates task with `completed: false` by default
- [ ] POST with `completed: true` creates completed task
- [ ] Created task has auto-generated integer ID
- [ ] Response includes all expected fields

### 3. Task Retrieval
- [ ] GET /api/tasks/{id} returns single task
- [ ] Task ID is integer
- [ ] Completed field is boolean
- [ ] Returns 404 for non-existent task
- [ ] Returns 403 for other user's task

### 4. Task Update (PATCH)
- [ ] PATCH /api/tasks/{id} with `{completed: true}` works
- [ ] Returns updated task with flipped completion
- [ ] Can update multiple fields at once
- [ ] Returns 404 for non-existent task

### 5. Task Toggle (NEW)
- [ ] PATCH /api/tasks/{id}/toggle toggles completion
- [ ] No request body needed
- [ ] Returns updated task with flipped `completed`
- [ ] Actually flips the value (true → false, false → true)
- [ ] Returns 404 for non-existent task

### 6. Task Deletion
- [ ] DELETE /api/tasks/{id} removes task
- [ ] Returns 204 No Content
- [ ] Task no longer exists (404 on GET)
- [ ] Returns 403 for other user's task

### 7. User Isolation
- [ ] User A cannot see User B's tasks
- [ ] User A cannot update User B's tasks
- [ ] User A cannot delete User B's tasks
- [ ] Filtering returns only user's tasks

### 8. Frontend Integration
- [ ] Create task shows as "○ Todo"
- [ ] Mark as completed shows as "✓ Done"
- [ ] Toggle checkbox flips completion
- [ ] Filter buttons work (All, Todo, Done)
- [ ] Edit modal shows completed checkbox

---

## Error Handling

### Expected Error Responses

```json
{
  "detail": "Invalid input"
}
```

or

```json
{
  "detail": "Task not found"
}
```

### Frontend Expects

- `400 Bad Request` for invalid input
- `401 Unauthorized` for missing/invalid token
- `403 Forbidden` for permission denied
- `404 Not Found` for non-existent resource

---

## Implementation Order

1. **Update Database Schema**
   - [ ] Add `completed` column (boolean)
   - [ ] Remove `status` column
   - [ ] Change `id` to SERIAL if not already
   - [ ] Change `priority` to VARCHAR if it's enum
   - [ ] Run migrations

2. **Update Models**
   - [ ] Remove `status` field from Task model
   - [ ] Add `completed` field (boolean)
   - [ ] Change `id` type to integer
   - [ ] Change `priority` type to string

3. **Implement Endpoints**
   - [ ] GET /api/tasks (with completed filtering)
   - [ ] GET /api/tasks/{id}
   - [ ] POST /api/tasks
   - [ ] PUT /api/tasks/{id}
   - [ ] PATCH /api/tasks/{id}
   - [ ] **NEW**: PATCH /api/tasks/{id}/toggle
   - [ ] DELETE /api/tasks/{id}

4. **Test Endpoints**
   - [ ] Unit tests for model conversion
   - [ ] Integration tests for all endpoints
   - [ ] User isolation tests
   - [ ] Edge case tests

5. **Integrate with Frontend**
   - [ ] Run frontend with live backend
   - [ ] Create, read, update, delete tasks
   - [ ] Toggle completion
   - [ ] Filter by completion status
   - [ ] Edit tasks
   - [ ] Verify no `status` field errors

---

## Verification Checklist

### Before Declaring Complete

- [ ] All 6 main endpoints implemented
- [ ] Toggle endpoint works
- [ ] All endpoints return correct response format
- [ ] Completed field is boolean (not string)
- [ ] No status field in responses
- [ ] Task IDs are integers
- [ ] User isolation verified
- [ ] Error responses are correct format
- [ ] Frontend passes all tests
- [ ] No console errors in frontend
- [ ] Frontend build succeeds
- [ ] All CRUD operations work end-to-end

---

## Quick Reference: What Changed in Frontend

```typescript
// OLD: Enum-based status
task.status === 'completed'        // false, pending, in_progress, completed, cancelled

// NEW: Boolean completion
task.completed === true            // Just true or false
```

```typescript
// OLD: Status in create
{ title: "...", status: "pending", ... }

// NEW: Completed in create
{ title: "...", completed: false, ... }
```

```typescript
// OLD: Filtering by status
GET /api/tasks?status=pending

// NEW: Filtering by completion
GET /api/tasks?completed=false
```

```typescript
// OLD: Toggle status
PATCH /api/tasks/{id} { status: "completed" }

// NEW: Dedicated toggle
PATCH /api/tasks/{id}/toggle
```

---

## Common Mistakes to Avoid

### ❌ Mistakes

1. **Returning status field in response**
   - Frontend doesn't expect it
   - Will cause errors in UI

2. **Task ID as string UUID**
   - Frontend expects integer
   - Type mismatch errors

3. **Completed as string ("true"/"false")**
   - Frontend expects boolean
   - Filter logic breaks

4. **Missing toggle endpoint**
   - Frontend calls it
   - 404 errors on every toggle

5. **Not filtering by user_id**
   - User can see/edit other users' tasks
   - Security vulnerability

6. **Returning status instead of completed**
   - Entire UI breaks
   - Filter buttons don't work

### ✅ Correct

1. Response has `completed: true/false`
2. Task `id` is integer
3. All booleans are JSON booleans (not strings)
4. Implement `PATCH /api/tasks/{id}/toggle`
5. Always filter queries by user_id from JWT
6. Never include `status` field

---

## Support & Debugging

If frontend shows errors:

1. Check API response format
   ```bash
   curl -H "Authorization: Bearer {token}" \
        http://localhost:8000/api/tasks
   ```

2. Verify response has:
   - `id`: number (not string)
   - `completed`: boolean (not string)
   - No `status` field
   - Correct field names

3. Check browser console for fetch errors

4. Check backend logs for validation errors

---

## Reference Links

- **Frontend Commit**: `854e793`
- **Frontend Files Updated**:
  - `/frontend/src/lib/api.ts` - API client
  - `/frontend/src/app/tasks/page.tsx` - Tasks page
- **Frontend Documentation**:
  - `FRONTEND_SCHEMA_UPDATE.md` - Detailed changes
  - `SCHEMA_BEFORE_AFTER.md` - Comparison
  - `FRONTEND_MIGRATION_QUICK_START.md` - Quick reference

---

**Status**: ✓ Frontend Complete, Ready for Backend Integration
**Last Updated**: 2024-01-23
**Prepared For**: Backend Developer
**Questions?**: Check the documentation files or the git commits
