package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"time"

	_ "modernc.org/sqlite"
)

var DB *sql.DB

// User model
type User struct {
	ID           int64     `json:"id"`
	Username     string    `json:"username"`
	Email        string    `json:"email"`
	PasswordHash string    `json:"-"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

// Project model
type Project struct {
	ID          int64     `json:"id"`
	UserID      int64     `json:"user_id,omitempty"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// Script model
type Script struct {
	ID        int64     `json:"id"`
	ProjectID int64     `json:"project_id"`
	Name      string    `json:"name"`
	Content   string    `json:"content,omitempty"`
	Language  string    `json:"language"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// ScriptExecution model
type ScriptExecution struct {
	ID              int64     `json:"id"`
	ScriptID        int64     `json:"script_id"`
	Status          string    `json:"status"`
	Output          string    `json:"output,omitempty"`
	ErrorMessage    string    `json:"error_message,omitempty"`
	ExecutionTimeMs int       `json:"execution_time_ms"`
	ExecutedAt      time.Time `json:"executed_at"`
}

// APIKey model
type APIKey struct {
	ID        int64      `json:"id"`
	UserID    int64      `json:"user_id"`
	KeyHash   string     `json:"-"`
	Name      string     `json:"name"`
	CreatedAt time.Time  `json:"created_at"`
	LastUsed  *time.Time `json:"last_used,omitempty"`
}

// Initialize opens the database and creates tables
func Initialize(dbPath string) error {
	// Ensure directory exists
	dir := filepath.Dir(dbPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create database directory: %w", err)
	}

	var err error
	DB, err = sql.Open("sqlite", dbPath+"?_busy_timeout=10000&_foreign_keys=on")
	if err != nil {
		return fmt.Errorf("failed to open database: %w", err)
	}

	// Set connection pool settings
	DB.SetMaxOpenConns(25)
	DB.SetMaxIdleConns(5)
	DB.SetConnMaxLifetime(5 * time.Minute)

	// Create tables
	if err := createTables(); err != nil {
		return fmt.Errorf("failed to create tables: %w", err)
	}

	fmt.Printf("Connected to SQLite database: %s\n", dbPath)
	return nil
}

func createTables() error {
	tables := []string{
		`CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			email TEXT UNIQUE NOT NULL,
			password_hash TEXT NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)`,
		`CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)`,

		`CREATE TABLE IF NOT EXISTS projects (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			name TEXT NOT NULL,
			description TEXT,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
		)`,
		`CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id)`,
		`CREATE INDEX IF NOT EXISTS idx_projects_updated_at ON projects(updated_at)`,

		`CREATE TABLE IF NOT EXISTS scripts (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			project_id INTEGER NOT NULL,
			name TEXT NOT NULL,
			content TEXT,
			language TEXT DEFAULT 'valyxoscript',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
		)`,
		`CREATE INDEX IF NOT EXISTS idx_scripts_project_id ON scripts(project_id)`,
		`CREATE INDEX IF NOT EXISTS idx_scripts_language ON scripts(language)`,

		`CREATE TABLE IF NOT EXISTS script_executions (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			script_id INTEGER NOT NULL,
			status TEXT DEFAULT 'pending',
			output TEXT,
			error_message TEXT,
			execution_time_ms INTEGER,
			executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (script_id) REFERENCES scripts(id) ON DELETE CASCADE
		)`,
		`CREATE INDEX IF NOT EXISTS idx_script_executions_script_id ON script_executions(script_id)`,
		`CREATE INDEX IF NOT EXISTS idx_script_executions_status ON script_executions(status)`,
		`CREATE INDEX IF NOT EXISTS idx_script_executions_executed_at ON script_executions(executed_at)`,

		`CREATE TABLE IF NOT EXISTS api_keys (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			key_hash TEXT UNIQUE NOT NULL,
			name TEXT,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			last_used DATETIME,
			FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
		)`,
		`CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id)`,
		`CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash)`,
	}

	for _, query := range tables {
		if _, err := DB.Exec(query); err != nil {
			return fmt.Errorf("failed to execute: %s, error: %w", query, err)
		}
	}

	return nil
}

// Close closes the database connection
func Close() error {
	if DB != nil {
		return DB.Close()
	}
	return nil
}

// User queries

func GetUserByID(id int64) (*User, error) {
	user := &User{}
	err := DB.QueryRow(
		`SELECT id, username, email, password_hash, created_at, updated_at FROM users WHERE id = ?`,
		id,
	).Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return user, err
}

func GetUserByUsername(username string) (*User, error) {
	user := &User{}
	err := DB.QueryRow(
		`SELECT id, username, email, password_hash, created_at, updated_at FROM users WHERE username = ?`,
		username,
	).Scan(&user.ID, &user.Username, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return user, err
}

func GetUserByUsernameOrEmail(username, email string) (*User, error) {
	user := &User{}
	err := DB.QueryRow(
		`SELECT id FROM users WHERE username = ? OR email = ?`,
		username, email,
	).Scan(&user.ID)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return user, err
}

func CreateUser(username, email, passwordHash string) (int64, error) {
	result, err := DB.Exec(
		`INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)`,
		username, email, passwordHash,
	)
	if err != nil {
		return 0, err
	}
	return result.LastInsertId()
}

func GetUserProjectAndScriptCount(userID int64) (projectCount, scriptCount int, err error) {
	err = DB.QueryRow(`SELECT COUNT(*) FROM projects WHERE user_id = ?`, userID).Scan(&projectCount)
	if err != nil {
		return
	}
	err = DB.QueryRow(
		`SELECT COUNT(*) FROM scripts WHERE project_id IN (SELECT id FROM projects WHERE user_id = ?)`,
		userID,
	).Scan(&scriptCount)
	return
}

func UpdateUserProfile(userID int64, email, username *string) error {
	if email == nil && username == nil {
		return nil
	}

	query := "UPDATE users SET updated_at = CURRENT_TIMESTAMP"
	args := []interface{}{}

	if email != nil {
		query += ", email = ?"
		args = append(args, *email)
	}
	if username != nil {
		query += ", username = ?"
		args = append(args, *username)
	}

	query += " WHERE id = ?"
	args = append(args, userID)

	_, err := DB.Exec(query, args...)
	return err
}

func UpdateUserPassword(userID int64, newPasswordHash string) error {
	_, err := DB.Exec(
		`UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
		newPasswordHash, userID,
	)
	return err
}

