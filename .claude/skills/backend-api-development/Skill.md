---
name: backend-api-development
description: Design and implement backend APIs with routing, request handling, and database connectivity. Use for server-side application development.
---

# Backend API Development

## Instructions

1. **Routing**
   - Define RESTful routes (GET, POST, PUT, DELETE)
   - Follow clear and consistent URL naming
   - Separate routes by feature/module

2. **Request & Response Handling**
   - Validate incoming requests
   - Parse request body, params, and query strings
   - Return proper HTTP status codes
   - Send structured JSON responses

3. **Database Integration**
   - Connect to database (SQL or NoSQL)
   - Perform CRUD operations
   - Use environment variables for DB credentials
   - Handle connection and query errors gracefully

4. **Middleware**
   - Authentication & authorization
   - Error handling
   - Logging and request tracing

## Best Practices
- Keep controllers thin, move logic to services
- Use async/await for non-blocking operations
- Never expose sensitive data in responses
- Validate input before DB operations
- Follow MVC or layered architecture
- Write reusable and modular code

## Example Structure
```js
// routes/user.routes.js
router.post("/users", createUser);

// controllers/user.controller.js
export const createUser = async (req, res) => {
  try {
    const user = await UserService.create(req.body);
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
