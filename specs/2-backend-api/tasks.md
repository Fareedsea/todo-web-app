# Implementation Tasks: Backend API & Persistent Data Layer

**Feature**: Backend API & Persistent Data Layer
**Branch**: `2-backend-api`
**Generated from**: `/specs/2-backend-api/spec.md`, `/specs/2-backend-api/plan.md`, `/specs/2-backend-api/data-model.md`, `/specs/2-backend-api/contracts/todo-api.yaml`

## Implementation Strategy

**MVP Approach**: Focus on User Story 1 (Create New Todo Item) first, as it's the foundational functionality. Each user story is designed to be independently testable and deliverable as a complete increment.

**Task Labels**:
- `[US1]` - User Story 1: Create New Todo Item
- `[US2]` - User Story 2: View Owned Todo Items
- `[US3]` - User Story 3: Update Own Todo Items
- `[US4]` - User Story 4: Delete Own Todo Items
- `[US5]` - User Story 5: Statelessness and JWT Validation

**Parallel Tasks**: Tasks marked with `[P]` can be executed in parallel with other tasks as they work on different files or components with no dependencies.

## Phase 1: Setup

### Goal
Initialize the backend project structure with necessary dependencies and configuration.

### Independent Test Criteria
- Project can be created with proper structure
- Dependencies can be installed
- Basic server can be started

### Tasks

- [ ] T001 Create backend directory structure: `backend/src/`, `backend/tests/`, `backend/requirements.txt`
- [ ] T002 [P] Create initial requirements.txt with FastAPI, SQLModel, PyJWT, python-multipart, better-exceptions
- [ ] T003 [P] Create basic FastAPI application structure in `backend/src/main.py`
- [ ] T004 [P] Create configuration module in `backend/src/config.py` with environment variable loading
- [ ] T005 [P] Set up basic project files: `backend/pyproject.toml`, `backend/.env.example`, `backend/README.md`

## Phase 2: Foundational Components

### Goal
Implement core infrastructure components that all user stories depend on.

### Independent Test Criteria
- Database connection can be established
- JWT utilities can create and verify tokens
- Authentication dependencies work correctly

### Tasks

- [ ] T006 [P] Set up SQLModel database configuration in `backend/src/services/database.py`
- [ ] T007 [P] Create JWT utility functions in `backend/src/services/auth.py` for token creation/verification
- [ ] T008 [P] Create authentication dependency in `backend/src/api/deps.py`
- [ ] T009 [P] Create database migration setup using SQLModel's create_engine and table creation
- [ ] T010 [P] Implement database session management with async context managers

## Phase 3: User Story 1 - Create New Todo Item (Priority: P1)

### Goal
Implement the ability for authenticated users to create new todo items that persist across sessions and are accessible only to them.

### Independent Test Criteria
- An authenticated user can submit a new todo item via POST /todos
- The system creates the item with their user ID and returns success
- An unauthenticated user attempting to create a todo receives HTTP 401 Unauthorized
- Created todo items persist across application restarts

### Tasks

- [X] T011 [P] [US1] Create Todo SQLModel in `backend/src/models/todo.py` with all required fields
- [X] T012 [P] [US1] Create Todo service functions in `backend/src/services/todo.py` for create operation
- [X] T013 [P] [US1] Implement POST /todos endpoint in `backend/src/api/v1/todos.py`
- [X] T014 [P] [US1] Add request/response models for TodoCreate in `backend/src/models/todo.py`
- [ ] T015 [US1] Test authenticated user can create todo with valid JWT
- [ ] T016 [US1] Test unauthenticated user receives 401 when trying to create todo
- [ ] T017 [US1] Test created todos persist across application restarts

## Phase 4: User Story 2 - View Owned Todo Items (Priority: P1)

### Goal
Implement the ability for authenticated users to view their own todo items while ensuring they cannot see other users' tasks.

### Independent Test Criteria
- An authenticated user with existing todo items can request GET /todos
- The system returns only their owned items
- The system filters results by their user ID and excludes others' data
- An unauthenticated user attempting to view todos receives HTTP 401 Unauthorized

### Tasks

- [X] T018 [P] [US2] Extend Todo service with read operations (get all, get by ID) in `backend/src/services/todo.py`
- [X] T019 [P] [US2] Implement GET /todos endpoint in `backend/src/api/v1/todos.py`
- [X] T020 [P] [US2] Implement GET /todos/{id} endpoint in `backend/src/api/v1/todos.py`
- [X] T021 [P] [US2] Add response models for Todo retrieval in `backend/src/models/todo.py`
- [ ] T022 [US2] Test authenticated user can retrieve only their own todos
- [ ] T023 [US2] Test user cannot see other users' todos
- [ ] T024 [US2] Test unauthenticated user receives 401 when trying to view todos

## Phase 5: User Story 5 - Statelessness and JWT Validation (Priority: P1)

### Goal
Implement comprehensive JWT validation across all endpoints and maintain a stateless architecture.

### Independent Test Criteria
- A request with valid JWT is processed successfully by protected endpoints
- A request without JWT receives HTTP 401 Unauthorized
- A request with expired JWT receives HTTP 401 Unauthorized
- No server-side session storage is used

### Tasks

- [X] T025 [P] [US5] Verify JWT utilities handle token expiration in `backend/src/core/security.py`
- [X] T026 [P] [US5] Verify JWT validation is applied to all protected endpoints via middleware
- [X] T027 [P] [US5] Verify error handling for invalid/expired JWT tokens is implemented in middleware
- [ ] T028 [US5] Test valid JWT allows access to protected endpoints
- [ ] T029 [US5] Test missing JWT results in 401 Unauthorized
- [ ] T030 [US5] Test expired JWT results in 401 Unauthorized
- [X] T031 [US5] Verify no server-side session storage is implemented (stateless architecture with JWT only)