func CheckEmailExists(email string, excludeUserID int64) (bool, error) {
	var count int
	err := DB.QueryRow(`SELECT COUNT(*) FROM users WHERE email = ? AND id != ?`, email, excludeUserID).Scan(&count)
	return count > 0, err
}

func CheckUsernameExists(username string, excludeUserID int64) (bool, error) {
	var count int
	err := DB.QueryRow(`SELECT COUNT(*) FROM users WHERE username = ? AND id != ?`, username, excludeUserID).Scan(&count)
	return count > 0, err
}

// Project queries

func GetProjectsByUserID(userID int64) ([]Project, error) {
	rows, err := DB.Query(
		`SELECT id, name, description, created_at, updated_at FROM projects WHERE user_id = ? ORDER BY updated_at DESC`,
		userID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var projects []Project
	for rows.Next() {
		var p Project
		if err := rows.Scan(&p.ID, &p.Name, &p.Description, &p.CreatedAt, &p.UpdatedAt); err != nil {
			return nil, err
		}
		projects = append(projects, p)
	}
	return projects, rows.Err()
}

func GetProjectByID(projectID, userID int64) (*Project, error) {
	p := &Project{}
	err := DB.QueryRow(
		`SELECT id, name, description, created_at, updated_at FROM projects WHERE id = ? AND user_id = ?`,
		projectID, userID,
	).Scan(&p.ID, &p.Name, &p.Description, &p.CreatedAt, &p.UpdatedAt)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return p, err
}

func CreateProject(userID int64, name, description string) (int64, error) {
	result, err := DB.Exec(
		`INSERT INTO projects (user_id, name, description) VALUES (?, ?, ?)`,
		userID, name, description,
	)
	if err != nil {
		return 0, err
	}
	return result.LastInsertId()
}

func UpdateProject(projectID int64, name, description string) error {
	_, err := DB.Exec(
		`UPDATE projects SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
		name, description, projectID,
	)
	return err
}

func DeleteProject(projectID int64) error {
	_, err := DB.Exec(`DELETE FROM projects WHERE id = ?`, projectID)
	return err
}

func CheckProjectOwnership(projectID, userID int64) (bool, error) {
	var id int64
	err := DB.QueryRow(`SELECT id FROM projects WHERE id = ? AND user_id = ?`, projectID, userID).Scan(&id)
	if err == sql.ErrNoRows {
		return false, nil
	}
	return err == nil, err
}

// Script queries

func GetScriptsByProjectID(projectID int64) ([]Script, error) {
	rows, err := DB.Query(
		`SELECT id, project_id, name, language, created_at, updated_at FROM scripts WHERE project_id = ? ORDER BY updated_at DESC`,
		projectID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var scripts []Script
	for rows.Next() {
		var s Script
		if err := rows.Scan(&s.ID, &s.ProjectID, &s.Name, &s.Language, &s.CreatedAt, &s.UpdatedAt); err != nil {
			return nil, err
		}
		scripts = append(scripts, s)
	}
	return scripts, rows.Err()
}

func GetScriptByID(scriptID, userID int64) (*Script, error) {
	s := &Script{}
	err := DB.QueryRow(
		`SELECT s.id, s.project_id, s.name, s.content, s.language, s.created_at, s.updated_at
		 FROM scripts s
		 JOIN projects p ON s.project_id = p.id
		 WHERE s.id = ? AND p.user_id = ?`,
		scriptID, userID,
	).Scan(&s.ID, &s.ProjectID, &s.Name, &s.Content, &s.Language, &s.CreatedAt, &s.UpdatedAt)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return s, err
}

func CreateScript(projectID int64, name, content, language string) (int64, error) {
	if language == "" {
		language = "valyxoscript"
	}
	result, err := DB.Exec(
		`INSERT INTO scripts (project_id, name, content, language) VALUES (?, ?, ?, ?)`,
		projectID, name, content, language,
	)
	if err != nil {
		return 0, err
	}
	return result.LastInsertId()
}

func UpdateScript(scriptID int64, name, content, language string) error {
	if language == "" {
		language = "valyxoscript"
	}
	_, err := DB.Exec(
		`UPDATE scripts SET name = ?, content = ?, language = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
		name, content, language, scriptID,
	)
	return err
}

func DeleteScript(scriptID int64) error {
	_, err := DB.Exec(`DELETE FROM scripts WHERE id = ?`, scriptID)
	return err
}

func CheckScriptOwnership(scriptID, userID int64) (*Script, error) {
	s := &Script{}
	err := DB.QueryRow(
		`SELECT s.id, s.project_id FROM scripts s JOIN projects p ON s.project_id = p.id WHERE s.id = ? AND p.user_id = ?`,
		scriptID, userID,
	).Scan(&s.ID, &s.ProjectID)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return s, err
}
