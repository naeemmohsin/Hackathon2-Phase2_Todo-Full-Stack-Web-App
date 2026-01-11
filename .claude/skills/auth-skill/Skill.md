---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Registration (Signup)**
   - Validate user input (email, password, username)
   - Enforce strong password rules
   - Prevent duplicate accounts
   - Store user data securely

2. **User Login (Signin)**
   - Verify credentials
   - Compare hashed passwords
   - Handle invalid login attempts
   - Return authenticated session/token

3. **Password Security**
   - Hash passwords using bcrypt or argon2
   - Never store plain-text passwords
   - Use proper salting and hashing rounds

4. **JWT Authentication**
   - Generate access tokens on login
   - Sign tokens with a secure secret
   - Set token expiration
   - Verify JWT on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Use adapters for database integration
   - Support email/password and OAuth (if needed)
   - Manage sessions and token refresh

## Best Practices
- Use HTTPS only
- Store secrets in environment variables
- Implement rate limiting on auth routes
- Use short-lived access tokens
- Refresh tokens securely
- Return generic error messages for auth failures

## Example Flow
```ts
// Signup
POST /auth/signup
→ validate input
→ hash password
→ save user
→ return success

// Signin
POST /auth/signin
→ verify user
→ compare password
→ issue JWT
→ return token

// Protected Route
GET /profile
→ verify JWT
→ allow access