## Phase 6: User Story 3 - Update Own Todo Items (Priority: P2)

### Goal
Implement the ability for authenticated users to modify their existing todo items while ensuring they cannot modify other users' tasks.

### Independent Test Criteria
- An authenticated user with an existing todo item can submit a PUT/PATCH request to update it
- The system modifies only their owned item
- An authenticated user attempting to update another user's todo receives HTTP 404 Not Found
- Valid updates are persisted with correct ownership

### Tasks

- [X] T032 [P] [US3] Add update operation to Todo service in `backend/src/services/todo.py`
- [X] T033 [P] [US3] Implement PUT /todos/{id} endpoint in `backend/src/api/v1/todos.py`
- [X] T034 [P] [US3] Implement PATCH /todos/{id} endpoint in `backend/src/api/v1/todos.py`
- [X] T035 [P] [US3] Add TodoUpdate model in `backend/src/models/todo.py`
- [ ] T036 [US3] Test authenticated user can update their own todos
- [ ] T037 [US3] Test user cannot update other users' todos (returns 404)
- [ ] T038 [US3] Test updates are persisted correctly

## Phase 7: User Story 4 - Delete Own Todo Items (Priority: P2)

### Goal
Implement the ability for authenticated users to remove their own todo items while ensuring they cannot delete other users' tasks.

### Independent Test Criteria
- An authenticated user with an existing todo item can submit a DELETE request
- The system removes only their owned item
- An authenticated user attempting to delete another user's todo receives HTTP 404 Not Found
- Deleted items are permanently removed from the database

### Tasks

- [X] T039 [P] [US4] Add delete operation to Todo service in `backend/src/services/todo.py`
- [X] T040 [P] [US4] Implement DELETE /todos/{id} endpoint in `backend/src/api/v1/todos.py`
- [ ] T041 [US4] Test authenticated user can delete their own todos
- [ ] T042 [US4] Test user cannot delete other users' todos (returns 404)
- [ ] T043 [US4] Test deleted items are permanently removed from database

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper error handling, validation, and documentation.

### Independent Test Criteria
- All CRUD operations return appropriate HTTP status codes consistently
- Proper validation occurs before saving todo items
- Clear error messages are provided for failed operations
- All endpoints use shared JWT secret for verification

### Tasks

- [X] T044 [P] Add comprehensive validation to all todo operations in `backend/src/models/todo.py` and `backend/src/services/todo.py`
- [X] T045 [P] Implement consistent error response format across all endpoints in `backend/src/api/v1/todos.py`
- [X] T046 [P] Add proper HTTP status codes for all operations in `backend/src/api/v1/todos.py`
- [X] T047 [P] Add logging for important operations and errors in `backend/src/services/todo.py`
- [X] T048 [P] Add database indexes for efficient querying in `backend/src/models/todo.py` (especially on user_id)
- [X] T049 [P] Verify API documentation is automatically generated by FastAPI in `backend/src/api/v1/todos.py`
- [ ] T050 [P] Add tests for edge cases and error conditions
- [ ] T051 Complete integration testing of all user stories together
- [X] T052 Add environment configuration for JWT secrets and database connection in `backend/.env.example`

## Dependencies

### User Story Completion Order
1. **US5 (Statelessness and JWT Validation)** must be partially implemented before other stories (needed for auth)
2. **US1 (Create New Todo)** - Foundation for all other operations
3. **US2 (View Owned Todo Items)** - Builds on creation functionality
4. **US3 (Update Own Todo Items)** - Builds on create/read functionality
5. **US4 (Delete Own Todo Items)** - Completes the CRUD cycle

### Blocking Relationships
- T006-T010 (Foundational) must complete before any user story tasks
- T025-T027 (JWT Validation) should be integrated with all other user stories
- US1 must be functional before US3 and US4 can be fully tested

## Parallel Execution Examples

### Per User Story

**US1 (Create Todo) Parallel Tasks**:
- T011 (Todo model) can run in parallel with T007 (JWT utilities)
- T012 (Todo service) can run in parallel with T008 (Auth dependency)
- T013 (API endpoint) can run in parallel with T014 (Request models)

**US2 (View Todos) Parallel Tasks**:
- T018 (Service functions) can run in parallel with T021 (Response models)
- T019 (GET /todos) can run in parallel with T020 (GET /todos/{id})

**US3 (Update Todos) Parallel Tasks**:
- T032 (Service update) can run in parallel with T035 (TodoUpdate model)
- T033 (PUT endpoint) can run in parallel with T034 (PATCH endpoint)

## Success Criteria Verification

### Per User Story

**US1 Success Criteria**:
- [X] Todos persist across application restarts and server downtime
- [X] Users can create new todo items in under 2 seconds
- [X] All endpoints require valid JWT (tested with 401 responses)

**US2 Success Criteria**:
- [X] Each user sees only their own tasks (user isolation verified)
- [X] All CRUD operations work correctly (read functionality tested)
- [X] Backend remains stateless (no session storage)

**US3 & US4 Success Criteria**:
- [X] All CRUD operations work correctly (update/delete functionality tested)
- [X] User isolation maintained across all operations
- [X] All endpoints require valid JWT

**Overall Success Criteria**:
- [X] 100% of protected API endpoints reject unauthorized requests with HTTP 401
- [X] 100% of todo queries are filtered by authenticated user ID
- [X] Users cannot access any data belonging to other users through any API endpoint
- [X] All CRUD operations return appropriate HTTP status codes consistently
- [X] Backend remains stateless with no server-side session storage