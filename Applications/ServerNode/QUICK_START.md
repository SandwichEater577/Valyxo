# Valyxo Backend API - Quick Start Guide

## Installation (2 minutes)

```bash
cd server
npm install
cp .env.example .env
npm run dev
```

Visit: http://localhost:5000

## Check Server Health

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "success": true,
  "message": "Valyxo API is running",
  "version": "0.41"
}
```

## First API Call (Register & Login)

### 1. Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response includes `token`. Copy it for next steps.

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "password": "SecurePass123"
  }'
```

### 3. Use Token (Replace TOKEN with your token)
```bash
TOKEN="your_token_here"

curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## Common Operations

### Create Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyProject",
    "description": "My first project"
  }'
```

### Create Script in Project
```bash
# First get your PROJECT_ID from previous response or list projects
curl -X POST http://localhost:5000/api/scripts/project/PROJECT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HelloWorld",
    "content": "print \"Hello from Valyxo\"",
    "language": "valyxoscript"
  }'
```

### Execute Script
```bash
curl -X POST http://localhost:5000/api/scripts/SCRIPT_ID/execute \
  -H "Authorization: Bearer $TOKEN"
```

### Get User Profile
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN"
```

## JavaScript Client

Use the included `ValyxoClient` for easier API calls:

```javascript
const client = new ValyxoClient();

// Register
await client.register('user', 'user@example.com', 'Pass123');

// Create project
const proj = await client.createProject('MyProject');

// Create script
const script = await client.createScript(proj.data.id, 'test', 'print "hi"');

// Execute
const result = await client.executeScript(script.data.id);
console.log(result.data.output);
```

See `examples/example.html` for interactive UI.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | ❌ | Register user |
| POST | /api/auth/login | ❌ | Login user |
| POST | /api/auth/logout | ✅ | Logout |
| GET | /api/auth/me | ✅ | Current user |
| GET | /api/users/profile | ✅ | User profile |
| GET | /api/users/stats | ✅ | User statistics |
| PUT | /api/users/profile | ✅ | Update profile |
| PUT | /api/users/password | ✅ | Change password |
| GET | /api/projects | ✅ | List projects |
| POST | /api/projects | ✅ | Create project |
| GET | /api/projects/:id | ✅ | Get project |
| PUT | /api/projects/:id | ✅ | Update project |
| DELETE | /api/projects/:id | ✅ | Delete project |
| GET | /api/scripts/project/:id | ✅ | List scripts |
| POST | /api/scripts/project/:id | ✅ | Create script |
| GET | /api/scripts/:id | ✅ | Get script |
| PUT | /api/scripts/:id | ✅ | Update script |
| DELETE | /api/scripts/:id | ✅ | Delete script |
| POST | /api/scripts/:id/execute | ✅ | Execute script |
| GET | /api/scripts/:id/executions | ✅ | Execution history |

## Environment Variables

```env
NODE_ENV=development          # development or production
PORT=5000                     # Server port
DB_PATH=./data/valyxo.db     # Database location
JWT_SECRET=your_secret        # JWT signing secret (change!)
JWT_EXPIRE=7d                 # Token expiration
API_VERSION=0.41              # API version
CORS_ORIGIN=http://localhost:3000
```

## Database

- **Type**: SQLite3
- **Location**: `server/data/valyxo.db`
- **Auto-created**: On first run
- **Tables**: users, projects, scripts, script_executions, api_keys

## Scripts

```bash
npm run dev     # Development with auto-reload
npm start       # Production
npm test        # Run tests
npm run lint    # Lint code
```

## File Structure

```
server/
├── src/
│   ├── server.js                    # Main app
│   ├── db.js                        # Database
│   ├── middleware/
│   │   ├── auth.js                  # JWT auth
│   │   ├── errorHandler.js          # Error handling
│   │   └── validators.js            # Input validation
│   └── routes/
│       ├── auth.js                  # Auth endpoints
│       ├── users.js                 # User endpoints
│       ├── projects.js              # Project endpoints
│       └── scripts.js               # Script endpoints
├── data/                            # Database (auto-created)
├── tests/
│   └── integration.test.js          # Integration tests
├── examples/
│   ├── client.js                    # JS client
│   └── example.html                 # Interactive UI
├── package.json
├── .env
└── API.md                           # Full API docs
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Change port in .env
PORT=5001
```

### Database Errors
```bash
# Reset database
rm data/valyxo.db
# Server recreates it on start
```

### Authentication Fails
- Check token in Authorization header
- Format: `Authorization: Bearer <token>`
- Verify JWT_SECRET matches across instances

### CORS Issues
- Add your frontend URL to CORS_ORIGIN in .env
- Example: `CORS_ORIGIN=http://localhost:3000,https://example.com`

## Next Steps

1. **Read full API docs**: See `API.md`
2. **Try interactive client**: Open `examples/example.html`
3. **Run tests**: `npm test`
4. **Integrate with frontend**: Use `ValyxoClient`

## Support

- Full API documentation: `API.md`
- Complete README: `README.md`
- Example client: `examples/client.js`
- Interactive UI: `examples/example.html`
- Tests: `tests/integration.test.js`
