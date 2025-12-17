#!/bin/bash

set -e

echo "Valyxo Backend API Setup"
echo "========================"

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please configure .env file before running the server"
fi

if [ ! -d node_modules ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "Starting Valyxo Backend API (v0.41)..."
echo "Server will run on http://localhost:5000"
echo ""

npm run dev
