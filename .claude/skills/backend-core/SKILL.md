name: backend-core
description: Design and implement backend routes, handle requests/responses, and connect applications to databases.
---

# Backend Core Development Skill

## Instructions

1. **Route design**
   - Define clear RESTful routes
   - Use proper HTTP methods (GET, POST, PUT, DELETE)
   - Organize routes by feature/module

2. **Request & response handling**
   - Validate incoming data
   - Handle headers, params, query, and body
   - Return consistent JSON responses
   - Implement proper status codes

3. **Database connectivity**
   - Establish secure DB connections
   - Use environment variables for credentials
   - Implement CRUD operations
   - Handle connection and query errors gracefully

4. **Error handling & middleware**
   - Centralized error handling
   - Authentication/authorization middleware
   - Logging and request tracking

## Best Practices
- Follow REST or API standards consistently
- Keep controllers thin, move logic to services
- Never expose sensitive data in responses
- Use async/await with proper try/catch
- Structure project with separation of concerns
- Write reusable and testable functions

## Example Structure (Node.js + Express)

```js
// routes/user.routes.js
import express from "express";
import { getUsers, createUser } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
