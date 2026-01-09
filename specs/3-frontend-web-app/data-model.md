# Data Model: Frontend Web Application

## Entity: User Session (Frontend State)

### Fields
- `isLoggedIn`: boolean (whether user is authenticated)
- `user`: User object (user information when logged in)
- `token`: string (JWT token for authenticated requests)
- `isLoading`: boolean (loading state during auth operations)
- `error`: string (error messages during auth operations)

### State Transitions
- `isLoggedIn` can transition from `false` to `true` (login) or `true` to `false` (logout)
- `token` is set during login and cleared during logout/token expiration
- `isLoading` toggles during authentication operations
- `error` is set when authentication errors occur, cleared on successful operations

## Entity: Todo Item (Frontend Representation)

### Fields
- `id`: string/UUID (unique identifier)
- `title`: string (required, 1-255 characters)
- `description`: string (optional, up to 1000 characters)
- `isCompleted`: boolean (default: false)
- `createdAt`: Date/string (timestamp when created)
- `updatedAt`: Date/string (timestamp when last updated)
- `userId`: string/UUID (foreign key reference to user)

### State Transitions
- `isCompleted` can transition from `false` to `true` (marking complete) or `true` to `false` (marking incomplete)
- `updatedAt` automatically updates when the todo is modified
- `title` and `description` can be modified through update operations

## Entity: UI State

### Fields
- `loadingStates`: object (tracks loading states for different operations)
- `errorStates`: object (tracks error states for different operations)
- `formStates`: object (tracks form validation and values)
- `navigationState`: object (tracks current route and navigation history)

### State Transitions
- `loadingStates` entries are set to true during operations, false when complete
- `errorStates` entries are set when operations fail, cleared when resolved
- `formStates` entries update as users interact with forms
- `navigationState` updates as users navigate between pages

## Entity: API Response

### Fields
- `data`: any (the actual response data)
- `status`: number (HTTP status code)
- `error`: object (error details if request failed)
- `loading`: boolean (whether request is in progress)

### State Transitions
- `loading` transitions from `false` to `true` when request starts, back to `false` when complete
- `data` or `error` is populated based on request outcome
- `status` reflects the HTTP status of the response

## Access Patterns (Frontend)

- Get all todos for current user
- Create a new todo
- Update an existing todo
- Delete a specific todo
- Get user profile information
- Update user profile information
- Handle authentication state changes

## Validation Rules (Frontend)

- Todo title must be 1-255 characters
- Todo description must be less than 1000 characters if provided
- Form inputs must be validated before submission
- JWT tokens must be present for authenticated requests
- Error states must be displayed for invalid inputs