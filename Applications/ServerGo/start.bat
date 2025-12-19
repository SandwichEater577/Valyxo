@echo off
echo ========================================
echo    Valyxo Backend Server (Go)
echo ========================================
echo.

REM Check if Go is installed
where go >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Go is not installed or not in PATH
    echo Please install Go from https://go.dev/dl/
    pause
    exit /b 1
)

echo [1/3] Downloading dependencies...
go mod download
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to download dependencies
    pause
    exit /b 1
)

echo [2/3] Building server...
go build -o valyxo-server.exe ./cmd/server
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo [3/3] Starting server...
echo.
valyxo-server.exe
