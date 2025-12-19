@echo off
echo ============================================
echo Valyxo Native Backend Build Script
echo ============================================
echo.

REM Check if Rust is installed
where rustc >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Rust is not installed!
    echo Please install Rust from https://rustup.rs/
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    exit /b 1
)

echo [INFO] Rust version:
rustc --version

echo [INFO] Node version:
node --version

echo.
echo [INFO] Installing @napi-rs/cli...
call npm install -g @napi-rs/cli

echo.
echo [INFO] Installing dependencies...
call npm install

echo.
echo [INFO] Building native module (Release)...
call napi build --platform --release

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed!
    exit /b 1
)

echo.
echo ============================================
echo [SUCCESS] Build completed!
echo The native module is ready at:
echo   native\valyxo-native.win32-x64.node
echo ============================================
