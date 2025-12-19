# Valyxo Native Backend

High-performance Rust backend for the Valyxo desktop application.

## Features

- **Fast File Operations** - Memory-mapped reads, atomic writes, parallel search
- **Terminal Emulation** - Native PTY support for shell integration
- **Settings Management** - JSON-based config with file watching
- **File Indexer** - Fast symbol and file search with gitignore support
- **Git Integration** - Native git operations via git2-rs
- **Process Management** - Spawn and manage child processes

## Building

### Prerequisites

1. Install Rust: https://rustup.rs/
2. Install Node.js: https://nodejs.org/

### Build Steps

```bash
# Install napi-rs CLI
npm install -g @napi-rs/cli

# Build the native module
cd native
napi build --release

# Or for development
napi build
```

### Windows

```powershell
# Make sure you have Visual Studio Build Tools installed
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

cd native
napi build --release --platform win32-x64
```

### macOS

```bash
cd native
napi build --release --platform darwin-x64
# Or for Apple Silicon
napi build --release --platform darwin-arm64
```

### Linux

```bash
cd native
napi build --release --platform linux-x64
```

## Usage in Electron

```javascript
const native = require("./native");

// Initialize
console.log(native.init());

// File operations
const content = native.fileOps.readFile("/path/to/file");
native.fileOps.writeFile("/path/to/file", "content");

// Search files
const results = native.fileOps.searchInFiles("/project", "function\\s+\\w+");

// Git operations
const status = native.git.status("/path/to/repo");
native.git.add("/path/to/repo", ["file.js"]);
native.git.commit("/path/to/repo", "Commit message");

// Terminal
const termId = native.terminal.create();
native.terminal.write(termId, "ls -la\n");
const output = native.terminal.read(termId);

// File indexer
native.indexer.start("/project");
const files = native.indexer.searchFiles("main");
```

## Performance

The Rust backend provides significant performance improvements over pure JavaScript:

| Operation        | JS (ms) | Rust (ms) | Speedup |
| ---------------- | ------- | --------- | ------- |
| Read 100MB file  | ~250    | ~50       | 5x      |
| Search 10k files | ~5000   | ~200      | 25x     |
| Index 100k files | ~30000  | ~2000     | 15x     |
| Git status       | ~500    | ~50       | 10x     |

## Architecture

```
native/
├── Cargo.toml          # Rust dependencies
├── build.rs            # NAPI build script
├── index.js            # JS bindings
├── src/
│   ├── lib.rs          # Main entry point
│   ├── error.rs        # Error types
│   ├── file_ops.rs     # File operations
│   ├── terminal.rs     # PTY terminal
│   ├── settings.rs     # Settings management
│   ├── indexer.rs      # File indexer
│   ├── git.rs          # Git operations
│   └── process.rs      # Process management
```

## License

MIT - Part of the Valyxo project
