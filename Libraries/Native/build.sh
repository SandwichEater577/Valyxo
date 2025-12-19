#!/bin/bash
echo "============================================"
echo "Valyxo Native Backend Build Script"
echo "============================================"
echo ""

# Check if Rust is installed
if ! command -v rustc &> /dev/null; then
    echo "[ERROR] Rust is not installed!"
    echo "Please install Rust from https://rustup.rs/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[INFO] Rust version:"
rustc --version

echo "[INFO] Node version:"
node --version

echo ""
echo "[INFO] Installing @napi-rs/cli..."
npm install -g @napi-rs/cli

echo ""
echo "[INFO] Installing dependencies..."
npm install

echo ""
echo "[INFO] Building native module (Release)..."
napi build --platform --release

if [ $? -ne 0 ]; then
    echo "[ERROR] Build failed!"
    exit 1
fi

echo ""
echo "============================================"
echo "[SUCCESS] Build completed!"
echo "The native module is ready."
echo "============================================"
