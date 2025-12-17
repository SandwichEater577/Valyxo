@echo off
setlocal enabledelayedexpansion

echo Valyxo Backend API Setup
echo ========================

if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo WARNING: Please configure .env file before running the server
    echo.
)

if not exist node_modules (
    echo Installing dependencies...
    call npm install
    echo.
)

echo.
echo Starting Valyxo Backend API (v0.41)...
echo Server will run on http://localhost:5000
echo.

call npm run dev

pause
