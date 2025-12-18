#!/bin/bash

echo "========================================"
echo "   Valyxo Backend Server (Go)"
echo "========================================"
echo

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "[ERROR] Go is not installed or not in PATH"
    echo "Please install Go from https://go.dev/dl/"
    exit 1
fi

echo "[1/3] Downloading dependencies..."
go mod download
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to download dependencies"
    exit 1
fi

echo "[2/3] Building server..."
go build -o valyxo-server ./cmd/server
if [ $? -ne 0 ]; then
    echo "[ERROR] Build failed"
    exit 1
fi

echo "[3/3] Starting server..."
echo
./valyxo-server
