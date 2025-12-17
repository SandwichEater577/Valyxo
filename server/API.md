# Valyxo Backend API Documentation (v0.41)

## Overview

RESTful API for Valyxo ecosystem. Provides user authentication, project management, script storage, and execution capabilities.

**Base URL:** `http://localhost:5000/api`

**Version:** 0.41

---

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

Token expires after 7 days (configurable via `JWT_EXPIRE` environment variable).

---

## Endpoints

### Auth Routes (`/auth`)

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_dev",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_dev",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Validation:**
- Username: 3-32 characters, alphanumeric + underscore/hyphen
- Email: Valid email format
- Password: 8+ characters, must contain uppercase, lowercase, number

---

#### Login User
```
POST /auth/login
Content-Type: application/json

{
  "username": "john_dev",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_dev",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### Logout
```
POST /auth/logout
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

#### Get Current User
```
GET /auth/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_dev",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### User Routes (`/users`)

#### Get User Profile
```
GET /users/profile
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_dev",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "projectCount": 5,
    "scriptCount": 12
  }
}
```

---

#### Update User Profile
```
PUT /users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "john_dev_new",
  "email": "newemail@example.com"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

#### Change Password
```
PUT /users/password
Authorization: Bearer <token>
Content-Type: application/json

{
  "currentPassword": "OldPass123",
  "newPassword": "NewPass456"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

#### Get User Statistics
```
GET /users/stats
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "stats": {
    "projects": 5,
    "scripts": 12,
    "executions": 145,
    "totalExecutionTimeMs": 3450
  }
}
```

---

### Project Routes (`/projects`)

#### Get All Projects
```
GET /projects
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "MyProject",
      "description": "My first project",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

#### Create Project
```
POST /projects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "NewProject",
  "description": "Project description"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Project created successfully",
  "data": {
    "id": 2,
    "name": "NewProject",
    "description": "Project description",
    "created_at": "2024-01-16T12:00:00Z"
  }
}
```

**Validation:**
- Name: 1-100 characters (required)
- Description: 0-500 characters (optional)

---

#### Get Project Details
```
GET /projects/:projectId
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "MyProject",
    "description": "My first project",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

#### Update Project
```
PUT /projects/:projectId
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "UpdatedName",
  "description": "Updated description"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Project updated successfully",
  "data": {
    "id": 1,
    "name": "UpdatedName",
    "description": "Updated description",
    "updated_at": "2024-01-16T12:00:00Z"
  }
}
```

---

#### Delete Project
```
DELETE /projects/:projectId
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Project deleted successfully"
}
```

---

### Script Routes (`/scripts`)

#### Get Project Scripts
```
GET /scripts/project/:projectId
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "project_id": 1,
      "name": "HelloWorld",
      "language": "valyxoscript",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

#### Create Script
```
POST /scripts/project/:projectId
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "HelloWorld",
  "content": "print \"Hello World\"",
  "language": "valyxoscript"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Script created successfully",
  "data": {
    "id": 1,
    "project_id": 1,
    "name": "HelloWorld",
    "language": "valyxoscript",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Validation:**
- Name: 1-100 characters (required)
- Content: Non-empty (required)
- Language: 'valyxoscript' | 'javascript' | 'python' (optional, default: valyxoscript)

---

#### Get Script Details
```
GET /scripts/:scriptId
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "project_id": 1,
    "name": "HelloWorld",
    "content": "print \"Hello World\"",
    "language": "valyxoscript",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

#### Update Script
```
PUT /scripts/:scriptId
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "HelloWorldUpdated",
  "content": "print \"Updated\"",
  "language": "valyxoscript"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Script updated successfully",
  "data": {
    "id": 1,
    "name": "HelloWorldUpdated",
    "language": "valyxoscript",
    "updated_at": "2024-01-16T12:00:00Z"
  }
}
```

---

#### Delete Script
```
DELETE /scripts/:scriptId
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Script deleted successfully"
}
```

---

#### Execute Script
```
POST /scripts/:scriptId/execute
Authorization: Bearer <token>
```

**Response (200 | 400):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "success",
    "output": "{\"result\": 42}",
    "error": null,
    "execution_time_ms": 125
  }
}
```

**Status Values:**
- `success`: Script executed without errors
- `error`: Script execution failed
- `unsupported`: Language not supported for execution

---

#### Get Script Execution History
```
GET /scripts/:scriptId/executions
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "status": "success",
      "execution_time_ms": 125,
      "executed_at": "2024-01-16T12:00:00Z"
    }
  ]
}
```

Returns last 50 executions ordered by most recent.

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Validation error",
  "details": [
    {
      "param": "password",
      "msg": "Password must be at least 8 characters long"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Invalid token"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "[error details in development only]"
}
```

---

## Setup & Running

### 1. Install Dependencies
```bash
cd server
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Development Server
```bash
npm run dev
```

Server runs on `http://localhost:5000` by default.

### 4. Check Server Health
```bash
curl http://localhost:5000/health
```

---

## Rate Limiting

Currently not implemented. Consider adding `express-rate-limit` for production deployments.

## Security Notes

- Passwords are hashed with bcrypt (10 rounds)
- JWT tokens include user ID and username
- All user-owned resources are verified before access
- SQL injection protection through parameterized queries
- CORS configured for specific origins
- Helmet.js for security headers

---

## Testing API with cURL

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'

# Create Project
curl -X POST http://localhost:5000/api/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"TestProject","description":"Test"}'
```

---

## Database Schema

### users
- `id` (INTEGER, PRIMARY KEY)
- `username` (TEXT, UNIQUE)
- `email` (TEXT, UNIQUE)
- `password_hash` (TEXT)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

### projects
- `id` (INTEGER, PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY)
- `name` (TEXT)
- `description` (TEXT)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

### scripts
- `id` (INTEGER, PRIMARY KEY)
- `project_id` (INTEGER, FOREIGN KEY)
- `name` (TEXT)
- `content` (TEXT)
- `language` (TEXT)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

### script_executions
- `id` (INTEGER, PRIMARY KEY)
- `script_id` (INTEGER, FOREIGN KEY)
- `status` (TEXT)
- `output` (TEXT)
- `error_message` (TEXT)
- `execution_time_ms` (INTEGER)
- `executed_at` (DATETIME)

### api_keys
- `id` (INTEGER, PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY)
- `key_hash` (TEXT, UNIQUE)
- `name` (TEXT)
- `created_at` (DATETIME)
- `last_used` (DATETIME)
