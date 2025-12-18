# Valyxo Backend Server (Go)

A high-performance backend API server for Valyxo, rewritten in Go.

## Features

- 🚀 **High Performance** - Built with Go and Gin framework
- 🔐 **JWT Authentication** - Secure token-based authentication
- 🗃️ **SQLite Database** - Lightweight, file-based database
- 🛡️ **Security** - Rate limiting, CORS, security headers
- 📊 **Metrics** - Health checks and runtime metrics

## Requirements

- Go 1.21 or later
- GCC (for SQLite compilation on Windows, use MinGW or TDM-GCC)

## Quick Start

### Windows

```batch
start.bat
```

### Linux/macOS

```bash
chmod +x start.sh
./start.sh
```

### Manual Build

```bash
# Download dependencies
go mod download

# Build
go build -o valyxo-server ./cmd/server

# Run
./valyxo-server
```

## Configuration

Create a `.env` file in the `server-go` directory:

```env
PORT=5000
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRE=168h
DB_PATH=./data/valyxo.db
CORS_ORIGIN=http://localhost:3000
API_VERSION=0.41
NODE_ENV=development
RATE_LIMIT_GENERAL=100
RATE_LIMIT_AUTH=5
```

## API Endpoints

### Public

| Method | Endpoint   | Description    |
| ------ | ---------- | -------------- |
| GET    | `/health`  | Health check   |
| GET    | `/metrics` | Server metrics |
| GET    | `/api`     | API info       |

### Authentication

| Method | Endpoint             | Description                      |
| ------ | -------------------- | -------------------------------- |
| POST   | `/api/auth/register` | Register new user                |
| POST   | `/api/auth/login`    | Login                            |
| POST   | `/api/auth/logout`   | Logout (requires auth)           |
| GET    | `/api/auth/me`       | Get current user (requires auth) |

### Users (requires auth)

| Method | Endpoint              | Description      |
| ------ | --------------------- | ---------------- |
| GET    | `/api/users/profile`  | Get user profile |
| PUT    | `/api/users/profile`  | Update profile   |
| PUT    | `/api/users/password` | Change password  |

### Projects (requires auth)

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| GET    | `/api/projects`     | List all projects |
| POST   | `/api/projects`     | Create project    |
| GET    | `/api/projects/:id` | Get project       |
| PUT    | `/api/projects/:id` | Update project    |
| DELETE | `/api/projects/:id` | Delete project    |

### Scripts (requires auth)

| Method | Endpoint                   | Description             |
| ------ | -------------------------- | ----------------------- |
| GET    | `/api/scripts/project/:id` | List scripts in project |
| POST   | `/api/scripts/project/:id` | Create script           |
| GET    | `/api/scripts/:id`         | Get script              |
| PUT    | `/api/scripts/:id`         | Update script           |
| DELETE | `/api/scripts/:id`         | Delete script           |

## Project Structure

```
server-go/
├── cmd/
│   └── server/
│       └── main.go          # Entry point
├── internal/
│   ├── config/
│   │   └── config.go        # Configuration
│   ├── db/
│   │   └── db.go            # Database operations
│   ├── handlers/
│   │   ├── auth.go          # Auth handlers
│   │   ├── projects.go      # Project handlers
│   │   ├── scripts.go       # Script handlers
│   │   └── users.go         # User handlers
│   └── middleware/
│       ├── auth.go          # JWT middleware
│       └── security.go      # Security middleware
├── data/                    # SQLite database (auto-created)
├── go.mod                   # Go modules
├── start.bat                # Windows start script
├── start.sh                 # Linux/macOS start script
└── README.md
```

## Performance Comparison

| Metric       | Node.js | Go       |
| ------------ | ------- | -------- |
| Startup time | ~2s     | ~100ms   |
| Memory usage | ~100MB  | ~15MB    |
| Requests/sec | ~10,000 | ~50,000+ |

## License

MIT License - See [LICENSE](../LICENSE) for details.
