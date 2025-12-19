# Valyxo Backend API Server (v0.41)

Complete backend API for the Valyxo ecosystem. Built with Express.js, SQLite, and JWT authentication.

## Features

- **User Authentication**: Registration, login, password management with JWT tokens
- **Project Management**: Create, read, update, delete projects
- **Script Management**: Full CRUD operations for ValyxoScript scripts
- **Script Execution**: Run scripts and track execution history
- **User Statistics**: Track projects, scripts, and execution metrics
- **Security**: Password hashing, token-based auth, input validation
- **Database**: SQLite with automatic schema initialization

## Tech Stack

- **Runtime**: Node.js 14+
- **Framework**: Express.js 4.18
- **Database**: SQLite3
- **Authentication**: JWT (jsonwebtoken)
- **Security**: bcryptjs, helmet
- **Logging**: morgan
- **Validation**: express-validator

## Quick Start

### Prerequisites

- Node.js 14 or higher
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   cd server
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Server runs on `http://localhost:5000`

### Verify Setup

```bash
# Check server health
curl http://localhost:5000/health

# Get API info
curl http://localhost:5000/api
```

## Environment Configuration

**Key variables in `.env`:**

```env
NODE_ENV=development
PORT=5000
DB_PATH=./data/valyxo.db
JWT_SECRET=your_jwt_secret_key_change_in_production
JWT_EXPIRE=7d
API_VERSION=0.41
CORS_ORIGIN=http://localhost:3000,http://localhost:5000
```

**For production:**
- Set `NODE_ENV=production`
- Use strong `JWT_SECRET` (min 32 characters)
- Configure `CORS_ORIGIN` for your domain
- Use environment variables, not `.env` file

## API Endpoints

### Public Routes
- `POST /api/auth/register` — Create new user account
- `POST /api/auth/login` — User login
- `GET /health` — Server health check
- `GET /api` — API information

### Protected Routes (require JWT token)

**Authentication:**
- `POST /api/auth/logout` — Logout
- `GET /api/auth/me` — Current user info

**Users:**
- `GET /api/users/profile` — User profile
- `PUT /api/users/profile` — Update profile
- `PUT /api/users/password` — Change password
- `GET /api/users/stats` — User statistics

**Projects:**
- `GET /api/projects` — List all projects
- `POST /api/projects` — Create project
- `GET /api/projects/:id` — Get project
- `PUT /api/projects/:id` — Update project
- `DELETE /api/projects/:id` — Delete project

**Scripts:**
- `GET /api/scripts/project/:projectId` — List project scripts
- `POST /api/scripts/project/:projectId` — Create script
- `GET /api/scripts/:id` — Get script
- `PUT /api/scripts/:id` — Update script
- `DELETE /api/scripts/:id` — Delete script
- `POST /api/scripts/:id/execute` — Execute script
- `GET /api/scripts/:id/executions` — Get execution history

See `API.md` for detailed endpoint documentation.

## Project Structure

```
server/
├── src/
│   ├── server.js              # Main server file
│   ├── db.js                  # Database setup and queries
│   ├── middleware/
│   │   ├── auth.js            # JWT authentication
│   │   ├── errorHandler.js    # Error handling
│   │   └── validators.js      # Input validation
│   └── routes/
│       ├── auth.js            # Authentication endpoints
│       ├── users.js           # User management
│       ├── projects.js        # Project CRUD
│       └── scripts.js         # Script management
├── data/                       # SQLite database (auto-created)
├── package.json               # Dependencies
├── .env                        # Environment config (create from .env.example)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── API.md                      # API documentation
└── README.md                   # This file
```

## Scripts

```bash
# Development (with auto-reload)
npm run dev

# Production
npm start

# Run tests
npm test

# Lint code
npm run lint
```

## Database

### Automatic Initialization

The database schema is automatically created on first startup:

**Tables:**
- `users` — User accounts and authentication
- `projects` — User projects
- `scripts` — Scripts within projects
- `script_executions` — Execution history
- `api_keys` — API keys for users

### Manual Database Inspection

```bash
# Using sqlite3 CLI
sqlite3 data/valyxo.db

# In SQLite shell
> .tables
> .schema users
> SELECT * FROM users;
```

### Database Reset

To reset the database:

```bash
rm data/valyxo.db
# Server will recreate it on next start
```

## Authentication Flow

1. **Register**: Create new user with username, email, password
2. **Login**: Submit credentials, receive JWT token
3. **Use Token**: Include token in `Authorization: Bearer <token>` header
4. **Token Expires**: After 7 days (configurable)
5. **Re-login**: Get new token when expired

### Example Auth Flow

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "devuser",
    "email": "dev@example.com",
    "password": "SecurePass123"
  }'

# Response includes token
# "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 2. Use token in subsequent requests
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Security Best Practices

1. **Passwords**: Hashed with bcrypt (10 rounds)
2. **Tokens**: JWT signed with secret, 7-day expiration
3. **Input Validation**: All inputs validated before processing
4. **SQL Injection**: Parameterized queries prevent injection
5. **CORS**: Restricted to configured origins
6. **Headers**: Helmet.js sets security headers

### Recommendations for Production

- Change `JWT_SECRET` to random 32+ character string
- Enable HTTPS/TLS
- Use environment variables for secrets
- Set up rate limiting with `express-rate-limit`
- Enable database backups
- Monitor error logs
- Set strong password requirements

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message",
  "details": "Optional validation details"
}
```

**Status Codes:**
- `200` — Success
- `201` — Created
- `400` — Bad request / Validation error
- `401` — Unauthorized / Invalid token
- `403` — Forbidden / Access denied
- `404` — Not found
- `500` — Server error

## Testing

Create basic tests:

```bash
npm test
```

## Deployment

### Using Node.js

```bash
npm install --production
NODE_ENV=production npm start
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY src ./src
EXPOSE 5000
CMD ["npm", "start"]
```

Build and run:

```bash
docker build -t valyxo-api .
docker run -p 5000:5000 -e JWT_SECRET=your_secret valyxo-api
```

## Performance Considerations

- Queries use indexes (user_id for quick lookups)
- Script execution history limited to last 50 entries
- Database uses connection pooling
- JWT tokens validated on each protected request

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Change port in .env
PORT=5001
```

### Database Locked

```bash
# SQLite error when running multiple instances
# Solution: Run only one server instance or use connection timeout
```

### Authentication Failed

- Verify JWT_SECRET is same on all server instances
- Check token hasn't expired
- Ensure Authorization header format: `Bearer <token>`

## Next Steps

- Add rate limiting
- Implement API key authentication
- Add request logging
- Set up CI/CD pipeline
- Add email verification
- Implement refresh tokens
- Add WebSocket support for real-time features

## Support

For issues or questions:
1. Check `API.md` for endpoint details
2. Review error messages in logs
3. Verify `.env` configuration
4. Check database permissions

## License

MIT - See LICENSE file in root directory
