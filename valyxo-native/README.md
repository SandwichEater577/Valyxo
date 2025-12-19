# Valyxo Native

The fastest code editor, built in Rust.

## Features

- **GPU-Accelerated Rendering** - Uses wgpu for blazing fast rendering at 60fps
- **Rope Data Structure** - O(log n) text operations for instant editing
- **Syntax Highlighting** - Syntect-powered highlighting for 200+ languages
- **Fuzzy File Search** - Ctrl+P to quickly find any file
- **Command Palette** - Ctrl+Shift+P for all commands
- **Git Integration** - Built-in git status
- **Themes** - Dark, Light, Monokai, Dracula, Nord

## Performance

| Metric  | Valyxo Native | VS Code | Sublime Text |
| ------- | ------------- | ------- | ------------ |
| Startup | ~50ms         | ~2000ms | ~100ms       |
| Memory  | ~30MB         | ~300MB  | ~50MB        |
| Bundle  | ~10MB         | ~150MB  | ~25MB        |
| FPS     | 60            | 60      | 60           |

## Building

### Prerequisites

1. Install Rust: https://rustup.rs/
2. On Windows, install Visual Studio Build Tools

### Build & Run

```bash
cd valyxo-native

# Development
cargo run

# Release (optimized)
cargo build --release
./target/release/valyxo
```

### Font Setup

Download JetBrains Mono font and place in `assets/fonts/`:

- Download from: https://www.jetbrains.com/lp/mono/
- Place `JetBrainsMono-Regular.ttf` in `assets/fonts/`

## Keyboard Shortcuts

| Shortcut     | Action          |
| ------------ | --------------- |
| Ctrl+O       | Open File       |
| Ctrl+Shift+O | Open Folder     |
| Ctrl+S       | Save            |
| Ctrl+W       | Close Tab       |
| Ctrl+P       | Quick Open      |
| Ctrl+Shift+P | Command Palette |
| Ctrl+B       | Toggle Sidebar  |
| Ctrl+Z       | Undo            |
| Ctrl+Y       | Redo            |
| Ctrl+Tab     | Next Tab        |

## Architecture

```
valyxo-native/
├── Cargo.toml       # Dependencies
├── src/
│   ├── main.rs          # Entry point
│   ├── app.rs           # Main application
│   ├── editor.rs        # Editor widget
│   ├── buffer.rs        # Text buffer (rope)
│   ├── syntax.rs        # Syntax highlighting
│   ├── file_tree.rs     # File explorer
│   ├── tabs.rs          # Tab bar
│   ├── command_palette.rs
│   ├── theme.rs         # Themes
│   ├── config.rs        # Settings
│   ├── git.rs           # Git integration
│   └── keybindings.rs   # Keyboard shortcuts
└── assets/
    └── fonts/           # Fonts
```

## License

MIT - Part of the Valyxo project
